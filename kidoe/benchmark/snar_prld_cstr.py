import hashlib

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp, trapezoid


class SnarPyrrolidineCSTRBenchmark:
    """Benchmark of a pyrrolidine nucleophilic aromatic substitution (SNAr) reaction

    The SNAr reactions occurs in a continuously stirred-tank reactor where residence 
    time, reactant concentration, and temperature can be adjusted. Yield maximization 
    is the target of single-objective optimization. Space-time yield (STY) and E-factor 
    are the targets of multi-objective optimization.

    Parameters:
        noise_level (float): The mean of the random relative noise added to the 
            concentration measurements. Default is 0.05.

    Examples:
    # TODO

    Notes:
    This benchmark relies on the kinetics observed by Hone et al and residence time 
    distribution obtained by Pittaway et al. The mechanistic segregation model is 
    integrated using scipy to find outlet concentrations of all species. These
    concentrations are then used to calculate yield, STY, and E-factor.

    References:
    .. Hone, C. A., Holmes, N., Akien, G. R., Bourne, R. A., & Muller, F. L. (2017). 
       Rapid multistep kinetic model generation from transient flow data. Reaction 
       Chemistry & Engineering, 2(2), 103–108. <https://doi.org/10.1039/C6RE00109B>
    .. Pittaway, P. M., Ghasemi, G., Knox, S. T., Cayre, O. J., Kapur, N., & Warren, 
       N. J. (2023). Continuous synthesis of block copolymer nanoparticles via 
       telescoped RAFT solution and dispersion polymerisation in a miniature CSTR 
       cascade. Reaction Chemistry & Engineering, 8(3), 707–717. 
       <https://doi.org/10.1039/D2RE00475E>

    """

    def __init__(self, noise_level: float = 0.005, seed: int = 0):
        super().__init__()
        self._setup_domain()
        self.noise_level = noise_level
        self.seed = seed
        self.thetas = np.array([
            0.079688185, 0.080699988, 0.083665617, 0.100412696, 0.122707245,
            0.130138762, 0.150828382, 0.168761713, 0.192905419, 0.243495554,
            0.300470513, 0.337069859, 0.373041190, 0.414106424, 0.463824315,
            0.520938833, 0.607709638, 0.730277324, 0.911564456, 1.084792057,
            1.328950516, 1.737683919, 2.160408110, 2.672833845, 3.179467881,
            3.507640855, 3.814705531, 4.220822202, 4.651954823, 5.061106902,
            5.372567686, 5.766612504, 6.141607520, 6.534675426, 6.794499382
        ])
        self.E_thetas = np.array([
            0.000000000, 0.135100729, 0.351590762, 0.514337545, 0.661415402,
            0.798701505, 0.877173440, 0.941620784, 0.978018947, 1.005834739,
            0.986802881, 0.959231087, 0.929049574, 0.880069593, 0.823249844,
            0.761666826, 0.685751567, 0.583208682, 0.452924265, 0.357107243,
            0.256760341, 0.155055536, 0.093960515, 0.054613157, 0.031751589,
            0.026298760, 0.018013431, 0.012189300, 0.008306547, 0.006439430,
            0.003193194, 0.002652154, 0.002970413, 0.000562257, 0.003415974
        ])

    def _setup_domain(self):
        self.domain = {
            'tau': [0.5, 2.0],
            'conc_dfnb': [0.1, 0.5],
            'equiv_prld': [1.0, 5.0],
            'temperature': [30, 120],
        }

    def _run(self, conditions):
        tau = conditions['tau']
        conc_dfnb = conditions['conc_dfnb']
        equiv_prld = conditions['equiv_prld']
        temperature = conditions["temperature"]
        outlet_conc_dfnb, outlet_conc_ortho, yld, sty, e_factor = self._integrate_equations(
            tau, conc_dfnb, equiv_prld, temperature)
        res = {
            'outlet_conc_dfnb': outlet_conc_dfnb,
            'outlet_conc_ortho': outlet_conc_ortho,
            'yield': yld,
            'sty': sty,
            'e-factor': e_factor,
        }
        return res

    def _integrate_equations(self, tau, conc_dfnb, equiv_prld, temperature):
        self.C_i = np.zeros(5)
        self.C_i[0] = conc_dfnb
        self.C_i[1] = equiv_prld * conc_dfnb

        # Integrate
        res = solve_ivp(
            self._integrand,
            [0, tau * self.thetas[-1]],
            self.C_i,
            t_eval=tau * self.thetas,
            args=(temperature,),
        )
        C_final = [trapezoid(res.y[i] * self.E_thetas, self.thetas) for i in range(5)]
        C_final = np.array(C_final)

        # Add measurement noise
        input_tuple = (round(float(tau), 6), round(float(conc_dfnb), 6),
                       round(float(equiv_prld), 6), round(float(temperature), 6))

        seed_str = str(input_tuple).encode('utf-8')
        seed_int = int(hashlib.md5(seed_str).hexdigest(), 16) % (2**32) + self.seed
        C_final += (
            C_final * self.noise_level *
            np.clip(np.random.default_rng(seed_int).normal(size=len(C_final)), -3, 3))
        C_final[C_final < 0] = 0


        M = [159.09, 71.12, 210.21, 210.21, 261.33]
        V = 5
        q_tot = V / tau
        rho_eth = 0.789
        yld = C_final[2] / self.C_i[0]
        sty = C_final[2] / tau * 60 * M[2]  # kg m^-3 h^-1
        term_2 = 1e-3 * sum(M[i] * C_final[i] * q_tot for i in range(5) if i != 2)
        if np.isclose(C_final[2], 0.0):
            e_factor = 1e3
        else:
            e_factor = (q_tot * rho_eth + term_2) / (1e-3 * M[2] * C_final[2] * q_tot)

        return C_final[0], C_final[2], yld, sty, e_factor

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
        res = []
        for i, condition in conditions.iterrows():
            condition = condition.to_dict()
            exp = condition.copy()
            exp.update(self._run(condition))
            res.append(exp)
        res = pd.DataFrame(res)
        res = res.round(6)
        return res
