from athenet.algorithm.numlike import NpInterval
from unittest import TestCase, main
from random import randrange, random, randint, uniform
from itertools import product
import numpy as np


class TestNpInterval(TestCase):
    def _random_shape(self, size_limit=10**4, dimensions_limit=7):
        result = None
        size = 1
        for i in xrange(randrange(1, dimensions_limit)):
            l = randrange(1, 10)
            if result is None:
                result = (l,)
            else:
                result += (l,)
            size *= l
            if size >= size_limit:
                return result
        return result

    def _check_lower_upper(self, a):
        self.assertTrue((a.lower <= a.upper).all())

    def _random_npinterval(self, shape=None, size_limit=10**2, number_limit=10**2):
        if shape is None:
            shape = self._random_shape(size_limit, 4)
        a = np.random.rand(*shape) * uniform(-number_limit, number_limit)
        b = np.random.rand(*shape) * uniform(-number_limit, number_limit)
        return NpInterval(np.minimum(a, b), np.maximum(a, b))

    def _random_ndarray(self, shape=None):
        if shape is None:
            shape = self._random_shape(10**2, 4)
        return np.random.rand(*shape)

    def _assert_npintervals_equal(self, a, b):
        self.assertTrue((a.lower == b.lower).all())
        self.assertTrue((a.upper == b.upper).all())


class TestShape(TestNpInterval):
    def _run_test(self, shape):
        i = NpInterval(np.zeros(shape), np.ones(shape))
        self.assertEquals(shape, i.shape)

    def test_shape(self):
        for i in xrange(100):
            self._run_test(self._random_shape())


class TestMultiplying(TestNpInterval):
    def test_case(self):
        al = np.asarray([[1, -2, -1], [-42, -5, -1]])
        au = np.asarray([[2, -1,  1], [4, -4, 7]])
        A = NpInterval(al, au)

        bl = np.asarray([[1, 1, 4], [-1, -2, -13]])
        bu = np.asarray([[2, 2, 5], [-1, -1,   1]])
        B = NpInterval(bl, bu)

        rl = np.asarray([[1, -4, -5], [-4,  4, -91]])
        ru = np.asarray([[4, -1,  5], [42, 10,  13]])

        R = A * B
        self.assertTrue((rl == R.lower).all())
        self.assertTrue((ru == R.upper).all())

        R = B
        R *= A
        self.assertTrue((rl == R.lower).all())
        self.assertTrue((ru == R.upper).all())

    def _check_result(self, A, B, R):
        al, au = A.lower[0], A.upper[0]
        bl, bu = B.lower[0], B.upper[0]
        rl, ru = R.lower[0], R.upper[0]
        for a, b in product(xrange(al, au), xrange(bl, bu)):
            self.assertTrue(rl <= a * b <= ru)

    def test_correct(self):
        for i in xrange(100):
            l = [randrange(-10, 10) for j in xrange(4)]
            A = NpInterval(np.asarray([l[0]]), np.asarray([l[1]]))
            B = NpInterval(np.asarray([l[2]]), np.asarray([l[3]]))

            if A.lower[0] > A.upper[0]:
                A.lower, A.upper = A.upper, A.lower
            if B.lower[0] > B.upper[0]:
                B.lower, B.upper = B.upper, B.lower

            self._check_result(A, B, B * A)

    def test_shape(self):
        for i in xrange(100):
            shape = self._random_shape()
            A = NpInterval(np.ones(shape), 2 * np.ones(shape))
            B = NpInterval(np.ones(shape) * 2, np.ones(shape) * 3)
            R = A * B
            self.assertEqual(R.shape, shape)

    def test_random_with_float(self):
        a = self._random_npinterval()
        b = uniform(1., 100.)
        result = a * b
        self.assertTrue((a.lower * b == result.lower).all())
        self.assertTrue((a.upper * b == result.upper).all())
        self._check_lower_upper(result)

        b = uniform(-100., -1.)
        result = a * b
        self.assertTrue((a.lower * b == result.upper).all())
        self.assertTrue((a.upper * b == result.lower).all())
        self._check_lower_upper(result)

    def test_set_with_float(self):
        a = NpInterval(np.array([1., -4., 0., 5., -3.]),
                       np.array([1., -1., 2., 12.5, 3]))
        b = 2.5
        result = a * b
        expected_result = NpInterval(
            np.array([2.5, -10, 0, 12.5, -7.5]),
            np.array([2.5, -2.5, 5, 31.25, 7.5])
        )
        self.assertTrue((result.lower == expected_result.lower).all())
        self.assertTrue((result.upper == expected_result.upper).all())

        b = -2.5
        result = a * b
        expected_result = NpInterval(
            np.array([-2.5, 2.5, -5., -31.25, -7.5]),
            np.array([-2.5, 10, 0, -12.5, 7.5])
        )
        self.assertTrue((result.lower == expected_result.lower).all())
        self.assertTrue((result.upper == expected_result.upper).all())

    def test_random_with_ndarray(self):
        shape = self._random_shape()
        a = self._random_npinterval(shape)
        b = np.full(shape, 6.)
        result = a * b
        self.assertTrue((a.lower * b == result.lower).all())
        self.assertTrue((a.upper * b == result.upper).all())
        self._check_lower_upper(result)


