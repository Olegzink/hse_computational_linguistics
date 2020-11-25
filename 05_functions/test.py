import random
import itertools
chars = 'qwertyuiopasdfghjklzxcvbnm'

p = [random.choice(chars[i]) for i in range(5)]
print(p)

a = [x for x in random.choice([p for p in itertools.permutations(chars, 3)])]
print(a)


# nums = ''.join([random.choice(digits) for x in range(digits_n)])