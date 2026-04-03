import itertools
import os
import shutil
import string
from copy import deepcopy
from itertools import product
from typing import Dict, List

import pubchempy as pcp
import yaml
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdchem import Mol

from ..reaction.uspto import uspto_reaction_templates
from .knowledge_graph_agent import KnowledgeGraphAgent

SANITIZE_ALL = Chem.SanitizeFlags.SANITIZE_ALL
SANITIZE_KEKULIZE = Chem.SanitizeFlags.SANITIZE_KEKULIZE
SANITIZE_SYMMRINGS = Chem.SanitizeFlags.SANITIZE_SYMMRINGS
SANITIZE_SETAROMATICITY = Chem.SanitizeFlags.SANITIZE_SETAROMATICITY

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
    for reagent_smi in rxn.split('>')[0].split('.'):
        if smi2index[reagent_smi] not in reagent_dict:
            reagent_dict[smi2index[reagent_smi]] = 1
        else:
            reagent_dict[smi2index[reagent_smi]] += 1
    for product_smi in rxn.split('>')[1].split('.'):
        if smi2index[product_smi] not in product_dict:
            product_dict[smi2index[product_smi]] = 1
        else:
            product_dict[smi2index[product_smi]] += 1
    reagent_dict = dict(sorted(reagent_dict.items()))
    product_dict = dict(sorted(product_dict.items()))
    lhs = [f'{n} {r}' if n > 1 else f'{r}' for r, n in reagent_dict.items()]
    rhs = [f'{n} {r}' if n > 1 else f'{r}' for r, n in product_dict.items()]
    return f'{" + ".join(lhs)} > {" + ".join(rhs)}'


