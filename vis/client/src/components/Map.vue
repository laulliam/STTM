<template>
  <div id="mapContainer"></div>
</template>

<script>
//Add a line to a map using a GeoJSON source
//https://docs.mapbox.com/mapbox-gl-js/example/geojson-line/ 
//set layers styles from FeatureCollection https://docs.mapbox.com/mapbox-gl-js/example/multiple-geometries/
//mapbox expression https://docs.mapbox.com/mapbox-gl-js/style-spec/expressions/#types
//Geojson https://www.rfc-editor.org/rfc/rfc7946#section-1.1
import mapboxgl from 'mapbox-gl';
import {MapTools} from './MapTools.js'
import {DataManager} from './DataManager.js'

export default {
  name: "BaseMap",
  data() {
    return {
      ACCESSTOKEN: 'pk.eyJ1Ijoid2VpeGluemhhbyIsImEiOiJja2ZucTB1c2cxb2c4MnJwamxiaXFpY2JxIn0.AZ2oSPWyf9fV0_RXXyMIFg',
      INITDATA: 0,
      TOPICMODEL_INFO: null,
      MAP_CONTAINER: null,
      MAP_INIT_CENTER: null
    };
  },
  beforeCreate(){
    let that = this
    DataManager.getTopicModelInfo().then((res) => {
      //['ID', 'lat', 'lng', 'passengers', 'timestamp']
      console.log(res)
      that.INITDATA = res.data.data.initdata
      that.TOPICMODEL_INFO = res.data.data
      that.MAP_INIT_CENTER = res.data.data.center
    }).catch((err) => {
      console.log(err)
    })

  },
  watch: {
    INITDATA(newVal, oldVal){
      //通过beforeCreate异步请求后台数据，当判断指标INITDATA获取到后台传递的信号后，调用地图初始化函数
      if(newVal == 1){
        console.log('async data')
        this.initMap()
      }
    }
  },
  mounted() {
  },
  methods:{
    initMap(){
      console.log('initMap')
      //Prepare data
      let that = this
      
      //InitMap
      mapboxgl.accessToken = this.ACCESSTOKEN;
      that.MAP_CONTAINER = new mapboxgl.Map({
        container: "mapContainer",
        style: "mapbox://styles/mapbox/dark-v11",
        center: that.MAP_INIT_CENTER,
        zoom: 10.2,
        projection: 'equirectangular'
      });

      this.MapTools = new MapTools(that.MAP_CONTAINER, that.TOPICMODEL_INFO)
      this.MapTools.color()
      //Add 
      //this.maptest()
      this.topicLines()
      this.AlltopicLines()
    },
    getTrajectoryFeatures(lng, lat){
      return {
        "type": 'Feature',
        "geometry": {
          "type": "LineString",
          "coordinates": this.mapdata.data.map((d) => {return [d[lng], d[lat]]})
        },
        "properties": {}
      }
    },
    getPointsFeatures(lng, lat){
      return {
        "type": 'Feature',
        "geometry": {
          "type": "MultiPoint",
          "coordinates": this.mapdata.data.map((d) => {return [d[lng], d[lat]]})
        },
        "properties": {}
      }
    },
    getMultiTrajectoryFeatures(coordinates, params){
      
        let res = {
          "type": 'Feature',
          "geometry": {
            "type": "MultiLineString",
            "coordinates": []
          },
          "properties": {}
        }
      },
    maptest(){
      let that = this,
          _lngIndex = 2, //lng index in array
          _LatIndex = 1, //lat index in array
          _isTra = 1, // 1:draw trajectory; 0:not draw trajectory
          _isPoints = 1 // 1:draw points; 0:not draw points
      
      let TraGeoJson = this.getTrajectoryFeatures(_lngIndex, _LatIndex),
        PoiGeoJson = this.getPointsFeatures(_lngIndex, _LatIndex)
      
      const nav = new mapboxgl.NavigationControl();
        that.MAP_CONTAINER.addControl(nav, "top-right");
      
      //Add navigator
      const geolocate = new mapboxgl.GeolocateControl({
          positionOptions: {
              enableHighAccuracy: true
          },
          trackUserLocation: true
      });
      that.MAP_CONTAINER.addControl(geolocate, "top-right")

      //Add Lines
      console.log({
        'type': 'geojson',
        'data': TraGeoJson
      })
      that.MapTools.addLines('test-trajectory-line', 'trajectory-line', TraGeoJson, {
          'line-color': '#000000'
      })


      that.MapTools.drawPoints('test-trajectory-points', 'trajectory-points', PoiGeoJson, {
          'circle-color': '#333333',
          'circle-opacity': 0.5,
          'circle-radius': 2
      })
    },
    topicLines(){
      let that = this,
        topicIdList = [...Array(10).keys()],
        //topicIdList = [0,1],
        timeId = 0,
        topn = 200,
        convertLatLng = 1
      
      DataManager.getTimesliceTopic(topicIdList, timeId, topn, convertLatLng).then(res => {
        let content = res.data.data
        console.log(content)
        let sliceTopic = content.data.map((d) => {
          return d.topic.map((v) => {
            return [v[3], v[4]] //lng lat
          })
        })
        let arrowSource = that.MapTools.getSTSource(sliceTopic, content.topicIdList)

        that.MapTools.addLines('topicLine', 'topicLine-layer', arrowSource, {
          'line-color': ['get', 'color'],
          'line-opacity': 0.5
        })

        // that.MapTools.deleteLines('topicLine', 'topicLine-layer')

        // that.MapTools.getSourceById('topicLine', (obj)=>{
        //   console.log(obj)
        // })

        // that.MapTools.getLayerById('topicLine-layer', (obj)=>{
        //   console.log(obj)
        // })
      })
    },
    
    AlltopicLines(){
      let that = this,
      convertLatLng = 1
      // DataManager.getOneDayTopic(convertLatLng).then(res => {
      //   console.log(res.data)
      // })

    }



  }
};
</script>

<style scoped>
#mapContainer {
    width: 1000px;
    height: 1000px;
    border: 2px black solid;
}
</style>
