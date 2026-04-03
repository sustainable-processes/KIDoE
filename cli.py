import argparse
import json
import os
import sys

import pandas as pd
import yaml
from terminaltables import AsciiTable

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kidoe.agent.mit_solubility_agent import MITSolubilityAgent
from kidoe.agent.model_agent import ModelAgent
from kidoe.agent.process_agent import ProcessAgent
from kidoe.agent.pubchem_agent import PubChemAgent
from kidoe.agent.reaction_agent import ReactionAgent
from kidoe.agent.thermo_agent import ThermoAgent

parser = argparse.ArgumentParser(
    prog='kidoe',
    description='KIDoE: knowledge-informed design of experiments'
)
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0')
subparsers = parser.add_subparsers(
    dest='mode', help='kidoe includes `chem`, `proc`, `query`, and `model` modes'
)

chem_parser = subparsers.add_parser(
    'chem',
    help='mode to infer reaction, parameterize '
    'kinetics, and generate candidate chemistry '
    'configs',
)
chem_parser.add_argument(
    'action', choices=['infer', 'param', 'gen'], help='actions under %(prog)s'
)
chem_parser.add_argument(
    '-c',
    '--chem_cfg',
    type=str,
    required=True,
    help='path to input chemistry config file',
)
chem_parser.add_argument(
    '-p', '--proc_cfg', type=str, help='path to input process config file'
)
chem_parser.add_argument(
    '-o', '--out_path', type=str, help='path to output config file or dir'
)
chem_parser.add_argument(
    '-d', '--depth', type=int, default=1, help='chemistry inference depth'
)
chem_parser.add_argument(
    '-s',
    '--source',
    choices=['uspto'],
    default='uspto',
    help='template source, (default: %(default)s)',
)

proc_parser = subparsers.add_parser(
    'proc', help='mode to parameterize process and generate candidate process configs'
)
proc_parser.add_argument(
    'action', choices=['param', 'gen'], help='actions under %(prog)s'
)
proc_parser.add_argument(
    '-p',
    '--proc_cfg',
    type=str,
    required=True,
    help='path to input process config file',
)
proc_parser.add_argument(
    '-c', '--chem_cfg', type=str, help='path to input chemistry config file'
)
proc_parser.add_argument(
    '-o', '--out_path', type=str, help='path to output config file or dir'
)

model_parser = subparsers.add_parser(
    'model', help='mode to simulate and calibrate candidate configs'
)
model_parser.add_argument(
    'action',
    choices=['sim', 'sim-mc', 'cal', 'cal-mc', 'sug', 'sug-mc'],
    help='actions under %(prog)s',
)
model_parser.add_argument(
    '-c', '--chem_path', type=str, help='path to input chemistry config file or dir'
)
model_parser.add_argument(
    '-p', '--proc_path', type=str, help='path to input process config file or dir'
)
model_parser.add_argument(
    '-f', '--fast_reaction', type=bool, default=False, help='fast reaction or not'
)
model_parser.add_argument(
    '-n',
    '--num_experiments',
    type=int,
    default=None,
    help='number of suggested experiments (default: overall candidate points',
)
model_parser.add_argument(
    '-d', '--data_path', type=str, help='path to experimental dataset'
)
model_parser.add_argument(
    '-o', '--out_path', type=str, help='path to output config file or dir'
)

query_parser = subparsers.add_parser(
    'query', help='query info from AI models and databases'
)
query_parser.add_argument(
    'action',
    choices=['all', 'pubchem', 'thermo', 'solubility'],
    help='actions under %(prog)s',
)
query_parser.add_argument(
    '-c', '--chem_path', type=str, help='path to input chemistry config file'
)
query_parser.add_argument(
    '-p', '--proc_path', type=str, help='path to input process config file'
)

