# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 01:05:30 2020

@author: Chintan Maniyar
"""

import osr, gdal
import os
import numpy as np
from tqdm import tqdm

temp = open('./local_data/PATH.txt')
PATH = temp.read()
LOCS = os.listdir(PATH)
temp = open('./local_data/PATH.txt')
W_PATH = temp.read()

def readBand(band):
    '''
    This function reads the jp2 file for the said band
    '''
    path = ''
    for i in LOCS:
        if band in i:
            path = os.path.join(PATH,i)
    img = gdal.Open(path)
    data = np.array(img.GetRasterBand(1).ReadAsArray())
    spatialRef = img.GetProjection()
    geoTransform = img.GetGeoTransform()
    targetprj = osr.SpatialReference(wkt = img.GetProjection())
    
    return data, spatialRef, geoTransform, targetprj

def writeBand(array, geoTransform, projection, filename):
    '''
    This function converts np array to raster image and stores a GeoTiff file on the disk
    '''
    
    pixels_x = array.shape[0]
    pixels_y = array.shape[1]
    
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(
            filename,
            pixels_x,
            pixels_y,
            1,
            gdal.GDT_Float64)
    dataset.SetGeoTransform(geoTransform)
    dataset.SetProjection(projection)
    dataset.GetRasterBand(1).WriteArray(array)
    dataset.FlushCache()
    

if __name__ == "__main__":
    '''
    driver function
    '''
    green = readBand('B03')
    red = readBand('B04')
    nir = readBand('B8A')
    swir = readBand('B11')
    
    classified_img = np.zeros((5490,5490),dtype=np.uint8)
    
    flag = False
    for row in tqdm(range(5490)):
        for col in range(5490):
            spectra = [green[0][row][col], red[0][row][col], nir[0][row][col], swir[0][row][col]]
            modulation = ""
            for x in range(len(spectra)):
                for y in range(x+1,len(spectra)):
                    if spectra[x] > spectra[y]:
                        modulation += '2'
                    elif spectra[y] < spectra[x]:
                        modulation += '1'
                    else:
                        modulation += '0'
                if modulation == '222222' and spectra[-1] < 91:
                    classified_img[row][col] = 50
                elif modulation == '022222' and spectra[-1] < 91:
                    classified_img[row][col] = 150
                else:
                    classified_img[row][col] = 255
            
            
    writeBand(classified_img, green[2], green[1], W_PATH + '/wb_s2_msi_l2a_swir_th_90.tiff')
                        
            
    
    