import argparse
import json
import os
import sys

import pandas as pd
import yaml
from terminaltables import AsciiTable

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kidoe.agent.knowledge_graph_agent import OntoBaseModel
from kidoe.agent.mit_solubility_agent import MITSolubilityAgent
from kidoe.agent.model_agent import ModelAgent
from kidoe.agent.process_agent import ProcessAgent
from kidoe.agent.pubchem_agent import PubChemAgent
from kidoe.agent.reaction_agent import ReactionAgent


def _jsonable(obj):
    """Replace OntoMo entities, also as dict keys, by their names."""
    if isinstance(obj, OntoBaseModel):
        return obj.name
    if isinstance(obj, dict):
        return {_jsonable(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    return obj

parser = argparse.ArgumentParser(
    prog='kidoe', description='KIDoE: knowledge-informed design of experiments'
)
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0')
parser.add_argument(
    'work_dir', type=str, help='path to working directory for config files'
)
subparsers = parser.add_subparsers(
    dest='mode', help='kidoe includes `query`, `chem`, `proc`, and `model` modes'
)

query_parser = subparsers.add_parser(
    'query', help='query information from AI models and databases')
query_parser.add_argument('action',
                          choices=['all', 'pubchem', 'solubility'],
                          help='actions under %(prog)s')

chem_parser = subparsers.add_parser(
    'chem',
    help='mode to infer reaction networks, parameterize kinetics, and generate '
    'candidate chemistry configs',
)
chem_parser.add_argument(
    'action', choices=['infer', 'param', 'gen'], help='actions under %(prog)s'
)
chem_parser.add_argument(
    '-s',
    '--source',
    choices=['uspto', 'march', 'stephen'],
    default='uspto',
    help='template source, (default: %(default)s)',
)
chem_parser.add_argument(
    '-d', '--depth', type=int, default=1, help='chemistry reaction inference depth'
)
chem_parser.add_argument(
    '-o', '--output', action='store_true', help='output config file or not'
)
chem_parser.add_argument(
    '-m',
    '--mechanistic',
    action='store_true',
    help='save mechanistic steps instead of stoichiometric reactions (with -o)',
)

proc_parser = subparsers.add_parser(
    'proc', help='mode to parameterize process and generate candidate process configs'
)
proc_parser.add_argument(
    'action', choices=['param', 'gen'], help='actions under %(prog)s'
)
proc_parser.add_argument(
    '-o', '--output', action='store_true', help='output config file or not'
)

model_parser = subparsers.add_parser(
    'model', help='mode to simulate, calibrate, and suggest experiments'
)
model_parser.add_argument(
    'action', choices=['sim', 'cal', 'sug'], help='actions under %(prog)s'
)
model_parser.add_argument(
    '-r', '--run_index', type=int, help='index of candidate chemistry config'
)
model_parser.add_argument(
    '-c', '--chem_index', type=int, help='index of candidate chemistry config'
)
model_parser.add_argument(
    '-p', '--proc_index', type=int, help='index of candidate process config'
)
model_parser.add_argument(
    '-d', '--data_file', type=str, default='data.csv', help='data file name'
)
model_parser.add_argument(
    '-o', '--output', action='store_true', help='output data or not'
)

# model_parser.add_argument(
#     '-d', '--data', type=str, help='path to experimental dataset'
# )
model_parser.add_argument(
    '-n',
    '--num_experiments',
    type=int,
    default=None,
    help='number of suggested experiments (default: all candidate points)',
)
# model_parser.add_argument(
#     '-o', '--output', type=str, help='path to output config file or dir'
# )


def main():
    args = parser.parse_args()
    if args.mode == 'query':
        if args.action in ['pubchem', 'all']:
            with open(os.path.join(args.work_dir, 'chem_infer.yaml')) as f:
                chem_config = yaml.load(f, yaml.FullLoader)
            with open(os.path.join(args.work_dir, 'proc_base.yaml')) as f:
                proc_config = yaml.load(f, yaml.FullLoader)
            pubchem_agent = PubChemAgent()
            info = pubchem_agent.query(chem_config, proc_config)
            print('PubChem')
            print(AsciiTable(info).table)
            print()
        if args.action in ['solubility', 'all']:
            with open(os.path.join(args.work_dir, 'chem_infer.yaml')) as f:
                chem_config = yaml.load(f, yaml.FullLoader)
            with open(os.path.join(args.work_dir, 'proc_base.yaml')) as f:
                proc_config = yaml.load(f, yaml.FullLoader)
            mit_solubilibity_agent = MITSolubilityAgent()
            solubility = mit_solubilibity_agent.query(chem_config, proc_config)
            print('MIT Solubility Model')
            print(AsciiTable(solubility).table)
            print()

    if args.mode == 'chem':
        reaction_agent = ReactionAgent(args.source)
        if args.action == 'infer':
            if args.output:
                reaction_agent.infer_and_dump(
                    os.path.join(args.work_dir, 'chem_base.yaml'),
                    os.path.join(args.work_dir, 'chem_infer.yaml'),
                    args.depth,
                    args.mechanistic
                )
            else:
                with open(os.path.join(args.work_dir, 'chem_base.yaml')) as f:
                    config = yaml.load(f, yaml.FullLoader)
                    reaction_res = reaction_agent.infer(config, args.depth)
                print(json.dumps(_jsonable(reaction_res), indent=2))
        if args.action == 'param':
            if args.output:
                reaction_agent.parameterize_and_dump(
                    os.path.join(args.work_dir, 'chem_infer.yaml'),
                    os.path.join(args.work_dir, 'proc_base.yaml'),
                    os.path.join(args.work_dir, 'chem_param.yaml'),
                )
            else:
                with open(os.path.join(args.work_dir, 'chem_infer.yaml')) as f:
                    chem_config = yaml.load(f, yaml.FullLoader)
                with open(os.path.join(args.work_dir, 'proc_base.yaml')) as f:
                    proc_config = yaml.load(f, yaml.FullLoader)
                chem_config = reaction_agent.parameterize(chem_config, proc_config)
                print(json.dumps(_jsonable(chem_config), indent=2))
        if args.action == 'gen':
            reaction_agent.generate_and_dump(
                os.path.join(args.work_dir, 'chem_param.yaml'),
                os.path.join(args.work_dir, 'chem'),
            )

    if args.mode == 'proc':
        process_agent = ProcessAgent()
        if args.action == 'param':
            if args.output:
                process_agent.parameterize_and_dump(
                    os.path.join(args.work_dir, 'proc_base.yaml'),
                    os.path.join(args.work_dir, 'chem_infer.yaml'),
                    os.path.join(args.work_dir, 'proc_param.yaml'),
                )
            else:
                with open(os.path.join(args.work_dir, 'chem_infer.yaml')) as f:
                    chem_config = yaml.load(f, yaml.FullLoader)
                with open(os.path.join(args.work_dir, 'proc_base.yaml')) as f:
                    proc_config = yaml.load(f, yaml.FullLoader)
                proc_config = process_agent.parameterize(proc_config, chem_config)
                print(json.dumps(_jsonable(proc_config), indent=2))
        if args.action == 'gen':
            process_agent.generate_and_dump(
                os.path.join(args.work_dir, 'proc_param.yaml'),
                os.path.join(args.work_dir, 'proc'),
            )

    if args.mode == 'model':
        model_agent = ModelAgent(njit=True)
        
        if args.action == 'sim':
            chem_path = os.path.join(
                args.work_dir,
                f'run/{args.run_index}/model',
                f'{args.chem_index}_{args.proc_index}',
                f'chem_{args.chem_index}.yaml',
            )
            proc_path = os.path.join(
                args.work_dir,
                f'run/{args.run_index}/model',
                f'{args.chem_index}_{args.proc_index}',
                f'proc_{args.proc_index}.yaml',
            )
            data_path = os.path.join(
                args.work_dir,
                f'run/{args.run_index}/data/{args.data_file}',
            )
            if args.output:
                out_path = os.path.join(
                    args.work_dir,
                    f'run/{args.run_index}/model',
                    f'{args.chem_index}_{args.proc_index}',
                    'data_sim.csv',
                )
                model_agent.simulate_and_dump(chem_path, proc_path, data_path, out_path)
            else:
                with open(chem_path) as f:
                    chem_config = yaml.load(f, yaml.FullLoader)
                with open(proc_path) as f:
                    proc_config = yaml.load(f, yaml.FullLoader)
                dataset = pd.read_csv(data_path)
                sim_dataset = model_agent.simulate(chem_config, proc_config, dataset)
                print(sim_dataset)
        
        if args.action == 'cal':
            if args.output:
                chem_path = f'chem/chem_{args.chem_index}.yaml'
                chem_path = os.path.join(args.work_dir, chem_path)
                proc_path = f'proc/proc_{args.proc_index}.yaml'
                proc_path = os.path.join(args.work_dir, proc_path)
                data_path = f'run/{args.run_index}/data/data.csv'
                data_path = os.path.join(args.work_dir, data_path)
                out_path = f'run/{args.run_index}/model/{args.chem_index}_{args.proc_index}'
                out_path = os.path.join(args.work_dir, out_path)
                model_agent.calibrate_and_dump(chem_path, proc_path, data_path, out_path)
            else:
                chem_path = f'chem/chem_{args.chem_index}.yaml'
                with open(os.path.join(args.work_dir, chem_path)) as f:
                    chem_config = yaml.load(f, yaml.FullLoader)
                proc_path = f'proc/proc_{args.proc_index}.yaml'
                with open(os.path.join(args.work_dir, proc_path)) as f:
                    proc_config = yaml.load(f, yaml.FullLoader)
                data_path = f'run/{args.run_index}/data/data.csv'
                dataset = pd.read_csv(os.path.join(args.work_dir, data_path))
                cal_param_dict, _ = model_agent.calibrate(
                    chem_config, proc_config, dataset
                )
                print()
                for key, val in cal_param_dict.items():
                    print(key)
                    print(json.dumps(_jsonable(val), indent=2))
                    print()
        
        if args.action == 'sug':
            data_path = os.path.join(
                args.work_dir,
                f'run/{args.run_index}/data/data.csv',
            )
            with open(os.path.join(args.work_dir, 'proc_param.yaml')) as f:
                proc_config = yaml.load(f, yaml.FullLoader)
            model_path = os.path.join(args.work_dir, f'run/{args.run_index}/model')
            dataset = pd.read_csv(data_path)
            sug_dataset = model_agent.suggest(
                model_path, proc_config, dataset, args.num_experiments
            )
            print(sug_dataset)
        # if args.action == 'sug-mc':
        #     if args.out_path:
        #         pass
        #     else:
        #         chem_path = f'chem/chem_{args.chem_index}.yaml'
        #         with open(os.path.join(args.work_dir, chem_path)) as f:
        #             chem_config = yaml.load(f, yaml.FullLoader)
        #         proc_path = f'proc/proc_{args.proc_index}.yaml'
        #         with open(os.path.join(args.work_dir, proc_path)) as f:
        #             proc_config = yaml.load(f, yaml.FullLoader)
        #         data_path = f'run/{args.run_index}/data/data.csv'
        #         dataset = pd.read_csv(os.path.join(args.work_dir, data_path))
        #         sug_dataset = model_agent.suggest_mc_with_single_model(
        #             chem_config,
        #             proc_config,
        #             dataset,
        #             args.num_experiments,
        #             njit=True,
        #         )
        #         print(sug_dataset)


if __name__ == '__main__':
    main()
