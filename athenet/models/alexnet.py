"""AlexNet model."""

from athenet import Network
from athenet.layers import ConvolutionalLayer, ReLU, LRN, MaxPool, \
    FullyConnectedLayer, Dropout, Softmax
from athenet.utils import load_data, get_bin_path

ALEXNET_FILENAME = 'alexnet_weights.pkl.gz'


def alexnet(trained=True, weights_filename=ALEXNET_FILENAME, weights_url=None):
    if trained:
        weights = load_data(get_bin_path(weights_filename), weights_url)
        if weights is None:
            raise Exception("cannot load AlexNet weights")

    # Normalization parameters
    local_range = 5
    alpha = 0.0001
    beta = 0.75
    k = 1

    net = Network([
        ConvolutionalLayer(image_shape=(227, 227, 3),
                           filter_shape=(11, 11, 96),
                           stride=(4, 4)),
        ReLU(),
        LRN(local_range=local_range,
            alpha=alpha,
            beta=beta,
            k=k),
        MaxPool(poolsize=(3, 3),
                stride=(2, 2)),
        ConvolutionalLayer(filter_shape=(5, 5, 256),
                           padding=(2, 2),
                           n_groups=2),
        ReLU(),
        LRN(local_range=local_range,
            alpha=alpha,
            beta=beta,
            k=k),
        MaxPool(poolsize=(3, 3),
                stride=(2, 2)),
        ConvolutionalLayer(filter_shape=(3, 3, 384),
                           padding=(1, 1)),
        ReLU(),
        ConvolutionalLayer(filter_shape=(3, 3, 384),
                           padding=(1, 1),
                           n_groups=2),
        ReLU(),
        ConvolutionalLayer(filter_shape=(3, 3, 256),
                           padding=(1, 1),
                           n_groups=2),
        ReLU(),
        MaxPool(poolsize=(3, 3),
                stride=(2, 2)),
        FullyConnectedLayer(4096),
        ReLU(),
        Dropout(),
        FullyConnectedLayer(4096),
        ReLU(),
        Dropout(),
        FullyConnectedLayer(1000),
        Softmax()
    ])
    if trained:
        net.set_params(weights)
    return net
