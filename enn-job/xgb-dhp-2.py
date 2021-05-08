# -*- coding: utf-8 -*-
import datetime
import numpy as np
import requests
import xgboost as xgb
import pandas as pd
from phecda.exception import *
from phecda.log import logger
import time
from sklearn.metrics import r2_score

# 训练集天数
TRAIN_NUM = 25
# 验证集天数， 目前暂设为0
VALIDATION_NUM = 0
# 全局变量日期list和节假日信息list ，为了缓存部分重复数据， 防止训练集和预测时候的多次调用
DATE_LIST = None
HOLIDAY_DICT = None


def gen_hour_list(begin, end, data_type):
    ret = []
    t = begin
    if data_type == 24:
        t1 = 1
    elif data_type == 96:
        t1 = 1 / 4
    while True:
        ret.append(t)
        t = t + datetime.timedelta(hours=t1)
        if t > end:
            break
    return ret


def get_time_features(time_list):
    '''
        [time.weekday, time.hour, time.month, time.day,
        "is_official_rest", 'is_official_holidays', 'is_ordinary_working',
        'is_legal_working', 'is_weekend_off', 'is_consecutive_holidays', 'is_day_off']    一共11维度特征
    '''
    ret = []
    global HOLIDAY_DICT
    global DATE_LIST

    for time in time_list:
        date = time.date()
        holiday = HOLIDAY_DICT[date]
        ret.append([time.weekday(), time.hour, time.month, time.day] + holiday)
        # if date <= datetime.date(2020, 10, 6) and date >= datetime.date(2020, 10, 1):
        #     ret.append([time.weekday(), time.hour, time.month, time.day] + holiday + [1])
        # else:
        #     ret.append([time.weekday(), time.hour, time.month, time.day] + holiday + [0])
    return np.array(ret)


def get_holiday(start_date, end_date):
    """
    is_official_rest是否法定休息日        is_official_holidays是否法定节假日          is_consecutive_holidays是否连休节假日
    is_weekend_off是否一般周末休息日  is_legal_working是否法定工作日          is_ordinary_working是否普通工作日
    is_day_off是否调休工作日
    """
    global DATE_LIST
    global HOLIDAY_DICT
    keys = ["is_official_rest", 'is_official_holidays', 'is_ordinary_working',
            'is_legal_working', 'is_weekend_off', 'is_consecutive_holidays', 'is_day_off']

    if HOLIDAY_DICT is None:
        HOLIDAY_DICT = {}
    r = requests.post(
        # url="http://bigdata-platapi.test.fnwintranet.com/internal/bigdata/business/get",
        url="http://bigdata-platapi.fnwintranet.com/internal/bigdata/business/get",
        json={
            "params": [{
                "datacodeParam": [{
                    "datacode": "COMP_hour_dateInfoByType",
                    "params": {
                        "startDate": datetime.datetime.strftime(start_date, "%Y-%m-%d"),
                        "endDate": datetime.datetime.strftime(end_date, "%Y-%m-%d"),
                        "values": "date,is_official_rest,is_official_holidays,is_consecutive_holidays,is_weekend_off,is_legal_working,is_ordinary_working,is_day_off"
                    }
                }]
            }]
        },
        timeout=5)
    data = r.json()
    date_list = []
    if data['msg'] == "ok" and data['retCode'] == 0:
        data_list = []
        date_info = data["result"][0]["data"][0]["data"]
        for i in range(len(date_info)):
            now_date = datetime.datetime.strptime(date_info[i]["date"], "%Y-%m-%d").date()
            date_list.append(now_date)
            tmp = []
            for k in keys:
                tmp.append(date_info[i][k])
            data_list.append(tmp)
            if now_date not in HOLIDAY_DICT:
                HOLIDAY_DICT[now_date] = tmp
    data_array = np.array(data_list)
    DATE_LIST = date_list
    assert (data_array.ndim == 2)
    assert (len(date_list) == data_array.shape[0])


