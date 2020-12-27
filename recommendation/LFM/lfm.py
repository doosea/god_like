import numpy as np
import sys

sys.path.append("./util")
from util.read import get_train_data, get_avg_score, get_item_deatial


def init_vec(vec_len):
    """
    初始化向量
    :param F:
    :return:
    """
    return np.random.randn(vec_len)


def model_predict(user_vec, item_vec):
    """
    user 对 item 的距离远近，喜爱程度
    :param user_vec:
    :param item_vec:
    :return:
    """
    return np.dot(user_vec, item_vec) / (np.linalg.norm(user_vec) * np.linalg.norm(item_vec))


def lfm_train(train_data, F, alpha, beta, step):
    """
    LFM 训练
    :param train_data: 训练样本
    :param F: user. item 向量维度，长度
    :param alpha: 正则化系数
    :param beta: 学习率
    :param step: 迭代次数
    :return: dict1 :
                key ：user_id
                value: vector
             dict2 :
                key ：movie_id
                value: vector
    """
    user_vec = {}
    item_vec = {}
    for step_index in range(step):
        # 初始化vec
        for data_instance in train_data:
            user_id, movie_id, label = data_instance
            if user_id not in user_vec:
                user_vec[user_id] = init_vec(F)
            if movie_id not in item_vec:
                item_vec[movie_id] = init_vec(F)

        # 梯度下降，求参数
        delta = label - model_predict(user_vec[user_id], item_vec[movie_id])
        for index in range(F):
            user_vec[user_id][index] += beta * (delta * item_vec[movie_id][index] - alpha * user_vec[user_id][index])
            item_vec[movie_id][index] += beta * (delta * user_vec[user_id][index] - alpha * item_vec[movie_id][index])
        beta = beta * 0.9

    return user_vec, item_vec


def model_train_process():
    """
    train LFM
    """
    train_data = get_train_data("../data/ratings.txt")
    user_vec, item_vec = lfm_train(train_data=train_data, F=50, alpha=0.01, beta=0.1, step=50)
    recom_list = give_recom_result(user_vec, item_vec, "1")
    analysis_recom_result(train_data, "1", recom_list)
    return


def give_recom_result(user_vec, item_vec, user_id):
    """
    给出userid 推荐结果
    :param user_vec: lfm result, user vec dict
    :param item_vec: lfm result, item vec dict
    :param user_id:
    :return: list = [(itemid, socre), (itemid, socre)]
    """
    if user_id not in user_vec:
        return []
    record = {}
    mix_num = 10
    recom_list = []
    user_vector = user_vec[user_id]
    for item_id in item_vec:
        item_vector = item_vec[item_id]
        pre = model_predict(user_vector, item_vector)
        record[item_id] = pre
    for zuhe in sorted(record.items(), key=lambda ele: ele[1], reverse=True)[:mix_num]:
        recom_list.append((zuhe[0], round(zuhe[1], 3)))
    return recom_list


def analysis_recom_result(train_data, user_id, recom_list):
    """
    分析推荐结果
    :param train_data:
    :param user_id:
    :param recom_list:
    :return:
    """
    item_info = get_item_deatial("../data/movies.txt")
    for data_instance in train_data:
        tmp_user_id, item_id, label = data_instance
        if label == 1 and tmp_user_id == user_id:
            print(item_info[item_id])
    print("*"*50)
    for zuhe in recom_list:
        print(item_info[zuhe[0]])


if __name__ == '__main__':
    res1 = init_vec(10)
    print(res1)

    model_train_process()
