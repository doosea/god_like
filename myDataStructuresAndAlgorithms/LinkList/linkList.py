class Node:
    def __init__(self, val=None):
        self.val = val
        self.next = None


def get_link_list_cycle():
    a = Node(1)
    b = Node(2)
    c = Node(3)
    d = Node(4)
    e = Node(5)
    f = Node(6)
    g = Node(7)
    a.next = b
    b.next = c
    c.next = d
    d.next = e
    e.next = f
    f.next = g
    g.next = b

    return a


def get_link_list():
    a = Node(1)
    b = Node(2)
    c = Node(3)
    d = Node(4)
    e = Node(5)
    a.next = b
    b.next = c
    c.next = d
    d.next = e

    return a


def print_link_list(head):
    while head:
        print(head.val, end="->")
        head = head.next
    print("success print")


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


# 链表快速排序

if __name__ == '__main__':
    # head = get_link_list()
    # print_link_list(head)

    # res = reverse_link_list(head)
    # print_link_list(res)

    # res2 = swapParis(head)
    # print_link_list(res2)

    # res3 = hasCycle(head)
    # print(res3)

    # res4 = get_reverse_k_element(head, 10)
    # print(res4)

    head = get_link_list_cycle()
    # res = detectCycle(head)
    #
    # print(res.val)
    #
    # head = get_link_list()
    #
    # print_link_list(head)
    # res = swapParis2(head)
    # print_link_list(res)
    res = get_cycle_lenth(head)
    print(res)