class TestAdding(TestNpInterval):
    def test_case(self):
        al = np.asarray([[1, -2, -1], [-4, -5, -1]])
        au = np.asarray([[2, -1,  1], [42, -4, 7]])
        A = NpInterval(al, au)

        bl = np.asarray([[1, 1, 4], [-1, -2, -13]])
        bu = np.asarray([[2, 2, 5], [-1, -1,   1]])
        B = NpInterval(bl, bu)

        rl = np.asarray([[2, -1, 3], [-5, -7, -14]])
        ru = np.asarray([[4,  1, 6], [41, -5,  8]])

        R = A + B
        self.assertTrue((rl == R.lower).all())
        self.assertTrue((ru == R.upper).all())

        R = B
        R += A
        self.assertTrue((rl == R.lower).all())
        self.assertTrue((ru == R.upper).all())

    def _check_result(self, A, B, R):
        al, au = A.lower[0], A.upper[0]
        bl, bu = B.lower[0], B.upper[0]
        rl, ru = R.lower[0], R.upper[0]
        for a, b in product(xrange(al, au), xrange(bl, bu)):
            self.assertTrue(rl <= a + b <= ru)
        self.assertTrue(al + bl - 1 < rl)
        self.assertTrue(au + bu + 1 > ru)

    def test_correct(self):
        for i in xrange(100):
            l = [randrange(-10, 10) for j in xrange(4)]
            A = NpInterval(np.asarray([l[0]]), np.asarray([l[1]]))
            B = NpInterval(np.asarray([l[2]]), np.asarray([l[3]]))

            if A.lower[0] > A.upper[0]:
                A.lower, A.upper = A.upper, A.lower
            if B.lower[0] > B.upper[0]:
                B.lower, B.upper = B.upper, B.lower

            self._check_result(A, B, B + A)

    def test_shape(self):
        for i in xrange(100):
            shape = self._random_shape()
            A = NpInterval(np.ones(shape), 2 * np.ones(shape))
            B = NpInterval(np.ones(shape) * 2, np.ones(shape) * 3)
            R = A + B
            self.assertEqual(R.shape, shape)


