from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from gensim.models.wrappers.dtmmodel import DtmModel
from gird import GirdID2LngLat
from func import DTMTools
import pandas as pd
import numpy as np
import ast

app = Flask(__name__)
CORS(app, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api
MODEL_FILEPATH = "C:\\code\\topic modeling dtm\\src\\model\\"
MODEL_FILENAME = 'model-stayFalse20140803_sequence_full'
dtmtools = DTMTools(MODEL_FILEPATH + MODEL_FILENAME)

@app.route('/topic')
def index():
    #day_isfull
    time_slice_num = int(request.args.get("t")) | 0
    data = []
    for i in range(18):
        topic = dtmtools.model.show_topic(topicid=i, time=time_slice_num, topn=50)
        topic = [[part[0], part[1], GirdID2LngLat(part[1].split('-')[0]), GirdID2LngLat(part[1].split('-')[1]) ] for part in topic]
        data.append({"id":i,"data":topic})
    return jsonify(code=200, data=data)

# 获取主题状态 主题个数，时间区间等基本信息
@app.route('/getTopicModelInfo', methods=['POST'])
def getTopicModelInfo():
    resdata = dtmtools.getTopicModelInfo()
    resdata['initdata'] = 1
    resdata['center'] = [103.81669622691902, 30.75013445945946]
    return jsonify(code=200, data=resdata)

# 获取一天主题所有内容
@app.route('/getOneDayTopic', methods=['POST'])
def getOneDayTopic():
    convertLatLng = int(request.form['convertLatLng'])
    return jsonify(code=200, data=dtmtools.getOneDayTopic(convertLatLng))

# 主题演变 单个主题+多个时间
@app.route('/topicEvolution', methods=['POST'])
def topicEvolution():
    topicid = int(request.args.get("topicid"))
    timeIdRangeStart = int(request.args.get('timeIdRangeStart'))
    timeIdRangeEnd = int(request.args.get('timeIdRangeEnd'))
    topn = int(request.args.get("topn"))
    convertLatLng = int(request.args.get('convertLatLng'))

    return jsonify(code=200, data=dtmtools.topicEvolution(
        topicid = topicid,
        timeIdRangeStart = timeIdRangeStart,
        timeIdRangeEnd = timeIdRangeEnd,
        topn = topn,
        convertLatLng = convertLatLng
    ))

# 主题分布 多个主题+单个时间
@app.route('/timesliceTopic', methods=['POST'])
def timesliceTopic():
    topicIdList = ast.literal_eval(request.form["topicIdList"])
    timeId = int(request.form['timeId'])
    topn = int(request.form["topn"])
    convertLatLng = int(request.form['convertLatLng'])
    if type(topicIdList) == int:
        topicIdList = (topicIdList,)

    return jsonify(code=200, data=dtmtools.timesliceTopic(
        topicIdList = topicIdList,
        timeId = timeId,
        topn = topn,
        convertLatLng = convertLatLng
    ))

@app.route('/exampleTrajectory', methods=['POST'])
def exampleTrajectory():
    filepath = '../assets/driver1_trajectory.csv'
    data = pd.read_csv(filepath)
    LAT_BIAS, LNG_BIAS = +0.0025, -0.0025
    data['lat'], data['lng'] = data['lat'] + LAT_BIAS, data['lng'] + LNG_BIAS
    resdata = {
        'code': 200,
        'columns': data.columns.tolist(),
        'data': data.values.tolist(),
        'initdata': 1
    }
    return jsonify(resdata)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999)