from dataset import dataset
import numpy as np
import math


def generateRandRoad(length):
    """
    随机生成若干条经过所有城市的路径
    :param length: 随机生成的路径长度
    :param num: 随机生成的路径条数
    :return: 路径numpy array, shape = (num,length)
    """
    road = np.zeros(length)
    road = np.arange(0, length, 1, dtype=np.int16)
    np.random.shuffle(road)
    return road


def calRoadLength(road, data):
    """
    :param road: 经过的路径
    :param data: 数据集
    :return: 该路径的总长度
    """
    x = np.zeros_like(data.getx())
    y = np.zeros_like(data.gety())
    for i in range(len(road)):
        x[i] = data.getx()[int(road[i])]
        y[i] = data.gety()[int(road[i])]
    xx = np.zeros_like(x)
    yy = np.zeros_like(y)
    xx[:-1] = x[1:]
    yy[:-1] = y[1:]
    dx = abs((x - xx)[:-1])
    dy = abs((y - yy)[:-1])
    dx = dx ** 2
    dy = dy ** 2
    back = math.sqrt((x[-1] - x[0]) ** 2 + (y[-1] - y[0]) ** 2)
    distance = sum(np.sqrt(dx + dy)) + back
    distance = round(distance, 2)
    return distance


class individual:
    """
    个体类，有路径、长度、适应度、被选择概率属性
    """

    def __init__(self, data):
        self.database = data.getData()
        self.road = generateRandRoad(len(self.database))  # 初始化个体，随机生成条路径
        self.total_dis = calRoadLength(self.road, data)  # 计算路径总长度
        self.pro_be_selected = 0  # 每个个体被选择的概率，在群体类中计算
        self.fitness = 0  # 个体的适应度，在群体类中计算

    def copy_individual(self, i):
        """
        为避免在交叉过程中父本个体DNA被改变，自定义的深复制函数
        :param i:
        :return:
        """
        self.database = self.database
        self.road = i.road.copy()
        self.total_dis = i.total_dis.copy()
        self.pro_be_selected = i.pro_be_selected.copy()
        self.fitness = i.fitness.copy()