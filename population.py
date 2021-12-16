import random
import numpy as np
from individual import individual
from individual import calRoadLength
from dataset import dataset
from dataset import read_data
from dataset import file_path

data = dataset(read_data(file_path))  # 生成数据集

# hyperparameters
pop_num = 400
select_rate = 0.4
cross_rate = 0.8
pumutation = 0.1


def cross_swap(list1, list2, start, end):
    """
    交换两个列表指定区域的片段
    """
    l = len(list1)
    cross1 = list1[start:end]
    cross2 = list2[start:end]
    list1[start:end] = cross2
    list2[start:end] = cross1


def duplicate(lis1, lis2, start, end):
    """
    将交叉生成的新DNA去重
    """
    to_process1 = lis1[:start] + lis1[end:]
    to_process2 = lis2[:start] + lis2[end:]
    to_com1 = lis1[start:end]
    to_com2 = lis2[start:end]
    for item in to_process1:
        while item in to_com1:
            rep_index = to_process1.index(item)
            get_index = to_com1.index(item)
            to_process1[rep_index] = to_com2[get_index]
            item = to_process1[rep_index]
    duplicated_list1 = to_process1[:start] + to_com1[:]
    duplicated_list1 = duplicated_list1[:] + to_process1[start:]

    for item in to_process2:
        while item in to_com2:
            rep_index = to_process2.index(item)
            get_index = to_com2.index(item)
            to_process2[rep_index] = to_com1[get_index]
            item = to_process2[rep_index]
    duplicated_list2 = to_process2[:start] + to_com2[:]
    duplicated_list2 = duplicated_list2[:] + to_process2[start:]
    return duplicated_list1, duplicated_list2


def cross_interchange(individual1, individual2):
    """
    交叉并去重
    :param individual1：待交叉个体1
    :param individual2: 待交叉个体2
    :return:
    """
    road1 = individual1.road.tolist()
    road2 = individual2.road.tolist()
    start = np.random.randint(0, int(len(road1) / 3))
    end = np.random.randint(int(2 * len(road1) / 3), len(road1))
    cross_swap(road1, road2, start, end)
    duplicated = duplicate(road1, road2, start, end)
    # lst_map0, lst_map1 = set(duplicated[0]), set(duplicated[1])
    # print(len(lst_map0) == len(duplicated[0]), len(lst_map1) == len(duplicated[1])) # 验证是否没有重复
    individual1.road = np.array(duplicated[0])
    individual2.road = np.array(duplicated[1])


def cross_over(selected_individual):
    """
    :param selected_individual:需要交叉的个体们
    :return:
    """
    for i in range(0, len(selected_individual), 2):
        if random.random() <= cross_rate:
            # 相邻两个个体完成交叉互换
            cross_interchange(selected_individual[i], selected_individual[i + 1])
            # 更新交叉后个体的适应度
            selected_individual[i].total_dis = calRoadLength(selected_individual[i].road, data)
            selected_individual[i + 1].total_dis = calRoadLength(selected_individual[i + 1].road, data)
            selected_individual[i].fitness = 40000 - selected_individual[i].total_dis
            selected_individual[i + 1].fitness = 40000 - selected_individual[i + 1].total_dis


def mutate(selected_individual):
    """
    变异操作
    :param selected_individual:
    :return:
    """
    for i in range(int(len(selected_individual))):
        if random.random() <= pumutation:
            rand1 = random.randint(0, len(selected_individual[i].road) - 1)
            rand2 = random.randint(0, len(selected_individual[i].road) - 1)
            while rand2 == rand1:
                rand2 = random.randint(0, len(selected_individual[i].road) - 1)
            temp = selected_individual[i].road[rand1]
            selected_individual[i].road[rand1] = selected_individual[i].road[rand2]
            selected_individual[i].road[rand2] = temp


class population:
    """
    种群类，有个体、种群数目属性，能够完成交叉、选择、变异、记录找到最优个体的功能
    """

    def __init__(self, data, num):
        """
        :param data:依据数据集生成一个种群
        :param num: 指定种群数目
        """
        self.groupNum = num
        self.indis = []
        # self.fitness = []
        for i in range(num):
            self.indis.append(individual(data))  # 随机生成个体
            self.indis[i].fitness = 40000 - self.indis[i].total_dis  # 计算个体的适应度

    def select(self, select_rate, model="roulette"):
        """
        默认轮盘赌模式：
        首先计算每个个体在种群中的占比
        然后制作轮盘
        最后依据选择概率选择个体
        :return:
        """
        selected_individual = []
        selected_index = []
        total_fitness = sum(i.fitness for i in self.indis)  # 计算所有个体总适应度
        for i in self.indis:  # 计算每个个体被选择的概率，存储至个体的pro_be_selected属性中
            i.pro_be_selected = i.fitness / total_fitness
        if model == "roulette":
            roulette = []  # 构造轮盘
            for i in range(self.groupNum):
                temp = 0
                for j in range(i + 1):
                    temp = temp + self.indis[j].pro_be_selected
                roulette.append(temp)
            selected_num = int(self.groupNum * select_rate)  # 选择的数量
            for i in range(selected_num):  # 选择指定数目的个体
                r = random.random()  # 随机生成0-1之间的小数
                for j in range(self.groupNum):  # 放入轮盘比较
                    if r < roulette[j]:  # 由于轮盘的数值是递增的，所以只要出现r < rolette[j]就代表落入了较大概率的那个个体的选择范围
                        temp_individual = individual(data)
                        temp_individual.copy_individual(self.indis[j])
                        selected_individual.append(temp_individual)
                        selected_index.append(j)
                        break
        elif model == "simple":
            selected_num = int(self.groupNum * select_rate)  # 选择的数量
            dis = []
            for indi in self.indis:
                dis.append(indi.fitness)
            sorted_index = np.array(dis).argsort().tolist()
            for j in range(selected_num):  # 选择指定数目的个体
                temp_individual = individual(data)
                temp_individual.copy_individual(self.indis[sorted_index[j]])
                selected_individual.append(temp_individual)
                selected_index.append(sorted_index[j])
        return selected_individual, selected_index

    def evolute(self, model="roulette"):
        """
        完成进化的操作。单次进化的具体步骤为：选择->交叉->变异->更新种群
        :return:
        """
        # 在当前种群的情况下选出优质个体，对其进行交叉互换、变异操作
        selected_individual, selected_index = self.select(select_rate, model)
        son_num = len(selected_individual)  # 子代数目
        cross_over(selected_individual)
        mutate(selected_individual)
        # 此时的selected_individual为完成繁殖后的子代个体，接下来需要完成种群的迭代
        # 返回种群中个体适应度由低到高排列的个体的序号
        fit = []
        for individual in self.indis:
            fit.append(individual.fitness)
        sorted_index = np.array(fit).argsort().tolist()
        # 用子代个体代替种群中适应度最差的等量个体
        for i in range(son_num):
            self.indis[sorted_index[i]] = selected_individual[i]

    def getBestIndividual(self):
        """
        找出当前种群最好的个体
        :return: 当前种群最好的个体
        """
        best_i = self.indis[0]
        for i in self.indis:
            if i.fitness > best_i.fitness:
                best_i = i
        return best_i