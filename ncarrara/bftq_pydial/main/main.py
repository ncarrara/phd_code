# from ncarrara.bftq_pydial.main.plot_data import main
import torch
from sklearn.model_selection import ParameterGrid

from ncarrara.bftq_pydial.tools.configuration import C
import sys
import numpy as np
import logging

if len(sys.argv) > 1:
    config_file = sys.argv[1]
    seed_start = int(sys.argv[2])
    number_seeds = int(sys.argv[3])
    seeds = range(seed_start, seed_start + number_seeds)
    C.load_matplotlib('agg')
else:
    config_file = "config/final2.json"
    seeds = [0]

C.load_matplotlib('agg')

# logging.getLogger("ncarrara.bftq_pydial.main.create_data").setLevel(logging.INFO)
# logging.getLogger("ncarrara.utils_rl.environments.slot_filling_env.slot_filling_env").setLevel(logging.INFO)

print("seeds = {}".format(seeds))

from ncarrara.bftq_pydial.main import run_ftq, create_data, run_hdc, learn_bftq, test_bftq, plot_data

with open(config_file, 'r') as infile:
    import json

    dict = json.load(infile)
    workspace = dict["general"]["workspace"]
# param_grid = {
#     'general.seed': seeds,
#     'net_params.intra_layers': [[128, 256], [32, 64], [512, 256, 128, 64, 32], [32, 128, 256, 512], [64, 128]],
#     'ftq_params.weight_decay': [0.0, 0.01, 0.001,0.0001],
#     'ftq_params.optimizer': ["RMS_PROP", "ADAM"],
#     'ftq_params.learning_rate': [0.01, 0.001]
# }

param_grid = {
    'net_params.intra_layers': [[64,32]],
    'ftq_params.weight_decay': [0.001],
    'ftq_params.optimizer': ["ADAM"],
    'ftq_params.learning_rate': [0.01],
    'ftq_params.max_nn_epoch':[10000],
    'ftq_params.reset_policy_each_ftq_epoch':[True,False],
    'general.seed': seeds,

}


grid = ParameterGrid(param_grid)
print(grid)
str_params = ""
for i_config,params in enumerate(grid):
    str_params += "id=" + str(i_config) + ' ' + ''.join([k + "=" + str(v) + ' ' for k, v in params.items()]) + '\n'
print(str_params)

with open(workspace + "/params", 'a') as infile:
    infile.write(str_params)

for i_config,params in enumerate(grid):
    # print(params)
    for k, v in params.items():
        keys = k.split('.')

        tochange = dict
        for ik in range(len(keys) - 1):
            tochange = tochange[keys[ik]]
        tochange[keys[-1]] = v

    print("------------------------------------------------------")
    print("------------------------------------------------------")

    print("------------------------------------------------------")
    print("------------------------------------------------------")
    dict["general"]["workspace"] = workspace + "/test5/" + str(i_config)
    C.load(dict).create_fresh_workspace(force=True)
    create_data.main()
    torch.cuda.empty_cache()
    # run_hdc.main(safenesses=np.linspace(0, 1, 10))
    # betas_test = eval(C["betas_test"])
    # learn_bftq.main()
    # torch.cuda.empty_cache()
    # test_bftq.main(betas_test=betas_test)
    # torch.cuda.empty_cache()
    lambdas = eval(C["lambdas"])
    run_ftq.main(lambdas_=lambdas)
    torch.cuda.empty_cache()
    # plot_data.main([["final/seed=0/ftq/results"]])


