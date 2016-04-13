"""Template class with arithmetic operations that can be passed through neural
network.

All classes that are being used for derest should inherit from this class."""


class Numlike(object):
    """Template class with arithmetic operations that can be passed through
    neural network.

    All classes that are being used for derest should inherit from this
    class."""

    def __init__(self):
        """Create numlike."""
        pass

    def __getitem__(self, at):
        """Returns specified slice of numlike.

        :at: Coordinates / slice to be taken.
        :rtype: Numlike
        """
        raise NotImplementedError

    def __setitem__(self, at, other):
        """Just like Theano set_subtensor function, but as a operator.

        :at: Coordinates / slice to be set.
        :other: Data to be put at 'at'.
        """
        raise NotImplementedError

    @property
    def shape(self):
        """Returns shape of numlike.

        :rtype: integer or tuple of integers or theano shape
        """
        raise NotImplementedError

    def __add__(self, other):
        """Returns sum of two numlikes.

        :param other: value to be added.
        :type other: Numlike or np.ndarray or theano.tensor
        :rtype: Numlike
        """
        raise NotImplementedError

    def __sub__(self, other):
        """Returns difference between two numlikes.

        :param other: value to be subtracted.
        :type other: Numlike or np.ndarray or theano.tensor
        :rtype: Numlike
        """
        raise NotImplementedError

    def __mul__(self, other):
        """Returns product of two numlikes.

        :param other: value to be multiplied.
        :type other: Numlike or np.ndarray or theano.tensor
        :rtype: Numlike
        """
        raise NotImplementedError

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
        """Returns reciprocal of the Numlike.

        :rtype: Numlike
        """
        raise NotImplementedError

    def neg(self):
        """Returns (-1) * Numlike.

        :rtype: Numlike
        """
        raise NotImplementedError

    def exp(self):
        """Returns Numlike representing the exponential of the Numlike.

        :rtype: Numlike
        """
        raise NotImplementedError

    def square(self):
        """Returns square of the Numlike.

        :rtype: Numlike
        """
        raise NotImplementedError

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
        """Returns absolute value of Numlike.

        :rtype: Numlike
        """
        raise NotImplementedError

    @property
    def T(self):
        """Tensor transposition like in numpy.ndarray.

        :rtype: Numlike
        """
        raise NotImplementedError

    @staticmethod
    def from_shape(shp, neutral=True):
        """Returns Numlike of given shape.

        :param integer tuple shp: shape to be set
        :param Boolean neutral: whether created Numlike should have neutral
                        values or significant values.
        :rtype: Numlike
        """
        raise NotImplementedError

    def eval(self, *args):
        """Returns some readable form of stored value."""
        raise NotImplementedError