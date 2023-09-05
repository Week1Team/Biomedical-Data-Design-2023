import numpy as np
from Draw import *


def match_once(i, array, M, N, p, vis):
    for j in range(N):
        if array[i, j] == 0 and not vis[j]:
            vis[j] = True
            if p[j] == -1 or match_once(p[j], array, M, N, p, vis):
                p[j] = i
                return True
    return False


def match_zero(array):
    M = array.shape[0]  # M, N分别表示左、右侧集合的元素数量
    N = array.shape[1]
    p = [-1] * N  # 记录当前右侧元素所对应的左侧元素
    vis = [False] * N  # 记录右侧元素是否已被访问过
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
        raise('Overload')
    elif doc_num == max_cap:
        print('方形:')
        for i in range(doc_num):
            ranking[i] = ranking[i] - min(ranking[i])
        for i in range(ranking.shape[1]):
            ranking[:, i] = ranking[:, i] - min(ranking[:, i])
        print(ranking)
        p = np.asarray(match_zero(ranking))  # 医院被分配到医生的最大匹配可能
        while sum(p != -1) < doc_num:
            row_lines, col_lines = drawLines(ranking, p)
            smallest_entry = np.min(np.delete(np.delete(ranking, row_lines, axis=0), col_lines, axis=1))
            ranking -= smallest_entry
            ranking[row_lines] += smallest_entry
            ranking[:, col_lines] += smallest_entry
            p = np.asarray(match_zero(ranking))
    else:
        print('矩形:')
        for i in range(doc_num):
            ranking[i] = ranking[i] - min(ranking[i])
        print(ranking)
        p = np.asarray(match_zero(ranking))  # 医院被分配到医生的最大匹配可能
        while sum(p != -1) < doc_num:
            row_lines, col_lines = drawLines(ranking, p)
            cut_array = ranking
            if len(row_lines) > 0:  # 有可能没有横线导致[]无法取值
                cut_array = np.delete(cut_array, row_lines, axis=0)
            if len(col_lines) > 0:
                cut_array = np.delete(cut_array, col_lines, axis=1)
            smallest_entry = np.min(cut_array)
            ranking -= smallest_entry
            if len(row_lines) > 0:  # 有可能没有横线导致[]无法取值
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