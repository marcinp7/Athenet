"""
    sender - SimplE Neuron DEleteR

    Place for some description
"""

import numpy as np

from athenet.layers import FullyConnectedLayer
from athenet.algorithm.utils import list_of_percentage_rows, delete_row


def simple_neuron_deleter(network, config):
    """ (this docstring should be writen better)
        :config: - tuple of 2 foats, p, and layer_limit
        :p, layer_limit: - floats between 0 and 1. Deletes [p] neurons from
            layers connected direclty to fully connected layer's, but at most
            [layer_limit] neurons from single layer.
            If layer_limit < p then at most [layer_limit] neurons will be
            deleted.
    """
    p, layer_limit = config
    assert p >= 0. and p <= 1.
    assert layer_limit >= 0. and layer_limit <= 1.

    all_rows = []
    neurons_for_layer = np.zeros((len(network.weighted_layers),))
    neurons_in_general = 0
    deleted_for_layer = np.zeros((len(network.weighted_layers),))
    deleted_in_general = 0

    for i in xrange(len(network.weighted_layers)):
        layer = network.weighted_layers[i]
        if isinstance(layer, FullyConnectedLayer):
            all_rows += list_of_percentage_rows(i, layer)
            neurons_for_layer[i] = layer.W.shape[1]
            neurons_in_general += neurons_for_layer[i]

    all_rows = sorted(all_rows)

    for val, row, layer_id in all_rows:
        if deleted_in_general >= p * neurons_in_general:
            break
        if 1 + deleted_for_layer[layer_id] > layer_limit * neurons_for_layer[i]:
            continue
        deleted_for_layer[layer_id] += 1
        delete_row(network.weighted_layers[layer_id], row)
        deleted_in_general += 1
