import unittest
import pandas as pd


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        self.cases = [1.5, "string"]
        for x in self.cases:
            with self.subTest(x=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        self.cases = [-1, -10, -100]
        for x in self.cases:
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        self.cases = [[0, (0,)], [1, (1,)]]
        for x,b in self.cases:
            # print (a,b)
            with self.subTest(x=x):
                self.assertEqual(factorize (x), b)

    def test_simple_numbers(self):
        self.cases = [[3, (3,)], [13, (13,)], [29, (29,)]]
        for x,b in self.cases:
            # print (a,b)
            with self.subTest(x=x):
                self.assertEqual(factorize (x), b)

    def test_two_simple_multipliers(self):
        self.cases = [[6, (2,3)], [26, (2,13)], [121, (11,11)]]
        for x,b in self.cases:
            # print (a,b)
            with self.subTest(x=x):
                self.assertEqual(factorize (x), b)

    def test_many_multipliers(self):
        self.cases = [[1001, (7, 11, 13)], [9699690, (2, 3, 5, 7, 11, 13, 17, 19)]]
        for x,b in self.cases:
            # print (x,b)
            with self.subTest(x=x):
                # self.assertIsNone(factorize (x))
                self.assertEqual(factorize (x), b)



def factorize(x):
    """
    Factorize positive integer and return its factors.
    :type x: int,>=0
    :rtype: tuple[N],N>0
    """
    # from functools import reduce
    # return tuple(reduce(list.__add__,
    #             ([i, x//i] for i in range(1, int(x**0.5) + 1) if x % i == 0)))



if __name__=='__main__':
    # import unittest


    print(factorize(150))

    unittest.main()