class TestSub(TestNpInterval):
    def test_case(self):
        al = np.asarray([[1, -2, -1], [-4, -5, -1]])
        au = np.asarray([[2, -1,  1], [42, -4, 7]])
        A = NpInterval(al, au)

        bl = np.asarray([[1, 1, 4], [-1, -2, -13]])
        bu = np.asarray([[2, 2, 5], [-1, -1,   1]])
        B = NpInterval(bl, bu)

        rl = np.asarray([[-1, -4, -6], [-3, -4, -2]])
        ru = np.asarray([[ 1, -2, -3], [43, -2, 20]])

        R = A - B
        self.assertTrue((rl == R.lower).all())
        self.assertTrue((ru == R.upper).all())

    def _check_result(self, A, B, R):
        al, au = A.lower[0], A.upper[0]
        bl, bu = B.lower[0], B.upper[0]
        rl, ru = R.lower[0], R.upper[0]
        for a, b in product(xrange(al, au), xrange(bl, bu)):
            self.assertTrue(rl <= a - b <= ru)

    def test_correct(self):
        for i in xrange(100):
            l = [randrange(-10, 10) for j in xrange(4)]
            A = NpInterval(np.asarray([l[0]]), np.asarray([l[1]]))
            B = NpInterval(np.asarray([l[2]]), np.asarray([l[3]]))

            if A.lower[0] > A.upper[0]:
                A.lower, A.upper = A.upper, A.lower
            if B.lower[0] > B.upper[0]:
                B.lower, B.upper = B.upper, B.lower

            self._check_result(A, B, A - B)

    def test_shape(self):
        for i in xrange(100):
            shape = self._random_shape()
            A = NpInterval(np.ones(shape), 2 * np.ones(shape))
            B = NpInterval(np.ones(shape) * 2, np.ones(shape) * 3)
            R = A - B
            self.assertEqual(R.shape, shape)


class TestSquare(TestNpInterval):
    def test_case(self):
        al = np.asarray([[1, -2, -1], [-42, -5, -1]])
        au = np.asarray([[2, -1,  1], [  4, -4, 7]])
        A = NpInterval(al, au)

        rl = np.asarray([[1, 1, 0], [   0, 16, 0]])
        ru = np.asarray([[4, 4, 1], [1764, 25, 49]])

        R = A.square()
        self.assertTrue((rl == R.lower).all())
        self.assertTrue((ru == R.upper).all())

    def _check_result(self, A, R):
        al, au = A.lower[0], A.upper[0]
        rl, ru = R.lower[0], R.upper[0]
        for a in xrange(al, au):
            self.assertTrue(rl <= a * a <= ru)
        bigger = max(al*al, au*au) + 1
        self.assertTrue(bigger > ru)
        self.assertTrue(rl > -1)

    def test_correct(self):
        for i in xrange(100):
            a, b = randrange(-10, 10), randrange(-10, 10)
            if a > b:
                a, b = b, a
            A = NpInterval(np.asarray([a]), np.asarray([b]))
            self._check_result(A, A.square())

    def test_shape(self):
        for i in xrange(100):
            shape = self._random_shape()
            A = NpInterval(np.ones(shape), 2 * np.ones(shape))
            self.assertEqual(A.square().shape, shape)


class TestGetSetitem(TestNpInterval):
    def test_1D(self):
        n = 100
        I = NpInterval(np.zeros((n,)), np.zeros((n,)))
        for i in xrange(n):
            I[i] = NpInterval(np.asarray([-i]),np.asarray([i]))
        for i in xrange(n):
            self.assertEquals(I[i].lower, -i)
            self.assertEquals(I[i].upper, i)

    def test_2D(self):
        n = 100
        I = NpInterval(np.zeros((n,n)), np.zeros((n,n)))
        for i, j in product(xrange(n), xrange(n)):
            I[i][j] = NpInterval(np.asarray([i ^ (j**2) - 42]),
                                 np.asarray([i**2 + j**3 / 7]))
        for i, j in product(xrange(n), xrange(n)):
            self.assertEquals(I[i][j].lower, i ^ (j**2) - 42)
            self.assertEquals(I[i][j].upper, i**2 + j**3 / 7)

    def test_3D(self):
        n = 10
        I = NpInterval(np.zeros((n, n, n)), np.zeros((n, n, n)))
        for i, j, k in product(xrange(n), xrange(n), xrange(n)):
            I[i][j][k] = NpInterval(np.asarray([i + j - k ^ 67]),
                                    np.asarray([i * j + 42 * k]))
        for i, j, k in product(xrange(n), xrange(n), xrange(n)):
            self.assertEquals(I[i][j][k].lower, i + j - k ^ 67)
            self.assertEquals(I[i][j][k].upper, i * j + 42 * k)

    def test_4D(self):
        n = 10
        I = NpInterval(np.zeros((n, n, n, n)), np.zeros((n, n, n, n)))
        for i, j, k, l in product(xrange(n), xrange(n), xrange(n), xrange(n)):
            I[i][j][k][l] = NpInterval(np.asarray([i*l ^ j*k]),
                                        np.asarray([(i*j ^ l*k) + 1000]))
        for i, j, k, l in product(xrange(n), xrange(n), xrange(n), xrange(n)):
            self.assertEquals(I[i][j][k][l].lower, i*l ^ j*k)
            self.assertEquals(I[i][j][k][l].upper, (i*j ^ l*k) + 1000)


