#
#
# class TestFactorize(unittest.TestCase):
#     def test_wrong_types_raise_exception(self):
#         self.assertRaises(ValueError, factorize, 1.5)
#         self.assertRaises(ValueError, factorize, "string")





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
    import unittest
    import pandas

    print(factorize(10))

    # unittest.main()