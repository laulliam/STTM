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
        return axios.post('http://localhost:5000/exampleTrajectory', params, {
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
        
        return axios.post('http://localhost:5000/topicEvolution', params, {
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

        return axios.post('http://localhost:5000/timesliceTopic', params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
    }

    static getTopicModelInfo () {
        return axios.post('http://localhost:5000/getTopicModelInfo', {}, {
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
        return axios.post('http://localhost:5000/getOneDayTopic', params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
    }

}

export {DataManager}