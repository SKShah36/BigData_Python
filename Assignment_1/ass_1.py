# Add the home directory to the system path for the interpreter to search from

import os
import sys
from simple_tokenize import simple_tokenize
from Assignment_0.top50 import count_tokens
from math import log

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

token_dic = count_tokens(filename='../Shakespeare.txt')
distinct_tokens_num = len(token_dic)

# The number of distinct tokens are 25975

# The number of distinct pairs is equal to the permuation of 2 items from distinct tokens
num_pairs = 25975*25974
print(num_pairs)

filename = "../Shakespeare.txt"
with open(filename) as f:
    total_lines = len(list(f))


def _number_cooccur(token1, token2):
    co_count = 0
    with open(filename) as f:
        for line in f:
            tokens = simple_tokenize(line)
            if token1 in tokens and token2 in tokens:
                    co_count += 1
    return co_count


def _two_token_query(token1, token2):
    nx = token_dic[token1]
    ny = token_dic[token2]
    nxy = _number_cooccur(token1, token2)

    px = nx / total_lines
    py = ny / total_lines
    pxy = nxy / total_lines
    pmi = log(pxy / px * py)

    return pmi


def consolidated_query(*q_tokens, threshold=None):
    n = 5
    q_tokens = q_tokens[0]
    print(len(q_tokens))

    if len(q_tokens) < 2:
        if threshold is None:
            raise Exception('Please provide a threshold for one-token query')

        else:
            token1 = q_tokens[0]
            pmi_list = []

            for token2 in token_dic:
                if token2 == token1:
                    continue

                n_co_occur = _number_cooccur(token1, token2)
                if n_co_occur >= threshold:
                    pmi = _two_token_query(token1, token2)
                    pmi_list.append((token1, token2, n_co_occur, pmi))
                index += 1
            pmi_list.sort(key=lambda x: x[2])
            pmi_n = pmi_list[:n]

    else:
        token1 = q_tokens[0]
        token2 = q_tokens[1]
        n_co_occur = _number_cooccur(token1, token2)
        pmi = _two_token_query(token1, token2)
        pmi_n = [(token1, token2, n_co_occur, pmi)]

    return pmi_n


###################################################################################################################
#  the user interface below defines the types of PMI queries that users can ask
#  you will need to modify it - where indicated - to access the results of your PMI analysis (above)
#  so that the queries can be answered
###################################################################################################################

while True:
    q = input("Input 1 or 2 space-separated tokens (return to quit): ")
    if len(q) == 0:
        break
    q_tokens = simple_tokenize(q)
    if len(q_tokens) == 1:
        threshold = 0
        while threshold <= 0:
            try:
                threshold = int(input("Input a positive integer frequency threshold: "))
            except ValueError:
                print("Threshold must be a positive integer!")
                continue

        # Put code here to answer a One-Token Query with token q_tokens[0] and the specified threshold,
        # and output the result.
        # The print() statements below exist to show you the desired output format.
        # Replace them with your own output code, which should produce results in a similar format.

        print("  n({0}) = {1}".format(q_tokens[0], token_dic[q_tokens[0]]))
        print("  high PMI tokens with respect to {0} (threshold: {1}):".format(q_tokens[0], threshold))
        lst = consolidated_query(q_tokens, threshold=8)
        # token1 = token2 = n_co_occur = pmi = None

        for data in lst:
            token1, token2, n_co_occur, pmi = data
            print("    n({0},{1}) = {2},  PMI({0},{1}) = {3}".format(token1, token2, n_co_occur, pmi))

    elif len(q_tokens) == 2:
        # Put code here to answer a Two-Token Query with tokens q_tokens[0] and q_tokens[1]
        # As was the case for the One-Token query, the print statements below show the desired output format
        # Replace them with your own output code
        lst = consolidated_query(q_tokens)
        for data in lst:
            token1, token2, n_co_occur, pmi = data
            print("    n({0},{1}) = {2},  PMI({0},{1}) = {3}".format(token1, token2, n_co_occur, pmi))
    #         print("  n({0},{1}) = XXX".format(q_tokens[0],q_tokens[1]))
    #         print("  PMI({0},{1}) = Y.YYY".format(q_tokens[0],q_tokens[1]))
    else:
        print("Input must consist of 1 or 2 space-separated tokens!")