class XGBLoadPredictModel:
    def __init__(self, data_type, history_begin_datetime, history_end_datetime,
                 predict_begin_datetime, predict_end_datetime, history_data):
        self.data_type = data_type
        self.history_begin_datetime = history_begin_datetime
        self.history_end_datetime = history_end_datetime
        self.predict_begin_datetime = predict_begin_datetime
        self.predict_end_datetime = predict_end_datetime

        self.gap = get_datetime_gaps(history_end_datetime, predict_begin_datetime, data_type)
        self.input_length = data_type
        self.output_length = get_output_length(predict_begin_datetime, predict_end_datetime, data_type)
        t3 = time.time()
        self.data = self.data_process(history_data)
        t4 = time.time()
        logger.info("数据处理耗时：{}".format(t4 - t3))

        # 预测时间和预测间隔的校验
        if self.output_length > 7 * data_type:
            raise ParamException("短期负荷预测至多7天")
        if self.gap > 7 * data_type:
            raise ParamException("短期负荷预测至多间隔7天")
        self.input_begin_time = predict_begin_datetime - datetime.timedelta(hours=self.get_begin_time_delta())
        self.input_end_time = predict_begin_datetime - datetime.timedelta(hours=self.get_end_time_delta())
        self.train_data = self.get_train_data()
        self.models = []
        self.r2_score_in_valid = []
        t5 = time.time()
        self.fit()
        t6 = time.time()

        logger.info("数据训练耗时：{}".format(t6 - t5))
        self.predict_time_list = gen_hour_list(self.predict_begin_datetime, self.predict_end_datetime, self.data_type)
        self.predict_time_features = get_time_features(self.predict_time_list)

    def get_begin_time_delta(self):
        train_sample_num = (TRAIN_NUM + VALIDATION_NUM) * self.data_type
        if self.data_type == 24:
            return train_sample_num + self.input_length + self.gap
        elif self.data_type == 96:
            return (train_sample_num + self.input_length + self.gap) / 4

    def get_end_time_delta(self):
        if self.data_type == 24:
            return self.gap
        elif self.data_type == 96:
            return self.gap // 4

    def get_train_data(self):
        # 这里即使历史数据数据很少，少于规定的25天，也不会报错
        time_list = self.data[self.input_begin_time: self.input_end_time]["datetime"].to_list()
        data_list = self.data[self.input_begin_time: self.input_end_time]["value"].to_list()
        self.time_features = get_time_features(time_list)

        return np.array(data_list)

    def data_process(self, history_data):
        # 这里先生成全局的时间特征字典， 后面训练集和测试集直接查全局字典
        try:
            get_holiday(self.history_begin_datetime, self.predict_end_datetime)
        except Exception as e:
            logger.error("call bigData api : get holidayInfo error:{}".format(e))
        date_list = gen_hour_list(self.history_begin_datetime, self.history_end_datetime, self.data_type)
        value = np.array(history_data).reshape(-1, 1)
        if len(date_list) != len(value):
            raise Exception("date length and data length are inconsistent")
        df = pd.DataFrame(data=value, index=date_list, columns=["value"])
        # 填空值
        df = df.fillna(method="ffill")
        df["datetime"] = pd.to_datetime(df.index)
        return df

    def fit(self):
        '''
            一共output_length 个模型
            对于下标为model_index的每一个样本：
                （1）起始样本下标: 输入长度 + 间隔gap + index
                     x_begin = input_length + gap + model_index
                （2）最后一个样本下标： 所有训练数据长度-输出长度 + index
                     x_end = len(time_features) - output_length + model_index
                (3) 每个simple = [当前时间点的time_features + 当前时间点往前推（gap+input_length, gap）的时间点的label] + [label = 当前时间点的label]
                    如： input_length = 24
                        gap = 48
                        output_length = 72
                        所有的label值按照[1,2,3,..24,|25,26...48,|49,50,...72,|73,74,...96.....]
                    simple1:
                        X: 第73个点的+timefeatures + 1-24 点的labels(具体实现中，24个倒序排列)
                        Y：第73个点的[label]
                    simple2:
                        X: 第74个点的+timefeatures + 2-25 点的labels
                        Y：第74个点的[label]
        '''

        for i in range(self.output_length):
            # print("第%s个模型" % i)
            # logger.info("第{}个模型".format(i))
            X = self.prepare_train_data_X(i)
            if i == self.output_length - 1:
                X_next = self.prepare_train_data_X(i)
                y_next = self.prepare_train_data_y(i)
            else:
                X_next = self.prepare_train_data_X(i + 1)
                y_next = self.prepare_train_data_y(i + 1)
            y = self.prepare_train_data_y(i)
            # regressor = xgb.XGBRegressor()
            regressor = xgb.XGBRegressor(max_depth=5, n_estimators=100, n_jobs=2, nthread=2)
            # print(regressor)
            y[np.isnan(y)] = np.mean(y[~np.isnan(y)])
            model = regressor.fit(X, y)
            # print("feature importance", model.feature_importances_)
            # print("训练集上表现：", model.predict(X))
            # print("训练集上表现：", r2_score(y_true=y, y_pred=model.predict(X)))
            # print("交叉验证集上表现：", r2_score(y_true=y_next, y_pred=model.predict(X_next)))
            self.r2_score_in_valid.append(r2_score(y_true=y_next, y_pred=model.predict(X_next)))
            self.models.append(model)

    def prepare_train_data_X(self, model_index):
        x_begin = self.gap + self.input_length + model_index
        x_end = len(self.time_features) - self.output_length + model_index

        features = self.time_features[x_begin: x_end]
        for i in range(self.input_length):
            t = i + self.gap + 1 + model_index
            f_new = self.train_data[x_begin - t:x_end - t]
            f_new = f_new[:, np.newaxis]
            features = np.hstack([features, f_new])
        return features

    def prepare_train_data_y(self, model_index):
        x_begin = self.gap + self.input_length + model_index
        x_end = len(self.time_features) - self.output_length + model_index
        return self.train_data[x_begin:x_end]

    # todo: 这里一直用的是最新的数据，而不是滑窗方式
    def predict(self):
        ret = []
        last_features = []
        for j in range(self.input_length):
            # 构造输入特征的倒序排列
            last_features.append(self.train_data[len(self.train_data) - 1 - j])
        for i in range(self.output_length):
            features = self.predict_time_features[i]
            features = list(features) + last_features
            # print("预测输入：", features)
            ret.append(self.models[i].predict(np.array(features).reshape(1, -1))[0])

        return ret

    def get_validate_r2_socre(self):
        pass


