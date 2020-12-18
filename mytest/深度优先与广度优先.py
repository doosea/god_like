# -*- coding: utf-8 -*-

"""
@Time        : 2020/12/14
@Author      : dosea
@File        :
@Description : 
"""
import queue


class TreeNode:
    def __init__(self, value=None):
        self.left = None
        self.right = None
        self.value = value


tree_node_0 = TreeNode(0)
tree_node_1 = TreeNode(1)
tree_node_2 = TreeNode(2)
tree_node_3 = TreeNode(3)
tree_node_4 = TreeNode(4)
tree_node_5 = TreeNode(5)
tree_node_6 = TreeNode(6)

tree_node_0.left = tree_node_1
tree_node_0.right = tree_node_2

tree_node_1.left = tree_node_3
tree_node_1.right = tree_node_4

tree_node_2.left = tree_node_5
tree_node_2.right = tree_node_6


# 深度优先搜索 DFS: Depth first search
def dfs(tree_node):
    if tree_node is not None:
        print(tree_node.value)
        if tree_node.left is not None:
            dfs(tree_node.left)
        if tree_node.right is not None:
            dfs(tree_node.right)


# 广度优先搜索 BFS： Breadth First Search
def bfs(tree_node):
    q = []
    q.append(tree_node)
    res = []
    while q:
        t = q.pop(0)
        res.append(t.value)
        if t.left is not None:
            q.append(t.left)
        if t.right is not None:
            q.append(t.right)

    return res


if __name__ == '__main__':
    dfs(tree_node_0)

    a = bfs(tree_node_0)
    print(a)
