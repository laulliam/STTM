from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from gensim.models.wrappers.dtmmodel import DtmModel
from gird import GirdID2LngLat

app = Flask(__name__)
CORS(app, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api


@app.route('/topic')
def index():
    time_slice_num = int(request.args.get("t")) | 0
    model_filepath = "../../model/chengdutaxi_process/"
    model_filename = 'model_20140803_full'
    ldaseq = DtmModel.load(os.path.join(model_filepath, model_filename))
    data = []
    for i in range(18):
        topic = ldaseq.show_topic(topicid=i, time=time_slice_num, topn=50)
        topic = [[part[0], part[1], GirdID2LngLat(part[1].split('-')[0]), GirdID2LngLat(part[1].split('-')[1]) ] for part in topic]
        data.append({"id":i,"data":topic})
    return jsonify(code=200, data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)