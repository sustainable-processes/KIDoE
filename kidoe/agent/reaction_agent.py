import itertools
import logging
import os
import shutil
import string
import sys
from collections import Counter
from copy import deepcopy
from itertools import product

import pubchempy as pcp
import yaml
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdchem import Mol

from ..reaction.march import march_reaction_templates
from ..reaction.stephen import stephen_reaction_templates
from ..reaction.uspto import uspto_reaction_templates
from .knowledge_graph_agent import KnowledgeGraphAgent

ALL = Chem.SanitizeFlags.SANITIZE_ALL
KEKULIZE = Chem.SanitizeFlags.SANITIZE_KEKULIZE
SYMMRINGS = Chem.SanitizeFlags.SANITIZE_SYMMRINGS
SETAROMATICITY = Chem.SanitizeFlags.SANITIZE_SETAROMATICITY

logger = logging.getLogger(__name__)


def alphabet_generator():
    letters = string.ascii_lowercase
    length = 1
    while True:
        for chars in product(letters, repeat=length):
            yield ''.join(chars)
        length += 1


def smiles2name(smi):
    compounds = pcp.get_compounds(smi, namespace='smiles')
    if compounds:
        name = compounds[0].iupac_name
    else:
        name = None
    return name


def rxn2formula(rxn, smi2index):
    reagent_dict, product_dict = {}, {}
    for reagent_smi in rxn.split('>>')[0].split('.'):
        if smi2index[reagent_smi] not in reagent_dict:
            reagent_dict[smi2index[reagent_smi]] = 1
        else:
            reagent_dict[smi2index[reagent_smi]] += 1
    for product_smi in rxn.split('>>')[1].split('.'):
        if smi2index[product_smi] not in product_dict:
            product_dict[smi2index[product_smi]] = 1
        else:
            product_dict[smi2index[product_smi]] += 1
    reagent_dict = dict(sorted(reagent_dict.items()))
    product_dict = dict(sorted(product_dict.items()))
    lhs = [f'{n} {r}' if n > 1 else f'{r}' for r, n in reagent_dict.items()]
    rhs = [f'{n} {r}' if n > 1 else f'{r}' for r, n in product_dict.items()]
    return f'{" + ".join(lhs)} > {" + ".join(rhs)}'


def formula2rxn(formula, name2smi):
    """Convert a formula such as `2 a + b > c` into reaction SMILES."""
    sides = []
    for side in formula.split('>'):
        smis = []
        for term in side.split('+'):
            coef, _, name = term.strip().rpartition(' ')
            smis.extend([name2smi[name]] * int(coef or 1))
        sides.append('.'.join(sorted(smis)))
    return '>>'.join(sides)


def _sanitized_mol(smi: str) -> Mol:
    """Parse SMILES and sanitize without kekulization."""
    mol = Chem.MolFromSmiles(smi, sanitize=False)
    Chem.SanitizeMol(mol, sanitizeOps=ALL ^ KEKULIZE)
    return mol


def _includes_rxn(rxn: str, sub_rxn: str) -> bool:
    """Check whether a reaction contains all reactants and products of another
    reaction, counting multiplicity.
    """
    return all(
        not Counter(sub_side) - Counter(side)
        for sub_side, side in zip(_split_rxn(sub_rxn), _split_rxn(rxn))
    )


def _split_rxn(rxn: str) -> tuple[list[str], list[str]]:
    """Split reaction SMILES into reactant and product SMILES lists."""
    lhs, rhs = rxn.split('>>')
    return lhs.split('.'), rhs.split('.')


def _has_substruct(mols: list[Mol], sma: str) -> bool:
    """Check whether any molecule matches a SMARTS pattern."""
    pat = Chem.MolFromSmarts(sma)
    return any(mol.HasSubstructMatch(pat) for mol in mols)


def _chain_rxn(overall_rxn: str, stage_rxn: str, reagent_smis: list[str]) -> str | None:
    """Chain a stage reaction onto an overall reaction.

    Each stage reactant is taken from the overall products, or else from the
    original reagents (added to the overall reactants).

    Returns:
        str | None: chained overall reaction, or None if a stage reactant is
            unavailable or the result has no net change
    """
    lhs, rhs = _split_rxn(overall_rxn)
    stage_lhs, stage_rhs = _split_rxn(stage_rxn)
    for smi in stage_lhs:
        if smi in rhs:
            rhs.remove(smi)
        elif smi in reagent_smis:
            lhs.append(smi)
        else:
            return None
    rhs.extend(stage_rhs)
    lhs, rhs = '.'.join(sorted(lhs)), '.'.join(sorted(rhs))
    if lhs == rhs:
        return None
    return f'{lhs}>>{rhs}'


