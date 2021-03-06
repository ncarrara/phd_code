import logging
import json

from ncarrara.continuous_dqn.dqn.utils_dqn import run_dqn
from ncarrara.continuous_dqn.tools.features import build_feature_dqn
from ncarrara.utils_rl.environments.envs_factory import generate_envs
from ncarrara.utils.math_utils import set_seed

logger = logging.getLogger(__name__)


def main(source_envs, feature_dqn_info, net_params, dqn_params,
         N, seed, device, workspace, decay, start_decay, traj_max_size, gamma, writer=None):
    envs, params = generate_envs(**source_envs)

    for ienv, env in enumerate(envs):
        logger.info("generating samples for env {}".format(ienv))
        set_seed(seed=seed, env=env)
        feature_dqn = build_feature_dqn(feature_dqn_info)
        _, _, memory, dqn = run_dqn(
            env,
            id="generate_sources_env_{}".format(ienv),
            workspace=workspace / "dqn_workspace",
            seed=seed,
            feature_dqn=feature_dqn,
            device=device,
            net_params=net_params,
            dqn_params=dqn_params,
            N=N,
            decay=decay,
            start_decay=start_decay,
            traj_max_size=traj_max_size,
            gamma=gamma,
            writer=writer)

        memory.save(workspace / "samples" / "{}.json".format(ienv), as_json=False)
        dqn.save(workspace / "dqn" / "{}.pt".format(ienv))
    with open(workspace / 'params.json', 'w') as file:
        dump = json.dumps(params, indent=4)
        print(dump)
        file.write(dump)
    return env.action_space.n

# if __name__ == "__main__":
#     from ncarrara.continuous_dqn.tools.configuration import C
#
#     C.load("config/0_pydial.json").load_pytorch()
#     main()
