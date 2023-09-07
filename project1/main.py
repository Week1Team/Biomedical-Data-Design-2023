import numpy as np
import random
from Match import *
from Draw import *
from Process import *
from Test_utils import *
import sys


# Example data: a preference ranking and a capacity list of hospital
ranking = np.array([[0, 1, 2, 3], [0, 1, 2, 3], [1, 3, 0, 2], [0, 1, 2, 3], [0, 1, 2, 3]])
capacity = np.array([1, 1, 1, 2])


def match_doctors(ranking, capacity):
    print('the doctors ranking list is :\n', ranking)
    print('the capacity list is :\n', capacity)
    if len(capacity) != ranking.shape[1]:
        raise 'the hospital number in ranking list should be equal to the number in capacity list'

    # preprocess the data and perform the match algorithm:
    new_ranking, hospital_list = broadcast(ranking, capacity)
    # broadcast multi-capacity hospital to multi- hospital allow 1-to-1 match
    new_ranking = na2maxWeight(new_ranking)
    # convert the NAN value to the lowest rank
    result = match(new_ranking)
    # perform the match algorithm
    visual_result = broadcastBack(result, hospital_list)
    # broadcast the match result back to hospitals with multi-capacity
    print('match result is', visual_result)

    ave_cost, median_cost = comput_cost(result, new_ranking)
    # compute the average loss and the median loss of the match result
    print('the average loss is ', ave_cost)
    print('the median loss is ', median_cost)


match_doctors(ranking, capacity)


# test()