def get_result(data_type, history_begin_datetime, history_end_datetime,
               predict_begin_datetime, predict_end_datetime, history_data):
    model = XGBLoadPredictModel(data_type, history_begin_datetime, history_end_datetime,
                                predict_begin_datetime, predict_end_datetime, history_data)
    result = model.predict()
    r2 = np.average(model.r2_score_in_valid)
    ret = []
    for i in range(len(result)):
        ret.append({"time": datetime.datetime.strftime(model.predict_time_list[i], "%Y-%m-%d %H:%M:%S"),
                    "value": float(result[i])})
    df = pd.DataFrame(data=ret)
    df.to_csv("pre.csv")
    return np.array(result).reshape(-1, data_type).tolist(), r2


def get_datetime_gaps(start, end, data_type):
    time_delta = end - start
    seconds = time_delta.seconds + 3600 * 24 * time_delta.days
    if data_type == 24:
        if seconds % 3600 != 0:
            raise ParamException(
                "the interval between  history_date_end and predict_date_start must be an integer multiple of 1 hours")
        return seconds // 3600 - 1
    elif data_type == 96:
        if seconds % 900 != 0:
            raise ParamException(
                "the interval between  history_date_end and predict_date_start must be an integer multiple of 1/4 hours ")
        else:
            return seconds // 900 - 1


