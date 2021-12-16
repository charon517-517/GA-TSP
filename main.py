import random
import numpy as np
import math
import matplotlib.pyplot as plt
from dataset import dataset
from population import population
from population import pop_num
from dataset import read_data
from dataset import file_path
import time


# 迭代次数
iter_num = 6000

if __name__ == '__main__':
    data = dataset(read_data(file_path))  # 生成数据集
    groups = population(data, pop_num)  # 初始化种群
    groups1 = population(data, pop_num)
    # 初始化迭代信息
    generation_best = []
    shortest_road = []
    best_road = []
    generation_best1 = []
    shortest_road1 = []
    best_road1 = []

    start = time.time()
    # 开始迭代
    for generation in range(iter_num):

        generation_best.append(groups.getBestIndividual().fitness)
        shortest_road.append(40000 - generation_best[generation])
        best_road.append(groups.getBestIndividual().road)

        generation_best1.append(groups1.getBestIndividual().fitness)
        shortest_road1.append(40000 - generation_best1[generation])
        best_road1.append(groups1.getBestIndividual().road)
        groups.evolute()
        groups1.evolute("simple")
    end = time.time()
    print(f"运行时间：{(end - start) / 60}min")
    # 结果可视化
    """axis = np.arange(iter_num).tolist()
    plt.figure(figsize=(10, 5), dpi=100)
    plt.plot(axis, shortest_road)
    plt.show()
    print(f"shortest_road = {shortest_road[-1]}")
    print(F"best_road = {best_road[-1]}")
    """
    fig, ax = plt.subplots()
    x = np.arange(iter_num).tolist()
    y1 = shortest_road
    y2 = shortest_road1
    ax.plot(x, y1, label='model = roulette')
    ax.plot(x, y2, label='model = simple')
    ax.set_xlabel('iter_num')
    ax.set_ylabel('shortest_road')
    ax.set_title('GA-TSP Two Models')
    ax.legend()
    plt.show()