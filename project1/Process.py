import numpy as np


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
    # print('the nan-moved array is \n', input)
    return(input)