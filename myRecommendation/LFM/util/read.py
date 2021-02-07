import os


def get_item_deatial(input_file):
    """
     获得item详情
     :param input_file:  movies.txt 路径
     :return: dict :
                   key ： itemId
                   value : [title, genre]
    """
    item_info = {}
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    with open(input_file, "r") as fr:
        for line in fr:
            if linenum == 0:
                linenum += 1
                continue
            item = line.split(",")
            if len(item) < 3:
                continue
            elif len(item) == 3:
                item_id, title, genre = item[0], item[1], item[2]
            else:
                item_id = item[0]
                title = ",".join(item[1:-1])
                genre = item[-1]

            item_info[item_id] = [title, genre]
    return item_info


def get_avg_score(input_file):
    """
    获得item 平均得份
    :param input_file:  ratings.txt 路径
    :return: dict
            key: itemId
            value avg_score
    """
    score_dict = {}
    record_dict = {}
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    with open(input_file, "r") as fp:
        for line in fp:
            if linenum == 0:
                linenum += 1
                continue
            item = line.split(",")
            if len(item) < 4:
                continue
            user_id, movie_id, rating, timestamp = item[0], item[1], float(item[2]), item[3]
            if movie_id not in record_dict:
                record_dict[movie_id] = [0, 0]
            record_dict[movie_id][0] += 1
            record_dict[movie_id][1] += rating
    for movie_id in record_dict:
        score_dict[movie_id] = round(record_dict[movie_id][1] / record_dict[movie_id][0], 3)
    return score_dict


def get_train_data(input_file):
    """
    获得 LFM 的训练样本
    :param input_file:
    :return:
    """
    neg_dict = {}
    pos_dict = {}
    train_data = []
    score_thr = 4.0
    if not os.path.exists(input_file):
        print("文件不存在")
        return []
    score_dic = get_avg_score(input_file)
    linenum = 0
    with open(input_file, "r") as fp:
        for line in fp:
            if linenum == 0:
                linenum += 1
                continue
            item = line.split(",")
            if len(item) < 4:
                continue
            user_id, movie_id, rating, timestamp = item[0], item[1], float(item[2]), item[3]
            if user_id not in pos_dict:
                pos_dict[user_id] = []
            if user_id not in neg_dict:
                neg_dict[user_id] = []
            if rating >= score_thr:
                pos_dict[user_id].append((movie_id, 1))
            else:
                score = score_dic.get(movie_id, 0)
                neg_dict[user_id].append((movie_id, score))
    # 正负样本的均衡和负采样
    for user_id in pos_dict:
        num = min(len(pos_dict[user_id]), len(neg_dict[user_id]))
        # 如果正负样本个数都大于0
        if num > 0:
            train_data += [(user_id, zuhe[0], zuhe[1]) for zuhe in pos_dict[user_id]][:num]
        else:
            continue
        # user_id 所对应的负样本排序, 逆序排列，并取num个
        sorted_neg_list = sorted(neg_dict[user_id], key= lambda ele: ele[1], reverse=True)[:num]
        train_data += [(user_id, zuhe[0], 0) for zuhe in sorted_neg_list]
    return train_data

if __name__ == '__main__':
    input_path_movie = "../../data/movies.txt"
    input_path_rating = "../../data/ratings.txt"
    # res = get_item_deatial(input_path_movie)
    # print(len(res))
    # print(res['1'])
    # print(res['11'])
    #
    # res2 = get_avg_score(input_path_rating)
    # print(len(res2))


    res3 = get_train_data(input_path_rating)
    print(len(res3))