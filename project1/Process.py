import sys

import numpy as np
# -This module provides several preprocess function.

# -broadcast function broadcasts the ranking array according to the capacity of each hospital,
#     so that each capacity is a single column.
# -The algorithm use this method to convert the question to a classical 1-to-1 matching Hungarian algorithm
# -broadcastBack function is used to convert the result in which each capacity is a single column,
#     back to a result in which each hospital is a single column, so we can understand the match result

# -na2maxWeight function convert na value to the equally lowest rank
# -This function is used when some docters don't give ranks to all hospital.


def broadcast(ranking, capacity):
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


def broadcastBack(result, hospital_list):
    new_result = []
    for i in result:
        new_result.append(int(hospital_list[i] - 1))
    return new_result


def na2maxWeight(input):
    for i in range(len(input)):
        if sum(np.isnan(input[i])) != 0:
            input[i][np.isnan(input[i])] = input.shape[i] - 1
    # print('the nan-moved array is \n', input)
    return input
