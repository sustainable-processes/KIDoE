import itertools
import os
import sys

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kidoe.agent.model_agent import ModelAgent

model_agent = ModelAgent()
chem_config_files = os.listdir('cases/suzuki_g3/chem')
proc_config_files = os.listdir('cases/suzuki_g3/proc')

chem_index, proc_index = 0, 0
out_path = f'cases/suzuki_g3/run/4/model/{chem_index}_{proc_index}'
chem_path = os.path.join(out_path, 'chem_0.yaml')
proc_path = os.path.join(out_path, 'proc_0.yaml')
with open(chem_path) as f:
    chem_config = yaml.load(f, yaml.FullLoader)
with open(proc_path) as f:
    proc_config = yaml.load(f, yaml.FullLoader)

dataset = {
    'conc_o2': [],
    'conc_sub': [],
    'residence_time': [],
    'coupl_part_mol_eq': [],
    'cat_loading': [],
    'base_mol_eq': [],
    'temperature': [],
}

for (
    residence_time,
    coupl_part_mol_eq,
    cat_loading,
    base_mol_eq,
    temperature,
) in itertools.product(
    np.linspace(90, 90, 1),
    np.linspace(1.0, 1.5, 21),
    np.linspace(2.5, 2.5, 1),
    np.linspace(1.5, 1.5, 1),
    np.linspace(80, 180, 21),
):
    dataset['conc_sub'].append(0.01)
    dataset['residence_time'].append(residence_time)
    dataset['coupl_part_mol_eq'].append(coupl_part_mol_eq)
    dataset['cat_loading'].append(cat_loading)
    dataset['base_mol_eq'].append(base_mol_eq)
    dataset['temperature'].append(temperature)
    dataset['conc_o2'].append(0.0014)

dataset = pd.DataFrame(dataset)
sim_dataset = model_agent.simulate(chem_config, proc_config, dataset)
for i in range(21):
    for j in range(21):
        print(sim_dataset.loc[21 * i + j, 'yield(sim)'] * 100, end=' ')
    print()