import itertools
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kidoe.agent.model_agent import ModelAgent

model_agent = ModelAgent(err='rmsre', high_prec=True)
chem_config_files = os.listdir('cases/lhe/chem')
proc_config_files = os.listdir('cases/lhe/proc')

data_path = 'cases/lhe/run/0/data/data_init.csv'
rmse_dict = {}
for chem_config_file, proc_config_file in itertools.product(chem_config_files, proc_config_files):
    chem_index = int(os.path.basename(chem_config_file).rsplit('_')[-1][:-5])
    proc_index = int(os.path.basename(proc_config_file).rsplit('_')[-1][:-5])
    chem_path = os.path.join('cases/lhe/chem', chem_config_file)
    proc_path = os.path.join('cases/lhe/proc', proc_config_file)
    out_path = f'cases/lhe/run/0/model/{chem_index}_{proc_index}'
    rmse = model_agent.calibrate_and_dump(chem_path, proc_path, data_path, out_path)
    rmse_dict[f'{chem_index}_{proc_index}'] = rmse
with open('cases/lhe/run/0/error.json', 'w') as f:
    json.dump(rmse_dict, f)
