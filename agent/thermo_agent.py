import re
from functools import partial
from multiprocessing.pool import ThreadPool
from typing import Dict, List, Tuple

from rdkit import Chem
from rdkit.Chem.rdchem import Mol
from thermo.chemical import Chemical, Mixture


class ThermoAgent:
    """Thermo agent for calculating physicochemical properties.
    
    Thermo is open-source software that facilitates the retrieval of constants of 
    chemicals, the calculation of temperature and pressure dependent chemical
    properties (both thermodynamic and transport), and the calculation of the same for 
    chemical mixtures (including phase equilibria) using various models.
    """

    def __init__(self):
        super().__init__()
        self.solvent_properties = ['Density', 'Viscosity']
        self.solute_properties = ['Diffusion Coefficient']

    def query(self, chem_config: Dict, proc_config: Dict) -> Tuple[List]:
        solutes = []
        for role in chem_config['chemistry']['species']:
            if not chem_config['chemistry']['species'][role]:
                continue
            solutes.extend(chem_config['chemistry']['species'][role].values())
        solvents = []
        for stream in proc_config['process']['inlet']:
            solvent = proc_config['process']['inlet'][stream]['solvent']
            if solvent not in solvents:
                solvents.append(solvent)
        pool = ThreadPool(8)
        solvent_properties = pool.map(self._query_solvent, solvents)
        solute_properties = pool.map(
            partial(self._query_solute,
                    solvents=solvents,
                    solvent_properties=solvent_properties), solutes)
        pool.close()
        solvent_table = [['Solvent'] + self.solvent_properties]
        for solvent, solvent_property in zip(solvents, solvent_properties):
            solvent_table.append(
                [solvent] +
                [solvent_property[property] for property in self.solvent_properties])
        solute_table = [['Solute'] + self.solute_properties]
        for solute, solute_property in zip(solutes, solute_properties):
            solute_table.append([solute['name']] + [
                solute_solvent_property[property]
                for property in self.solute_properties for solvent,
                solute_solvent_property in solute_property.items()
            ])
        return solvent_table, solute_table

    def _query_solvent(self, solvent: str) -> Dict:
        def assoc_mapping(solvent: str) -> float:
            if solvent.lower() == 'water':
                return 2.6
            elif solvent.lower() == 'methanol':
                return 1.9
            elif solvent.lower().endswith('nol'):
                return 1.5
            else:
                return 1.0
        try:
            match = re.match(r'^(.*)\(([^\(\)]*)\)$', solvent)
            if match:
                solvents = match[1].split(':')
                ratios = [float(r) for r in match[2].split(':')]
                ratios = [r / sum(ratios) for r in ratios]
                mixture = Mixture(solvents, Vfls=ratios, T=263.15, P=101325)
                assocs = [assoc_mapping(s) for s in solvents]
                assoc = sum(a * r for a, r in zip(assocs, ratios))
                return {
                    'Density': f'{mixture.rho:.4f} kg/m3',
                    'Viscosity': f'{mixture.mu:.6f} Pa.s',
                    'MW': f'{mixture.MW:.4f}',
                    'Association': f'{assoc:.4f}',
                }
            else:
                chemical = Chemical(solvent)
                chemical.calculate(T=263.15, P=101325)
                return {
                    'Density': f'{chemical.rho:.4f} kg/m3',
                    'Viscosity': f'{chemical.mu:.6f} Pa.s',
                    'MW': f'{chemical.MW:.4f}',
                    'Association': f'{assoc_mapping(solvent):.4f}'
                }
        except Exception:
            return {
                'Density': None,
                'Viscosity': None,
                'MW': None,
                'Association': None
            }

    def _query_solute(self, solute: Dict, solvents: List[str],
                      solvent_properties: List[Dict]) -> Dict:
        """Wilke-Chang equation"""
        def estimate_vc(mol: Mol) -> float:
            joback_groups = {
                '-CH3': ('[CH3;X4]', 65),
                '-CH2-': ('[CH2;X4;!R]', 56),
                '>CH-': ('[CH1;X4;!R]', 41),
                '>C<': ('[CH0;X4;!R]', 31),
                '-CH2- (ring)': ('[CH2;X4;R]', 52),
                '>CH- (ring)': ('[CH1;X4;R]', 37),
                '=CH2': ('[CH2;X3;!R]', 56),
                '=CH-': ('[CH1;X3;!R]', 46),
                '-OH (alcohol)': ('[OX2H;!$(OC=O);!$(Oc)]', 28),
                '-Cl': ('[Cl]', 58),
                '-F': ('[F]', 27),
                '-NH2': ('[NH2;X3]', 28),
                '>NH (ring)': ('[NH1;X3;R]', 35),
            }
            total_contribution = 0
            matched_atoms = set()
            for name, (smarts, weight) in joback_groups.items():
                pattern = Chem.MolFromSmarts(smarts)
                matches = mol.GetSubstructMatches(pattern)
                for match in matches:
                    if not any(idx in matched_atoms for idx in match):
                        total_contribution += weight
                        for idx in match:
                            matched_atoms.add(idx)
            v_c = 17.5 + total_contribution
            return v_c
        vc = estimate_vc(Chem.MolFromSmiles(solute['smiles']))
        res = {}
        T = 263.15
        for j, solvent in enumerate(solvents):
            res[solvent] = {}
            assoc = float(solvent_properties[j]['Association'].split(' ')[0])
            mw = float(solvent_properties[j]['MW'])
            mu = float(solvent_properties[j]['Viscosity'].split(' ')[0])
            D = 7.4e-8 * (
                assoc * mw)**0.5 * T / (1000 * mu) / (0.285 * vc**1.048)**0.6 * 1e-4
            res[solvent]['Diffusion Coefficient'] = f'{D:.6g} m2/s [{solvent}]'
        return res
