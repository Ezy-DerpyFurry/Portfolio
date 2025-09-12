### Eh I dunno first try :p
class Solution(object):
    def twoSum(self, nums, target):
        for i in range(len(nums)):
            if nums[i] + nums[i+1] == target:
                print(nums.index(nums[i]), nums.index(nums[i]) + 1)
                return nums.index(nums[i]), nums.index(nums[i]) + 1
        return 0

### I followed a tutorial for this one link -> https://www.youtube.com/watch?v=KLlXCFG5TnA

class Solution(object):
    def twoSum(self, nums, target):
        prevMap = {}

        for i, n in enumerate(nums):
            diff = target - n
            if diff in prevMap:
                return [prevMap[diff], i]
            prevMap[n] = i
        return
