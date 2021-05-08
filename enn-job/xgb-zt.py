import datetime
import requests
import numpy as np
from phecda.exception import *
from sklearn.metrics import r2_score

TIME_SERIES_INPUT_LENGTH = 96  # 标识一天有多少个数据点
TRAIN_NUM = 25
VALIDATION_NUM = 1


def check_params(params_list, type_list):
    for para in params_list:
        match = False
        for tp in type_list:
            if isinstance(para, tp):
                match = True
                break
        if not match:
            raise Exception("invalid params %s" % para)


def gen_hour_list(begin, end, delta):
    ret = []
    t = begin
    while True:
        ret.append(t)
        t = t + datetime.timedelta(hours=1 / delta)
        if t > end:
            break
    return ret


def check_time_list_hourly(time_list):
    hour_list = gen_hour_list(time_list[0], time_list[-1], 4.0)

    lost_data = []
    i, j = 0, 0
    while True:
        if i >= len(hour_list):
            break
        if hour_list[i] < time_list[j]:
            print((i, j))
            lost_data.append(hour_list[i])
            i += 1
        else:
            i += 1
            j += 1
    # print("丢失数据",",".join(lost_data))
    if len(lost_data) > 0:
        raise DataException("负荷数据缺失" + ",".join(lost_data))


def get_output_length(predict_begin_datetime, predict_end_datetime):
    time_delta = predict_end_datetime - predict_begin_datetime
    seconds = time_delta.seconds + 3600 * 24 * time_delta.days
    return seconds // 900 + 1


SESS_LOAD = None


def left_mean(value_list):
    num = 0
    total = 0
    for value in value_list:
        if not np.isnan(value):
            total += value
            num += 1
    return total / num


def fill_value(value_list):
    if np.isnan(value_list[0]):
        value_list[0] = left_mean(value_list)
    for i in range(1, len(value_list)):
        if np.isnan(value_list[i]):
            value_list[i] = value_list[i - 1]


def get_load_data(proj_data_id, company_id, begin_datetime, end_datetime, env="prod"):
    url = "http://etsp-service-cust.fnwintranet.com/sequence/analysis/getPubOrPriData"
    if env == "dev":
        url = "http://etsp-service-cust.xianhuo.fnwrancher-dev.enncloud.cn/sequence/analysis/getPubOrPriData"
    end_datetime = end_datetime - datetime.timedelta(days=1)
    data = {"endTime": datetime.datetime.strftime(end_datetime, "%Y-%m-%d %H:%M:%S"),
            "projInsDataId": proj_data_id,
            "startTime": datetime.datetime.strftime(begin_datetime, "%Y-%m-%d %H:%M:%S"),
            "companyId": company_id}
    if begin_datetime < datetime.datetime(2019, 1, 1):
        raise AlgException("节假日数据缺失%s-%s" % (begin_datetime, end_datetime))
    global SESS_LOAD
    if SESS_LOAD is None:
        SESS_LOAD = requests.Session()
    r = SESS_LOAD.post(url, json=data, headers={"ticket": "123456"})
    result = r.json()
    if result["code"] != 200:
        raise DataException(result["msg"])
    if not result["data"]:
        raise DataException("requested data between %s and %s is None" % (begin_datetime, end_datetime))
    data = result["data"]["list"]
    time_list = [datetime.datetime.strptime(
        x['time'], "%Y-%m-%d %H:%M:%S") for x in data]
    check_time_list_hourly(time_list)
    value_list = [float(x['value']) if x['value'] is not None else np.nan for x in data]
    nan_number = 0
    for value in value_list:
        if np.isnan(value):
            nan_number += 1
    if nan_number / len(value_list) > 0.05:
        raise DataException("%s-%s期间，空值太多，共%s个空值" % (time_list[0], time_list[-1], nan_number))
    if nan_number > 0:
        fill_value(value_list)
    time_list = [time_list[i] for i in range(len(time_list)) if i % 4 == 0]
    value_list = [sum(value_list[i:i + 4]) for i in range(len(value_list)) if i % 4 == 0]
    return time_list, value_list


# 这些数据作为缓存，为了提高查询性能
DATABASE_HOLIDAY_BEGIN_DATE = datetime.date(2019, 1, 1)
DATE_LIST = None
HOLIDAY_DICT = None

SES = None


