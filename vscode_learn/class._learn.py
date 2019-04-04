# Python OOP 初探系列 --> 设计模式
class FirstClass:
    def setdata(self, value):
        self.data = value

    def display(self):
        print(self.data)

class SecondClass(FirstClass):
    def display(self): 
        print('Current value = {}'.format(self.data))

# 类的重载

# x = SecondClass()
# print(x)

class ThirdClass(SecondClass):
    # __init__ 自动设置变量属性
    def __init__(self, value):
        self.data = value
    # 运算符重载方法
    def __add__(self, other):
        return ThirdClass(self.data + other)
    def __str__(self):
        return '[ThirdClass:{}]'.format(self.data)
    def mul(self, other):
        self.data *= other
    
a = ThirdClass('abc')
a.display()
print(a)
b = a + 'xyz'
b.display()

# the most sample class
class rec:
    pass
    # ...
rec.name = 'rec_name'
rec.age = 'rec_age'
print(list(rec.__dict__.keys()))
x = rec()
print(list(x.__dict__.keys()))
x.name = 'x_re_name'
print(list(x.__dict__.keys()))

def upperName(self):
    return self.name.upper()

print(upperName(x))