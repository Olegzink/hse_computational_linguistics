# задание 1
# какие из этих строк можно конкатенировать? Какие умножать? Какие вычитать? Запишите все результаты, которые у Вас получились

import sys

a = 23
b = 34.02
c = "python is cool"
d = "you are cool, too"

# all math operations are possible for int and float types. As an example:
multiplication = a*b
division = a/b
print(multiplication)
print(division)

# though you can't do, for example, these math operations on str and float
try:
    print(c*b)
    print(c/b)
    print(c-b)
    print(c+b)
except:
    print('this operation is not allowed', sys.exc_info()[0])

print()
# you can operate on str and int in this way
str_int_multiplication = a*c
print(str_int_multiplication)

# though you can't do, for example, these math operations on str and int
try:
    print(c/a)
    print(c-a)
    print(c+a)
except:
    print('this operation is not allowed', sys.exc_info()[0])

print()
# you can concatenate str + str
print(c+d)

# though you can't do, for example, these math operations on str and str
try:
    print(c/d)
    print(c-d)
    print(c*d)
except:
    print('this operation is not allowed', sys.exc_info()[0])





