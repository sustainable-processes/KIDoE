from multiprocessing.pool import ThreadPool
from typing import Dict, List, Tuple

import pubchempy as pcp
import requests
from bs4 import BeautifulSoup


def name2smiles(name):
    compounds = pcp.get_compounds(name, namespace='name')
    if compounds:
        return compounds[0].connectivity_smiles
    return None


class MITSolubilityAgent:
    """MIT solubility agent for predicting solubility."""

    def __init__(self):
        super().__init__()
        self.url = ('https://rmg.mit.edu/database/solvation/searchSolubility/'
                    'solv={solv}__solu={solu}__T={temp}__refSolv={ref_solv}__'
                    'refS={ref_s}__refT={ref_t}__Hsub={h_sub}__Cpg={c_pg}__Cps={c_ps}')

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
        solvents = [solvent for solvent in solvents if ':' not in solvent]
        solute_smis = [solute['smiles'] for solute in solutes]
        pool = ThreadPool(8)
        solvent_smis = pool.map(name2smiles, solvents)
        pool.close()
        url = self.url
        solu_span = '_'.join([smi for smi in solute_smis for _ in solvent_smis])
        solv_span = '_'.join([smi for _ in solute_smis for smi in solvent_smis])
        temp_span = '_'.join(['303.15' for _ in solvent_smis for _ in solute_smis])
        none_span = '_'.join(['None'] * (len(solute_smis) * len(solvent_smis)))
        url = url.replace('{solu}', solu_span)
        url = url.replace('{solv}', solv_span)
        url = url.replace('{temp}', temp_span)
        url = url.replace('{ref_solv}', none_span)
        url = url.replace('{ref_s}', none_span)
        url = url.replace('{ref_t}', none_span)
        url = url.replace('{h_sub}', none_span)
        url = url.replace('{c_pg}', none_span)
        url = url.replace('{c_ps}', none_span)
        url = url.replace('#', '%23')
        soup = BeautifulSoup(requests.get(url).text, features='lxml')
        solubility = [tr.find_all('td')[11].text for tr in soup.find_all('tr')[1:]]
        solubility = [
            [
                str(round(10 ** float(solubility[i * len(solute_smis) + j]), 3))
                if solubility[i * len(solute_smis) + j] != '-'
                else '-'
                for i in range(len(solvent_smis))
            ]
            for j in range(len(solute_smis))
        ]
        res = [[''] + solvents]
        for solute, sol in zip(solutes, solubility):
            res.append([solute['name']] + sol)
        return res
