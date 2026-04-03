from typing import Dict

import numpy as np
from pandas import DataFrame
from scipy.stats import qmc
from scipy.stats.qmc import LatinHypercube


class DoEAgent:
    """Agent for design of Experiments to construct initial dataset.
    """
    def __init__(self, seed=42):
        super().__init__()
        self.rng = np.random.default_rng(seed)
    
    def run(self, domain: Dict, method: str, num_exps: int) -> DataFrame:
        """Generate experimental conditions based on the given domain and method.

        Args:
            domain (Dict): operation domain with parameter ranges
            method (str): DoE method, e.g., 'latin_hypercube'
            num_exps (int): number of experiments to generate
        
        Returns:
            DataFrame: generated experimental conditions
        """
        if method == 'latin_hypercube':
            lhc = LatinHypercube(len(domain), rng=self.rng)
            sample = lhc.random(num_exps)
            l_bounds = [bounds[0] for bounds in domain.values()]
            u_bounds = [bounds[1] for bounds in domain.values()]
            sample = qmc.scale(sample, l_bounds, u_bounds)
            sample = DataFrame(sample, columns=domain.keys())
        else:
            raise NotImplementedError(f'DoE method {method} not implemented.')
        return sample