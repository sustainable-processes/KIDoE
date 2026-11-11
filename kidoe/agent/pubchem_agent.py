from multiprocessing.pool import ThreadPool
from typing import Dict, List

import pubchempy as pcp
import requests
from pubchempy import Compound


class PubChemAgent:
    """PubChem agent for retrieving physicochemical properties.
    
    PUG View is used as a REST-style web service that provides information content as 
    a programmatic web service.
    """

    def __init__(self):
        super().__init__()
        self.properties = ['Density', 'Viscosity']
        self.pubchem_url = ('https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/'
                            'compound/{cid}/JSON?heading={property}')

    def query(self, chem_config: Dict, proc_config: Dict) -> List[list]:
        solvents = []
        for stream in proc_config['process']['inlet']:
            solvent = proc_config['process']['inlet'][stream]['solvent']
            if solvent not in solvents:
                solvents.append(solvent)
        pool = ThreadPool(8)
        compounds = pool.map(self._get_compound, solvents)
        res = pool.map(self._query, compounds)
        pool.close()
        table = [['Solvent'] + self.properties]
        for solvent, r in zip(solvents, res):
            table.append([solvent] + [r[property] for property in self.properties])
        return table

    def _query(self, compound):
        res = {}
        for property in self.properties:
            url = self.pubchem_url
            url = url.replace('{cid}', str(compound.cid))
            url = url.replace('{property}', property)
            response = requests.get(url).json()
            response = response['Record']['Section'][0]['Section'][0]['Section'][0]
            response = [
                {
                    'reference':
                    res['Reference'][0],
                    'value':
                    res['Value']['StringWithMarkup'][0]['String'].replace(
                        r'\u00b0', '&deg;'),
                } for res in response['Information']
                if 'Reference' in res and 'Value' in res and 'StringWithMarkup' in
                res['Value'] and 'Markup' not in res['Value']['StringWithMarkup'][0]
            ]
            if response:
                res[property] = response[0]['value']
        return res

    def _get_compound(self, identifier: str) -> Compound | None:
        compound = pcp.get_compounds(identifier, namespace='name')
        if compound:
            return compound[0]
        return None
