import os
import sys

import numpy as np
import pandas as pd
from bayes_opt import BayesianOptimization, acquisition
from pandas import DataFrame
from scipy.stats.qmc import LatinHypercube, scale

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kidoe.benchmark import SnarPyrrolidineCSTRBenchmark

N = 6
seed = 12
rng = np.random.default_rng(seed)
snar_prld_exp = SnarPyrrolidineCSTRBenchmark()
domain = snar_prld_exp.domain
domain = {k: v for k, v in domain.items() if k != 'conc_dfnb'}
lhc = LatinHypercube(len(domain), rng=rng)
sample = lhc.random(N)
l_bounds = [v[0] for v in domain.values()]
u_bounds = [v[1] for v in domain.values()]
dataset = DataFrame(scale(sample, l_bounds, u_bounds), columns=domain.keys())
dataset['conc_dfnb'] = 0.1
dataset = snar_prld_exp.run_experiments(dataset)

acq = acquisition.UpperConfidenceBound()
optimizer = BayesianOptimization(
    f=None,
    pbounds=domain,
    acquisition_function=acq,
    random_state=seed
)
for i, data in dataset.iterrows():
    x = [data[k] for k in domain]
    y = data['yield']
    optimizer.register(params=x, target=y)
for i in range(N):
    sug_dataset = optimizer.suggest()
    sug_dataset = {k: [v.item()] for k, v in sug_dataset.items()}
    sug_dataset['conc_dfnb'] = [0.1]
    sug_dataset = pd.DataFrame(sug_dataset)
    new_dataset = snar_prld_exp.run_experiments(sug_dataset)
    x = [new_dataset.loc[0, k] for k in domain]
    y = new_dataset.loc[0, 'yield']
    optimizer.register(params=x, target=y)
    dataset = pd.concat([dataset, new_dataset], ignore_index=True)
print(dataset)