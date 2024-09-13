# 定义一个简单的装饰器函数
def my_decorator(func):
    def wrapper():
        print("在调用原始函数之前")
        func()  # 调用原始函数
        print("在调用原始函数之后")
    return wrapper

# 使用装饰器
# AOP
@my_decorator
def say_hello():
    print("Hello, world!")

# 调用被装饰的函数
say_hello()

def add(a, b):
    return a + b

# 按照定义的顺序传递给函数
print(add(3, 5))  # 输出：8

# 默认参数
def greet(name="Guest"):
    return f"Hello, {name}!"

print(greet())  # 输出：Hello, Guest!
print(greet("Alice"))  # 输出：Hello, Alice!

def introduce(name, age):
    return f"My name is {name} and I am {age} years old."
# 允许你在调用函数时显式指定参数的名称
print(introduce(age=25, name="Alice"))  # 输出：My name is Alice and I am 25 years old.

# *args: 用于传递任意数量的位置参数
def multiply(*args):
    result = 1
    for num in args:
        result *= num
    return result

print(multiply(2, 3, 4))  # 输出：24

# **kwargs: 用于传递任意数量的关键字参数
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25, city="New York")


# 偏函数
# 创建偏函数
from functools import partial

def power(base, exponent):
    return base ** exponent

# 创建偏函数，将 exponent 参数固定为 2
square = partial(power, exponent=2)

# 调用偏函数
print(square(5))  # 输出：25
print(square(10)) # 输出：100
