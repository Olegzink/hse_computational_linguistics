# !/usr/bin/python
# coding: utf-8

# генератор паролей

import random

names = ["пром", "агро", "торг", "урал", "север", "юг", "техно",
         "экспо", "метал", "нефть", "сельхоз", "фарм", "строй",
         "кредит", "алмаз", "-девелопмент", "развитие", "мос",
         "рос", "кубань", "сибирь", "восток", "нано", "софт",
         "микро", "онлайн", "инвест", "текстиль", "цемент"]


def name_generator(names_list, roots, capitalize=True):
    """The function generates a company name with the given list of roots.

    Args and params:
    ---------------

        names_list : list
            The list of roots.
        roots : int
            The number of roots to form the final name.
        capitalize: True/False
            Capitalizes the roots to form more readable abbreviations.

    Return:
    -------
        name: str
    """

    name = ''

    for x in range(roots):

        if capitalize:
            chosen_str = random.choice(names_list).capitalize()
        else:
            chosen_str = random.choice(names_list)

        # check for root duplicates in the name as 'росалмазалмазцементкубаньюг'
        if chosen_str not in name:
            name = name + chosen_str

    # check if generated name starts with '-' as in '-девелопментнефть...', rerun the function
    if name.startswith('-'):

        return name_generator(names_list, roots)

    return name


if __name__ == "__main__":

    print(name_generator(names_list=names, roots=6, capitalize=True))
