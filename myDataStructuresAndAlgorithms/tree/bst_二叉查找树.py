class TreeNode(object):
    def __init__(self, data=None):
        self.left = None
        self.right = None
        self.data = data


class BinarySearchTree(object):
    def __init__(self, root=None):
        self.root = root

    def find_min(self):
        if self.root is None:
            return None
        curr = self.root
        while curr.left is not None:
            curr = curr.left
        return curr.data

    def find_max(self):
        if self.root is None:
            return None
        curr = self.root
        while curr.right is not None:
            curr = curr.right
        return curr.data

    def insert(self, data):
        node = TreeNode(data)
        if self.root is None:
            self.root = node
        else:
            curr = self.root
            while True:
                if data < curr.data:
                    if curr.left is None:
                        curr.left = node
                        return
                    curr = curr.left
                else:
                    if curr.right is None:
                        curr.right = node
                        return
                    curr = curr.right

    def delete(self, data):
        pass

    def search(self, data):
        if self.root is None:
            return None
        curr = self.root
        while curr is not None:
            if curr.data == data:
                return curr
            if data < curr.data:
                curr = curr.left
            else:
                curr = curr.right
        return curr

    def mid_traverse(self, node):
        if node is None:
            return
        self.mid_traverse(node.left)
        print(node.data)
        self.mid_traverse(node.right)


if __name__ == '__main__':
    bst = BinarySearchTree()
    a = [7, 5, 9, 8, 15, 16, 18, 17]
    for i in a:
        bst.insert(i)
    bst.mid_traverse(bst.root)
    print(bst.find_min())
    print(bst.find_max())
    print(bst.search(15))