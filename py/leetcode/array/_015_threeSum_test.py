import unittest

from array._015_threeSum import Solution


class ThreeSumTest(unittest.TestCase):
    def __init__(self):
        solution = Solution()

    def test_leetcode_sample(self):
        nums = [-1, 0, -1, 2, -1, -4]
        result = self.solution.threeSum(nums)

    def result_check(self, cal, pre):
        pass




if __name__ == '__main__':
    unittest.main()
