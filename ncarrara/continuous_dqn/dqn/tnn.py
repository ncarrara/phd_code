import torch
from torch._jit_internal import weak_script_method
from torch.nn import Module, init

from ncarrara.utils.torch_utils import BaseModule
import numpy as np
import math

import torch
from torch.nn.parameter import Parameter

import torch.nn.functional as F


class ProbalisticLinear(Module):
    __constants__ = ['bias']

    def __init__(self, in_features, out_features, eps):
        super(ProbalisticLinear, self).__init__()
        self.in_features = in_features
        self.eps = eps
        self.out_features = out_features
        self.weight = Parameter(torch.Tensor(out_features, in_features))
        self.reset_parameters()

    def reset_parameters(self):
        init.kaiming_uniform_(self.weight, a=math.sqrt(5))

    @weak_script_method
    def forward(self, input):
        weight = self.weight / self.weight.sum(1, keepdim=True).clamp(min=self.eps)
        return F.linear(input, weight)

    def extra_repr(self):
        return 'in_features={}, out_features={} (eps={})'.format(
            self.in_features, self.out_features, self.eps
        )


class TNN2(BaseModule):
    def __init__(self, n_in, n_out, intra_layers, activation_type="RELU", reset_type="XAVIER", normalize=None):
        super(TNN2, self).__init__(activation_type, reset_type, normalize)
        self.n_out = n_out
        all_layers = [n_in] + intra_layers + [n_out]
        self.layers = []
        for i in range(0, len(all_layers) - 2):
            module = torch.nn.Linear(all_layers[i], all_layers[i + 1])
            self.layers.append(module)
            self.add_module("h_" + str(i), module)
        self.predict = torch.nn.Linear(all_layers[-2], all_layers[-1])

        self.actions_layers = []
        self.actions_weights = []

        for action in range(n_out):
            action_layer = ProbalisticLinear(2, 1, eps=1e-7)
            self.add_module("a_" + str(action), action_layer)
            self.actions_layers.append(action_layer)

    def set_Q_source(self, Q_source):
        self.Q_source = Q_source

    def reset(self):
        self.Q_source = None
        super(TNN2, self).reset()

    def forward(self, s):
        input_Q = s
        if self.normalize:
            input_Q = (input_Q.float() - self.mean.float()) / self.std.float()

        for layer in self.layers:
            input_Q = self.activation(layer(input_Q))
        out_Q = self.predict(input_Q)
        out_Q_transfer = self.Q_source(s)

        actions_values = []
        for action in range(self.n_out):
            q = torch.cat((out_Q_transfer[:, action], out_Q[:, action]), dim=1)
            actions_values.append(self.actions_layers[action](q))
            y = torch.cat(actions_values, dim=1)
        return y.view(y.size(0), -1)


class TNN(BaseModule):
    def __init__(self, n_in, n_out, intra_layers, activation_type="RELU", reset_type="XAVIER", normalize=None):
        super(TNN, self).__init__(activation_type, reset_type, normalize)
        all_layers = [n_in] + intra_layers + [n_out]
        self.layers = []
        for i in range(0, len(all_layers) - 2):
            module = torch.nn.Linear(all_layers[i], all_layers[i + 1])
            self.layers.append(module)
            self.add_module("h_" + str(i), module)
        self.predict = torch.nn.Linear(all_layers[-2], all_layers[-1])

        self.concat_layer = torch.nn.Linear(n_out * 2 + 1, all_layers[-1])

    def set_Q_source(self, Q_source, ae_score):
        self.Q_source = Q_source
        self.ae_score = torch.tensor(ae_score)

    def reset(self):
        self.Q_source = None
        self.ae_score = np.nan
        super(TNN, self).reset()

    def forward(self, s):
        input_Q = s
        if self.normalize:
            input_Q = (input_Q.float() - self.mean.float()) / self.std.float()

        for layer in self.layers:
            input_Q = self.activation(layer(input_Q))
        out_Q = self.predict(input_Q)
        out_Q_transfer = self.Q_source(s)

        in_concat = torch.cat((out_Q, out_Q_transfer, self.ae_score), dim=1)

        y = self.concat_layer(in_concat)

        return y.view(y.size(0), -1)


if __name__ == "__main__":
    xaxa = TNN2(10, 3, [7, 6], activation_type="RELU", reset_type="XAVIER", normalize=None)
    print(xaxa)
