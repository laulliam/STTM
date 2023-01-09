import axios from 'axios';
import qs from 'qs'

let DataManager = class {
    static exampleTrajectory (dataName) {
        let data = {
            'dataName': dataName
        }
        const params = new URLSearchParams();
        for(let key of Object.keys(data)){
            params.append(key, data[key])
        }
        return axios.post('/api/exampleTrajectory', params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
    }

    static getTopicEvolution (topicid, timeIdRangeStart, timeIdRangeEnd, topn, convertLatLng) {
        let data = {
            'topicid': topicid,
            'timeIdRangeStart': timeIdRangeStart,
            'timeIdRangeEnd': timeIdRangeEnd,
            'topn': topn,
            'convertLatLng': convertLatLng
        }

        const params = new URLSearchParams();
        for(let key of Object.keys(data)){
            params.append(key, data[key])
        }
        
        return axios.post('/api/topicEvolution', params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
    }

    static getTimesliceTopic (topicIdList, timeId, topn, convertLatLng) {
        let data = {
            'topicIdList': topicIdList,
            'timeId': timeId,
            'topn': topn,
            'convertLatLng': convertLatLng
        }

        const params = new URLSearchParams();
        for(let key of Object.keys(data)){
            params.append(key, data[key])
        }

        return axios.post('/api/timesliceTopic', params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
    }

    static getTopicModelInfo () {
        return axios.post('/api/getTopicModelInfo', {}, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
    }

    static getOneDayTopic () {
        let data = {
            'convertLatLng': convertLatLng
        }
        const params = new URLSearchParams();

        for(let key of Object.keys(data)){
            params.append(key, data[key])
        }
        return axios.post('/api/getOneDayTopic', params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
    }

}

export {DataManager}