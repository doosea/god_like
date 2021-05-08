class Node:
    def __init__(self, val=None):
        self.val = val
        self.next = None


# 1. 链表反转
def reverse_link_list(head):
    pre = None
    cur = head
    while cur:
        tmp = cur.next
        cur.next = pre
        pre = cur
        cur = tmp
    return pre


# 2. 链表交换相邻元素 (leetcode24)
def swapParis(head):
    if not head or not head.next:
        return head
    a = head
    cur = head.next
    head = head.next  # return 的首节点
    while cur.next and cur.next.next:
        tmp = cur.next
        cur.next = a
        a.next = tmp.next
        a = tmp
        cur = tmp.next
    if cur.next:
        a.next = cur.next
        cur.next = a
    else:
        cur.next = a
        a.next = None
    return head


def swapParis2(head):
    if not head or not head.next:
        return head
    second = head.next
    head.next = swapParis2(second.next)
    second.next = head
    return second


# 3. 检测链表是否有环(leetcode141)
def hasCycle(head):
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


# 4. 环的长度
def get_cycle_lenth(head):
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    size = 1
    fast = fast.next.next
    slow = slow.next
    while fast is not slow:
        fast = fast.next.next
        slow = slow.next
        size += 1
    return size


# 5. 检测入环点位置 (leetcode142)
def detectCycle(head):
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    if fast is None or fast.next is None:
        return None
    else:
        fast = head
        while fast != slow:
            fast = fast.next
            slow = slow.next
        return fast


# 6. 如何获取倒数第K个元素，(leetcode19) （两个指针，第一个指针先走k步， 然后同时走， 当第一个指针指null,则慢指针为倒数第k个元素）
def get_reverse_k_element(head, k):
    fast = head
    slow = head
    while fast and k > 0:
        fast = fast.next
        k = k - 1

    if k > 0:
        return None

    while fast:
        fast = fast.next
        slow = slow.next
    return slow.val


# 7. 删除倒数第K个节点
def removeNthFromEnd(head, n):
    """
        提示：
            链表中结点的数目为 sz
            1 <= sz <= 30
            0 <= Node.val <= 100
            1 <= n <= sz
    """
    fast = head
    slow = head
    while n > 0:  # 先走n步b
        if fast.next:
            fast = fast.next
        else:
            return head.next
        n -= 1
    while fast.next:  # 这里注意使用fast.next， 这样slow 对应的就是要删除节点的前继节点
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next  # 删除slow.next 节点
    return head


# 8. 合并两个有序链表 leetcode21
def mergeTwoLists(l1, l2):
    if l1 is None:
        return l2
    if l2 is None:
        return l1
    pre = Node(-1)
    end = pre
    while l1 and l2:
        if l1.val <= l2.val:
            end.next = l1
            l1 = l1.next
        else:
            end.next = l2
            l2 = l2.next
        end = end.next

    if l1 is None:
        end.next = l2
    if l2 is None:
        end.next = l1
    return pre.next


# 9.  leetcode 108. 将有序数组转换为二叉搜索树
def sortedArrayToBST(nums):
    if not nums:
        return None

    # 找到中点作为根节点
    mid = len(nums) // 2
    node = Node(nums[mid])

    # 左侧数组作为左子树
    left = nums[:mid]
    right = nums[mid + 1:]

    # 递归调用
    node.left = sortedArrayToBST(left)
    node.right = sortedArrayToBST(right)

    return node


# 10. leetcode109 有序链表转化为二叉搜索树
def sortedListToBST(head):
    def getMedian(left, right):
        fast = slow = left
        while fast != right and fast.next != right:
            fast = fast.next.next
            slow = slow.next
        return slow

    def buildTree(left, right):
        if left == right:
            return None
        mid = getMedian(left, right)
        root = Node(mid.val)
        root.left = buildTree(left, mid)
        root.right = buildTree(mid.next, right)
        return root

    return buildTree(head, None)

