"""
假设按照升序排序的数组在预先未知的某个点上进行了旋转。例如，数组 [0,1,2,4,5,6,7] 可能变为 [4,5,6,7,0,1,2] 。

请找出其中最小的元素。
"""


def search(nums, target):
    l = 0
    r = len(nums) - 1
    while l <= r:
        m = (l + r) // 2
        if nums[m] == target:
            return m
        if nums[m] > nums[l]:  # 左边有序
            if nums[l] <= target < nums[m]:  # 且目标值在左
                r = m - 1
            else:  # 且目标值在右
                l = m + 1
        else:  # 右边有序
            if nums[m] < target <= nums[r]:  # 且目标值在右
                l = m + 1
            else:  # 且目标值在右
                r = m - 1
    return -1


if __name__ == '__main__':
    # nums = [4, 5, 6, 7, 0, 1, 2]
    nums = [3, 1]
    print(search(nums, 7))
