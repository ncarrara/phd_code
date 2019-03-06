from ncarrara.continuous_dqn.dqn.tnn import transfer_network_factory
from ncarrara.continuous_dqn.dqn.transfer_module import TransferModule
import random
import numpy as np
import logging

from ncarrara.utils.math_utils import epsilon_decay, set_seed
from ncarrara.utils_rl.algorithms.dqn import NetDQN, DQN

logger = logging.getLogger(__name__)


def run_dqn(env, workspace, device, net_params, dqn_params, decay, N, seed, feature_dqn, start_decay,
            transfer_params=None, evaluate_greedy_policy=True, traj_max_size=None):
    size_state = len(feature_dqn(env.reset()))
    if transfer_params is None or transfer_params["selection_method"] == "no_transfer":
        tm = None
    else:
        tm = TransferModule(**transfer_params)
        tm.reset()

    if tm is not None and tm.is_q_transfering():
        net = transfer_network_factory(
            type=transfer_params["transfer_network_type"],
            params={**{"n_in": size_state, "n_out": env.action_space.n}, **net_params})
    else:
        net = NetDQN(n_in=size_state, n_out=env.action_space.n, **net_params)
    dqn = DQN(policy_network=net, device=device, transfer_module=tm, workspace=workspace, **dqn_params)
    dqn.reset()
    set_seed(seed=seed, env=env)
    rrr = []
    rrr_greedy = []
    epsilons = epsilon_decay(start=start_decay, decay=decay, N=N, savepath=workspace)
    nb_samples = 0
    for n in range(N):
        s = env.reset()
        done = False
        rr = 0
        it = 0
        while (not done):

            if random.random() < epsilons[n]:
                if hasattr(env, "action_space_executable"):
                    a = np.random.choice(env.action_space_executable())
                else:
                    a = env.action_space.sample()
            else:
                if hasattr(env, "action_space_executable"):
                    exec = env.action_space_executable()
                    action_mask = np.ones(env.action_space.n)
                    for ex in exec:
                        action_mask[ex] = 0.
                    a = dqn.pi(feature_dqn(s), action_mask)
                else:
                    a = dqn.pi(feature_dqn(s), np.zeros(env.action_space.n))

            s_, r_, done, info = env.step(a)
            rr += r_
            t_dqn = (feature_dqn(s), a, r_, feature_dqn(s_), done, info)
            dqn.update(*t_dqn)
            s = s_
            nb_samples += 1
            it += 1
            if traj_max_size is not None and it >= traj_max_size:
                break

        rrr.append(rr)

        if evaluate_greedy_policy:
            s = env.reset()
            done = False
            rr = 0
            it = 0
            while not done:
                if hasattr(env, "action_space_executable"):
                    exec = env.action_space_executable()
                    action_mask = np.ones(env.action_space.n)
                    for ex in exec:
                        action_mask[ex] = 0.
                    a = dqn.pi(feature_dqn(s), action_mask)
                else:
                    a = dqn.pi(feature_dqn(s), np.zeros(env.action_space.n))

                s_, r_, done, info = env.step(a)
                rr += r_
                s = s_
                it += 1
                if traj_max_size is not None and it >= traj_max_size:
                    break
            rrr_greedy.append(rr)
    return rrr, rrr_greedy, dqn


# if tm is not None and n % 50 == 0 and transfer_params["selection_method"] == "transfer":
#     logger.info("------------------------------------")
#     logger.info("[N_trajs={},N_samples={}] {}"
#                 .format(n, nb_samples, utils.format_errors(tm.errors,
#                                                            transfer_params["sources_params"],
#                                                            transfer_params["test_params"])))
#     logger.info("--------------------------------------")
