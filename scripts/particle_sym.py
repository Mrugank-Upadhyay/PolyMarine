from operator import itemgetter
import time
import math
import random
import numpy as np
import datetime
from osgeo import ogr, osr

def getCoordConverter(src='', targ=''):
    srcproj = osr.SpatialReference()
    srcproj.ImportFromEPSG(src)
    targproj = osr.SpatialReference()
    if isinstance(targ, str):
        targproj.ImportFromProj4(targ)
    else:
        targproj.ImportFromEPSG(targ)
    transform = osr.CoordinateTransformation(srcproj, targproj)

    def convertCoords(xy):
        pt = ogr.Geometry(ogr.wkbPoint)
        pt.AddPoint(xy[0], xy[1])
        pt.Transform(transform)
        return  [pt.GetX(), pt.GetY()]

    return convertCoords

latlongToAlbers = getCoordConverter(4326,5070)
albersToLatlong = getCoordConverter(5070,4326)

start_date = datetime.datetime(1992,1,1)
end_date = datetime.datetime(2017,12,31)

current_date = start_date
increment = datetime.timedelta(minutes=15)

sample_point = (-41.8822705,28.4248646) # (Long, Lat)
travel_path = [sample_point]


def get_neighbors(vector_field, x, y):
    neighbors = []
    for i in range(-1,2):
        for j in range(-1,2):
            neighbors.append(vector_field[y + j, x + i])
    return list(filter(lambda x: not np.isnan(x[0]), neighbors)) 

def map_range(input_start,input_end,output_start,output_end,val):   
    slope = (output_end - output_start) / (input_end - input_start)
    return output_start + slope * (val - input_start)


def move_point(latlong, distance):
    #print(f"Lat Long Before: {latlong}")
    point = latlongToAlbers(latlong)
    #print(f"Point: {point}")
    #print(f"Distance: {distance}")
    point[0] += distance[0] * 900
    point[1] += distance[1] * 900
    #print(f"Transformed Point: {point}")
    return albersToLatlong(point)

def latlongToIndex(latlong):
    print(f"LatLong: {latlong}")
    return [
        math.floor(map_range(90,-90,0,360,latlong[1])),
        math.floor(map_range(-180,180,0,720, latlong[0])),
    ]




while current_date < end_date:
#    while line != "":
#        line = sea_file.readline()
#        point_data =  line.split(',')
#        try:       
#            print(type(point_data))
#            print(type(point_data[1]))
#            print(datetime.datetime.strptime(point_data[1][1],"%Y-%m-%d"))
#           # sorted(point_data, key=lambda e: datetime.datetime.strptime(e[1], "%Y-%m-%d"))
#        except Exception:
#            print("sorting didn't work")
#        print(point_data)
#        line = ""
    bin_file = f"ecco_{str(current_date.year).zfill(4)}-{str(current_date.month).zfill(2)}_000.npy"
    curr_vector_field = np.load(f"../images/{bin_file}")
    [y,x] = latlongToIndex(sample_point)
   # print(f"Index: {[y,x]}")
   # print(f"Possible Index: {curr_vector_field[y,x]}")
   # print(f"Possible Index: {curr_vector_field[x,y]}")
   # print(f"Does this shit even exist???? {curr_vector_field[360-y-1,x]}")
    curr_vector = curr_vector_field[y,x]
    if np.isnan(curr_vector[0]):
        neighbors = get_neighbors(curr_vector_field, x, y)
        if len(neighbors) is not 0:
            curr_vector = random.choice(neighbors)
    sample_point = move_point(sample_point, curr_vector)
    travel_path.append(sample_point)

    current_date += increment
    
