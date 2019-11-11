from simple_tokenize import simple_tokenize


def count_tokens(filename='Shakespeare.txt'):
    dic = {}

    with open(filename) as f:
        for line in f:
            # tokenize, one line at a time
            t = simple_tokenize(line)
            for token in t:
                if token in dic:
                    dic[token] += 1
                else:
                    dic[token] = 1
    return dic


def top_50_tokens(filename='Shakespeare.txt'):
    global dic
    dic_items = [di for di in dic.items()]
    dic_items.sort(key=lambda x:x[1])
    top_50_tokens_list = [x[0] for x in dic_items]
    top_50_tokens_list = top_50_tokens_list[:50]

    # In this function, write Python code to find the 50 most frequent tokens in Shakespeare.txt
    # Make sure that your code is commented
    return top_50_tokens_list


# dic = count_tokens(filename='Shakespeare.txt')
# top_50_tokens()
