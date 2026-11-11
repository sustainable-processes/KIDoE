import itertools
import json
import os
import sys

import numpy as np
import pandas as pd
import yaml
from pandas import DataFrame
from scipy.stats.qmc import LatinHypercube, scale

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kidoe.agent.model_agent import ModelAgent
from kidoe.benchmark import SnarPyrrolidineCSTRBenchmark

N = 6
seed = 12
rng = np.random.default_rng(seed)
snar_prld_exp = SnarPyrrolidineCSTRBenchmark()
domain = snar_prld_exp.domain
lhc = LatinHypercube(len(domain), rng=rng)
sample = lhc.random(N)
l_bounds = [v[0] for v in domain.values()]
u_bounds = [v[1] for v in domain.values()]
dataset = DataFrame(scale(sample, l_bounds, u_bounds), columns=list(domain.keys()))
dataset = snar_prld_exp.run_experiments(dataset)

model_agent = ModelAgent(maxiter=500)
chem_config_files = os.listdir('cases/snar_multi_obj/chem')
proc_config_files = os.listdir('cases/snar_multi_obj/proc')

os.mkdir('cases/snar_multi_obj/run/0')
os.mkdir('cases/snar_multi_obj/run/0/data')
data_path = 'cases/snar_multi_obj/run/0/data/data.csv'
dataset.to_csv(data_path, index=False)
for i in range(6):
    os.mkdir(f'cases/snar_multi_obj/run/{i}/model')
    data_path = f'cases/snar_multi_obj/run/{i}/data/data.csv'
    rmse_dict = {}
    for chem_config_file, proc_config_file in itertools.product(chem_config_files, proc_config_files):
        chem_index = int(os.path.basename(chem_config_file).rsplit('_')[-1][:-5])
        proc_index = int(os.path.basename(proc_config_file).rsplit('_')[-1][:-5])
        chem_path = os.path.join('cases/snar_multi_obj/chem', chem_config_file)
        proc_path = os.path.join('cases/snar_multi_obj/proc', proc_config_file)
        out_path = f'cases/snar_multi_obj/run/{i}/model/{chem_index}_{proc_index}'
        rmse = model_agent.calibrate_and_dump(chem_path, proc_path, data_path, out_path)
        rmse_dict[f'{chem_index}_{proc_index}'] = rmse
    with open(f'cases/snar_multi_obj/run/{i}/rmse.json', 'w') as f:
        json.dump(rmse_dict, f)
    with open('cases/snar_multi_obj/proc_param.yaml') as f:
        proc_config = yaml.load(f, yaml.FullLoader)
    sug_dataset = model_agent.suggest(f'cases/snar_multi_obj/run/{i}/model', proc_config, dataset, 1)
    sug_dataset = sug_dataset[list(domain.keys())]
    new_dataset = snar_prld_exp.run_experiments(sug_dataset)
    dataset = pd.concat([dataset, new_dataset], ignore_index=True)
    os.mkdir(f'cases/snar_multi_obj/run/{i+1}')
    os.mkdir(f'cases/snar_multi_obj/run/{i+1}/data')
    dataset.to_csv(f'cases/snar_multi_obj/run/{i+1}/data/data.csv', index=False)
print(dataset)