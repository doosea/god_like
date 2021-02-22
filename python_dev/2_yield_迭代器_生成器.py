class MyIterator(object):
    """ 自定义迭代器 """

    def __init__(self, items):
        self.items = items
        self.current_index = 0

    def __iter__(self):
        pass

    def __next__(self):
        if self.current_index < len(self.items):
            data = self.items[self.current_index]
            self.current_index += 1
        else:
            raise StopIteration
        return data


class MyList(object):
    """ 自定义列表 """

    def __init__(self):
        self.items = []

    def __iter__(self):
        return MyIterator(self.items)

    def add_item(self, item):
        self.items.append(item)


# 斐波那契数列-迭代器
class Fibnacci(object):
    def __init__(self, num):
        self.num = num
        self.index = 0
        self.a = 1
        self.b = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.num:
            res = self.a
            self.a, self.b = self.a + self.b, self.a
            self.index += 1
            return res
        else:
            raise StopIteration


# 定义生成器
def fibonacci(num):
    # num: 表示斐波那契数列的个数
    # 保存前两个值
    a = 0
    b = 1
    # 记录生成数列的下标
    current_index = 0
    print("----11----")
    # 循环判断条件是否成立
    while current_index < num:
        # 生成下一个斐波那契数列
        result = b
        a, b = b, a + b
        current_index += 1
        print("----22----")
        # 代码执行到yield会暂停，把结果返回出取，再次启动生成器的时候会在暂停的位置继续往下执行
        yield result
        print("----33----")



if __name__ == '__main__':
    mylist = MyList()
    mylist.add_item(11)
    mylist.add_item(21)
    mylist.add_item(31)

    """
        for 循环：
            （1）iter(mylist) , 通过iter() 获取对象的迭代器， -->  
    """
    for i in mylist:
        print(i)

    aa = fibonacci(5)
    print(aa)
    for i in aa:
        print(i)

    bb = Fibnacci(5)
    for i in bb:
        print(i)
