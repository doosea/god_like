from recommendation.PersonalRank.read import *
from recommendation.PersonalRank import mat_util
from scipy.sparse.linalg import gmres
import numpy as np


def personal_rank(graph, root, alpha, item_num, recom_num=10):
    """
    Args:
        graph: user - item 的图结构字典
        root:  给哪个user 推荐
        alpha: 游走概率
        item_num: 迭代次数
        recom_num: 推荐个数

    :return: dict : {
                    key: itemid,
                    value: pr
                        }
    """
    rank = {}
    recom_res = {}
    # 初始化 r0, 长度 = len(user) + len(item)
    rank = {point: 0 for point in graph}
    rank["user_" + root] = 1
    for iter_index in range(item_num):
        tmp_rank = {}
        tmp_rank = {point: 0 for point in graph}
        for out_point, out_dict in graph.items():
            for inner_point, value in graph[out_point].items():
                tmp_rank[inner_point] += round(alpha * rank[out_point] / len(out_dict), 4)
                if inner_point == "user_" + root:
                    tmp_rank[inner_point] += round(1 - alpha, 4)
        if tmp_rank == rank:
            print(iter_index)
            break
        rank = tmp_rank

    right_num = 0
    for zuhe in sorted(rank.items(), key=lambda x: x[1], reverse=True):
        point, pr_score = zuhe[0], zuhe[1]
        if "user_" in point:
            continue
        if point in graph["user_" + root]:
            continue
        recom_res[point] = pr_score
        right_num += 1
        if right_num > recom_num:
            break
    return recom_res


def personal_rank_mat(graph, root, alpha, recom_num=10):
    """
    求解 r = (E-alpha*M^T)^-1 * (1-alpha)* r0
    AX=B : gmres(A, B, tol=1e-8)

        Args:
        graph: user - item 的图结构字典
        root:  给哪个user 推荐
        alpha: 游走概率
        recom_num: 推荐个数
    """
    m, vertex, address_dict = mat_util.graph_to_mat(graph)
    if root not in address_dict:
        return {}
    score_dict = {}
    recom_dict = {}
    A = mat_util.mat_all_point(m, vertex, alpha)
    index = address_dict[root]
    r0 = [0] * len(address_dict)
    r0[index] = 1
    r0 = np.array(r0)
    res = gmres(A, r0, tol=1e-8)[0]
    for index in range(len(res)):
        point = vertex[index]
        if "user_" in point:
            continue
        if point in graph[root]:
            continue
        score_dict[point] = round(res[index], 3)
    for zuhe in sorted(score_dict.items(), key=lambda x: x[1], reverse=True)[:recom_num]:
        point, score = zuhe[0], zuhe[1]
        recom_dict[point] = score
    return recom_dict


def get_one_user_recom():
    """

    :return:
    """
    user = '1'
    alpha = 0.7
    graph = get_graph_from_data("../data/ratings.txt")
    iter_num = 10
    res = personal_rank(graph, user, alpha, iter_num, 100)
    item_info = get_item_deatial("../data/movies.txt")
    for itemid in res:
        pure_itemid = itemid.split("_")[1]
        # print(item_info[pure_itemid])
        # print(res[itemid])
    return res


def get_one_recom_by_mat():
    user = 'user_1'
    alpha = 0.7
    graph = get_graph_from_data("../data/ratings.txt")
    res = personal_rank_mat(graph, user, alpha, 100)
    return res


if __name__ == '__main__':
    res1 = get_one_user_recom()
    res2 = get_one_recom_by_mat()
    print(res1)
    print(res2)

    num = 0
    for i in res1:
        if i in res2:
            num +=1
    print(num)
