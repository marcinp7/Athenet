"""Testing athenet.algorithm.numlike.Numlike class with its methods.
"""

import numpy as np
import unittest
from nose.tools import raises
from athenet.algorithm.numlike import Numlike


class NumlikeTest(unittest.TestCase):

    def test_init(self):
        _ = Numlike()

    @raises(NotImplementedError)
    def test_getitem(self):
        _ = Numlike()[0]

    @raises(NotImplementedError)
    def test_setitem(self):
        Numlike()[0] = 0.0

    @raises(NotImplementedError)
    def test_shape(self):
        _ = Numlike().shape()

    @raises(NotImplementedError)
    def test_add(self):
        _ = Numlike() + Numlike()

    @raises(NotImplementedError)
    def test_sub(self):
        _ = Numlike() - 1.0

    @raises(NotImplementedError)
    def test_mul(self):
        _ = Numlike() * 3.0

    @raises(NotImplementedError)
    def test_div(self):
        _ = Numlike() / 5.0

    @raises(NotImplementedError)
    def test_rdiv(self):
        _ = 5.0 / Numlike()

    @raises(NotImplementedError)
    def test_reciprocal(self):
        _ = Numlike().reciprocal()

    @raises(NotImplementedError)
    def test_neg(self):
        _ = Numlike().neg()

    @raises(NotImplementedError)
    def test_exp(self):
        _ = Numlike().exp()

    @raises(NotImplementedError)
    def test_square(self):
        _ = Numlike().square()

    @raises(NotImplementedError)
    def test_power(self):
        _ = Numlike().power(3.0)

    @raises(NotImplementedError)
    def test_dot(self):
        w = np.array([[1, 2], [3, 4]])
        _ = Numlike().dot(w)

    @raises(NotImplementedError)
    def test_max(self):
        _ = Numlike().max(Numlike())

    @raises(NotImplementedError)
    def test_amax(self):
        _ = Numlike().amax()

    @raises(NotImplementedError)
    def test__hape(self):
        _ = Numlike().reshape((1, 2, 3))

    @raises(NotImplementedError)
    def test_flatten(self):
        _ = Numlike().flatten()

    @raises(NotImplementedError)
    def test_sum(self):
        _ = Numlike().sum(0)

    @raises(NotImplementedError)
    def test_abs(self):
        _ = Numlike().abs()

    @raises(NotImplementedError)
    def test_T(self):
        _ = Numlike().T

    @raises(NotImplementedError)
    def test_from_shape1(self):
        _ = Numlike.from_shape((3, 4))

    @raises(NotImplementedError)
    def test_from_shape2(self):
        _ = Numlike.from_shape((3, 4), neutral=True)

    @raises(NotImplementedError)
    def test_from_shape3(self):
        _ = Numlike.from_shape((3, 4), neutral=False)

    @raises(NotImplementedError)
    def test_eval(self):
        _ = Numlike().eval()

if __name__ == '__main__':
    unittest.main(verbosity=2, catchbreak=True)