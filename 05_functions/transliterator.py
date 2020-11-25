import json

# ! Before running check the 'Data' directory path, mapping tables are located there.

def cyr_transliterate(text, gost='gost_7_79_2000_b.json', upper=False):
    """
    The function translates cyrillic chars into latin, using predefined ГОСТ.

    Args and params:
    ---------------
        text: str
            Text to process

        gost : json file
            'gost_7_79_2000_a.json' - default value. ГОСТ 7.79-2000 / ISO 9:1995.
            'gost_7_79_2000_a.json' - translates into latin chars with diacritic signs.
            'gost_7_79_2000_b.json' - translates into two-chars form (ж>zh).
            'icao.json' - the standard, used for airline tickets, foreign passport (https://www.icao.int/publications/Documents/9303_p3_cons_en.pdf, page 33 'Transliteration of Cyrillic Characters').

        upper: True/False
            Return uppercase copy of a text

    """

    with open('{}/{}'.format('data', gost), 'r', encoding='utf-8') as myfile:

        data = myfile.read()
        obj = json.loads(data)

    trans_table = {}

    for k, v in obj.items():
        # ord - return a unicode code for a chr
        trans_table[ord(k)] = v

    text = text.translate(trans_table)

    if upper:

        text_upper = text.upper()

        return text_upper

    return text


if __name__ == "__main__":

    original_text = '''В противоположность транскрипции, предназначаемой для максимально точной передачи звуков языка, транслитерация, как это показывает сам термин (лат. litera — буква), касается письменной формы языка: текст, написанный на том или ином алфавите, передаётся алфавитом другой какой-либо системы. При этом обычно принимается во внимание только соответствие букв двух алфавитов, а звуки, скрывающиеся за ними, не учитываются. '''

    print(cyr_transliterate(text=original_text, gost='gost_7_79_2000_b.json', upper=False))

    # print(cyr_transliterate(text=original_text, gost='gost_7_79_2000_a.json', upper=False))

    # print(cyr_transliterate(text=original_text, gost='icao.json', upper=False))

