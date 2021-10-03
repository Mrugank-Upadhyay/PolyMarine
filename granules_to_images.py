import netCDF4
import pandas as pd
import numpy as np
import math
from PIL import Image
import cv2

def map_range(input_start,input_end,output_start,output_end,val):
    slope = (output_end - output_start) / (input_end - input_start)
    return output_start + slope * (val - input_start)

for year in range(1992,2018):
    for month in range(1,13):
        ecco_nc_file = f"OCEAN_VELOCITY_mon_mean_{str(year).zfill(4)}-{str(month).zfill(2)}_ECCO_V4r4_latlon_0p50deg.nc"
        nc = netCDF4.Dataset(ecco_nc_file, mode="r")
        nc.variables.keys()
        lat_bnds = nc.variables['latitude_bnds'][:]
        long_bnds = nc.variables['longitude_bnds'][:]
        time_bnds_var = nc.variables['time_bnds']
        time_var = nc.variables['time']
        dtime = netCDF4.num2date(time_var[:],time_var.units)
        evel = nc.variables['EVEL']
        nvel = nc.variables['NVEL']

        min_vel = -2
        max_vel = 2

        w = 720
        h = 360
        pic_size = (h,w,3)

        for i, (e_arr,n_arr) in enumerate(zip(evel[:][0],nvel[:][0])):
            filename = f"test{i}.png"
            out_arr = np.zeros(pic_size,dtype=np.int8)
            for y, (e_row,n_row) in enumerate(zip(reversed(e_arr), reversed(n_arr))):
                for x, (e_val,n_val) in enumerate(zip(e_row,n_row)):
                    if e_val.dtype == 'float64':
                        out_arr[y,x] = [0,100,0]
                        continue
                    mapped_e_val = math.floor(map_range(min_vel, max_vel,0,255,e_val))
                    mapped_n_val = math.floor(map_range(min_vel, max_vel,0,255,n_val))
                    out_arr[y,x] = [mapped_e_val,0,mapped_n_val]

            img = Image.fromarray(out_arr,"RGB")
            filename = f"images/ecco_2017_12_{str(i).zfill(3)}.png"
            img.save(filename)
            break
