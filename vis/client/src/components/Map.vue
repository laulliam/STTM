<template>
  <div id="mapContainer" ref="baseMap"></div>
</template>

<script>
//Add a line to a map using a GeoJSON source
//https://docs.mapbox.com/mapbox-gl-js/example/geojson-line/ 
//set layers styles from FeatureCollection https://docs.mapbox.com/mapbox-gl-js/example/multiple-geometries/
//mapbox expression https://docs.mapbox.com/mapbox-gl-js/style-spec/expressions/#types
//Geojson https://www.rfc-editor.org/rfc/rfc7946#section-1.1
import mapboxgl from 'mapbox-gl';
import axios from 'axios';
import * as d3 from 'd3'

export default {
  name: "BaseMap",
  data() {
    return {
      ACCESS_TOKEN: 'pk.eyJ1Ijoid2VpeGluemhhbyIsImEiOiJja2ZucTB1c2cxb2c4MnJwamxiaXFpY2JxIn0.AZ2oSPWyf9fV0_RXXyMIFg',
      MAP_CONTAINER: null,
      INITDATA: 0,
      topic_data: []
    };
  },
  beforeCreate() {
    axios.get('/api/topic', {
      params: {
        t: 6
      }
    }).then(res => {
      //console.log(res.data.data)
      this.topic_data = res.data.data
    }).catch((err) => {
      console.log(err)
    })

    // axios.all()
  },
  watch: {
  },
  mounted() {
    this.initMap()
    this.showTopic()
  },
  methods: {
    initMap() {
      console.log('Init Map')
      mapboxgl.accessToken = this.ACCESS_TOKEN;
      this.MAP_CONTAINER = new mapboxgl.Map({
        container: this.$refs.baseMap,
        style: "mapbox://styles/mapbox/dark-v9",
        center: [103.939665499999998, 30.6615715],
        zoom: 10,
        projection: 'equirectangular',
        // pitch: 50
      });

      // this.MAP_CONTAINER.on('click',(e)=>{
      //     console.log(e.lngLat);
      // })
    },

    showTopic() {
    
      this.MAP_CONTAINER.on('load', () => {

        console.log(this.topic_data)

        let points = [];
        // let colors = ['#5D22BD', '#CE009B', '#FF2D71', '#FF7B50', '#4cff3d']
        var colourSet = d3.scaleOrdinal(d3.schemePaired);
        var colorScale = d3.scaleOrdinal(d3.schemePRGn)
        // 设置一个线性比例尺将节点个数映射到[0,1]中
        let scale = d3.scaleLinear().domain([0, 17]).range([0,1])


        for(let i =0; i<18; i++){
          this.topic_data[i].data.forEach(d => {
          points.push({
            "type": "Feature",
            "properties": {
              // "color": colourSet(this.topic_data[i].id),
              "color": d3.interpolateTurbo(scale(this.topic_data[i].id)),
              "opacity": 0.8,
              "radius": 2
            },
            "geometry": {
              "type": "Point",
              "coordinates": [d[2][1], d[2][0]]
            }
          });
        });
        }

        this.MAP_CONTAINER.addSource("points_source", {
          "type": "geojson",
          'data': {
            "type": "FeatureCollection",
            "features": points
          }
        });
        this.MAP_CONTAINER.addLayer({
          'id': 'points_layer',
          'source': 'points_source',
          "type": "circle",
          'layout': {},
          'paint': {
            'circle-color': ['get', 'color'],
            'circle-opacity': ['get', 'opacity'],
            'circle-radius': ['get', 'radius']
          }
        });
      });
    }



  }
};
</script>

<style scoped>
#mapContainer {
  width: 100%;
  height: 100%;
}
</style>
