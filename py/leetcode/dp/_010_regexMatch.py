
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        input, pattern = s, p
        iIndex, pIndex = 0, 0


    def findStarts(self, p):
        indexs = []
        for i in p:
            if i == '*':
                indexs.append(i)
        return indexs
