# GeoJson summary
**组合原则：同层级不能放、低层级（多※）放置到高层级（少※），一般放到"data""geometry / geotries"**

※  
0 地基  

        base = {
            "type": "geojson",
            "data": data
        }

※※※  
1.1 单特征（可以放到0地基data中、1.2特征集合features中）  

        data = {
            "type": "Feature",
            "geometry": data,
            'properties': {}
        }

※※  
1.2 特征集合（可以放到0地基data中）  

        data = {
            "type": "FeatureCollection",
            "features": []
        }

※※※  
2.1 几何集合(可以放到1.2特征集合的features中)  

        data = {
            "type"： 'GeometryCollection',
            'geometries': data
        }

※※※※  
3.1 单实体(可以放到1.1单特征geometry、1.2特征集合的features中、2.1几何集合的geometries，也可以直接放到0地基中)  

        data = {
            "type"： 'Point' ('LineString', 'Polygon', 'GeometryCollection'),
            'coordinates': []
        }

※※※※  
3.2 多实体(可以放到1.2单特征、1.2特征集合的features、2.1几何集合的geometries，也可以直接放到0地基中)  

        data = {
            "type"： 'MultiPoint' ('MultiLineString', 'MultiPolygon'),
            'coordinates': []
        }

# Geometry Examples
A.1.  Points

   Point coordinates are in x, y order (easting, northing for projected
   coordinates, longitude, and latitude for geographic coordinates):

     {
         "type": "Point",
         "coordinates": [100.0, 0.0]
     }

A.2.  LineStrings

   Coordinates of LineString are an array of positions (see
   Section 3.1.1):

     {
         "type": "LineString",
         "coordinates": [
             [100.0, 0.0],
             [101.0, 1.0]
         ]
     }
A.3.  Polygons

   Coordinates of a Polygon are an array of linear ring (see
   Section 3.1.6) coordinate arrays.  The first element in the array
   represents the exterior ring.  Any subsequent elements represent
   interior rings (or holes).

   No holes:

     {
         "type": "Polygon",
         "coordinates": [
             [
                 [100.0, 0.0],
                 [101.0, 0.0],
                 [101.0, 1.0],
                 [100.0, 1.0],
                 [100.0, 0.0]
             ]
         ]
     }

   With holes:

     {
         "type": "Polygon",
         "coordinates": [
             [
                 [100.0, 0.0],
                 [101.0, 0.0],
                 [101.0, 1.0],
                 [100.0, 1.0],
                 [100.0, 0.0]
             ],
             [
                 [100.8, 0.8],
                 [100.8, 0.2],
                 [100.2, 0.2],
                 [100.2, 0.8],
                 [100.8, 0.8]
             ]
         ]
     }
A.4.  MultiPoints

   Coordinates of a MultiPoint are an array of positions:

     {
         "type": "MultiPoint",
         "coordinates": [
             [100.0, 0.0],
             [101.0, 1.0]
         ]
     }
A.5.  MultiLineStrings

   Coordinates of a MultiLineString are an array of LineString
   coordinate arrays:

     {
         "type": "MultiLineString",
         "coordinates": [
             [
                 [100.0, 0.0],
                 [101.0, 1.0]
             ],
             [
                 [102.0, 2.0],
                 [103.0, 3.0]
             ]
         ]
     }
A.6.  MultiPolygons

   Coordinates of a MultiPolygon are an array of Polygon coordinate
   arrays:

     {
         "type": "MultiPolygon",
         "coordinates": [
             [
                 [
                     [102.0, 2.0],
                     [103.0, 2.0],
                     [103.0, 3.0],
                     [102.0, 3.0],
                     [102.0, 2.0]
                 ]
             ],
             [
                 [
                     [100.0, 0.0],
                     [101.0, 0.0],
                     [101.0, 1.0],
                     [100.0, 1.0],
                     [100.0, 0.0]
                 ],
                 [
                     [100.2, 0.2],
                     [100.2, 0.8],
                     [100.8, 0.8],
                     [100.8, 0.2],
                     [100.2, 0.2]
                 ]
             ]
         ]
     }

A.7.  GeometryCollections

   Each element in the "geometries" array of a GeometryCollection is one
   of the Geometry objects described above:

     {
         "type": "GeometryCollection",
         "geometries": [{
             "type": "Point",
             "coordinates": [100.0, 0.0]
         }, {
             "type": "LineString",
             "coordinates": [
                 [101.0, 0.0],
                 [102.0, 1.0]
             ]
         }]
     }