def get_holiday(end_date):
    """
    is_official_rest是否法定休息日        is_official_holidays是否法定节假日          is_consecutive_holidays是否连休节假日
    is_weekend_off是否一般周末休息日  is_legal_working是否法定工作日          is_ordinary_working是否普通工作日
    is_day_off是否调休工作日
    """
    keys = ["is_official_rest", 'is_official_holidays', 'is_ordinary_working',
            'is_legal_working', 'is_weekend_off', 'is_consecutive_holidays', 'is_day_off']

    global DATE_LIST
    global HOLIDAY_DICT
    start_date = DATABASE_HOLIDAY_BEGIN_DATE
    if DATE_LIST is not None and DATE_LIST[-1] >= end_date:

        # 从缓存里取数据
        date_list = DATE_LIST
        data_list = []
        for date in date_list:
            data_list.append(HOLIDAY_DICT[date])
        data_array = np.array(data_list)
        return date_list, keys, data_array

    global SES
    if SES is None:
        SES = requests.Session()
    if HOLIDAY_DICT is None:
        HOLIDAY_DICT = {}
    r = SES.post(
        "http://bigdata-platapi.test.fnwintranet.com/internal/bigdata/business/get",
        # "http://bigdata-api.test.fnwintranet.com/internal/bigdata/business/get",
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
        })

    #     print(start_date, end_date)
    #     print(r.content)
    data = r.json()

    date_list = []
    if data['msg'] == "ok" and data['retCode'] == 0:
        data_list = []
        # print(data["result"][0])
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

    return date_list, keys, data_array


def get_time_features(time_list):
    ret = []
    global HOLIDAY_DICT
    global DATE_LIST
    if HOLIDAY_DICT is None or DATE_LIST[-1] < time_list[-1].date():
        get_holiday(time_list[-1].date())
    for time in time_list:
        date = time.date()
        holiday = HOLIDAY_DICT[date]
        ret.append([time.weekday(), time.hour, time.month,
                    time.day] + holiday)
    return np.array(ret)


import xgboost as xgb


class XGBLoadPredictModel:
    def __init__(self, data_type, data_name, predict_begin_datetime, predict_end_datetime, time_gap_hours=0,
                 env="prod"):
        check_params([predict_begin_datetime, predict_end_datetime], [
            datetime.datetime, datetime.date])
        self.env = env
        self.input_length = TIME_SERIES_INPUT_LENGTH
        self.data_type = data_type
        self.data_name = data_name
        self.gap = time_gap_hours
        self.predict_begin_datetime = predict_begin_datetime
        self.predict_end_datetime = predict_end_datetime
        self.output_length = get_output_length(
            predict_begin_datetime, predict_end_datetime)
        if self.output_length > 7 * 96:
            raise ParamException("短期负荷预测至多7天")
        if self.gap > 7 * 96:
            raise ParamException("短期负荷预测至多间隔7天")
        self.train_data = self.get_train_data(
            self.data_type, self.data_name, self.predict_begin_datetime, predict_end_datetime, self.gap)
        self.models = []  # 预测第一个小时至最后一个小时，一共 output_length 个模型
        self.fit()
        self.predict_time_list = gen_hour_list(self.predict_begin_datetime, self.predict_end_datetime, 1.0)
        self.predict_time_list_quarter = gen_hour_list(self.predict_begin_datetime, self.predict_end_datetime, 4.0)
        self.predict_time_features = get_time_features(self.predict_time_list)
        return

    def prepare_train_data_X(self, model_index):
        """
        从 predict_data 提取 X
        """

        # input_begin_index 下标为 0，训练数据开始下标为 input_begin_index + gap + input_length
        # input_end_index 下标为 -1，结束下标为 input_end_index-output_length

        x_begin = self.gap + int(self.input_length/4) + model_index
        x_end = len(self.time_features) - self.output_length + model_index

        features = self.time_features[x_begin: x_end]
        for i in range(int(self.input_length/4)):
            t = i + self.gap + 1 + model_index
            f_new = self.train_data[x_begin - t:x_end - t]
            f_new = f_new[:, np.newaxis]
            features = np.hstack([features, f_new])
        return features

    def prepare_train_data_y(self, model_index):
        """
        从 predict_data 提取 y
        """

        features = self.time_features

        x_begin = self.gap + int(self.input_length/4) + model_index
        x_end = len(self.time_features) - self.output_length + model_index

        return self.train_data[x_begin:x_end]

    def fit(self):
        if self.output_length % 4 == 0:
            output_length = int(self.output_length / 4)
        else:
            output_length = self.output_length // 4 + 1
        for i in range(output_length):
            # print("第%s个模型"%i)
            X = self.prepare_train_data_X(i)
            y = self.prepare_train_data_y(i)
            regressor = xgb.XGBRegressor(n_jobs=2, nthread=2)
            y[np.isnan(y)] = np.mean(y[~np.isnan(y)])
            model = regressor.fit(X, y)
            self.models.append(model)

        return

    def predict(self):
        ret = []
        last_features = []
        if self.output_length % 4 == 0:
            output_length = int(self.output_length / 4)
        else:
            output_length = self.output_length // 4 + 1
        for j in range(int(self.input_length/4)):
            last_features.append(self.train_data[len(self.train_data) - 1 - j])
        for i in range(output_length):
            features = self.predict_time_features[i]
            features = list(features) + last_features
            # print("预测输入：", features)
            ret.append(self.models[i].predict(np.array(features).reshape(1, -1)))
        return ret

    def get_train_data(self, data_type, data_name, predict_begin_datetime, predict_end_datetime, predict_gap):

        input_begin_time = predict_begin_datetime - datetime.timedelta(hours=(self.get_begin_time_delta(
            TRAIN_NUM, TIME_SERIES_INPUT_LENGTH, self.output_length, predict_gap)) / 4)
        input_end_time = predict_begin_datetime - datetime.timedelta(hours=predict_gap/4)
        # print(("input_begin_time:", input_begin_time, "input_end_time:", input_end_time))
        time_list, data_list = get_load_data(
            data_type, data_name, input_begin_time, input_end_time, self.env)
        #         print(time_list,data_list)
        #         print(len(time_list), len(data_list))
        self.time_features = get_time_features(time_list)

        self.input_begin_time = input_begin_time
        self.input_end_time = input_end_time
        return np.array(data_list)

    def get_train_sample_num(self):
        """
        首先取决于模型容量；
        其次取决于训练/预测还是训练/验证/预测数据划分；
        """
        return (TRAIN_NUM + VALIDATION_NUM) * TIME_SERIES_INPUT_LENGTH

    def get_begin_time_delta(self, train_num, input_length, output_length, gap):
        """
        得到数据开始时间至第一个被预测时间的小时数量
        根据训练样本个数，样本输入输出长度，和输入输出gap来确定
        """
        return self.get_train_sample_num() + input_length + gap + output_length - 1 + gap


