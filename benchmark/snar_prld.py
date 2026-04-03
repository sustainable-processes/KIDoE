import hashlib

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp


class SnarPyrrolidineBenchmark:
    """Benchmark of a pyrrolidine nucleophilic aromatic substitution (SNAr) reaction

    The SNAr reactions occurs in a plug flow reactor where residence time, reactant 
    concentration, and temperature can be adjusted. Yield maximization is the target 
    in single-objective optimization. Space time yield (STY) and E-factor are the 
    targets in multi-objective optimization.

    Parameters:
        noise_level (float): The mean of the random relative noise added to the 
            concentration measurements. Default is 0.05.

    Examples:
    # TODO

    Notes:
    This benchmark relies on the kinetics observerd by Hone et al. The mechanistic
    model is integrated using scipy to find outlet concentrations of all species. These
    concentrations are then used to calculate yield.

    References:
    .. [Hone] C. A. Hone et al., React. Chem. Eng., 2017, 2, 103–108. DOI:
       `10.1039/C6RE00109B <https://doi.org/10.1039/C6RE00109B>`_
    """

    def __init__(self, noise_level: float = 0.01, seed: int = 0):
        super().__init__()
        self._setup_domain()
        self.noise_level = noise_level
        self.seed = seed

    def _setup_domain(self):
        self.domain = {
            'tau': [0.5, 2.0],
            'conc_dfnb': [0.1, 0.5],
            'equiv_pldn': [1.0, 5.0],
            'temperature': [30, 120],
        }

    def _run(self, conditions):
        tau = conditions['tau']
        conc_dfnb = conditions['conc_dfnb']
        equiv_pldn = conditions['equiv_pldn']
        temperature = conditions["temperature"]
        outlet_conc_ortho, yld, sty, e_factor = self._integrate_equations(
            tau, conc_dfnb, equiv_pldn, temperature)
        res = {
            'outlet_conc_ortho': outlet_conc_ortho,
            'yield': yld,
            'sty': sty,
            'e-factor': e_factor,
        }
        return res

    def _integrate_equations(self, tau, conc_dfnb, equiv_pldn, temperature):
        self.C_i = np.zeros(5)
        self.C_i[0] = conc_dfnb
        self.C_i[1] = equiv_pldn * conc_dfnb

        # Integrate
        res = solve_ivp(self._integrand, [0, tau], self.C_i, args=(temperature,))
        C_final = res.y[:, -1]

        # Add measurement noise
        input_tuple = (
            round(float(tau), 6),
            round(float(conc_dfnb), 6),
            round(float(equiv_pldn), 6),
            round(float(temperature), 6)
        )

        seed_str = str(input_tuple).encode('utf-8')
        seed_int = int(hashlib.md5(seed_str).hexdigest(), 16) % (2**32) + self.seed
        C_final += (
            C_final * self.noise_level *
            np.clip(np.random.default_rng(seed_int).normal(size=len(C_final)), -3, 3))
        C_final[
            C_final < 0
        ] = 0  # prevent negative values of concentration introduced by noise

        M = [159.09, 71.12, 210.21, 210.21, 261.33]
        V = 5
        q_tot = V / tau
        rho_eth = 0.789
        yld = C_final[2] / self.C_i[0]
        sty = C_final[2] / tau * 60 * M[2] # kg m^-3 h^-1
        term_2 = 1e-3 * sum([M[i] * C_final[i] * q_tot for i in range(5) if i != 2])
        if np.isclose(C_final[2], 0.0):
            e_factor = 1e3
        else:
            e_factor = (q_tot * rho_eth + term_2) / (1e-3 * M[2] * C_final[2] * q_tot)

        return C_final[2], yld, sty, e_factor

    def _integrand(self, t, C, T):
        # Kinetic Constants
        R = 8.314 / 1000  # kJ/K/mol
        T_ref = 90 + 273.71  # Convert to deg K
        T = T + 273.71  # Convert to deg K
        # Need to convert from 10^-2 M^-1s^-1 to M^-1min^-1
        def k(k_ref, E_a, temp):
            return 0.6 * k_ref * np.exp(-E_a / R * (1 / temp - 1 / T_ref))
        k_a = k(57.9, 33.3, T)
        k_b = k(2.70, 35.3, T)
        k_c = k(0.865, 38.9, T)
        k_d = k(1.63, 44.8, T)

        # Reaction Rates
        r = np.zeros(5)
        for i in [0, 1]:  # Set to reactants when close
            C[i] = 0 if C[i] < 1e-6 * self.C_i[i] else C[i]
        r[0] = -(k_a + k_b) * C[0] * C[1]
        r[1] = -(k_a + k_b) * C[0] * C[1] - k_c * C[1] * C[2] - k_d * C[1] * C[3]
        r[2] = k_a * C[0] * C[1] - k_c * C[1] * C[2]
        r[3] = k_b * C[0] * C[1] - k_d * C[1] * C[3]
        r[4] = k_c * C[1] * C[2] + k_d * C[1] * C[3]

        # Deltas
        dcdtau = r
        return dcdtau

    def run_experiments(self, conditions):
        """Run the experiments at the given conditions

        Args:
            conditions (pd.DataFrame): A dataset with columns matching variables in 
                the experiment.
        """
        # Run experiments
        # TODO: Add an option to run these in parallel
        res = []
        for i, condition in conditions.iterrows():
            condition = condition.to_dict()
            exp = condition.copy()
            exp.update(self._run(condition))
            res.append(exp)
        res = pd.DataFrame(res)
        return res