def _chain_stage(
    overall_rxns: list[str],
    overall_paths: list[list[int]],
    stage_rxns: list[str],
    reagent_smis: list[str],
) -> tuple[list[str], list[str], list[list[int]]]:
    """Chain the reactions of one stage onto the overall reactions so far.

    Every stage is required, so overall reactions that no stage reaction can
    be chained onto are dropped.

    Returns:
        tuple: stage reactions used, chained overall reactions and their paths
    """
    used_rxns, next_rxns, next_paths = [], [], []
    for overall_rxn, path in zip(overall_rxns, overall_paths):
        for stage_rxn in stage_rxns:
            next_rxn = _chain_rxn(overall_rxn, stage_rxn, reagent_smis)
            if next_rxn is None:
                continue
            if stage_rxn not in used_rxns:
                used_rxns.append(stage_rxn)
            if next_rxn not in next_rxns:
                next_rxns.append(next_rxn)
                next_paths.append(path + [used_rxns.index(stage_rxn)])
    return used_rxns, next_rxns, next_paths


def _contains_stage_rxn(
    overall_rxn: str, path: list[int], stage_rxns: list[list[str]]
) -> bool:
    """Check whether an overall reaction contains one of its stage reactions
    unchanged, i.e. all its reactants and products appear on the same sides.
    """
    overall_lhs, overall_rhs = _split_rxn(overall_rxn)
    for rxns, idx in zip(stage_rxns, path):
        stage_lhs, stage_rhs = _split_rxn(rxns[idx])
        if all(s in overall_lhs for s in stage_lhs) and all(
            s in overall_rhs for s in stage_rhs
        ):
            return True
    return False


def _drop_seen_rxns(mechanism_res: dict, seen_rxns: set[str]) -> dict:
    """Drop overall reactions that were already found.

    Stages keep only the reactions used by the remaining overall reactions,
    and the paths are reindexed to match.
    """
    stages = {stage: [] for stage in mechanism_res['stages']}
    overall, overall_path = [], []
    for rxn, path in zip(mechanism_res['overall'], mechanism_res['overall_path']):
        if rxn in seen_rxns:
            continue
        new_path = []
        for (stage, stage_rxns), idx in zip(mechanism_res['stages'].items(), path):
            stage_rxn = stage_rxns[idx]
            if stage_rxn not in stages[stage]:
                stages[stage].append(stage_rxn)
            new_path.append(stages[stage].index(stage_rxn))
        overall.append(rxn)
        overall_path.append(new_path)
    return {'overall': overall, 'overall_path': overall_path, 'stages': stages}


