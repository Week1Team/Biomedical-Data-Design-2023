import numpy as np
import random
from Match import *
from Draw import *
from Process import *
from Test import *
import sys
# 代办:
# 把结果根据医院名单进行匹配
# 把并列排名设为其中最低权重，剩下的往后靠
# 抽象
ranking = np.array([[0, 1, 2, 3], [0, 1, 3, 2]])
capacity = np.array([1, 1])





# new_ranking, hospital_list = broadcast(ranking, capacity)
# new_ranking = na2maxWeight(new_ranking)
# result = match(ranking)
# print('match result is', result)
# ave_cost, median_cost = comput_cost(result, ranking)
# print('the average loss is ', ave_cost)
# print('the median loss is ', median_cost)
test()
