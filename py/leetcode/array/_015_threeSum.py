'''

给定一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？找出所有满足条件且不重复的三元组。
注意：答案中不可以包含重复的三元组。

'''

from utils import List


class Solution:

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # 1. 将数组按拆分成大于0和小于等于0的两个有序数组，并判断是否剩下为0的
        #       1.1 如果存在为0的，标识taketwo置为true
        # 2. 将小于０和大于０的分别按两个进行求和
        # 3. 按２－１，１－２进行组合，看能否得到０
        lt0dict, gt0dict, eq0list = Solution.__group_by_with_zero_relation(nums)
        lt0two_sums, gt0two_sums = Solution.__eval_two_sums(lt0dict), Solution.__eval_two_sums(gt0dict)
        contains0 = len(eq0list) > 0
        result = []
        Solution.__append_sum_zero(result, lt0dict, gt0two_sums, gt0dict, eq0list, contains0)
        Solution.__append_sum_zero(result, gt0dict, lt0two_sums, lt0dict, eq0list, contains0)
        return result

    @staticmethod
    def __append_sum_zero(result, base_dict, suppl_two_sum, suppl_dict, zero_list, contains0):
        for base_value, indexes in base_dict.items():
            if -base_value in suppl_two_sum.keys():
                for m in indexes:
                    for n in suppl_two_sum[-base_value]:
                        tmp = [m]
                        tmp.extend(n)
                        result.append(tmp)
            if contains0 and -base_value in suppl_dict.keys():
                for m in indexes:
                    for n in suppl_dict[-base_value]:
                        for k in zero_list:
                            result.append([m, n, k])

    @staticmethod
    def __eval_two_sums(values):
        two_sums = {}
        keys = list(values.keys())
        for i in range(0, len(keys) - 1):
            if len(values[keys[i]]) > 1:
                two_sum = keys[i] * 2
                if two_sum not in two_sums.keys():
                    two_sums[keys[i] * 2] = []
                for m in range(0, len(values[keys[i]]) - 1):
                    for n in range(m + 1, len(values[keys[i]])):
                        two_sums[keys[i] * 2].append([m, n])
            for j in range(i + 1, len(keys)):
                two_sum = keys[i] + keys[j]
                if two_sum not in two_sums.keys():
                    two_sums[two_sum] = []
                for m in values[i]:
                    for n in values[j]:
                        two_sums[two_sum].append([m, n])
        return two_sums

    @staticmethod
    def __group_by_with_zero_relation(nums):
        lt0dict, gt0dict, eq0list = {}, {}, []
        for i in range(0, len(nums)):
            if nums[i] == 0:
                eq0list.append(i)
            elif nums[i] > 0:
                if nums[i] in gt0dict.keys():
                    gt0dict[nums[i]].append(i)
                else:
                    gt0dict[nums[i]] = [i]
            else:
                if nums[i] in lt0dict.keys():
                    gt0dict[nums[i]].append(i)
                else:
                    gt0dict[nums[i]] = [i]
        return lt0dict, gt0dict, eq0list
