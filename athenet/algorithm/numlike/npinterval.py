"""Intervals implemented in Numpy including special functions for
sparsifying.

This module contains NpInterval class and auxiliary objects.
"""

from athenet.algorithm.numlike import Numlike
from itertools import product
import numpy as np
import math

class NpInterval(Numlike):
    def __init__(self, lower, upper):
        """
        :param numpy.ndarray lower:
        :param numpy.ndarray upper:
        :return:
        """
        self.lower = lower
        self.upper = upper

    def __getitem__(self, at):
        """Returns specified slice of NpInterval.

        :at: Coordinates / slice to be taken.
        :rtype: NpInterval
        """
        return NpInterval(self.lower[at], self.upper[at])

    def __setitem__(self, at, other):
        """Just like numpy __setitem__ function, but as a operator.
        :at: Coordinates / slice to be set.
        :other: Data to be put at 'at'.
        """
        self.lower[at] = other.lower
        self.upper[at] = other.upper

    def __str__(self):
        return "<<<\n" + self.lower.__str__() + "\n;;;\n" + self.upper.__str__() + "\n>>>"

    @property
    def shape(self):
        """Returns shape of numlike.

        :rtype: tuple of integers
        """
        return self.lower.shape

    def __add__(self, other):
        """Returns sum of two NpIntervals.

        :param other: value to be added.
        :type other: NpInterval or numpy.array or float
        :rtype: NpInterval
        """
        if isinstance(other, NpInterval):
            res_lower = self.lower + other.lower
            res_upper = self.upper + other.upper
        else:
            res_lower = self.lower + other
            res_upper = self.upper + other
        return NpInterval(res_lower, res_upper)

    def __sub__(self, other):
        """Returns difference between two numlikes.

        :param other: value to be subtracted.
        :type other: NpInterval or np.ndarray or float
        :rtype: NpInterval
        """
        if isinstance(other, NpInterval):
            res_lower = self.lower - other.upper
            res_upper = self.upper - other.lower
        else:
            res_lower = self.lower - other
            res_upper = self.upper - other
        return NpInterval(res_lower, res_upper)

    def __mul__(self, other):
        """Returns product of two NpIntervals

        :param other: value to be multiplied.
        :type other: NpInterval
        :rtype: Numlike
        """
        if isinstance(other, NpInterval):
            ll = self.lower * other.lower
            lu = self.lower * other.upper
            ul = self.upper * other.lower
            uu = self.upper * other.upper
            lower = np.minimum(np.minimum(ll, lu), np.minimum(ul, uu))
            upper = np.maximum(np.maximum(ll, lu), np.maximum(ul, uu))
        else:
            ll = self.lower * other
            uu = self.upper * other
            lower = np.minimum(ll, uu)
            upper = np.maximum(ll, uu)
        return NpInterval(lower, upper)

    def __div__(self, other):
        """Returns quotient of self and other.

        :param other: divisor
        :type other: Numlike or np.ndarray or theano.tensor
        :rtype: Numlike
        """
        raise NotImplementedError

    def __rdiv__(self, other):
        """Returns quotient of other and self.

        :param other: dividend
        :type other: float
        :rtype: Nplike
        .. warning:: divisor (self) should not contain zero, other must be
                     float
        """
        raise NotImplementedError

    def reciprocal(self):
        """Returns reciprocal (1/x) of the NpInterval.

        :rtype: Numlike
        """
        upper_reciprocal = np.reciprocal(self.upper)
        lower_reciprocal = np.reciprocal(self.lower)
        return NpInterval(np.minimum(upper_reciprocal, lower_reciprocal),
                          np.maximum(upper_reciprocal, lower_reciprocal))

    def neg(self):
        """Returns (-1) * NpInterval

        :rtype: NpInterval
        """
        return NpInterval(np.negative(self.upper), np.negative(self.lower))

    def exp(self):
        """Returns NpInterval representing the exponential of the Numlike.

        :rtype: NpInterval
        """
        raise NpInterval(np.exp(self.lower), np.exp(self.upper))

    def _has_zero(self):
        """For any interval in NpInterval, returns whether is contains zero.

        :rtype: Boolean
        """
        return np.logical_and(self.lower <= 0, self.upper >= 0)

    def square(self):
        """Returns square of the NpInterval

        :rtype: NpInterval
        """
        uu = self.upper * self.upper
        ll = self.lower * self.lower
        lower = np.select([self._has_zero(), True], [0, np.minimum(ll, uu)])
        upper = np.maximum(ll, uu)
        return NpInterval(lower, upper)

    def power(self, exponent):
        """For numlike N, returns N^exponent.

        :param float exponent: Number to be passed as exponent to N^exponent.
        :rtype: Numlike
        """
        raise NotImplementedError

    def dot(self, other):
        """Dot product of numlike vector and a other.

        :param unspecified other: second dot param, type to be specified
        :rtype: Numlike
        """
        raise NotImplementedError

    def max(self, other):
        """Returns maximum of self and other.

        :param unspecified other: second masx param, type to be specified
        :rtype: Numlike
        """
        raise NotImplementedError

    def amax(self, axis=None, keepdims=False):
        """Returns maximum of a Numlike along an axis.

        Works like theano.tensor.max

        :param axis: axis along which max is evaluated
        :param Boolean keepdims: whether flattened dimensions should remain
        :rtype: Numlike
        """
        raise NotImplementedError

    def reshape(self, shape):
        """Reshapes numlike tensor like theano Tensor.

        :param integer tuple shape: shape to be set
        :rtype: Numlike
        """
        raise NotImplementedError

    def flatten(self):
        """Flattens numlike tensor like theano Tensor.

        :rtype: Numlike
        """
        raise NotImplementedError

    def sum(self, axis=None, dtype=None, keepdims=False):
        """Sum of array elements over a given axis like in numpy.ndarray.

        :param axis: axis along which this function sums
        :param numeric type or None dtype: just like dtype argument in
                                   theano.tensor.sum
        :param Boolean keepdims: Whether to keep squashed dimensions of size 1
        :type axis: integer, tuple of integers or None
        :rtype: Numlike

        """
        raise NotImplementedError

    def abs(self):
        """Returns absolute value of NpInterval.

        :rtype: NpInterval
        """
        raise NpInterval(np.abs(self.lower), np.abs(self.upper))

    @property
    def T(self):
        """Tensor transposition like in numpy.ndarray.

        :rtype: NpInterval
        """
        raise NpInterval(self.lower.T, self.upper.T)

    @staticmethod
    def from_shape(shp, neutral=True):
        """Returns Numlike of given shape.

        :param integer tuple shp: shape to be set
        :param Boolean neutral: whether created Numlike should have neutral
                        values or significant values.
        :rtype: Numlike
        """
        raise NotImplementedError

    def reshape_for_padding(self, shape, padding):
        """Returns padded Numlike.

        :param tuple of 4 integers shape: shape of input in format
                                          (batch size, number of channels,
                                           height, width)
        :param pair of integers padding: padding to be applied
        :returns: padded layer_input
        :rtype: Numlike
        """
        raise NotImplementedError

    def eval(self, *args):
        """Returns some readable form of stored value."""
        raise self

    def op_relu(self):
        """Returns result of relu operation on given Numlike.

        :rtype: Numlike
        """
        raise NotImplementedError

    def op_softmax(self, input_shp):
        """Returns result of softmax operation on given Numlike.

        :param integer input_shp: shape of 1D input
        :rtype: Numlike
        """
        raise NotImplementedError

    def op_norm(self, input_shape, local_range, k, alpha, beta):
        """Returns estimated activation of LRN layer.

        :param input_shape: shape of input in format
                            (n_channels, height, width)
        :param integer local_range: size of local range in local range
                                    normalization
        :param integer k: local range normalization k argument
        :param integer alpha: local range normalization alpha argument
        :param integer beta: local range normalization beta argument
        :type input_shape: tuple of 3 integers
        :rtype: Numlike
        """
        raise NotImplementedError

    def op_conv(self, weights, image_shape, filter_shape, biases, stride,
                padding, n_groups):
        """Returns estimated activation of convolution applied to Numlike.

        :param weights: weights tensor in format (number of output channels,
                                                  number of input channels,
                                                  filter height,
                                                  filter width)
        :param image_shape: shape of input in the format
                    (number of input channels, image height, image width)
        :param filter_shape: filter shape in the format
                             (number of output channels, filter height,
                              filter width)
        :param biases: biases in convolution
        :param stride: pair representing interval at which to apply the filters
        :param padding: pair representing number of zero-valued pixels to add
                        on each side of the input.
        :param n_groups: number of groups input and output channels will be
                         split into, two channels are connected only if they
                         belong to the same group.
        :type image_shape: tuple of 3 integers
        :type weights: 3D numpy.ndarray or theano.tensor
        :type filter_shape: tuple of 3 integers
        :type biases: 1D numpy.ndarray or theano.vector
        :type stride: pair of integers
        :type padding: pair of integers
        :type n_groups: integer
        :rtype: Numlike
        """
        raise NotImplementedError

    def op_d_relu(self, activation):
        """Returns estimated impact of input of relu layer on output of
        network.

        :param Numlike activation: estimated activation of input
        :param Numlike self: estimated impact of output of layer on output
                               of network in shape (batch_size, number of
                               channels, height, width)
        :returns: Estimated impact of input on output of network
        :rtype: Numlike
        """
        raise NotImplementedError

    def op_d_max_pool(self, activation, input_shape, poolsize, stride,
                      padding):
        """Returns estimated impact of max pool layer on output of network.

        :param Numlike self: estimated impact of output of layer on output
                               of network in shape (batch_size, number of
                               channels, height, width)
        :param Numlike activation: estimated activation of input
        :param input_shape: shape of layer input in format (batch size,
                            number of channels, height, width)
        :type input_shape: tuple of 4 integers
        :param pair of integers poolsize: pool size in format (height, width),
                                          not equal (1, 1)
        :param pair of integers stride: stride of max pool
        :param pair of integers padding: padding of max pool
        :returns: Estimated impact of input on output of network
        :rtype: Numlike
        """
        raise NotImplementedError

    def op_d_avg_pool(self, activation, input_shape, poolsize, stride,
                      padding):
        """Returns estimated impact of avg pool layer on output of network.

        :param Numlike self: estimated impact of output of layer on output
                               of network in shape (batch_size, number of
                               channels, height, width)
        :param Numlike activation: estimated activation of input
        :param input_shape: shape of layer input in format (batch size,
                            number of channels, height, width)
        :type input_shape: tuple of 4 integers
        :param pair of integers poolsize: pool size in format (height, width),
                                          not equal (1, 1)
        :param pair of integers stride: stride of avg pool
        :param pair of integers padding: padding of avg pool
        :returns: Estimated impact of input on output of network
        :rtype: Numlike
        """
        raise NotImplementedError

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> HERE YOU WORK

    def op_d_norm(self, activation, input_shape, local_range, k, alpha,
                  beta):
        """Returns estimated impact of input of norm layer on output of
        network.

        :param NpInterval self: estimated impact of output of layer on output
                               of network in shape (batch_size, number of
                               channels, height, width)
        :param NpInterval activation: estimated activation of input
        :param input_shape: shape of layer input in format (batch size,
                            number of channels, height, width)
        :type input_shape: tuple of 4 integers
        :param integer local_range: size of local range in local range
                                    normalization
        :param float k: local range normalization k argument
        :param float alpha: local range normalization alpha argument
        :param float beta: local range normalization beta argument
        :rtype: NpInterval
        """
        result = NpInterval(np.zeros_like(activation.lower),
                            np.zeros_like(activation.upper))
        activation_sqares = activation.square()

        # some piece of math, unnecessary in any other place:
        # derivative for x placed in denominator of norm function
        def der_eq(x, c):
            """
            Return derivative of norm function for value in denominator
            :param x: value in denominator
            :param c: k + sum of squares of other values

            In this representation norm function equals to
            x / (c + alpha * (x ** 2)) ** beta

            :return: value of derivative of norm function
            """
            return (alpha * (1-2*beta) * x**2 + c) / \
                   (alpha * x**2 + c) ** (beta + 1)

        # possible extremas
        def root1_2d(c_low, c_up, x_low, x_up):
            # returns roots of derivative of derivetive of norm function
            # x = 0
            # intersects solution rectangle with x = 0
            if x_low <= 0 and x_up >= 0:
                return [(0, c_low), (0, c_up)]
            return []

        def root2_2d(c_low, c_up, x_low, x_up):
            # returns roots of derivative of derivetive of norm function
            # x = - sqrt(c) / sqrt (alpha * (2*beta+1))
            # intersects solution rectangle with half-parabola above
            possibilities_c = [(-math.sqrt(c) / math.sqrt(alpha*(2*beta+1)), c)
                             for c in [c_low, c_up]]
            possibilities_x = [(x, alpha*(2*beta+1) * x**2)
                               for x in [x_low, x_up]]

            return [(x,c) for x,c in possibilities_x + possibilities_c
                    if x_low <= x and x <= x_up and c_low <= c and c <= c_up]

        # derivative for x not from denominator
        def der_not_eq(x, y, c):
            """
            Returns value of derivative of norm function for element not
            placed in derivative
            :param x: element to compute derivative after
            :param y: element placed in denominator
            :param c: k + alpha * sum of squares of other elements

            In this representation norm function equals to
            y / (c + aplha * x**2 + alpha * y**2) ** beta

            :return: Returns value of derivative of norm function
            """
            return 2 * alpha*beta * x*y / \
                   (c + alpha*(x**2 + y**2)) ** (beta+1)

        # possible extremas of this derivative
        def extremas_3d(x_low, x_up, y_low, y_up, c_low, c_up):
            # as far as wolfram knows, possible extremas are for x=0 and y=0
            return [(x,y,c) for x,y,c in
                    product([x_low, x_up, 0], [y_low, y_up, 0], [c_low, c_up])
                    if x_low <= x <= x_up and y_low <= y <= y_up]


        batches, channels, h, w = input_shape
        for b, channel, at_h, at_w in product(xrange(batches), xrange(channels),
                                              xrange(h), xrange(w)):
            C = NpInterval(np.asarray([k]), np.asarray([k]))
            for i in xrange(-local_range, local_range):
                if 0 <= i + channel < channels and i != 0:
                    C += activation_sqares[b][channel + i][at_h][at_w]

            Y = activation[b][channel][at_h][at_w]

            # eq case
            extremas = [(x, c) for x, c in product([Y.lower, Y.upper],
                                                   [C.lower, C.upper])]
            extremas.extend(root1_2d(C.lower, C.upper, Y.lower, Y.upper))
            extremas.extend(root2_2d(C.lower, C.upper, Y.lower, Y.upper))
            der = NpInterval()
            for x, c in extremas:
                val = der_eq(x, c)
                if der.lower is None or der.lower > val:
                    der.lower = val
                if der.upper is None or der.upper < val:
                    der.upper = val
            result[b][channel][at_h][at_w] += self[b][channel][at_h][at_w]*der

            #not_eq_case
            for i in xrange(-local_range, local_range):
                if i != 0 and 0 <= i + channel < channels:
                    X = activation_sqares[b][channel + i][at_h][at_w]
                    C = NpInterval(np.asarray([k]), np.asarray([k]))
                    for j in xrange(-local_range, local_range):
                        if j != 0 and j != i and 0 <= j + channel < channels:
                            C += activation_sqares[b][channel + j][at_h][at_w]
                    extremas = extremas_3d(X.lower, X.upper, Y.lower, Y.upper,
                                           C.lower, C.upper)
                    der = NpInterval()
                    for x, y, c in extremas:
                        val = der_not_eq(x, y, c)
                        if der.lower is None or der.lower > val:
                            der.lower = val
                        if der.upper is None or der.upper < val:
                            der.upper = val
                    result[b][channel + i][at_h][at_w] += \
                        der * self[b][channel][at_h][at_w]

        return result

    def op_d_conv(self, input_shape, filter_shape, weights,
                  stride, padding, n_groups):
        """Returns estimated impact of input of convolutional layer on output
        of network.

        :param Numlike self: estimated impact of output of layer on output
                             of network in shape (batch_size,
                             number of channels, height, width)
        :param input_shape: shape of layer input in the format
                            (number of batches,
                             number of input channels,
                             image height,
                             image width)
        :type input_shape: tuple of 4 integers
        :param filter_shape: filter shape in the format
                             (number of output channels, filter height,
                              filter width)
        :type filter_shape: tuple of 3 integers
        :param weights: Weights tensor in format (number of output channels,
                                                  number of input channels,
                                                  filter height,
                                                  filter width)
        :type weights: numpy.ndarray or theano tensor
        :param stride: pair representing interval at which to apply the filters
        :type stride: pair of integers
        :param padding: pair representing number of zero-valued pixels to add
                        on each side of the input.
        :type padding: pair of integers
        :param n_groups: number of groups input and output channels will be
                         split into, two channels are connected only if they
                         belong to the same group.
        :type n_groups: integer
        :returns: Estimated impact of input on output of network
        :rtype: Numlike
        """
        raise NotImplementedError

    @staticmethod
    def derest_output(n_outputs):
        """Generates Numlike of impact of output on output.

        :param int n_outputs: Number of outputs of network.
        :returns: 2D square Numlike in shape (n_batches, n_outputs) with one
                  different "1" in every batch.
        :rtype: Numlike
        """
        raise NotImplementedError
