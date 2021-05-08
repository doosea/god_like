"""
假设按照升序排序的数组在预先未知的某个点上进行了旋转。例如，数组 [0,1,2,4,5,6,7] 可能变为 [4,5,6,7,0,1,2] 。

请找出其中最小的元素。
"""


def findMin(nums):
    if nums[0] <= nums[-1]:
        return nums[0]
    l, r = 0, len(nums) - 1
    while l < r:
        mid = (l + r) // 2
        if nums[mid] >= nums[l] and nums[mid] > nums[r]:
            l = mid + 1
        else:
            r = mid
    return nums[l]


if __name__ == '__main__':
    nums = [2, 1]
    r = findMin(nums)
    print(r)

