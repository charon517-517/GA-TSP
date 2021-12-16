import numpy as np

# 文件路径
file_path = './data.txt'


def read_data(fp):
    """
    :param fp: 文件路径
    :return: （城市数*3）的np array
    """
    data = np.loadtxt(fp)
    return data


class dataset:
    """

    """
    def __init__(self, data):
        x = []
        y = []
        for i in range(data.shape[0]):
            x.append(data[i][1])
            y.append(data[i][2])
        self.x_data = np.array(x)
        self.y_data = np.array(y)
        self.data = data

    def getx(self):
        return self.x_data

    def gety(self):
        return self.y_data

    def getData(self):
        return self.data