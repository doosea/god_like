# https://www.cnblogs.com/wuxinyan/p/8615127.html
# 1. 冒泡排序
def bubble_sort(a):
    n = len(a)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


# 2. 选择排序
def selection_sort(nums):
    for i in range(len(nums) - 1):
        min_index = i
        for j in range(i + 1, len(nums)):
            if nums[min_index] > nums[j]:
                min_index = j
        nums[i], nums[min_index] = nums[min_index], nums[i]
    return nums


# 3.快速排序： 递归方法
def quickly_sort(nums):
    if len(nums) <= 1:
        return nums
    pivot = nums[0]
    left = [i for i in nums if i < pivot]
    right = [i for i in nums if i > pivot]
    return quickly_sort(left) + [pivot] + quickly_sort(right)


# 3. 快速排序
def qucikly_sort2(nums, low, high):
    if low >= high:
        return nums
    pivot = nums[low]
    i = low
    j = high

    while i < j:
        while i < j and nums[j] >= pivot:
            j -= 1
        while i < j and nums[i] <= pivot:
            i += 1
        if i < j:
            nums[i], nums[j] = nums[j], nums[i]

    # 这里把基准值和ij位置的元素互换
    nums[low] = nums[i]
    nums[i] = pivot
    qucikly_sort2(nums, 0, i - 1)
    qucikly_sort2(nums, j + 1, high)


# 4.堆排序
def heap_sort(nums):
    build_max_heap(nums)
    for i in range(len(nums) - 1, -1, -1):
        nums[i], nums[0] = nums[0], nums[i]
        max_heapify(nums, i, 0)
    return nums


def build_max_heap(nums):
    n = len(nums)
    for i in range(n // 2 - 1, -1, -1):
        max_heapify(nums, n, i)


def max_heapify(nums, size, root):
    left = 2 * root + 1
    right = left + 1
    larger = root
    if left < size and nums[left] > nums[larger]:
        larger = left
    if right < size and nums[right] > nums[larger]:
        larger = right
    if larger != root:  # 需要调整的时候
        nums[larger], nums[root] = nums[root], nums[larger]
        max_heapify(nums, size, larger)  # 递归调整子节点


# 5. 归并排序
def merge_sort(nums):
    if len(nums) <= 1:
        return nums
    mid = len(nums) // 2
    left = merge_sort(nums[0:mid])
    right = merge_sort(nums[mid:])
    return merge(left, right)


def merge(a, b):
    i = 0
    j = 0
    res = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            res.append(a[i])
            i += 1
        else:
            res.append(b[j])
            j += 1
    res += a[i:]
    res += b[j:]
    return res


if __name__ == '__main__':
    a = [1, 3, 5, 2, 4, 6, 8, 20, 19, 18, 17, 16, 14, 12, 13]
    #
    # b = bubble_sort(a)
    # b = quickly_sort(a)
    # b = qucikly_sort2(a, 0, len(a) - 1)
    # b = selection_sort(a)
    # b = heap_sort(a)
    b = merge_sort(a)
    print(b)
