import os


def get_graph_from_data(input_file):
    """
    从用户与item行为文件中，获取图结构
    :param input_file: user item rating file
    :return: dict:{
                UserA: {itema: 1, itemb: 1, itemd: 1},
                UserB: {itema: 1, itemc: 1},
                ...
                }
    """
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    score_thr = 4.0
    graph = {}
    with open(input_file, "r")as fr:
        for line in fr:
            if linenum == 0:
                linenum += 1
                continue
            item = line.split(",")
            if len(item) < 3:
                continue
            userid, itemid, rating = "user_" + item[0], "item_" + item[1], item[2]
            if float(rating) < score_thr:
                continue

            # 构造 user 与 item 的双边无向图
            if userid not in graph:
                graph[userid] = {}
            graph[userid][itemid] = 1
            if itemid not in graph:
                graph[itemid] = {}
            graph[itemid][userid] = 1

    return graph


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


if __name__ == '__main__':
    input_file = "../data/ratings.txt"
    res = get_graph_from_data(input_file)
    print(res)
