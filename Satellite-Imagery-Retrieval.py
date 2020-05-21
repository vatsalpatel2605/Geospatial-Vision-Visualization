# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 20:50:59 2020

@author: vatsal
"""

from math import sin, cos, log, pi
import cv2
import numpy as np
import urllib
import urllib.request
import sys


LAT_RANGE = (-85.05112878, 85.05112878)
LONG_RANGE = (-180., 180.)
E_RADIUS = 6378137

def clip(n, minMax):
    return min(max(n, minMax[0]), minMax[1])

def map_size(level):
    return 256 << level

def ground_resolution(lat, level):
    lat = clip(lat, LAT_RANGE)
    return cos(lat * pi / 180) * 2 * pi * E_RADIUS / map_size(level)

def map_scale(lat, level, dpi):
    return ground_resolution(lat, level) * dpi / 0.0254

def conv_g_to_p(geo, level):
    lat, lon = float(geo[0]), float(geo[1])
    lat = clip(lat, LAT_RANGE)
    lon = clip(lon, LONG_RANGE)
    x = (lon + 180) / 360
    sin_lat = sin(lat * pi / 180)
    y = 0.5 - log((1 + sin_lat) / (1 - sin_lat)) / (4 * pi)
    mapsize = map_size(level)
    pixel_x = int(clip(x * mapsize + 0.5, (0, mapsize - 1)))
    pixel_y = int(clip(y * mapsize + 0.5, (0, mapsize - 1)))
    return pixel_x, pixel_y

def conv_p_to_t(pixel):
    return pixel[0] / 256, pixel[1] / 256

def t_to_qkey(t, l):
    tile_x = t[0]
    tile_y = t[1]
    quadkey = ""
    for i in range(l):
        bit = l - i
        digit = ord('0')
        mask = 1 << (bit - 1)  # if (bit - 1) > 0 else 1 >> (bit - 1)
        if (int(tile_x) & mask) != 0:
            digit += 1
        if (int(tile_y) & mask) != 0:
            digit += 2
        quadkey += chr(digit)
    return quadkey

def get_tile(g, threshold):
    p = conv_g_to_p(g, threshold)
    t = conv_p_to_t(p)
    return t

def get_image(k):
    ext = ".jpeg"
    urlA = 'http://h0.ortho.tiles.virtualearth.net/tiles/h'
    urlB = '.jpeg?g=131'
    #023131022213211200
    
    for i in range(0,len(k)):
        filename = str(i+1)+ext
        
        url = urlA + k[i] + urlB
        urllib.request.urlretrieve(url,filename)
        

def stitch_image():
    img1 = cv2.imread('1.jpeg')
    img2 = cv2.imread('2.jpeg')
    img3 = cv2.imread('3.jpeg')
    img4 = cv2.imread('4.jpeg')
    
    img5 = cv2.imread('5.jpeg')
    img6 = cv2.imread('6.jpeg')
    img7 = cv2.imread('7.jpeg')
    img8 = cv2.imread('8.jpeg')
    
    img9 = cv2.imread('9.jpeg')
    img10 = cv2.imread('10.jpeg')
    img11 = cv2.imread('11.jpeg')
    img12 = cv2.imread('12.jpeg')
    
    
    i = [[img1,img2,img3,img4],[img5,img6,img7,img8],[img9,img10,img11,img12]]
    
    result = np.hstack((np.vstack(i[0]),np.vstack(i[1]),np.vstack(i[2])))
    
    cv2.imwrite('result.jpeg',result)

def main():	 
    lat1 = float(sys.argv[1])
    lon1 = float(sys.argv[2])
    lat2 = float(sys.argv[3])
    lon2 = float(sys.argv[4])
    l = 17
    print("--Generating Tiles for given 2 points--")
    x = get_tile((lat1,lon1), l)
    y = get_tile((lat2,lon2), l)
    print("---Generating Tiles between 2 points---")
    zipped = []
    if (x[0]>y[0]):
        t = y
        y = x
        x = t
    for i in np.arange(x[0],y[0]+1):
        for j in np.arange(x[1],y[1]+1):
            zipped.append((i,j))
    print("Total tiles generated: %d" %len(zipped))
    print("--Generating Quadkeys for generated tiles--")
    keys = []
    for i in range(0,len(zipped)):
        keys.append(t_to_qkey(zipped[i], l))
    print("--Quadkeys Generated--")
    print("--Downloading images for quadkeys--")
    get_image(keys)
    print("--Stiching images--")
    stitch_image()
    print("Final image generated.")

if __name__ == '__main__':
    main()