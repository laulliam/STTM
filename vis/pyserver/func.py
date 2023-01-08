import pandas as pd
import numpy as np
from gensim.models.wrappers.dtmmodel import DtmModel
from gird import GirdID2LngLat


class DTMTools:
    def __new__(cls, *args, **kwargs):
        print("1. Create a new instance of initDTMmodel.")
        return super().__new__(cls)

    def __init__(self, modelpath):
        print("2. Initialize the new instance of initDTMmodel.")
        self.modelpath = modelpath
        self.model = DtmModel.load(self.modelpath)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(modelpath={self.modelpath})"

    # 获取主题状态 主题个数，时间区间等基本信息
    def model(self):
        return self.model

    def getTopicModelInfo(self):
        dic = {
            'topic_number': self.model.num_topics,
            'topic_index_id': [i for i,v in enumerate(range(self.model.num_topics))],
            'time_rawdata_id': self.model.time_slices,
            'time_index_id': [i for i,v in enumerate(self.model.time_slices)],
            'time_range': [i+6 for i,v in enumerate(self.model.time_slices)],
            'corpus_features': self.model.num_terms,
            'corpus_len': self.model.lencorpus
        }
        return dic

    # 获取一天主题所有内容
    def getOneDayTopic(self, convertLatLng=0):
        _lentime = 18
        _lentopic = 18
        #topicid range (0, 18); time_slice range(0, 18) indicate-> (6, 24)
        # whole day
        dic = {'info': "one day topics with tree hierarchy like: '{hour-topic-entity}' ",
                    'data': {}}
        
        for i, item_time in enumerate(range(_lentime)):
            dic['data'].update({str(item_time): {}})
            for j, item_topic in enumerate(range(_lentopic)):
                topic = self.model.show_topic(topicid=item_topic, time=item_time, topn=10)
                concate = np.concatenate(
                        (np.array(topic), 
                            np.array([v.split('-') for v in np.array(np.array(topic))[:,1]])
                        ),
                    axis=1)
                concate = np.delete(concate, 1, axis=1).tolist()
                dic['data'][str(item_time)].update({item_topic: concate})

        if convertLatLng == 1:
            for i, time in enumerate(dic['data']):
                for j, topic in enumerate(dic['data'][time]):
                    for v, entity in enumerate(dic['data'][time][topic]):
                        entity[0] = float(entity[0])
                        entity[1] = int(entity[1])
                        entity[2] = int(entity[2])
                        entity.append(GirdID2LngLat(entity[1]))
                        entity.append(GirdID2LngLat(entity[2]))
        return dic

    # 主题演变 单个主题+多个时间
    def topicEvolution(self, topicid=1, timeIdRangeStart=0, timeIdRangeEnd=4, topn=10, convertLatLng=0):
        dic = {'info': "topic evolution", 
                'topicid': topicid,
                'timeIdRangeStart': timeIdRangeStart,
                'timeIdRangeEnd': timeIdRangeEnd,
                'topn': topn,
                'data': []}
        
        for i, time in enumerate(range(timeIdRangeStart, timeIdRangeEnd)):
            topic = self.model.show_topic(topicid=topicid, time=time, topn=topn)
            concate = np.concatenate(
                    (np.array(topic), 
                        np.array([v.split('-') for v in np.array(np.array(topic))[:,1]])
                    ),
                axis=1)
            concate = np.delete(concate, 1, axis=1).tolist()
            dic['data'].append({'time': time, 'topic': concate})

        if convertLatLng == 1:
            for i, collection in enumerate(dic['data']):
                for j, v in enumerate(collection['topic']):
                    v.append(GirdID2LngLat(int(v[1])))
                    v.append(GirdID2LngLat(int(v[2])))               
        return dic

    # 主题分布 多个主题+单个时间
    def timesliceTopic(self, topicIdList=[1,2,3], timeId=0, topn=10, convertLatLng=0):
        dic = {'info': "timeslice topics", 
                'topicIdList': topicIdList,
                'timeId': timeId,
                'topn': topn,
                'data': []}
        
        for i, topicnum in enumerate(topicIdList):
            topic = self.model.show_topic(topicid=topicnum, time=timeId, topn=topn)
            concate = np.concatenate(
                    (np.array(topic), 
                        np.array([v.split('-') for v in np.array(np.array(topic))[:,1]])
                    ),
                axis=1)
            concate = np.delete(concate, 1, axis=1).tolist()
            dic['data'].append({'timeId': timeId, 'topic': concate})

        if convertLatLng == 1:
            for i, collection in enumerate(dic['data']):
                for j, v in enumerate(collection['topic']):
                    v.append(GirdID2LngLat(int(v[1])))
                    v.append(GirdID2LngLat(int(v[2])))
        return dic