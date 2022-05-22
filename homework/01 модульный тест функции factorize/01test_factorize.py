import unittest

class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        self.cases = [1.5, "string"]
        for b in self.cases:
            with self.subTest(case=b):
                self.assertRaises(TypeError, factorize, b)







def factorize(x):
    """
    Factorize positive integer and return its factors.
    :type x: int,>=0
    :rtype: tuple[N],N>0
    """
    from functools import reduce
    return tuple(reduce(list.__add__,
                ([i, x//i] for i in range(1, int(x**0.5) + 1) if x % i == 0)))


if __name__=='__main__':
    # import unittest


    print(factorize(10))

    unittest.main()