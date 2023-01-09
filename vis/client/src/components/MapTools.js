import * as d3 from 'd3'

// 根据sourceid和layerid增加source、layer，删除source和layer，
// 查找source和layer的方法。同时在Maptools的constructor里维护一个对象，专门存放已有的轨迹线

let MapTools = class {

  constructor(mapcon, topicmodelinfo) {
    this.con = mapcon
    this.TopicMoldeInfo = topicmodelinfo
    this.indexlinear = null
    this.colorDict = {}
    this.tracks = []
  }

  addLines(source_id, layer_id, data, paint, layout = {}) {
    this.con.on('load', ()=>{
      this.con.addSource(source_id, {
        'type': 'geojson',
        'data': data
      })

      this.con.addLayer({
        'id': layer_id,
        'type': 'line',
        'source': source_id,
        'paint': paint
      })
    })
  }

  deleteLines(source_id, layer_id) {
    this.con.on('load', ()=>{

      if (this.con.getLayer(layer_id)) {
        this.con.removeLayer(layer_id);
      }

      if(this.con.getSource(source_id)){
        this.con.removeSource(source_id)
      }

    })
  }

  getSourceById(source_id, callback){
    this.con.on('load', ()=>{
      callback(this.con.getSource(source_id))      
    })
  }

  getLayerById(layer_id, callback){
    this.con.on('load', ()=>{
      callback(this.con.getLayer(layer_id))
    })
  }

  drawPoints(source, layerid, data, paint) {
    console.log('drwaPoints')
    let that = this
    this.con.on('load', ()=>{
      that.con.addSource(source, {
        'type': 'geojson',
        'data': data
      })
      that.con.addLayer({
        'id': layerid,
        'type': 'circle',
        'source': source,
        'paint': paint
      })
    })
  }

  getArrowLine(sourceDestinationPairs) {

    sourceDestinationPairs = [
      [
        ["-122.4194", "37.7949"],
        ["-122.4794","37.7749"],
      ],
    ];

    function rotate(a, theta) {
      return [
        a[0] * Math.cos(theta) - a[1] * Math.sin(theta),
        a[0] * Math.sin(theta) + a[1] * Math.cos(theta),
      ];
    }

    function createArrow(a, b) {
      // a: source point
      // b: destination point
      var angle = Math.atan2(a[1] - b[1], a[0] - b[0]);
      var v = [b[0] - a[0], b[1] - a[1]]; // get direction vector
      var m = Math.sqrt(Math.pow(v[0], 2) + Math.pow(v[1], 2)); // module
      var u = [v[0] / m, v[1] / m]; // get unitary vector in the direction
      var k = 0; // how far to place the arrow end
      var newb = [b[0] - u[0] * k, b[1] - u[1] * k]; // place the arrow end a bit before the destination
      var s1 = rotate([0.01, 0.005], angle); // "sides" of the arrow. Applied to a base vector in left direction <--, and rotated to match the correct angle
      var s2 = rotate([0.01, -0.005], angle);
      return [
        a,
        newb,
        [newb[0] + s1[0], newb[1] + s1[1]],
        newb,
        [newb[0] + s2[0], newb[1] + s2[1]],
      ];
    }

    //...
    console.log(sourceDestinationPairs);
    var arrows = sourceDestinationPairs.map((x) => createArrow(x[0], x[1]));

    var style = {
      type: "line",
      layout: {
        "line-cap": "round",
      },
      paint: {
        "line-width": 2,
      }
    };

    var source = {
      type: "FeatureCollection",
      features: [
        {
          type: "Feature",
          geometry: {
            coordinates: arrows,
            type: "MultiLineString",
          },
        },
      ],
    };

    return { source, style };
  }

  getSTSource(data = arrows, idlist = null) {
    //getSliceTopicSource
    var source = {
      type: "FeatureCollection",
      features: []
    }
    
    data.forEach((element, ind) => {
      source.features.push({
        type: "Feature",
        geometry: {
          type: "MultiLineString",
          coordinates: element
        },
        properties: {
          id: idlist[ind],
          color: this.colorDict[ind]
        }
      })
    });
    return source
  }
  color(){
    this.indexlinear = d3.scaleLinear()
      .domain([d3.min(this.TopicMoldeInfo.topic_index_id), d3.max(this.TopicMoldeInfo.topic_index_id)])
      .range([0,1])
    this.TopicMoldeInfo.topic_index_id.forEach((d, i) => {
      this.colorDict[d] = d3.interpolateSinebow(this.indexlinear(d))
    })
    console.log(this.colorDict)
  }
  getcolor(index){
    return this.colorDict[index]
  }
}

let d3Tools = class{
  getRandomColor(lis){

  }
}



export { MapTools };

