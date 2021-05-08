class TrieNode:
    def __init__(self):
        self.children = dict()
        self.valid = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        p = self.root
        for c in word:
            if c not in p.children:
                p.children[c] = TrieNode()
            p = p.children[c]
        p.valid += 1

    def search(self, word):
        p = self.root
        for c in word:
            if c not in p.children:
                return False
            p = p.children[c]
        return p.valid

    def start_with(self, prefix):
        p = self.root
        for c in prefix:
            if c not in p.children:
                return False
            p = p.children[c]
        return True


if __name__ == '__main__':
    a = Trie()
    a.insert("bee")
    a.insert("can")
    a.insert("cat")
    a.insert("cd")
    print(a.search("bee"))
    print(a.search("cat"))