def get_output_length(predict_begin_datetime, predict_end_datetime, data_type):
    time_delta = predict_end_datetime - predict_begin_datetime
    seconds = time_delta.seconds + 3600 * 24 * time_delta.days
    if data_type == 24:
        if seconds % 3600 != 0:
            raise ParamException(
                "the interval between  predict_begin_datetime and predict_end_datetime must be an integer multiple of 1 hours")
        return seconds // 3600 + 1
    elif data_type == 96:
        if seconds % 900 != 0:
            raise ParamException(
                "the interval between  predict_begin_datetime and predict_end_datetime must be an integer multiple of 1/4 hours ")
        else:
            return seconds // 900 + 1


def call(*args, **kwargs):
    # 参数校验
    if "param" not in kwargs:
        raise ParamException("Missing required parameter in the JSON body: param")

    # 参数解析
    data_type = kwargs['param'].get("data_type")
    if not data_type:
        raise ParamException('Required parameter \'data_type\' not found in \'param\'')
    if data_type != 24 and data_type != 96:
        raise ParamException("Input parameter 'data_type' must be 24 or 96")

    history_begin_datetime = kwargs['param'].get("history_begin_datetime")
    if not history_begin_datetime:
        raise ParamException('Required parameter \'history_begin_datetime\' not found in \'param\'')

    history_end_datetime = kwargs['param'].get("history_end_datetime")
    if not history_end_datetime:
        raise ParamException('Required parameter \'history_end_datetime\' not found in \'param\'')

    predict_begin_datetime = kwargs['param'].get("predict_begin_datetime")
    if not predict_begin_datetime:
        raise ParamException('Required parameter \'predict_begin_datetime\' not found in \'param\'')

    predict_end_datetime = kwargs['param'].get("predict_end_datetime")
    if not predict_end_datetime:
        raise ParamException('Required parameter \'predict_end_datetime\' not found in \'param\'')

    history_data = kwargs['param'].get("history_data")
    if not history_data:
        raise ParamException('Required parameter \'predict_end_datetime\' not found in \'param\'')

    try:
        if data_type == 24:
            history_begin_datetime += " 00:00:00"
            history_end_datetime += " 23:00:00"
            predict_begin_datetime += " 00:00:00"
            predict_end_datetime += " 23:00:00"
        elif data_type == 96:
            history_begin_datetime += " 00:00:00"
            history_end_datetime += " 23:45:00"
            predict_begin_datetime += " 00:00:00"
            predict_end_datetime += " 23:45:00"
        history_begin_datetime = datetime.datetime.strptime(history_begin_datetime, "%Y-%m-%d %H:%M:%S")
        history_end_datetime = datetime.datetime.strptime(history_end_datetime, "%Y-%m-%d %H:%M:%S")
        predict_begin_datetime = datetime.datetime.strptime(predict_begin_datetime, "%Y-%m-%d %H:%M:%S")
        predict_end_datetime = datetime.datetime.strptime(predict_end_datetime, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        raise ParamException(str(e))

    result, r2 = get_result(data_type, history_begin_datetime, history_end_datetime, predict_begin_datetime,
                        predict_end_datetime, history_data)
    return {"result": result, "loss_rate": min(1.0, 1-r2)}


import random

if __name__ == '__main__':
    dp = 24
    a = []
    # a = np.array(range(dp * 31)).reshape(-1, dp)
    for i in range(dp*31):
        aa = random.randint(1, 100)
        a.append(aa)

    print(a)
    param = {
        "data_type": dp,
        "history_begin_datetime": "2020-8-1",
        "history_end_datetime": "2020-8-31",
        "predict_begin_datetime": "2020-9-3",
        "predict_end_datetime": "2020-9-3",
        "history_data": a
    }
    res = call(param=param)
    print(res)

# 与之前做比对
# if __name__ == '__main__':
#     df = pd.read_csv("./用户4_origin_data.csv")
#     data = df["value"].tolist()
#     param = {
#         "data_type": 24,
#         "history_begin_datetime": "2020-6-1",
#         "history_end_datetime": "2020-8-10",
#         "predict_begin_datetime": "2020-8-11",
#         "predict_end_datetime": "2020-8-17",
#         "history_data": data
#     }
#     res = call(param=param)
#     print(res)