def main():
    args = parser.parse_args()
    if args.mode == 'chem':
        reaction_agent = ReactionAgent(args.source)
        if args.action == 'infer':
            if args.out_path:
                reaction_agent.infer_and_dump(args.chem_cfg, args.out_path)
            else:
                config = yaml.load(open(args.chem_cfg), yaml.FullLoader)
                reaction_res = reaction_agent.infer(config, args.depth)
                print(json.dumps(reaction_res, indent=2))
        if args.action == 'param':
            if args.out_path:
                reaction_agent.parameterize_and_dump(args.chem_cfg, args.proc_cfg,
                                                     args.out_path)
            else:
                chem_config = yaml.load(open(args.chem_cfg), yaml.FullLoader)
                proc_config = yaml.load(open(args.proc_cfg), yaml.FullLoader)
                chem_config = reaction_agent.parameterize(chem_config, proc_config)
                print(json.dumps(chem_config, indent=2))
        if args.action == 'gen':
            reaction_agent.generate_and_dump(args.chem_cfg, args.out_path)

    if args.mode == 'proc':
        process_agent = ProcessAgent()
        if args.action == 'param':
            if args.out_path:
                process_agent.parameterize_and_dump(args.proc_cfg, args.chem_cfg,
                                                    args.out_path)
            else:
                chem_config = yaml.load(open(args.chem_cfg), yaml.FullLoader)
                proc_config = yaml.load(open(args.proc_cfg), yaml.FullLoader)
                proc_config = process_agent.parameterize(proc_config, chem_config)
                print(json.dumps(proc_config, indent=2))
        if args.action == 'gen':
            process_agent.generate_and_dump(args.proc_cfg, args.out_path)

    if args.mode == 'model':
        model_agent = ModelAgent()
        if args.action == 'sim':
            if args.out_path:
                model_agent.simulate_and_dump(
                    args.chem_path,
                    args.proc_path,
                    args.data_path,
                    args.out_path,
                    fast_reaction=args.fast_reaction,
                    njit=False,
                )
            else:
                chem_config = yaml.load(open(args.chem_path), yaml.FullLoader)
                proc_config = yaml.load(open(args.proc_path), yaml.FullLoader)
                dataset = pd.read_csv(args.data_path)
                sim_dataset = model_agent.simulate(
                    chem_config,
                    proc_config,
                    dataset,
                    fast_reaction=args.fast_reaction,
                    njit=True,
                )
                print(sim_dataset)
        if args.action == 'sim-mc':
            if args.out_path:
                model_agent.simulate_mc_and_dump(
                    args.chem_path,
                    args.proc_path,
                    args.data_path,
                    args.out_path,
                    fast_reaction=args.fast_reaction,
                    njit=False,
                )
            else:
                chem_config = yaml.load(open(args.chem_path), yaml.FullLoader)
                proc_config = yaml.load(open(args.proc_path), yaml.FullLoader)
                dataset = pd.read_csv(args.data_path)
                sim_dataset = model_agent.simulate_mc(
                    chem_config,
                    proc_config,
                    dataset,
                    fast_reaction=args.fast_reaction,
                    njit=False,
                )
                print(sim_dataset)
        if args.action == 'cal':
            if args.out_path:
                model_agent.calibrate_and_dump(
                    args.chem_path,
                    args.proc_path,
                    args.data_path,
                    args.out_path,
                    fast_reaction=args.fast_reaction,
                    njit=True,
                )
            else:
                chem_config = yaml.load(open(args.chem_path), yaml.FullLoader)
                proc_config = yaml.load(open(args.proc_path), yaml.FullLoader)
                dataset = pd.read_csv(args.data_path)
                cal_param_dict, _ = model_agent.calibrate(
                    chem_config,
                    proc_config,
                    dataset,
                    fast_reaction=args.fast_reaction,
                    njit=True,
                )
                print()
                for key, val in cal_param_dict.items():
                    print(key)
                    print(json.dumps(val, indent=2))
                    print()
        if args.action == 'cal-mc':
            if args.out_path:
                model_agent.calibrate_mc_and_dump(
                    args.chem_path,
                    args.proc_path,
                    args.data_path,
                    args.out_path,
                    fast_reaction=args.fast_reaction,
                    njit=True,
                )
            else:
                chem_config = yaml.load(open(args.chem_path), yaml.FullLoader)
                proc_config = yaml.load(open(args.proc_path), yaml.FullLoader)
                dataset = pd.read_csv(args.data_path)
                cal_param_dict, _ = model_agent.calibrate_mc(
                    chem_config,
                    proc_config,
                    dataset,
                    fast_reaction=args.fast_reaction,
                    njit=True,
                )
                print()
                for key, val in cal_param_dict.items():
                    print(key)
                    print(json.dumps(val, indent=2))
                    print()
        if args.action == 'sug':
            if args.out_path:
                pass
            else:
                chem_config = yaml.load(open(args.chem_path), yaml.FullLoader)
                proc_config = yaml.load(open(args.proc_path), yaml.FullLoader)
                dataset = pd.read_csv(args.data_path)
                sug_dataset = model_agent.suggest_with_single_model(
                    chem_config,
                    proc_config,
                    dataset,
                    args.num_experiments,
                    fast_reaction=args.fast_reaction,
                    njit=True,
                )
                print(sug_dataset)
        if args.action == 'sug-mc':
            if args.out_path:
                pass
            else:
                chem_config = yaml.load(open(args.chem_path), yaml.FullLoader)
                proc_config = yaml.load(open(args.proc_path), yaml.FullLoader)
                dataset = pd.read_csv(args.data_path)
                sug_dataset = model_agent.suggest_mc_with_single_model(
                    chem_config,
                    proc_config,
                    dataset,
                    args.num_experiments,
                    fast_reaction=args.fast_reaction,
                    njit=True,
                )
                print(sug_dataset)

    if args.mode == 'query':
        if args.action in ['pubchem', 'all']:
            chem_config = yaml.load(open(args.chem_path), yaml.FullLoader)
            proc_config = yaml.load(open(args.proc_path), yaml.FullLoader)
            pubchem_agent = PubChemAgent()
            info = pubchem_agent.query(chem_config, proc_config)
            print('PubChem')
            print(AsciiTable(info).table)
            print()
        if args.action in ['thermo', 'all']:
            chem_config = yaml.load(open(args.chem_path), yaml.FullLoader)
            proc_config = yaml.load(open(args.proc_path), yaml.FullLoader)
            thermo_agent = ThermoAgent()
            solvent_table, solute_table = thermo_agent.query(chem_config, proc_config)
            print('Thermo')
            print(AsciiTable(solvent_table).table)
            print(AsciiTable(solute_table).table)
            print()
        if args.action in ['solubility', 'all']:
            chem_config = yaml.load(open(args.chem_path), yaml.FullLoader)
            proc_config = yaml.load(open(args.proc_path), yaml.FullLoader)
            mit_solubilibity_agent = MITSolubilityAgent()
            solubility_table = mit_solubilibity_agent.query(chem_config, proc_config)
            print('MIT Solubility Model')
            print(AsciiTable(solubility_table).table)
            print()

if __name__ == '__main__':
    main()
