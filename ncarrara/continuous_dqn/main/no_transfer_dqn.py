import numpy as np
import logging

from ncarrara.continuous_dqn.dqn.utils_dqn import run_dqn_without_transfer
from ncarrara.continuous_dqn.tools.configuration import C
from ncarrara.continuous_dqn.tools.features import build_feature_dqn

logger = logging.getLogger(__name__)
import gym

import matplotlib.pyplot as plt


def main():
    env = gym.make(C["no_transfer_dqn"]['env_str'])
    N = C["no_transfer_dqn"]['N']
    feature_dqn = build_feature_dqn(C["feature_dqn_info"])

    rewards = run_dqn_without_transfer(i_env=0,
                                       env=env,
                                       seed=C.seed,
                                       env_params=C["no_transfer_dqn"]['env_str'],
                                       feature_dqn=feature_dqn,
                                       **C["no_transfer_dqn"])
    n_dots = 10
    xaxax = int(len(rewards) / int(N / n_dots))
    xxx = np.mean(np.reshape(np.array(rewards), (10, -1)), axis=1)
    print(xxx)
    plt.plot(range(len(xxx)), xxx)
    plt.title("DQN, no transfer")
    plt.show()
    plt.close()


if __name__ == "__main__":
    C.load("config/0_pydial.json")
    main()