class TestDiv(TestNpInterval):

    def _random_npinterval_without_zeros(self, shape=None, size_limit=10**2,
                                         number_limit=10**2):
        if shape is None:
            shape = self._random_shape(size_limit, 4)
        sign = np.select([np.random.rand(*shape) > 0.5, True], [1, -1])
        a = np.random.rand(*shape) * uniform(1, number_limit) * sign
        b = np.random.rand(*shape) * uniform(1, number_limit) * sign
        return NpInterval(np.minimum(a, b), np.maximum(a, b))

    def test_div_random_with_float(self):
        for _ in xrange(20):
            a = self._random_npinterval()
            b = uniform(-100., 100.)

            if b == 0:
                continue

            result = a / b
            if b > 0:
                self.assertTrue((a.lower / b == result.lower).all())
                self.assertTrue((a.upper / b == result.upper).all())
            else:
                self.assertTrue((a.lower / b == result.upper).all())
                self.assertTrue((a.upper / b == result.lower).all())
            self._check_lower_upper(result)

    def test_rdiv_random_with_float(self):
        for _ in xrange(20):
            a = uniform(-100., 100.)
            b = self._random_npinterval_without_zeros()

            result = a / b
            if a < 0:
                self.assertTrue(( a / b.lower == result.lower).all())
                self.assertTrue(( a / b.upper == result.upper).all())
            else:
                self.assertTrue((a / b.lower == result.upper).all())
                self.assertTrue((a / b.upper == result.lower).all())
            self._check_lower_upper(result)

    def test_div_random_with_ndarray(self):
        #todo - fix in Interval
        for _ in xrange(20):
            shape = self._random_shape()
            a = self._random_npinterval(shape)
            b = self._random_ndarray(shape)

            if (b == 0).any():
                continue

            result = a / b
            self._check_lower_upper(result)

    def test_div_with_float(self):
        pass

    def test_rdiv_with_float(self):
        a = 2.
        b = NpInterval(
            np.array([[2., 1.], [-5., -10.]]),
            np.array([[4., 10.], [-1., -8]])
        )

        result = a / b
        expected_result = NpInterval(
             np.array([[0.5, 0.2], [-2., -0.25]]),
            np.array([[1, 2.], [-0.4, -0.2]])
        )
        self._assert_npintervals_equal(result, expected_result)

    def test_div_with_ndarray(self):
        pass

    def test_div_random(self):
        pass

    def test_div(self):
        pass


class TestPower(TestNpInterval):
    pass


class TestDot(TestNpInterval):
    pass


class TestMaxMin(TestNpInterval):
    def test_max_min(self):
        pass

    def test_amax_amin(self):
        pass


class TestSmallFunctions(TestNpInterval):
    def test_flatten(self):
        pass

    def test_exp(self):
        pass

    def test_sum(self):
        pass

    def test_neg(self):
        pass

    def test_reciprocal(self):
        pass

    def test_reshape(self):
        pass

    def test_abs(self):
        pass

    def testT(self):
        pass

    def testEval(self):
        pass

    def testDerestOutput(self):
        pass


class TestReshapeForPadding(TestNpInterval):
    pass


class TestFromShape(TestNpInterval):
    pass

class Just(TestCase):
    def test(self):
        shape = (2, 5, 3, 3)
        act = NpInterval(np.ones(shape), np.ones(shape) * 2)
        norm = act.op_d_norm(act, shape, 5, 1, 1, 0.5)


if __name__ == '__main__':
    main(verbosity=2)