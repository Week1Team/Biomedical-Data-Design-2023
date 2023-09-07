import sys
import numpy as np
import random
from Process import *
from Match import *
# -This module provides metrics to evaluate the algorithm and a test function.

# -comput_cost function takes match result and the ranking array as input, and outputs the average loss and median loss

# -test function generates a lot of random ranking arrays and a random match result to each of the ranking array,
#       then see is there some situation the algorithm fails to the random result as a random control.
# -If the algorithm always find the optimal result, it should fail zero times in a huge random pool(test_num = 1e8/1e9).
# -Three parameters can be set to test the algorithm in different situation:
#       hospital_num, hospital_capacity, and redundancy.


def comput_cost(result, new_ranking):
    cost = []
    for i in range(len(result)):
        cost.append(new_ranking[i, result[i]])
    ave_cost = sum(cost) / len(result)
    median_cost = np.median(cost)
    return ave_cost, median_cost


def test(test_num = 1e1, hospital_num_range = (4, 5), capacity_range = (1, 1), redundancy = True):
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
