from simple_tokenize import simple_tokenize


def perfect_x(filename='Shakespeare.txt'):
    # In this function, write Python code to find tokens that follow "perfect" in Shakespeare.txt
    # Make sure that your code is commented
    perfect_x_list = {}
    with open(filename) as f:
        for line in f:
            t = simple_tokenize(line)
            ln = t[:-1]
            # print("T is {}".format(t))
            # print("ln is {}".format(ln))

            try:
                next_ind = ln.index('perfect') + 1
            except ValueError:
                continue

            next_word = t[next_ind]
            if next_word in perfect_x_list:
                perfect_x_list[next_word] += 1
            else:
                perfect_x_list[next_word] = 1

    perfect_keys = list(perfect_x_list.keys())
    for key in perfect_keys:
        if perfect_x_list[key] < 2:
            perfect_x_list.pop(key)

    perfect_x_list = list(perfect_x_list.keys())
    return perfect_x_list


print(perfect_x())
