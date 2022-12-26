from flask import Flask, request
import os
from gensim.models.wrappers.dtmmodel import DtmModel

app = Flask(__name__)

@app.route('/topic')
def index():
    topic_id = int(request.args.get("id"))
    time_slice_num = int(request.args.get("t"))
    model_filepath = "../../model/chengdutaxi_process/"
    model_filename = 'model_20140803_full'
    ldaseq = DtmModel.load(os.path.join(model_filepath, model_filename))
    topic = ldaseq.show_topic(topicid=topic_id, time=time_slice_num, topn=50)

    return topic

if __name__ == '__main__':
    app.run()