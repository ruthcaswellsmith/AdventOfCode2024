from utils import read_file

if __name__ == '__main__':
    filename = 'input/Day1.txt'
    data = read_file(filename)

    list1, list2 = zip(*sorted([(int(x), int(y)) for x, y in [line.split() for line in data]]))

    print(f"The answer to part 1 is {sum(abs(x - y) for x, y in zip(list1, list2))}")
    print(f"The answer to part 2 is {sum(list2.count(x) * x for x in list1)}")
