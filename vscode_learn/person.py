# 对完整对象进行构建 对代码细节进行封装，将逻辑行为放到类中再赋予实例
# 利用类的继承，是OOP思想浓墨重彩的一笔


class Person:
    def __init__(self, name, job=None, pay=0):
        self.name = name
        self.job = job
        self.pay = pay

    def lastName(self):
        return self.name.split()[-1]

    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))

    # 运算重载符
    def __str__(self):
        return "Person: {}, {}".format(self.name, self.pay)

# 定义Person的子类，通过定制来编程，而不是复制和修改已有的代码


class Manager1(Person):
    # 定制构造函数，为超类步骤添加初始化逻辑
    def __init__(self, name, job='mgr', pay=0):
        Person.__init__(self, name, job, pay)

    def giveRaise(self, percent, bonus=.10):
        # self.pay = int(self.pay * (1 + percent + bonus))
        Person.giveRaise(self, percent + bonus)


class Manager:
    def __init__(self, name, pay):
        self.person = Person(name, 'mgr', pay)

    def giveRaise(self, percent, bonus=.10):
        self.person.giveRaise(percent+bonus)
    def __getattr__(self, attr):
        return getattr(self.person, attr)
    def __str__(self):
        return str(self.person)
    

if __name__ == '__main__':
    bob = Person('Bob Smith')
    sue = Person(name='Sue Jones', job='dev', pay=100000)

    print(bob.name, bob.pay)
    print(sue.name, sue.pay)

    # print(bob.name.split()[-1])
    print(sue.lastName())
    sue.giveRaise(0.1)
    print(sue.pay)
    # 利用运算重载符 __str__ 完成打印制定实例信息输出
    print(sue)

    tom = Manager(name='tom', pay=50000)
    print(tom)
