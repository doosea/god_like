"""
二分查找升序数组
"""


def binary_search(nums, target):
    l = 0
    r = len(nums) - 1
    while l <= r:
        m = (l + r) // 2
        if nums[m] == target:
            return m
        if nums[m] < target:
            l = m + 1
        else:
            r = m - 1
    return -1


if __name__ == '__main__':
    nums = [1, 2]
    r = binary_search(nums, 2)
    print(r)
