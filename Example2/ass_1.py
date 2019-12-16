# Add the home directory to the system path for the interpreter to search from

import os
import sys
from simple_tokenize import simple_tokenize
from Assignment_0.top50 import count_tokens
from math import log


def add_dependencies():
    module_path = os.path.abspath(os.path.join('..'))
    if module_path not in sys.path:
        sys.path.append(module_path)


class Query:
    def __init__(self):
        self._all_tokens = []
        self._spec_token = []
        self._text_to_tokens()

    def _text_to_tokens(self, filename="../Shakespeare.txt"):
        with open(filename) as f:
            for line in f:
                self._all_tokens.append(simple_tokenize(line))

    def _specific_token(self, token):
        self._spec_token = []
        for tokens in self._all_tokens:
            if token in tokens:
                self._spec_token.append(tokens)

    def _number_occur(self, token2):
        co_count = 0
        for tokens in self._spec_token:
            if token2 in tokens:
                co_count += 1
        return co_count

    def _two_token_query(self, token1, token2):
        nx = token_dic[token1]
        ny = token_dic[token2]
        nxy = self._number_occur(token2)
        total_lines = len(self._all_tokens)
        px = nx / total_lines
        py = ny / total_lines
        pxy = nxy / total_lines
        pmi = log(pxy / px * py)

        return pmi

    def consolidated_query(self, *q_tokens, threshold=None):
        n = 5
        q_tokens = q_tokens[0]

        if len(q_tokens) < 2:
            if threshold is None:
                raise Exception('Please provide a threshold for one-token query')

            else:
                token1 = q_tokens[0]
                pmi_list = []
                self._specific_token(token1)

                for token2 in token_dic:
                    if token2 == token1:
                        continue

                    n_co_occur = self._number_occur(token2)

                    if n_co_occur >= threshold:
                        pmi = self._two_token_query(token1, token2)
                        pmi_list.append((token1, token2, n_co_occur, pmi))

                pmi_list.sort(key=lambda x: x[3])
                pmi_n = pmi_list[:n]

        else:
            token1 = q_tokens[0]
            token2 = q_tokens[1]
            self._specific_token(token1)
            n_co_occur = self._number_occur(token2)
            pmi = self._two_token_query(token1, token2)
            pmi_n = [(token1, token2, n_co_occur, pmi)]

        return pmi_n


def main():

    query = Query()
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

            print("  n({0}) = {1}".format(q_tokens[0], token_dic[q_tokens[0]]))
            print("  high PMI tokens with respect to {0} (threshold: {1}):".format(q_tokens[0], threshold))
            lst = query.consolidated_query(q_tokens, threshold=threshold)

            for data in lst:
                token1, token2, n_co_occur, pmi = data
                print("    n({0},{1}) = {2},  PMI({0},{1}) = {3}".format(token1, token2, n_co_occur, pmi))

        elif len(q_tokens) == 2:
            lst = query.consolidated_query(q_tokens)
            for data in lst:
                token1, token2, n_co_occur, pmi = data
                print("    n({0},{1}) = {2},  PMI({0},{1}) = {3}".format(token1, token2, n_co_occur, pmi))

        else:
            print("Input must consist of 1 or 2 space-separated tokens!")


if __name__ == '__main__':
    token_dic = count_tokens(filename='../Shakespeare.txt')
    distinct_tokens_num = len(token_dic)

    # The number of distinct tokens are 25975

    # The number of distinct pairs is equal to the permuation of 2 items from distinct tokens
    num_pairs = 25975*25974
    print(num_pairs)

    main()

