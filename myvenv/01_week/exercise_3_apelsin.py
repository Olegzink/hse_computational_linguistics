# задание 3
"""
Как из слова "апельсин" сделать слово "спаниель" ?
Подсказка: вам помогут срезы и операции с индексами
"""

str = 'апельсин'

s = str[-3:-2]
# also making reversion, or ''.join(reversed(str[:2]))
pa = str[:2][::-1]
ni = str[:-3:-1]
el = str[2:5]

all_word = s+pa+ni+el
print(all_word)



