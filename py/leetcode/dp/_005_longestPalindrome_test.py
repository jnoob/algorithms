import unittest
from leetcode.dp._005_longestpalindrome import Solution


class longestPalindromeTest(unittest.TestCase):

    def setUp(self):
        self.solution = Solution()

    def emptyStrTest(self):
        str = ''
        self.assertPalindrome(str, str)

    def noneInputTest(self):
        self.assertPalindrome(None, None)

    def allSingleCharInputTest(self):
        self.assertPalindrome('abcde', ['a', 'b', 'c', 'd', 'e'])

    def evenCountFullMatchInputTest(self):
        self.assertPalindrome('abccba', 'abccba')

    def evenMatchInInputTest(self):
        self.assertPalindrome('ijnhjhjhjhjhjhj', 'hjhjhjhjhjh')

    def oddCountFullMatchInputTest(self):
        self.assertPalindrome('abcdedcba', 'abcdedcba')

    def oddMatchInInputTest(self):
        self.assertPalindrome('jasdmnnbvccvbnnmookp', 'mnnbvccvbnnm')

    def repeatingCharInputTest(self):
        self.assertPalindrome('aaaaaa', 'aaaaaa')
        self.assertPalindrome('aaaaa', 'aaaaa')

    def multiPalindromeTest(self):
        self.assertPalindrome('vasacjlmjuiiujmoo', 'mjuiiujm')

    def assertPalindrome(self, input, compareTo):
        output = self.solution.longestPalindrome(input)
        if isinstance(compareTo, list):
            self.assertIn(output, compareTo)
        else:
            self.assertEquals(output, compareTo)
