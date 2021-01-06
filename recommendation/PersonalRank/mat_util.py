from scipy.sparse import coo_matrix
from recommendation.PersonalRank.read import *
import numpy as np


def graph_to_mat(graph):
    """
    :return:
         matrix M,
         a list 所有(item+user)顶点,
         a dict 所有(item+user)顶点位置
    """
    vertex = list(graph.keys())
    address_dict = {}
    for index in range(len(vertex)):
        address_dict[vertex[index]] = index
    row = []
    col = []
    data = []
    for i in graph:
        weight = round(1 / len(graph[i]), 3)
        row_index = address_dict[i]
        for j in graph[i]:
            col_index = address_dict[j]
            row.append(row_index)
            col.append(col_index)
            data.append(weight)
    row = np.array(row)
    col = np.array(col)
    data = np.array(data)
    m = coo_matrix((data, (row, col)), shape=(len(vertex), len(vertex)))
    # print(m.todense())
    return m, vertex, address_dict


def mat_all_point(m_mat, vertex, alpha=0.6):
    """
    这里得到的是矩阵运算的（E-alpha*M^T）
    :param m_mat:
    :param vertex:
    :param alpha:
    :return:
    """
    total_len = len(vertex)
    row = np.array(list(range(total_len)))
    col = list(range(total_len))
    data = [1] * total_len
    row = np.array(row)
    col = np.array(col)
    data = np.array(data)
    eye_t = coo_matrix((data, (row, col)), shape=(total_len, total_len))
    # print(eye_t.todense())

    return eye_t.tocsr() - alpha * m_mat.tocsr().transpose()


if __name__ == '__main__':
    graph = get_graph_from_data("../data/log.txt")
    m, vertex, address_dict = graph_to_mat(graph)
    res = mat_all_point(m, vertex, alpha=0.6)
    print(res.todense())
