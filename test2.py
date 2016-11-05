class Parent1(object):
    def __init__(self):
        self.var1 = 1

class Parent2(object):
    def _init__(self):
        self.var2 = 2

class Child(Parent1, Parent2):
    def __init__(self):
        Parent1.__init__(self)
        Parent2.__init__(self)


if __name__ == '__main__':
    # a = Parent1()
    # b = Parent2()

    c = Child()

    print c.var2