class ReactionAgent:
    """Reaction agent for generating reaction steps and configs.
    
    Reactions are generated based on SMILES Arbitrary Target Specification 
    (SMARTS) templates.

    Args:
        source (str): SMARTS template source, supported options: `uspto`

    Example:
        # TODO
    """

    template_sources = {'uspto': uspto_reaction_templates}

    def __init__(self, source: str) -> None:
        super().__init__()
        assert source in ['uspto'], f'Unknown SMARTS template source: {source}'
        self.templates = self.template_sources[source]
        ontomo_path = os.path.join(os.path.abspath(__file__),
                                   '../../ontology/OntoMo.owl')
        self.ontomo = KnowledgeGraphAgent(ontomo_path)
        self.entity = self.ontomo.query()

    def _infer_smarts_template(
        self,
        mols: List[Mol],
        template: str,
        intact_mols: List[Mol] = None,
        sanitize: bool = False,
    ) -> List[str]:
        """Infer mechanistic reaction template for given molecules.

        Args:
            mols (List[Mol]): rdkit molecules
            template (str): SMARTS reaction template

        Return:
            List[str]: Reaction formulas, or empty list if no template is matched
        """
        rxn_template = AllChem.ReactionFromSmarts(template)

        sma2mol = {}
        template_lhs = template.split('>>')[0]
        for sma in template_lhs.split('.'):
            if sma not in sma2mol:
                sma2mol[sma] = []
            pat = Chem.MolFromSmarts(sma)
            for mol in mols:
                if mol.HasSubstructMatch(pat):
                    sma2mol[sma].append(mol)

        res = []
        for comb in itertools.product(
                *[sma2mol[sma] for sma in template_lhs.split('.')]):
            rxn_lhs = '.'.join(sorted(Chem.MolToSmiles(mol) for mol in comb))
            if intact_mols and sanitize:
                intact_mols_atom_num_hs = []
                lhs_intact_mol_nums = []
                for intact_mol in intact_mols:
                    lhs_intact_mol_nums.append(0)
                    atom_num_hs = [
                        atom.GetTotalNumHs() for atom in intact_mol.GetAtoms()
                    ]
                    intact_mols_atom_num_hs.append(atom_num_hs)
                    for mol in comb:
                        matched_atom_idxs = set()
                        for match in mol.GetSubstructMatches(intact_mol):
                            if matched_atom_idxs.intersection(match):
                                continue
                            match_atom_num_hs = [
                                mol.GetAtomWithIdx(i).GetTotalNumHs() for i in match
                            ]
                            if match_atom_num_hs == atom_num_hs:
                                lhs_intact_mol_nums[-1] += 1
                                matched_atom_idxs.update(match)

            for prod in rxn_template.RunReactants(comb):
                rxn_rhs = []
                for smi in sorted(Chem.MolToSmiles(mol) for mol in prod):
                    mol = Chem.MolFromSmiles(smi, sanitize=False)
                    Chem.SanitizeMol(mol,
                                     sanitizeOps=SANITIZE_SYMMRINGS
                                     | SANITIZE_SETAROMATICITY)
                    rxn_rhs.append(Chem.MolToSmiles(mol))
                rxn_rhs = '.'.join(rxn_rhs)
                rxn = f'{rxn_lhs}>{rxn_rhs}'
                if intact_mols and sanitize:
                    rhs_intact_mol_nums = []
                    for intact_mol, atom_num_hs in zip(intact_mols,
                                                       intact_mols_atom_num_hs):
                        rhs_intact_mol_nums.append(0)
                        for mol in prod:
                            Chem.SanitizeMol(
                                mol,
                                sanitizeOps=SANITIZE_ALL ^ SANITIZE_KEKULIZE,
                            )
                            matched_atom_idxs = set()
                            for match in mol.GetSubstructMatches(intact_mol):
                                if matched_atom_idxs.intersection(match):
                                    continue
                                match_atom_num_hs = [
                                    mol.GetAtomWithIdx(i).GetTotalNumHs() for i in match
                                ]
                                if match_atom_num_hs == atom_num_hs:
                                    rhs_intact_mol_nums[-1] += 1
                    if lhs_intact_mol_nums != rhs_intact_mol_nums:
                        continue
                if rxn not in res:
                    res.append(rxn)
        return res

    def _infer_reaction_mechanism(
        self,
        mols: List[Mol],
        mechanism_dict: Dict,
        intact_mols: List[Mol] = None,
    ) -> Dict:
        """Infer stepwise reaction mechanism for given molecules.

        Args:
            mols (List[Mol]): rdkit molecules
            mechanism_dict (Dict): name reaction mechanism dictionary, with 
                                   structure as
                {
                    'Reagent': [...],
                    'Exclude_reagent': [...],
                    'Stages': {
                        0: {
                            'Description': ...,
                            'pKa': [...],
                            'Templates': [...],
                        },
                        ...
                    }
                }

        Returns:
            Dict: inferred stepwise and overall reaction dictionary
        """
        res = {
            'overall': [],
            'stages': {
                stage: []
                for stage in mechanism_dict['Stages']
            },
        }

        has_reagents = []
        if mechanism_dict['Reagent']:
            for reagent_sma in mechanism_dict['Reagent']:
                reagent_pat = Chem.MolFromSmarts(reagent_sma)
                for mol in mols:
                    mol.HasSubstructMatch(reagent_pat)
                if any(mol.HasSubstructMatch(reagent_pat) for mol in mols):
                    has_reagents.append(True)
                else:
                    has_reagents.append(False)
            if not all(has_reagents):
                return res

        has_excludes = []
        if mechanism_dict['Exclude_reagent']:
            for exclude_sma in mechanism_dict['Exclude_reagent']:
                exclude_pat = Chem.MolFromSmarts(exclude_sma)
                if any(mol.HasSubstructMatch(exclude_pat) for mol in mols):
                    has_excludes.append(True)
                else:
                    has_excludes.append(False)
            if any(has_excludes):
                return res

        smis = [Chem.MolToSmiles(mol) for mol in mols]
        curr_smis = [Chem.MolToSmiles(mol) for mol in mols]
        curr_mols = mols
        sanitize = mechanism_dict.get('Sanitize', True)
        for stage, stage_dict in mechanism_dict['Stages'].items():
            next_smis = deepcopy(curr_smis)
            next_mols = deepcopy(curr_mols)
            stage_rxns = []
            for template in stage_dict['Templates']:
                stage_rxns.extend(
                    self._infer_smarts_template(next_mols, template, intact_mols,
                                                sanitize))
                for stage_rxn in stage_rxns:
                    for smi in stage_rxn.split('>')[1].split('.'):
                        if smi not in next_smis:
                            mol = Chem.MolFromSmiles(smi, sanitize=False)
                            if sanitize:
                                try:
                                    Chem.SanitizeMol(
                                        mol,
                                        sanitizeOps=SANITIZE_ALL ^ SANITIZE_KEKULIZE,
                                    )
                                    next_smis.append(smi)
                                    next_mols.append(mol)
                                except Exception:
                                    pass
                            else:
                                next_smis.append(smi)
                                next_mols.append(mol)
            stage_rxns = list(set(stage_rxns))
            if stage == 0:
                next_overall_rxns = stage_rxns
                next_overall_paths = [[i] for i in range(len(stage_rxns))]
                res['stages'][stage] = stage_rxns
            else:
                res['stages'][stage] = []
                next_overall_rxns = []
                next_overall_paths = []
                for overall_rxn, overall_path in zip(res['overall'],
                                                     res['overall_path']):
                    if stage != len(mechanism_dict['Stages']) - 1:
                        charge_equal_flag = False
                        for stage_rxn in stage_rxns:
                            stage_rxn_template = AllChem.ReactionFromSmarts(
                                stage_rxn.replace('>', '>>'))
                            lhs_charge = 0
                            for mol in stage_rxn_template.GetReactants():
                                for atom in mol.GetAtoms():
                                    query = atom.DescribeQuery().split()
                                    if 'AtomFormalCharge' in query:
                                        lhs_charge += int(
                                            query[query.index('AtomFormalCharge') + 1])
                            rhs_charge = 0
                            for mol in stage_rxn_template.GetProducts():
                                for atom in mol.GetAtoms():
                                    query = atom.DescribeQuery().split()
                                    if 'AtomFormalCharge' in query:
                                        rhs_charge += int(
                                            query[query.index('AtomFormalCharge') + 1])
                            if lhs_charge == rhs_charge:
                                charge_equal_flag = True
                        if charge_equal_flag:
                            next_overall_rxns.append(overall_rxn)
                            next_overall_paths.append(overall_path + [None])
                    for stage_rxn in stage_rxns:
                        reagent_smis = overall_rxn.split('>')[0].split('.')
                        product_smis = overall_rxn.split('>')[1].split('.')
                        stage_reagent_flags = []
                        for stage_reagent_smi in stage_rxn.split('>')[0].split('.'):
                            if stage_reagent_smi in product_smis:
                                stage_reagent_flags.append(True)
                                product_smis.pop(product_smis.index(stage_reagent_smi))
                            elif stage_reagent_smi in smis:
                                stage_reagent_flags.append(True)
                                reagent_smis.append(stage_reagent_smi)
                            else:
                                stage_reagent_flags.append(False)
                        if all(stage_reagent_flags):
                            product_smis.extend(stage_rxn.split('>')[1].split('.'))
                            lhs = '.'.join(sorted(reagent_smis))
                            rhs = '.'.join(sorted(product_smis))
                            if lhs == rhs:
                                continue
                            next_overall_rxn = f'{lhs}>{rhs}'
                            if stage_rxn not in res['stages'][stage]:
                                res['stages'][stage].append(stage_rxn)
                            if next_overall_rxn not in next_overall_rxns:
                                next_overall_rxns.append(next_overall_rxn)
                                next_overall_paths.append(
                                    overall_path +
                                    [res['stages'][stage].index(stage_rxn)])
            curr_mols = next_mols
            curr_smis = next_smis
            res['overall'] = next_overall_rxns
            res['overall_path'] = next_overall_paths

        filter_overall_rxns = []
        filter_overall_paths = []
        for overall_rxn, overall_path in zip(res['overall'], res['overall_path']):
            overall_lhs = overall_rxn.split('>')[0].split('.')
            overall_rhs = overall_rxn.split('>')[1].split('.')
            flag = True
            if len(res['stages']) > 1:
                for stage in res['stages']:
                    if overall_path[stage] is None:
                        continue
                    stage_rxn = res['stages'][stage][overall_path[stage]]
                    stage_lhs = stage_rxn.split('>')[0].split('.')
                    stage_rhs = stage_rxn.split('>')[1].split('.')
                    lhs_flag = all(s in overall_lhs for s in stage_lhs)
                    rhs_flag = all(s in overall_rhs for s in stage_rhs)
                    if lhs_flag and rhs_flag:
                        flag = False
                        break
            if flag:
                filter_overall_rxns.append(overall_rxn)
                filter_overall_paths.append(overall_path)
        res['overall'] = filter_overall_rxns
        res['overall_path'] = filter_overall_paths
        return res

    def _infer_reaction_net(self,
                            mols: List[Mol],
                            depth: int = 1,
                            intact_mols: List[Mol] = None) -> Dict:
        """Infer reaction net for given molecules.

        Args:
            mols (List[Mol]): rdkit molecules
            depth (int, optional): reaction net search depth. Default to 1.

        Returns:
            Dict: inferred stepwise and overall reaction dictionary
        """
        res = {i: {} for i in range(depth)}
        smis = [Chem.MolToSmiles(mol) for mol in mols]
        for i in range(depth):
            curr_mols = deepcopy(mols)
            for _, name_reaction_dict in self.templates.items():
                for mechanism, mechanism_dict in name_reaction_dict.items():
                    mechanism_res = self._infer_reaction_mechanism(
                        curr_mols, mechanism_dict, intact_mols)
                    if not mechanism_res['overall']:
                        continue
                    for j in range(i):
                        if mechanism not in res[j]:
                            continue
                        for rxn in res[j][mechanism]['overall']:
                            if rxn not in mechanism_res['overall']:
                                continue
                            overall_rxn_idx = mechanism_res['overall'].index(rxn)
                            mechanism_res['overall'].pop(overall_rxn_idx)
                        for k in res[j][mechanism]['stages']:
                            if k not in mechanism_res['stages']:
                                continue
                            for rxn in res[j][mechanism]['stages'][k]:
                                if rxn not in mechanism_res['stages'][k]:
                                    continue
                                stage_rxn_idx = mechanism_res['stages'][k].index(rxn)
                                mechanism_res['stages'][k].pop(stage_rxn_idx)
                    if mechanism_res['overall']:
                        res[i][mechanism] = mechanism_res
                        for overall_rxn in mechanism_res['overall']:
                            for smi in overall_rxn.split('>')[1].split('.'):
                                if smi not in smis:
                                    mol = Chem.MolFromSmiles(smi, sanitize=False)
                                    try:
                                        Chem.SanitizeMol(mol,
                                                         sanitizeOps=SANITIZE_ALL
                                                         ^ SANITIZE_KEKULIZE)
                                    except Exception:
                                        pass
                                    smis.append(smi)
                                    mols.append(mol)
            if not res[i]:
                res.pop(i)
                break
        return res

    def infer(self, chem_config: Dict, depth: int = 1) -> Dict:
        """Infer chemistry configuration file using SMARTS templates.

        Args:
            chem_config (Dict): chemistry base config dictionary
            depth (int, optional): reaction net search depth. Defaults to 3.

        Returns:
            Dict: searched reaction dictionary, including main, side,
                and missed reactions.
        """
        reagent_smis, smi_dict, smi2mol_dict, intact_mols = [], {}, {}, []
        for species, species_dict in chem_config['chemistry']['species'][
                'reagents'].items():
            mol = Chem.MolFromSmiles(species_dict['smiles'], sanitize=False)
            Chem.SanitizeMol(mol, sanitizeOps=SANITIZE_ALL ^ SANITIZE_KEKULIZE)
            smi = Chem.MolToSmiles(mol)
            reagent_smis.append(smi)
            smi_dict[species] = smi
            smi2mol_dict[smi] = mol
            if 'intact' in species_dict and species_dict['intact']:
                intact_mols.append(mol)
        for species, species_dict in chem_config['chemistry']['species'][
                'products'].items():
            mol = Chem.MolFromSmiles(species_dict['smiles'], sanitize=False)
            Chem.SanitizeMol(mol, sanitizeOps=SANITIZE_ALL ^ SANITIZE_KEKULIZE)
            smi = Chem.MolToSmiles(mol)
            smi_dict[species] = smi
            smi2mol_dict[smi] = mol

        main_rxns = []
        for rxn in chem_config['chemistry']['reaction']['main']:
            rxn_reagents = [r.strip() for r in rxn.split('>')[0].split('+')]
            rxn_reagents = [r if ' ' in r else f'1 {r}' for r in rxn_reagents]
            rxn_products = [p.strip() for p in rxn.split('>')[1].split('+')]
            rxn_products = [p if ' ' in p else f'1 {p}' for p in rxn_products]
            rxn_reagent_smis = [
                smi_dict[r.split(' ')[1]] for r in rxn_reagents
                for _ in range(int(r.split(' ')[0]))
            ]
            rxn_product_smis = [
                smi_dict[p.split(' ')[1]] for p in rxn_products
                for _ in range(int(p.split(' ')[0]))
            ]
            rxn_lhs = '.'.join(sorted(rxn_reagent_smis))
            rxn_rhs = '.'.join(sorted(rxn_product_smis))
            main_rxns.append(f'{rxn_lhs}>{rxn_rhs}')

        reagent_mols = [smi2mol_dict[smi] for smi in reagent_smis]
        reaction_net = self._infer_reaction_net(reagent_mols, depth, intact_mols)
        overall_rxns = []
        for stage_dict in reaction_net.values():
            for mechanism_dict in stage_dict.values():
                for rxn in mechanism_dict['overall']:
                    overall_rxns.append(rxn)

        res = {'main': [], 'side': [], 'missed': []}
        main_rxn_flags = [False for _ in range(len(main_rxns))]
        for rxn in overall_rxns:
            for i, main_rxn in enumerate(main_rxns):
                main_rxn_lhs = main_rxn.split('>')[0]
                main_rxn_rhs = main_rxn.split('>')[1]
                if f'{main_rxn_lhs}>' in rxn and main_rxn_rhs in rxn.split('>')[1]:
                    if rxn not in res['main']:
                        res['main'].append(rxn)
                    main_rxn_flags[i] = True
            if rxn not in res['main']:
                res['side'].append(rxn)
        for main_rxn_flag, main_rxn in zip(main_rxn_flags, main_rxns):
            if not main_rxn_flag:
                res['missed'].append(main_rxn)
        return res

    def update(self, chem_config: Dict, chem_res: Dict) -> Dict:
        """Update searched results to chemistry base config file  

        Args:
            chem_res (Dict): searched chemistry results
            chem_config (Dict): chemistry base config dictionary

        Returns:
            Dict: chemistry inferred config dictionary
        """
        assert not chem_res['missed'], ('Reactions failed to identify:\n'
                                        '\n'.join(chem_res['missed']))
        reagent_smis, reagent_mols, product_smis, product_mols = [], [], [], []
        for species_dict in chem_config['chemistry']['species']['reagents'].values():
            reagent_mol = Chem.MolFromSmiles(species_dict['smiles'], sanitize=False)
            try:
                Chem.SanitizeMol(reagent_mol,
                                 sanitizeOps=SANITIZE_ALL ^ SANITIZE_KEKULIZE)
            except Exception:
                pass
            reagent_smi = Chem.MolToSmiles(reagent_mol)
            reagent_smis.append(reagent_smi)
            reagent_mols.append(reagent_mol)
        for species_dict in chem_config['chemistry']['species']['products'].values():
            product_mol = Chem.MolFromSmiles(species_dict['smiles'], sanitize=False)
            try:
                Chem.SanitizeMol(product_mol,
                                 sanitizeOps=SANITIZE_ALL ^ SANITIZE_KEKULIZE)
            except Exception:
                pass
            product_smi = Chem.MolToSmiles(product_mol)
            product_smis.append(product_smi)
            product_mols.append(product_mol)

        alphabet_gen = alphabet_generator()
        chem_config['chemistry']['species']['reagents'] = {}
        smi2index = {}
        for reagent_smi in reagent_smis:
            species_index = next(alphabet_gen)
            chem_config['chemistry']['species']['reagents'][species_index] = {
                'name': smiles2name(reagent_smi),
                'smiles': reagent_smi,
            }
            smi2index[reagent_smi] = species_index
        for product_smi in product_smis:
            species_index = next(alphabet_gen)
            chem_config['chemistry']['species']['products'][species_index] = {
                'name': smiles2name(product_smi),
                'smiles': product_smi,
            }
            smi2index[product_smi] = species_index

        main_lhs_smis, main_rhs_smis = [], []
        for main_rxn in chem_res['main']:
            for reagent_smi in main_rxn.split('>')[0].split('.'):
                if reagent_smi not in main_lhs_smis:
                    main_lhs_smis.append(reagent_smi)
            for product_smi in main_rxn.split('>')[1].split('.'):
                if product_smi not in main_rhs_smis:
                    main_rhs_smis.append(product_smi)
        intermediate_smis = [smi for smi in main_lhs_smis if smi in main_rhs_smis]
        byproduct_smis = [smi for smi in main_rhs_smis if smi not in main_lhs_smis]
        chem_config['chemistry']['species']['intermediates'] = {}
        chem_config['chemistry']['species']['byproducts'] = {}
        for intermediate_smi in intermediate_smis:
            if intermediate_smi not in smi2index:
                species_index = next(alphabet_gen)
                chem_config['chemistry']['species']['intermediates'][species_index] = {
                    'name': smiles2name(intermediate_smi),
                    'smiles': intermediate_smi,
                }
                smi2index[intermediate_smi] = species_index
        for byproduct_smi in byproduct_smis:
            if byproduct_smi not in smi2index:
                species_index = next(alphabet_gen)
                chem_config['chemistry']['species']['byproducts'][species_index] = {
                    'name': smiles2name(byproduct_smi),
                    'smiles': byproduct_smi,
                }
                smi2index[byproduct_smi] = species_index
        if not chem_config['chemistry']['species']['intermediates']:
            chem_config['chemistry']['species']['intermediates'] = None
        if not chem_config['chemistry']['species']['byproducts']:
            chem_config['chemistry']['species']['byproducts'] = None

        side_rhs_smis = []
        for side_rxn in chem_res['side']:
            for product_smi in side_rxn.split('>')[1].split('.'):
                if product_smi not in side_rhs_smis:
                    side_rhs_smis.append(product_smi)
        chem_config['chemistry']['species']['side products'] = {}
        for side_rhs_smi in side_rhs_smis:
            if side_rhs_smi not in smi2index:
                species_index = next(alphabet_gen)
                chem_config['chemistry']['species']['side products'][species_index] = {
                    'name': smiles2name(side_rhs_smi),
                    'smiles': side_rhs_smi,
                }
                smi2index[side_rhs_smi] = species_index
        if not chem_config['chemistry']['species']['side products']:
            chem_config['chemistry']['species']['side products'] = None

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

    def append_default_kinetics(self, chem_config: Dict) -> Dict:
        """Append default kinetics to searched reactions.

        Args:
            chem_config (Dict): Inferred chemistry configuration

        Returns:
            Dict: Inferred chemistry configuration with default kinetic phenomena
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

    def parameterize(self, chem_config: Dict, proc_config: Dict) -> Dict:
        chem_config['chemistry']['parameter'] = {}

        constants = []
        for rxn, rxn_phenos in chem_config['chemistry']['kinetics'].items():
            for rxn_pheno in rxn_phenos:
                for law_dict in self.entity['law'].values():
                    if law_dict['pheno'] != rxn_pheno:
                        continue
                    for param in law_dict['vars']:
                        param_dict = self.entity['var'][param]
                        if param_dict['cls'] == 'Constant':
                            if param not in constants:
                                constants.append(param)
        if constants:
            chem_config['chemistry']['parameter']['constant'] = {}
        else:
            chem_config['chemistry']['parameter']['constant'] = None
        for constant in constants:
            constant_dict = self.entity['var'][constant]
            chem_config['chemistry']['parameter']['constant'][constant] = {
                'unit': constant_dict['unit'],
                'val': constant_dict['val']
            }

        for rxn, rxn_phenos in chem_config['chemistry']['kinetics'].items():
            chem_config['chemistry']['parameter'][rxn] = {}
            for rxn_pheno in rxn_phenos:
                for law_dict in self.entity['law'].values():
                    if law_dict['pheno'] != rxn_pheno:
                        continue
                    for param in law_dict['vars']:
                        param_dict = self.entity['var'][param]
                        unit = param_dict['unit']
                        if param_dict['cls'] != 'ReactionParameter':
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
                        config_param_dict = {}
                        if set(param_dict['dims']) == set(['Reaction']):
                            config_param_dict['unit'] = unit
                            config_param_dict['min'] = None
                            config_param_dict['max'] = None
                        if set(param_dict['dims']) == set(['Reaction', 'Species']):
                            for species, val in lhs_species_dict.items():
                                config_param_dict[species] = {}
                                config_param_dict[species]['unit'] = unit
                                if param == 'Partial_Order':
                                    config_param_dict[species]['val'] = val
                                else:
                                    config_param_dict[species]['val'] = None
                        if set(param_dict['dims']) == set(['Stream', 'Reaction']):
                            for stream in streams:
                                config_param_dict[stream] = {}
                                config_param_dict[stream]['unit'] = unit
                                config_param_dict[stream]['min'] = None
                                config_param_dict[stream]['max'] = None
                        chem_config['chemistry']['parameter'][rxn][
                            param] = config_param_dict

        chem_config['file type'] = 'chemistry parameterized'
        return chem_config

    def infer_and_dump(self, in_chem_cfg_path: str, out_chem_cfg_path: str):
        """Infer and dump chemistry base config

        Args:
            in_chem_cfg_path (str): path to input chemistry base config
            out_chem_cfg_path (str): path to output chemistry inferred config
        """
        config = yaml.load(open(in_chem_cfg_path), yaml.FullLoader)
        reaction_net_res = self.infer(config)
        config = self.update(config, reaction_net_res)
        config = self.append_default_kinetics(config)
        yaml.dump(config, open(out_chem_cfg_path, 'w'), sort_keys=False)

    def parameterize_and_dump(self, in_chem_cfg_path: str, proc_cfg_path: str,
                              out_chem_cfg_path: str):
        """Parameterize chemistry config based on assigned phenomena

        Args:
            in_chem_cfg_path (str): path to input chemistry inferred config file
            proc_cfg_path (str): path to process base config file
            out_chem_cfg_path (str): path to output chemistry inferred config file
        """
        chem_config = yaml.load(open(in_chem_cfg_path), yaml.FullLoader)
        proc_config = yaml.load(open(proc_cfg_path), yaml.FullLoader)
        chem_config = self.parameterize(chem_config, proc_config)
        yaml.dump(chem_config, open(out_chem_cfg_path, 'w'), sort_keys=False)

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
                    exit(0)
        else:
            os.mkdir(out_chem_dir)

        config = yaml.load(open(in_chem_cfg_path), yaml.FullLoader)
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
            yaml.dump(cand_config, open(out_chem_cfg_path, 'w'), sort_keys=False)
