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
import axios from 'axios';

export default {
  name: "BaseMap",
  data() {
    return {
      ACCESSTOKEN: 'pk.eyJ1Ijoid2VpeGluemhhbyIsImEiOiJja2ZucTB1c2cxb2c4MnJwamxiaXFpY2JxIn0.AZ2oSPWyf9fV0_RXXyMIFg',
      INITDATA: 0,
      mapdata:{},
      MAP_CONTAINER: null
    };
  },
  beforeCreate(){
    // let that = this
    // axios.get('http://localhost:3000/read-csv').then((res) => {
    //   // ['ID', 'lat', 'lng', 'passengers', 'timestamp']
    //   that.INITDATA = res.data.initdata
    //   that.mapdata = res.data
    //   // console.log(that.mapdata)
    // }).catch((err) => {
    //   console.log(err)
    // })
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
      let that = this

      //Prepare data
      let MAP_INIT_CENTER = [this.mapdata.data[0][2], this.mapdata.data[0][1]],
      _lngIndex = 2, //lng index in array
      _LatIndex = 1, //lat index in array
      _isTra = 1, // 1:draw trajectory; 0:not draw trajectory
      _isPoints = 1 // 1:draw points; 0:not draw points

      let TraGeoJson = this.getTrajectoryFeatures(_lngIndex, _LatIndex),
        PoiGeoJson = this.getPointsFeatures(_lngIndex, _LatIndex)
      console.log('GeoJson:', TraGeoJson)
      
      //InitMap
      mapboxgl.accessToken = this.ACCESSTOKEN;
      that.MAP_CONTAINER = new mapboxgl.Map({
        container: "mapContainer",
        style: "mapbox://styles/mapbox/streets-v11",
        center: MAP_INIT_CENTER,
        zoom: 10,
        projection: 'equirectangular'
      });
      const nav = new mapboxgl.NavigationControl();
      that.MAP_CONTAINER.addControl(nav, "top-right");

      //Add start point
      const marker = new mapboxgl.Marker()
          .setLngLat(MAP_INIT_CENTER)
          .addTo(that.MAP_CONTAINER);
      
      //Add navigator
      const geolocate = new mapboxgl.GeolocateControl({
          positionOptions: {
              enableHighAccuracy: true
          },
          trackUserLocation: true
      });
      that.MAP_CONTAINER.addControl(geolocate, "top-right")

      //Add Lines
      that.MAP_CONTAINER.on('load', ()=> {

        that.MAP_CONTAINER.addSource('test-trajectory-line', {
          'type': 'geojson',
          'data': TraGeoJson
        })
        that.MAP_CONTAINER.addSource('test-trajectory-points', {
          'type': 'geojson',
          'data': PoiGeoJson
        })

        that.MAP_CONTAINER.addLayer({
          'id': 'trajectory-line',
          'type': 'line',
          'source': 'test-trajectory-line',
          'paint': {
            'line-color': '#000000'
          }
        })

        that.MAP_CONTAINER.addLayer({
          'id': 'trajectory-points',
          'type': 'circle',
          'source': 'test-trajectory-points',
          'paint': {
            'circle-color': '#333333',
            'circle-opacity': 0.5,
            'circle-radius': 2
          }
        })
        
      })
      //Add 
    
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
      return traGeojson
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
    }
  }
};
</script>





<style scoped>
#mapContainer {
    width: 500px;
    height: 500px;
    border: 2px black solid;
}
</style>
