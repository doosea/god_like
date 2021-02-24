class TreeNode(object):
    def __init__(self, val=None):
        self.left = None
        self.right = None
        self.val = val


# 先序打印二叉树（递归）
def preOrderTraverse1(node):
    if not node:
        return None
    print(node.val)
    preOrderTraverse1(node.left)
    preOrderTraverse1(node.right)


# 先序打印二叉树（非递归）
def preOrderTraverse2(node):
    stack = [node]
    while len(stack) > 0:
        print(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
        node = stack.pop()


# 中序打印二叉树（递归）
def inOrderTraverse1(node):
    if node is None:
        return None
    inOrderTraverse1(node.left)
    print(node.val)
    inOrderTraverse1(node.right)


# 中序打印二叉树（非递归）
def inOrderTraverse2(node):
    stack = []
    pos = node
    while pos or len(stack) > 0:
        if pos:
            stack.append(pos)
            pos = pos.left
        else:
            pos = stack.pop()
            print(pos.val)
            pos = pos.right


# 后序打印二叉树（递归）
def postOrderTraverse1(node):
    if node is None:
        return None
    postOrderTraverse1(node.left)
    postOrderTraverse1(node.right)
    print(node.val)


# 后序打印二叉树（非递归）
# 使用两个栈结构
# 第一个栈进栈顺序：左节点->右节点->跟节点
# 第一个栈弹出顺序： 跟节点->右节点->左节点(先序遍历栈弹出顺序：跟->左->右)
# 第二个栈存储为第一个栈的每个弹出依次进栈
# 最后第二个栈依次出栈
def postOrderTraverse(node):
    stack = [node]
    stack2 = []
    while len(stack) > 0:
        node = stack.pop()
        stack2.append(node)
        if node.left is not None:
            stack.append(node.left)
        if node.right is not None:
            stack.append(node.right)
    while len(stack2) > 0:
        print(stack2.pop().val)


a = TreeNode(1)
b = TreeNode(2)
c = TreeNode(3)
d = TreeNode(4)
e = TreeNode(5)
f = TreeNode(6)
g = TreeNode(7)

a.left = b
a.right = c
b.left = d
b.right = e
c.left = f
c.right = g

if __name__ == '__main__':
    preOrderTraverse1(a)
    preOrderTraverse2(a)