class ReactionAgent:
    """Reaction agent for generating reaction steps and configs.

    Reactions are generated using SMILES Arbitrary Target Specification (SMARTS).

    Args:
        source (str): SMARTS template source, supported options:
        `uspto`, `march`, `stephen`
    """

    def __init__(self, source: str) -> None:
        super().__init__()
        self.template_sources = {
            'uspto': uspto_reaction_templates,
            'march': march_reaction_templates,
            'stephen': stephen_reaction_templates,
        }
        assert source in self.template_sources, (
            f'Unknown SMARTS template source: {source}'
        )
        self.templates = self.template_sources[source]
        ontomo_path = os.path.join(
            os.path.abspath(__file__), '../../ontology/OntoMo.owl'
        )
        self.ontomo = KnowledgeGraphAgent(ontomo_path)
        self.entity = self.ontomo.query()

    def _infer_smarts_template(self, mols: list[Mol], template: str) -> list[str]:
        """Infer mechanistic reaction template for given molecules.

        Args:
            mols (List[Mol]): rdkit molecules
            template (str): SMARTS reaction template

        Return:
            List[str]: Inferred reaction formulas
        """
        rxn_template = AllChem.ReactionFromSmarts(template)

        sma2mol = {}
        template_lhs = template.split('>>', maxsplit=1)[0]
        for sma in template_lhs.split('.'):
            if sma not in sma2mol:
                sma2mol[sma] = []
            pat = Chem.MolFromSmarts(sma)
            for mol in mols:
                if mol.HasSubstructMatch(pat):
                    sma2mol[sma].append(mol)

        res = []
        for comb in itertools.product(*[sma2mol[s] for s in template_lhs.split('.')]):
            rxn_lhs = '.'.join(sorted(Chem.MolToSmiles(mol) for mol in comb))
            for prod in rxn_template.RunReactants(comb):
                rxn_rhs = []
                for smi in sorted(Chem.MolToSmiles(mol) for mol in prod):
                    mol = Chem.MolFromSmiles(smi, sanitize=False)
                    Chem.SanitizeMol(mol, sanitizeOps=SYMMRINGS | SETAROMATICITY)
                    rxn_rhs.append(Chem.MolToSmiles(mol))
                rxn_rhs = '.'.join(rxn_rhs)
                rxn = f'{rxn_lhs}>>{rxn_rhs}'
                if rxn not in res:
                    res.append(rxn)
        return res

    def _infer_stage(
        self, mols: list[Mol], smis: list[str], templates: list[str], sanitize: bool
    ) -> tuple[list[str], list[Mol], list[str]]:
        """Apply the templates of one mechanism stage.

        Products formed by a template are added to the species pool and are
        available to later templates of the same stage and to later stages.

        Args:
            mols (list[Mol]): current species pool
            smis (list[str]): SMILES of `mols`
            templates (list[str]): SMARTS reaction templates of the stage
            sanitize (bool): only keep products that can be sanitized

        Returns:
            tuple: stage reactions, updated species pool and its SMILES
        """
        mols, smis = list(mols), list(smis)
        stage_rxns = []
        for template in templates:
            rxns = self._infer_smarts_template(mols, template)
            stage_rxns.extend(rxns)
            for rxn in rxns:
                for smi in _split_rxn(rxn)[1]:
                    if smi in smis:
                        continue
                    mol = Chem.MolFromSmiles(smi, sanitize=False)
                    if sanitize:
                        try:
                            Chem.SanitizeMol(mol, sanitizeOps=ALL ^ KEKULIZE)
                        except Chem.MolSanitizeException as e:
                            logger.debug('Dropped species %s: %s', smi, e)
                            continue
                    smis.append(smi)
                    mols.append(mol)
        return list(dict.fromkeys(stage_rxns)), mols, smis

    def _infer_reaction_mechanism(self, mols: list[Mol], mechanism_dict: dict) -> dict:
        """Infer stepwise reaction mechanism for given molecules.

        Stages are applied in order. Each stage reaction is chained onto the
        overall reactions of the previous stages. Every overall reaction is
        traced back to one reaction per stage.

        Args:
            mols (list[Mol]): rdkit molecules
            mechanism_dict (dict): name reaction mechanism dictionary

        Returns:
            dict: inferred reactions, with keys
                `stages`: reactions found for each stage,
                `overall`: overall reactions across all stages,
                `overall_path`: for each overall reaction, the index of the
                    reaction used in each stage.
        """
        stages = mechanism_dict['Stages']
        res = {
            'overall': [],
            'overall_path': [],
            'stages': {stage: [] for stage in stages},
        }

        required = mechanism_dict['Reagent'] or []
        excluded = mechanism_dict['Exclude_reagent'] or []
        if not all(_has_substruct(mols, sma) for sma in required):
            return res
        if any(_has_substruct(mols, sma) for sma in excluded):
            return res

        reagent_smis = [Chem.MolToSmiles(mol) for mol in mols]
        curr_mols, curr_smis = list(mols), list(reagent_smis)
        sanitize = mechanism_dict.get('Sanitize', True)
        for i, (stage, stage_dict) in enumerate(stages.items()):
            stage_rxns, curr_mols, curr_smis = self._infer_stage(
                curr_mols, curr_smis, stage_dict['Templates'], sanitize
            )
            if i == 0:
                res['stages'][stage] = stage_rxns
                res['overall'] = list(stage_rxns)
                res['overall_path'] = [[j] for j in range(len(stage_rxns))]
            else:
                (
                    res['stages'][stage],
                    res['overall'],
                    res['overall_path'],
                ) = _chain_stage(
                    res['overall'],
                    res['overall_path'],
                    stage_rxns,
                    reagent_smis,
                )
            if not res['overall']:
                return res

        if len(stages) > 1:
            stage_rxns = list(res['stages'].values())
            kept = [
                (rxn, path)
                for rxn, path in zip(res['overall'], res['overall_path'])
                if not _contains_stage_rxn(rxn, path, stage_rxns)
            ]
            res['overall'] = [rxn for rxn, _ in kept]
            res['overall_path'] = [path for _, path in kept]
        return res

    def _infer_reaction_net(self, mols: list[Mol], depth: int = 1) -> dict:
        """Infer reaction net for given molecules.

        Each level applies every mechanism to the species pool, and the
        products of newly found overall reactions join the pool for the next
        level. Overall reactions found at an earlier level are not repeated.

        Args:
            mols (list[Mol]): rdkit molecules
            depth (int, optional): reaction net search depth. Default to 1.

        Returns:
            dict: `{level: {(name_reaction, mechanism): mechanism result}}`,
                keeping only levels with new reactions
        """
        mols = list(mols)
        smis = {Chem.MolToSmiles(mol) for mol in mols}
        seen_rxns = {}
        res = {}
        for level in range(depth):
            level_res = {}
            n_species = len(smis)
            curr_mols = list(mols)
            for name, name_reaction_dict in self.templates.items():
                for mechanism, mechanism_dict in name_reaction_dict.items():
                    key = (name, mechanism)
                    seen = seen_rxns.setdefault(key, set())
                    mechanism_res = _drop_seen_rxns(
                        self._infer_reaction_mechanism(curr_mols, mechanism_dict), seen
                    )
                    if not mechanism_res['overall']:
                        continue
                    level_res[key] = mechanism_res
                    seen.update(mechanism_res['overall'])
                    for rxn in mechanism_res['overall']:
                        for smi in _split_rxn(rxn)[1]:
                            if smi in smis:
                                continue
                            mol = Chem.MolFromSmiles(smi, sanitize=False)
                            try:
                                Chem.SanitizeMol(mol, sanitizeOps=ALL ^ KEKULIZE)
                            except Chem.MolSanitizeException as e:
                                logger.debug('Dropped species %s: %s', smi, e)
                                continue
                            smis.add(smi)
                            mols.append(mol)
            if not level_res:
                break
            res[level] = level_res
            # no new species, so the next level would find nothing new
            if len(smis) == n_species:
                break
        return res

    def infer(self, chem_config: dict, depth: int = 1) -> dict:
        """Infer chemistry configuration file using SMARTS templates.

        Args:
            chem_config (dict): chemistry base config dictionary
            depth (int, optional): reaction net search depth. Defaults to 1.

        Returns:
            dict: searched reaction dictionary, with keys
                `main`: found reactions that include a main reaction,
                `side`: other found reactions,
                `missed`: main reactions not found.
                Each found reaction is `{'template': name reaction(s),
                'mechanism': mechanism, 'stoichiometric': overall reaction,
                'mechanistic': [step reactions]}`.
        """
        species = chem_config['chemistry']['species']
        mol_dict = {
            name: _sanitized_mol(species_dict['smiles'])
            for group in (
                'substrate',
                'reagent',
                'product',
                'side product',
                'byproduct',
                'intermediate',
            )
            for name, species_dict in species.get(group, {}).items()
        }
        name2smi = {name: Chem.MolToSmiles(mol) for name, mol in mol_dict.items()}
        main_rxns = [
            formula2rxn(formula, name2smi)
            for formula in chem_config['chemistry']['reaction'].get('main', [])
        ]
        side_rxns = [
            formula2rxn(formula, name2smi)
            for formula in chem_config['chemistry']['reaction'].get('side', [])
        ]

        mols = [
            mol_dict[name]
            for group in ('substrate', 'reagent')
            for name in species[group]
        ]
        smi2mol = {name2smi[name]: mol for name, mol in mol_dict.items()}
        mol_smis = {
            name2smi[name]
            for group in ('substrate', 'reagent')
            for name in species[group]
        }
        for rxn in main_rxns + side_rxns:
            for smi in _split_rxn(rxn)[1]:
                if smi not in mol_smis:
                    mol_smis.add(smi)
                    mols.append(smi2mol[smi])
        reaction_net = self._infer_reaction_net(mols, depth)

        res = {'main': [], 'side': [], 'missed': []}
        found_main_rxns = set()
        for level_res in reaction_net.values():
            for (name, mechanism), mechanism_res in level_res.items():
                template = name if isinstance(name, str) else ' / '.join(name)
                stage_rxns = list(mechanism_res['stages'].values())
                for rxn, path in zip(
                    mechanism_res['overall'], mechanism_res['overall_path']
                ):
                    matched = [m for m in main_rxns if _includes_rxn(rxn, m)]
                    found_main_rxns.update(matched)
                    group = 'main' if matched else 'side'
                    if any(r['stoichiometric'] == rxn for r in res[group]):
                        continue
                    res[group].append({
                        'template': template,
                        'mechanism': mechanism,
                        'stoichiometric': rxn,
                        'mechanistic': [
                            stage_rxns[i][idx] for i, idx in enumerate(path)
                        ],
                    })
        main_overall_rxns = {r['stoichiometric'] for r in res['main']}
        res['side'] = [
            r for r in res['side'] if r['stoichiometric'] not in main_overall_rxns
        ]
        res['missed'] = [m for m in main_rxns if m not in found_main_rxns]
        return res

    def update(self, chem_config: dict, chem_res: dict) -> dict:
        """Update searched results to chemistry base config file  

        Args:
            chem_res (dict): searched chemistry results
            chem_config (dict): chemistry base config dictionary

        Returns:
            dict: chemistry inferred config dictionary
        """
        assert not chem_res['missed'], ('Reactions failed to identify:\n'
                                        '\n'.join(chem_res['missed']))
        substrate_smis, substrate_mols = [], []
        reagent_smis, reagent_mols = [], []
        product_smis, product_mols = [], []
        for species_dict in chem_config['chemistry']['species']['substrate'].values():
            substrate_mol = Chem.MolFromSmiles(species_dict['smiles'], sanitize=False)
            try:
                Chem.SanitizeMol(substrate_mol, sanitizeOps=ALL ^ KEKULIZE)
            except Chem.MolSanitizeException as e:
                logger.debug('Dropped species %s: %s', species_dict['smiles'], e)
                continue
            substrate_smi = Chem.MolToSmiles(substrate_mol)
            substrate_smis.append(substrate_smi)
            substrate_mols.append(substrate_mol)
        for species_dict in chem_config['chemistry']['species']['reagent'].values():
            reagent_mol = Chem.MolFromSmiles(species_dict['smiles'], sanitize=False)
            try:
                Chem.SanitizeMol(reagent_mol, sanitizeOps=ALL ^ KEKULIZE)
            except Chem.MolSanitizeException as e:
                logger.debug('Dropped species %s: %s', species_dict['smiles'], e)
                continue
            reagent_smi = Chem.MolToSmiles(reagent_mol)
            reagent_smis.append(reagent_smi)
            reagent_mols.append(reagent_mol)
        for species_dict in chem_config['chemistry']['species']['product'].values():
            product_mol = Chem.MolFromSmiles(species_dict['smiles'], sanitize=False)
            try:
                Chem.SanitizeMol(product_mol, sanitizeOps=ALL ^ KEKULIZE)
            except Chem.MolSanitizeException as e:
                logger.debug('Dropped species %s: %s', species_dict['smiles'], e)
                continue
            product_smi = Chem.MolToSmiles(product_mol)
            product_smis.append(product_smi)
            product_mols.append(product_mol)

        alphabet_gen = alphabet_generator()
        chem_config['chemistry']['species']['substrate'] = {}
        chem_config['chemistry']['species']['reagent'] = {}
        chem_config['chemistry']['species']['product'] = {}
        smi2index = {}
        for substrate_smi in substrate_smis:
            species_index = next(alphabet_gen)
            chem_config['chemistry']['species']['substrate'][species_index] = {
                'name': smiles2name(substrate_smi),
                'smiles': substrate_smi,
            }
            smi2index[substrate_smi] = species_index
        for reagent_smi in reagent_smis:
            species_index = next(alphabet_gen)
            chem_config['chemistry']['species']['reagent'][species_index] = {
                'name': smiles2name(reagent_smi),
                'smiles': reagent_smi,
            }
            smi2index[reagent_smi] = species_index
        for product_smi in product_smis:
            species_index = next(alphabet_gen)
            chem_config['chemistry']['species']['product'][species_index] = {
                'name': smiles2name(product_smi),
                'smiles': product_smi,
            }
            smi2index[product_smi] = species_index

        main_lhs_smis, main_rhs_smis = [], []
        for main_rxn in chem_res['main']:
            for reagent_smi in main_rxn.split('>>')[0].split('.'):
                if reagent_smi not in main_lhs_smis:
                    main_lhs_smis.append(reagent_smi)
            for product_smi in main_rxn.split('>>')[1].split('.'):
                if product_smi not in main_rhs_smis:
                    main_rhs_smis.append(product_smi)
        intermediate_smis = [smi for smi in main_lhs_smis if smi in main_rhs_smis]
        byproduct_smis = [smi for smi in main_rhs_smis if smi not in main_lhs_smis]
        chem_config['chemistry']['species']['intermediate'] = {}
        chem_config['chemistry']['species']['byproduct'] = {}
        for intermediate_smi in intermediate_smis:
            if intermediate_smi not in smi2index:
                species_index = next(alphabet_gen)
                chem_config['chemistry']['species']['intermediate'][species_index] = {
                    'name': smiles2name(intermediate_smi),
                    'smiles': intermediate_smi,
                }
                smi2index[intermediate_smi] = species_index
        for byproduct_smi in byproduct_smis:
            if byproduct_smi not in smi2index:
                species_index = next(alphabet_gen)
                chem_config['chemistry']['species']['byproduct'][species_index] = {
                    'name': smiles2name(byproduct_smi),
                    'smiles': byproduct_smi,
                }
                smi2index[byproduct_smi] = species_index
        if not chem_config['chemistry']['species']['intermediate']:
            chem_config['chemistry']['species']['intermediate'] = None
        if not chem_config['chemistry']['species']['byproduct']:
            chem_config['chemistry']['species']['byproduct'] = None

        side_rhs_smis = []
        for side_rxn in chem_res['side']:
            for product_smi in side_rxn.split('>>')[1].split('.'):
                if product_smi not in side_rhs_smis:
                    side_rhs_smis.append(product_smi)
        chem_config['chemistry']['species']['side product'] = {}
        for side_rhs_smi in side_rhs_smis:
            if side_rhs_smi not in smi2index:
                species_index = next(alphabet_gen)
                chem_config['chemistry']['species']['side product'][species_index] = {
                    'name': smiles2name(side_rhs_smi),
                    'smiles': side_rhs_smi,
                }
                smi2index[side_rhs_smi] = species_index
        if not chem_config['chemistry']['species']['side product']:
            chem_config['chemistry']['species']['side product'] = None

        chem_config['chemistry']['reaction']['main'] = []
        for rxn in chem_res['main']:
            formula = rxn2formula(rxn, smi2index)
            chem_config['chemistry']['reaction']['main'].append(formula)
        chem_config['chemistry']['reaction']['side'] = []
        for rxn in chem_res['side']:
            formula = rxn2formula(rxn, smi2index)
            chem_config['chemistry']['reaction']['side'].append(formula)
        if not chem_config['chemistry']['reaction']['side']:
            chem_config['chemistry']['reaction']['side'] = None
        chem_config['file type'] = 'chemistry inferred'
        return chem_config

    def append_default_kinetics(self, chem_config: dict) -> dict:
        """Append default kinetics to searched reactions.

        Args:
            chem_config (dict): Inferred chemistry configuration
        Returns:
            dict: Inferred chemistry configuration with default kinetic phenomena
        """
        chem_config['chemistry']['kinetics'] = {}
        for rxn_idx in chem_config['chemistry']['reaction']['main']:
            chem_config['chemistry']['kinetics'][rxn_idx] = [
                'Arrhenius_Log10', 'Concentration_Power_Dependence'
            ]
        for rxn_idx in chem_config['chemistry']['reaction']['side']:
            chem_config['chemistry']['kinetics'][rxn_idx] = [
                'Arrhenius_Log10', 'Concentration_Power_Dependence'
            ]
        print('Using default kinetic phenomenon: `Arrhenius_Log10` and'
              '`Concentration_Power_Dependence`\n'
              'Assign specific kinetics in the output chem_config file.')
        return chem_config

    def parameterize(self, chem_config: dict, proc_config: dict) -> dict:
        chem_config['chemistry']['parameter'] = {}

        consts = []
        for rxn_phenos in chem_config['chemistry']['kinetics'].values():
            for rxn_pheno in rxn_phenos:
                for law in self.entity['law'].values():
                    if law.pheno != rxn_pheno:
                        continue
                    for var in law.vars:
                        if var.cls == 'Constant' and var not in consts:
                            consts.append(var)
        if consts:
            chem_config['chemistry']['parameter']['constant'] = {}
            for const in consts:
                chem_config['chemistry']['parameter']['constant'][const.name] = {
                    'unit': const.unit,
                    'val': const.val,
                }
        else:
            chem_config['chemistry']['parameter']['constant'] = None

        for rxn, rxn_phenos in chem_config['chemistry']['kinetics'].items():
            chem_config['chemistry']['parameter'][rxn] = {}
            for rxn_pheno in rxn_phenos:
                for law in self.entity['law'].values():
                    if law.pheno != rxn_pheno:
                        continue
                    for var in law.vars:
                        if var.cls != 'ReactionParameter':
                            continue
                        lhs_species_dict = {}
                        for r in rxn.split('>')[0].split('+'):
                            r = r.strip()
                            r = r.split(' ')[1] if ' ' in r else r
                            if r in lhs_species_dict:
                                lhs_species_dict[r] += 1
                            else:
                                lhs_species_dict[r] = 1
                        streams = list(proc_config['process']['inlet'].keys())
                        var_dict = {}
                        if set(var.dims) == set(['Reaction']):
                            var_dict['unit'] = var.unit
                            var_dict['min'] = None
                            var_dict['max'] = None
                        if set(var.dims) == set(['Reaction', 'Species']):
                            for species, val in lhs_species_dict.items():
                                var_dict[species] = {}
                                var_dict[species]['unit'] = var.unit
                                if var.name == 'Partial_Order':
                                    var_dict[species]['val'] = val
                                else:
                                    var_dict[species]['val'] = None
                        if set(var.dims) == set(['Stream', 'Reaction']):
                            for stream in streams:
                                var_dict[stream] = {}
                                var_dict[stream]['unit'] = var.unit
                                var_dict[stream]['min'] = None
                                var_dict[stream]['max'] = None
                        chem_config['chemistry']['parameter'][rxn][var.name] = var_dict

        chem_config['file type'] = 'chemistry parameterized'
        return chem_config

    def infer_and_dump(
        self,
        in_chem_cfg_path: str,
        out_chem_cfg_path: str,
        depth: int = 1,
        mechanistic: bool = False,
    ):
        """Infer and dump chemistry base config

        Args:
            in_chem_cfg_path (str): path to input chemistry base config
            out_chem_cfg_path (str): path to output chemistry inferred config
            depth (int, optional): reaction net search depth. Defaults to 1.
            mechanistic (bool, optional): save the mechanistic step reactions
                of each found reaction instead of the stoichiometric
                reaction. Defaults to False.
        """
        with open(in_chem_cfg_path) as f:
            config = yaml.load(f, yaml.FullLoader)
        reaction_net_res = self.infer(config, depth)
        key = 'mechanistic' if mechanistic else 'stoichiometric'
        rxn_res = {}
        for group in ('main', 'side'):
            rxns = []
            for r in reaction_net_res[group]:
                rxns.extend(r[key] if mechanistic else [r[key]])
            rxn_res[group] = list(dict.fromkeys(rxns))
        rxn_res['side'] = [
            rxn for rxn in rxn_res['side'] if rxn not in rxn_res['main']
        ]
        rxn_res['missed'] = reaction_net_res['missed']
        config = self.update(config, rxn_res)
        config = self.append_default_kinetics(config)
        with open(out_chem_cfg_path, 'w') as f:
            yaml.dump(config, f, sort_keys=False)

    def parameterize_and_dump(
        self, in_chem_cfg_path: str, proc_cfg_path: str, out_chem_cfg_path: str
    ):
        """Parameterize chemistry config based on assigned phenomena

        Args:
            in_chem_cfg_path (str): path to input chemistry inferred config file
            proc_cfg_path (str): path to process base config file
            out_chem_cfg_path (str): path to output chemistry inferred config file
        """
        with open(in_chem_cfg_path) as f:
            chem_config = yaml.load(f, yaml.FullLoader)
        with open(proc_cfg_path) as f:
            proc_config = yaml.load(f, yaml.FullLoader)
        param_chem_config = self.parameterize(chem_config, proc_config)
        with open(out_chem_cfg_path, 'w') as f:
            yaml.dump(param_chem_config, f, sort_keys=False)

    def generate_and_dump(self, in_chem_cfg_path: str, out_chem_dir: str):
        """Dump candidate config files based on parameterized chemistry configuration

        Args:
            in_chem_cfg_path (str): Path to input parameterized chemistry configuration
            out_chem_dir (str): Path to output chemistry candidate config dir
        """
        if os.path.exists(out_chem_dir):
            while True:
                delete_flag = input(f'Delete files in "{out_chem_dir}"? (y/n)')
                if delete_flag in ['Y', 'y', '']:
                    for filename in os.listdir(out_chem_dir):
                        file_path = os.path.join(out_chem_dir, filename)
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    break
                elif delete_flag in ['N', 'n']:
                    sys.exit()
        else:
            os.mkdir(out_chem_dir)

        with open(in_chem_cfg_path) as f:
            config = yaml.load(f, yaml.FullLoader)
        main_species = []
        for main_rxn in config['chemistry']['reaction']['main']:
            for r in main_rxn.replace('>', '+').split('+'):
                r = r.strip()
                species = r.split(' ')[1] if ' ' in r else r
                if species not in main_species:
                    main_species.append(species)
        side_rxns = config['chemistry']['reaction']['side']

        cand_side_rxns = []
        for num_side_rxns in range(len(side_rxns) + 1):
            for pre_sel_side_rxns in itertools.combinations(side_rxns, num_side_rxns):
                sel_side_rxns = []
                sel_species = main_species.copy()
                for _ in range(num_side_rxns):
                    for pre_sel_side_rxn in pre_sel_side_rxns:
                        if pre_sel_side_rxn in sel_side_rxns:
                            continue
                        rs = []
                        for r in pre_sel_side_rxn.split('>')[0].split('+'):
                            r = r.strip()
                            rs.append(r.split(' ')[1] if ' ' in r else r)
                        if not all(r in sel_species for r in rs):
                            continue
                        sel_side_rxns.append(pre_sel_side_rxn)
                        for p in pre_sel_side_rxn.split('>')[1].split('+'):
                            p = p.strip()
                            p = p.split(' ')[1] if ' ' in p else p
                            if p not in sel_species:
                                sel_species.append(p)
                if sel_side_rxns not in cand_side_rxns:
                    cand_side_rxns.append(sel_side_rxns)

        main_rxns = config['chemistry']['reaction']['main']
        for cand_idx, side_rxns in enumerate(cand_side_rxns):
            cand_config = deepcopy(config)
            cand_config['file type'] = 'chemistry candidate'
            cand_config['chemistry']['reaction']['side'] = side_rxns
            if not cand_config['chemistry']['reaction']['side']:
                cand_config['chemistry']['reaction']['side'] = None

            cand_config['chemistry']['kinetics'] = {
                k: v
                for k, v in cand_config['chemistry']['kinetics'].items()
                if k in main_rxns or k in side_rxns
            }

            cand_config['chemistry']['parameter'] = {}
            cand_config['chemistry']['parameter']['constant'] = config['chemistry'][
                'parameter']['constant']
            for rxn in config['chemistry']['reaction']['main']:
                cand_config['chemistry']['parameter'][rxn] = config['chemistry'][
                    'parameter'][rxn]
            for rxn in side_rxns:
                cand_config['chemistry']['parameter'][rxn] = config['chemistry'][
                    'parameter'][rxn]

            out_chem_cfg_path = os.path.join(out_chem_dir, f'chem_{cand_idx}.yaml')
            with open(out_chem_cfg_path, 'w') as f:
                yaml.dump(cand_config, f, sort_keys=False)