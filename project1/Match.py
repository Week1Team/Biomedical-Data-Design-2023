import numpy as np
from Draw import *
# -This module provides a match function.
# -The match function is based on Hungarian algorithm.
# -The match function firstly minus the min value or each row,
#       then it applies match_zero function to find-out the max match-zeros,
#       if the max match-zeros is same as doctor number, the algorithm successfully give the match result,
#       if not, the algorithm use draw_lines function to cover all zeros using the fewest lines,
#       and then use the lines to generated more zeros in the array,
#       until successfully match.

# -The match_zero function is used to find-out the max match-zeros
# -The match_once function is used by match_zero function.


def match_once(i, array, M, N, p, vis):
    for j in range(N):
        if array[i, j] == 0 and not vis[j]:
            vis[j] = True
            if p[j] == -1 or match_once(p[j], array, M, N, p, vis):
                p[j] = i
                return True
    return False


def match_zero(array):
    M = array.shape[0]
    N = array.shape[1]
    p = [-1] * N  # a list of hospital recording their matched doctors
    vis = [False] * N  # a list of hospital recoding whether they are visitied.
    for i in range(M):
        vis = [False] * N
        match_once(i, array, M, N, p, vis)
    return np.asarray(p)


def match(X):
    print('Match start:')
    print('the preprocessed array is : \n', X)
    ranking = X.copy()
    max_cap = X.shape[1]
    doc_num = len(ranking)
    if doc_num > max_cap:
        raise 'The doctor number cant overload the max capacity of the hospital'
    elif doc_num == max_cap:
        for i in range(doc_num):
            ranking[i] = ranking[i] - min(ranking[i])
        for i in range(ranking.shape[1]):
            ranking[:, i] = ranking[:, i] - min(ranking[:, i])
        # print(ranking)
        p = np.asarray(match_zero(ranking))
        while sum(p != -1) < doc_num:
            row_lines, col_lines = drawLines(ranking, p)
            smallest_entry = np.min(np.delete(np.delete(ranking, row_lines, axis=0), col_lines, axis=1))
            ranking -= smallest_entry
            ranking[row_lines] += smallest_entry
            ranking[:, col_lines] += smallest_entry
            p = np.asarray(match_zero(ranking))
    else:
        # Even if the capacity number is larger than doctor number, the algorithm basically runs the same,
        # only some coding problems such as line 69,71,75,77.
        for i in range(doc_num):
            ranking[i] = ranking[i] - min(ranking[i])
        # print(ranking)
        p = np.asarray(match_zero(ranking))
        while sum(p != -1) < doc_num:
            row_lines, col_lines = drawLines(ranking, p)
            cut_array = ranking
            if len(row_lines) > 0:
                cut_array = np.delete(cut_array, row_lines, axis=0)
            if len(col_lines) > 0:
                cut_array = np.delete(cut_array, col_lines, axis=1)
            smallest_entry = np.min(cut_array)
            ranking -= smallest_entry
            if len(row_lines) > 0:
                ranking[row_lines] += smallest_entry
            if len(col_lines) > 0:
                ranking[:, col_lines] += smallest_entry
            p = np.asarray(match_zero(ranking))
    result = [-1] * len(ranking)
    for i in range(len(p)):
        if p[i] != -1:
            result[p[i]] = i
    result = np.asarray(result).astype(np.int8)
    return result
