import random

# Задание - генератор пароля.
#  - длина пароля - 15 символов
#  - в пароле есть 3 заглавные буквы (любые, в любом месте пароля)
#  - в пароле есть 4 цифры (любые, в любом месте)
#  - оставшиеся символы пароля - строчные латинские буквы


def pass_generator(digits_n=4, capital_chars_n=3, passw_length=15, shuffle=True):
    """
    The function generates a password.

    Args and params:
    ---------------
        digits_n: int
            number of digits to insert into generated password.

        capital_chars_n : int
            number of capitalized chars to insert into generated password.

        passw_length: int
            generated password length.

        shuffle: True/False
            if true: perform final password chars and digits shuffle.

    """

    rest_chars_n = passw_length - (digits_n + capital_chars_n)

    digits = '1234567890'
    chars = 'qwertyuiopasdfghjklzxcvbnm'

    capital_chars = ''.join([random.choice(chars).upper() for _ in range(capital_chars_n)])

    # cap_chars = ''
    # for x in range(capital_chrs_n):
    #     cap_chars = cap_chars + random.choice(chars).capitalize()

    nums = ''.join([random.choice(digits) for _ in range(digits_n)])

    rest_chars = ''.join([random.choice(chars) for _ in range(rest_chars_n)])

    final_pass = capital_chars + nums + rest_chars

    if shuffle:

        pass_in_list = list(final_pass)
        random.shuffle(pass_in_list)
        final_pass = ''.join(pass_in_list)

        return final_pass

    return final_pass


if __name__ == "__main__":

    print(pass_generator(digits_n=4, capital_chars_n=3, passw_length=15, shuffle=True))
