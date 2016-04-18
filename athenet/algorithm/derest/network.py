import theano
import numpy

from athenet.layers import ConvolutionalLayer, PoolingLayer,\
    FullyConnectedLayer, Softmax, Dropout, ReLU, LRN, InceptionLayer
from athenet.algorithm.derest.activation import *
from athenet.algorithm.derest.derivative import *
from itertools import product


def _add_tuples(a, b):
    if not isinstance(a, tuple):
        a = (a, )
    if not isinstance(b, tuple):
        b = (b, )
    return a + b


class DerestNetwork():

    def __init__(self, network):
        self.network = network
        self.layers = [DerestLayer(layer) for layer in network.layers]

    def _get_layer_input_shape(self, i):
        if i > 0:
            return self.layers[i - 1].layer.output_shape
        return self.layers[i].layer.input_shape

    def count_activations(self, inp):
        for layer in self.layers:
            inp = layer.count_activation(inp)
        return inp

    def count_derivatives(self, outp, batches):
        #we assume that batches is equal to outp.shape[0] (for now)
        for i in range(len(self.layers) - 1, -1, -1):
            input_shape = _add_tuples(batches, _change_order(self._get_layer_input_shape(i)))
            outp = self.layers[i].count_derivatives(outp, input_shape)
        return outp

    def count_derest(self):
        return [layer.count_derest() for layer in self.layers]


class DerestLayer():

    def __init__(self, layer):
        self.layer = layer
        self.activations = None
        self.derivatives = None

    def count_activation(self, input):
        self.activations = input
        return count_activation(input, self.layer)

    def count_derivatives(self, output, input_shape):
        self.derivatives = output
        return count_derivative(output, self.activations, input_shape, self.layer)

    def count_derest(self):
        if isinstance(self.layer, ConvolutionalLayer):
            return self.count_derest_conv()
        if isinstance(self.layer, FullyConnectedLayer):
            return self.count_derest_fc()
        if isinstance(self.layer, InceptionLayer):
            raise NotImplementedError

    def count_derest_fc(self):
        indicators = numpy.zeros_like(self.layer.W)
        nr_of_batches = self.derivatives.shape.eval()[0]
        for i in range(nr_of_batches):
            act = self.activations.reshape((self.layer.input_shape, 1))
            der = self.derivatives[i].reshape((1, self.layer.output_shape))
            indicators = indicators + numpy.amax((act.dot(der) * self.layer.W).eval(), 0)
        return indicators

    def _get_activation_for_weight(self, i1, i2, i3):
        #no padding or strides yet considered
        n1, n2, _ = self.layer.input_shape
        m1, m2, _ = self.layer.filter_shape
        return self.activations[i1, i2:(n1-m2+i2+1), i3:(n2-m2+i3+1)]

    def count_derest_conv(self):
        indicators = numpy.zeros_like(self.layer.W)

        i0, i1, i2, i3 = self.layer.W.shape
        for batch_nr in range(self.derivatives.shape.eval()[0]): #for every batch
            der = self.derivatives[batch_nr]
            for j1, j2, j3, j4 in product(range(i0), range(i1), range(i2), range(i3)):
                y = self._get_activation_for_weight(j2, j3, j4)
                x = (der[j1] * y * self.layer.W[j1, j2, j3, j4]).eval()
                indicators[j1, j2, j3, j4] = indicators[j1, j2, j3, j4] + numpy.sum(numpy.amax(x, 0))

        return indicators





