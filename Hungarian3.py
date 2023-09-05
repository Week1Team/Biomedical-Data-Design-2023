import numpy as np
import random
import sys
# 代办:
# 把结果根据医院名单进行匹配
# 把并列排名设为其中最低权重，剩下的往后靠
ranking = np.array([[0, 1, 2, 3], [0, 1, 3, 2]])
capacity = np.array([1, 1])


def draw_col(array, i, rows, cols, p):
    row = array[i]
    new_cols = list(set(np.where(row == 0)[0]) - set(np.where(p == i)[0]) - set(cols))
    if len(new_cols) != 0:
        cols += new_cols
        for j in new_cols:
            draw_row(array, j, rows, cols, p)


def draw_row(array, j, rows, cols, p):
    new_row = p[j]
    if new_row != -1 and sum(rows == new_row) == 0:
        rows.append(p[j])
        draw_col(array, p[j], rows, cols, p)


def drawLines(ranking, p):
    X = ranking.copy()
    marked_rows = []
    marked_cols = []
    new_rows = list(set(range(len(X))) - set(p))
    marked_rows += new_rows
    for i in new_rows:
        draw_col(ranking, i, marked_rows, marked_cols, p)
    row_lines = np.asarray(list(set(range(len(X))) - set(marked_rows)))
    col_lines = np.asarray(marked_cols)
    return row_lines, col_lines


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


def broadcast(ranking, capacity):
    # 将ranking根据hospital的capacity进行扩增，使每个capacity占一列
    new_ranking = np.zeros((1, ranking.shape[0]))
    hospital_list = np.zeros((1, ))
    for i in range(ranking.shape[1]):
        new_ranking = np.vstack((new_ranking, np.tile(ranking[:, i], (capacity[i], 1))))
        hospital_list = np.hstack((hospital_list, np.tile((i+1), (capacity[i], ))))
    new_ranking = new_ranking[1:, ].T
    hospital_list = hospital_list[1:]
    # print('original ranking is \n', ranking)
    # print('hospital capacity is \n', capacity)
    # print('new array is \n', new_ranking)
    # print('hospital list is \n', hospital_list)
    # print('')
    return new_ranking, hospital_list


def na2maxWeight(input):
    # 将Na转化为最低的rank，从而处理医生不输入某些hosptal排名的情况
    for i in range(len(input)):
        input[i][np.isnan(input[i])] = max(input[i])
    #print('the nan-moved array is \n', input)
    return(input)


def comput_cost(result, new_ranking):
    # 计算平均的分配成本（总体成本最小）和成本的中位数（个人损失分布）
    cost = []
    for i in range(len(result)):
        cost.append(new_ranking[i, result[i]])
    ave_cost = sum(cost) / len(result)
    median_cost = np.median(cost)
    return ave_cost, median_cost


def test(test_num = 1e1, hospital_num_range = (4, 5), capacity_range = (1, 1), redundancy = True):
    # 产生大量随机数据
    # 通过调整参数范围，可以根据需要设置在不同情境下探究算法的好坏
    print('testing start:')
    fail = 0
    for i in range(int(test_num)):
        print('times: ', i)
        hospital_num = random.randint(hospital_num_range[0], hospital_num_range[1])
        capacity = [random.randint(capacity_range[0], capacity_range[1]) for _ in range(hospital_num)]
        capacity_num = sum(capacity)
        if redundancy:
            patient_num = random.randint(2, capacity_num - 1)
        else:
            patient_num = capacity_num
        generated_ranking = np.array([np.random.permutation(np.arange(1, hospital_num + 1)) for _ in range(patient_num)])

        new_ranking, hospital_list = broadcast(generated_ranking, capacity)
        result = match(new_ranking)
        print('the algorithm result is: \n', result)
        ave_cost, median_cost = comput_cost(result, new_ranking)

        generated_result = random.sample(range(sum(capacity)), len(generated_ranking))
        ctl_ave_cost, ctl_median_cost = comput_cost(generated_result, new_ranking)

        if ave_cost > ctl_ave_cost:
            fail += 1
            print('In', test_num, 'times sampling, the algorithm fail to random result in ', fail, 'times:')
            print('the original array is: \n', generated_ranking)
            print('the boadcasted array is: \n', new_ranking)
            print('the algorithm result is: \n', result)
            print('the random result is: \n', generated_result)


# new_ranking, hospital_list = broadcast(ranking, capacity)
# new_ranking = na2maxWeight(new_ranking)
# result = match(ranking)
# print('match result is', result)
# ave_cost, median_cost = comput_cost(result, ranking)
# print('the average loss is ', ave_cost)
# print('the median loss is ', median_cost)
test()
