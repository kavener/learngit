# 对完整对象进行构建 对代码细节进行封装，将逻辑行为放到类中再赋予实例
class Person:
    def __init__(self, name, job=None, pay=0):
        self.name = name
        self.job = job
        self.pay = pay
    def lastName(self):
        return self.name.split()[-1]
    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))
    
if __name__ == '__main__':
    bob = Person('Bob Smith')
    sue = Person(name='Sue Jones', job='dev', pay=100000)

    print(bob.name, bob.pay)
    print(sue.name, sue.pay)

    # print(bob.name.split()[-1])
    print(sue.lastName())
    sue.giveRaise(0.1)
    print(sue.pay)