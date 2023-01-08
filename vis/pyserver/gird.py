import math

# split gird
# 1经度111KM

def gird_by_span():
    #根据框个数划分
    column_num, row_num = 200, 200
    gird_lat_span = (LATMAX - LATMIN)/row_num
    gird_lng_span = (LNGMAX - LNGMIN)/column_num
    return gird_lat_span, gird_lng_span, column_num, row_num

def gird_by_distance(lng_dis = 0.5, lat_dis = 0.4):
    #根据距离划分
    #纬度跨度0.4km 经度跨度0.5km
    #经纬度距离估算https://blog.csdn.net/weixin_35301706/article/details/112527068

    gird_lat_span = 1 / (111 / lat_dis)
    gird_lng_span = 1 / ((111 * math.cos( (LATMAX + LATMIN) / 2)) / lng_dis)
    row_num = round((LATMAX - LATMIN) / gird_lat_span)
    column_num = round((LNGMAX - LNGMIN) / gird_lng_span)
    return gird_lat_span, gird_lng_span, column_num, row_num

LATMAX, LATMIN, LNGMAX, LNGMIN = 31.032468, 30.290675, 104.609693, 103.269638


# gird_lat_span, gird_lng_span, column_num, row_num = gird_by_span()
gird_lat_span, gird_lng_span, column_num, row_num = gird_by_distance()


def LngLat2GirdID(lat,lng):
    if lng < LNGMIN or lng > LNGMAX or lat < LATMIN or lat > LATMAX:
        return -1

    return int((lat-LATMIN)/gird_lat_span) + int((lng-LNGMIN)/gird_lng_span) * column_num 


def GirdID2LngLat(gird_id):
    if type(gird_id) != 'int':
        gird_id = int(gird_id)
    curr_row = int(gird_id/row_num)
    curr_column = gird_id % column_num

    return [LNGMIN + gird_lng_span * (curr_column + 0.5), LATMIN + gird_lat_span * (curr_row + 0.5 )]
    # return [LATMIN + gird_lat_span * (curr_row + 0.5 ), LNGMIN + gird_lng_span * (curr_column + 0.5)]

