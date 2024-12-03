from utils import read_file
import re

PATTERN = r"mul\([0-9]+,[0-9]+\)"
DO_PATT = r"do\(\)"
DONT_PATT = r"don't\(\)"


def get_products(text: str):
    result = 0
    locs = [(match.start(), match.end()) for match in re.finditer(PATTERN, text)]
    for loc in locs:
        parts = [int(ele) for ele in text[loc[0]:loc[1]].strip('mul').strip('(').strip(')').split(',')]
        result += parts[0] * parts[1]
    return result


if __name__ == '__main__':
    filename = 'input/Day3.txt'
    data = read_file(filename)
    text = ''.join(data)

    print(f"The answer to part 1 is {get_products(text)}")

    result, enabled = 0, True
    while text:
        match = re.search(DONT_PATT if enabled else DO_PATT, text)
        if match:
            enabled = not enabled
            result += get_products(text[:match.start()]) if enabled else 0
        else:
            break
        text = text[match.end():]
    if enabled:
        result += get_products(text)

    print(f"The answer to part 2 is {result}")
