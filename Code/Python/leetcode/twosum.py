### Eh I dunno first try :p
class Solution(object):
    def twoSum(self, nums, target):
        for i in range(len(nums)):
            if nums[i] + nums[i+1] == target:
                print(nums.index(nums[i]), nums.index(nums[i]) + 1)
                return nums.index(nums[i]), nums.index(nums[i]) + 1
        return 0