# 颜色分类
def sortColors(nums):
    n = len(nums)
    p0, p2 = 0, n - 1
    i = 0
    while i <= p2:
        while i <= p2 and nums[i] == 2:
            nums[i], nums[p2] = nums[p2], nums[i]
            p2 -= 1
        if nums[i] == 0:
            nums[i], nums[p0] = nums[p0], nums[i]
            p0 += 1
        i += 1


# 03. 大数相加， leetcode 415 easy
def big_data_add(a, b):
    # 1.先获取两个中最大的长度，然后将短进行补充，使长度一致
    max_len = max(len(a), len(b))
    res = [0] * (max_len + 1)

    if len(a) < len(b):
        a = '0' * (len(b) - len(a)) + a
    else:
        b = '0' * (len(a) - len(b)) + b

    # 翻转
    a = list(a[::-1])
    b = list(b[::-1])

    for i in range(max_len):
        tmp_add = int(a[i]) + int(b[i]) + res[i]
        if tmp_add >= 10:
            res[i] = tmp_add % 10
            res[i + 1] = tmp_add // 10
        else:
            res[i] = tmp_add

    if res[-1] == 0:
        res = res[:-1]
    res = res[::-1]
    r = ""
    for i in res:
        r += str(i)

    return r


# 二分查找：剑指 Offer 11. 旋转数组的最小数字
def minarray(nums):
    l = 0
    r = len(nums) - 1
    while l < r:
        mid = (l + r) // 2
        if nums[mid] > nums[r]:
            l = mid + 1
        elif nums[mid] < nums[r]:
            r = mid
        else:
            r = r - 1
    return nums[l]


# 二分查找：搜索旋转排序数组， 旋转数组target
def search(nums, target):
    l = 0
    r = len(nums) - 1
    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target:
            return mid
        # 左边有序
        if nums[l] <= nums[mid]:
            if nums[l] <= target < nums[mid]:  # 在左边
                r = mid - 1
            else:  # 不在左边范围
                l = mid + 1
        else:  # 左边无序， 右边有序
            if nums[mid] < target <= nums[r]:
                l = mid + 1
            else:
                r = mid - 1
    return -1


# leetcode152. 乘积最大子数组
def maxproduct1(nums):
    n = len(nums)
    p1 = [0] * n  # 保存当前最大值
    p2 = [0] * n  # 保存当前最小值

    p1[0] = p2[0] = nums[0]
    for i in range(1, n):
        if nums[i] >= 0:
            p1[i] = max(p1[i - 1] * nums[i], nums[i])
            p2[i] = min(p2[i - 1] * nums[i], nums[i])
        else:
            p1[i] = max(p2[i - 1] * nums[i], nums[i])
            p2[i] = min(p1[i - 1] * nums[i], nums[i])
    return max(p1)


# leetcode152. 乘积最大子数组(优化空间)
def maxproduct2(nums):
    n = len(nums)
    res_max, tmp_max, tmp_min = nums[0], nums[0], nums[0]
    for i in range(1, n):
        if nums[i] < 0:
            tmp_max, tmp_min = tmp_min, tmp_max
        tmp_max = max(tmp_max * nums[i], nums[i])
        tmp_min = min(tmp_min * nums[i], nums[i])
        res_max = max(tmp_max, res_max)
    return res_max


# leetcode  283 数组移动零
def move_zeros(nums):
    """
        l 指向处理好序列的尾部
        r 指向待处理序列的头部。
        l- r 之间全部为0 元素
    """
    n = len(nums)
    l, r = 0, 0
    while r < n:
        if nums[r] != 0:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
        r += 1
    return nums

# 颜色分类
def sortColors( nums):
    l = 0
    i = 0
    r = len(nums)-1
    while i <= r:
        if nums[i] == 0:
            nums[l], nums[i] = nums[i], nums[l]
            l += 1
            i += 1
        elif nums[i] == 2:
            nums[r], nums[i] = nums[i], nums[r]
            r -= 1
        else:
            i += 1

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
    print(move_zeros([1, 0, 0, 12, 0, 3]))