def get_result(proj_data_id, company_id, predict_begin_datetime, predict_end_datetime, gap_hours, env):
    model = XGBLoadPredictModel(proj_data_id, company_id, predict_begin_datetime, predict_end_datetime, gap_hours, env)
    validate_end = model.input_end_time
    validate_begin = validate_end - datetime.timedelta(hours=24-1/4)
    validate_model = XGBLoadPredictModel(proj_data_id, company_id, validate_begin, validate_end, gap_hours, env)
    tmp_result = model.predict()
    validate_result = validate_model.predict()
    # validate_real_data = get_load_data(proj_data_id, company_id, validate_begin, validate_end)[1]
    validate_real_data = model.train_data[-24:]
    r2 = r2_score(validate_real_data, validate_result)
    if (r2 <= 0):
        loss_rate = 1
    else:
        loss_rate = 1 - r2
    result = []
    for i in range(len(tmp_result)):
        res = [tmp_result[i][0]/4] * 4
        result += res
    ret = []
    for i in range(len(model.predict_time_list_quarter)):
        ret.append({"time": datetime.datetime.strftime(model.predict_time_list_quarter[i], "%Y-%m-%d %H:%M:%S"),
                    "value": float(result[i])})
    return ret, loss_rate


def call(*args, **kwargs):
    for p in ['param']:
        if p not in kwargs.keys():
            raise ParamException(
                'Missing required parameter in the JSON body: \'%s\'' % p)

    # print(kwargs)
    proj_data_id = kwargs['param'].get('proj_data_id')
    if not proj_data_id:
        raise ParamException(
            'Required parameter \'proj_data_id\' not found in \'param\'')

    company_id = kwargs['param'].get("company_id")
    if not company_id:
        raise ParamException(
            'Required parameter \'company_id\' not found in \'param\'')

    predict_begin_datetime = kwargs['param'].get("predict_begin_datetime")
    if not predict_begin_datetime:
        raise ParamException(
            'Required parameter \'predict_begin_datetime\' not found in \'param\'')

    predict_end_datetime = kwargs['param'].get("predict_end_datetime")
    if not predict_end_datetime:
        raise ParamException(
            'Required parameter \'predict_end_datetime\' not found in \'param\'')

    gap_hours = kwargs['param'].get("gap_hours")
    if not gap_hours:
        if gap_hours != 0:
            raise ParamException(
                'Required parameter \'gap_hours\' not found in \'param\'')
    gap_hours = 4 * gap_hours

    try:
        predict_begin_datetime = datetime.datetime.strptime(predict_begin_datetime, "%Y-%m-%d %H:%M:%S")
        predict_end_datetime = datetime.datetime.strptime(predict_end_datetime, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise ParamException(str(e))
    env = kwargs['param'].get("env")
    if not env:
        env = "prod"

    result = get_result(proj_data_id, company_id,
                        predict_begin_datetime, predict_end_datetime, gap_hours, env)

    return {"result": result[0], "loss_rate": result[1]}
