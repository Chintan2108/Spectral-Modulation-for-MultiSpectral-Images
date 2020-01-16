# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 01:05:30 2020

@author: Chintan Maniyar
"""

import osr, gdal
import os, pickle
import numpy as np
from tqdm import tqdm

PATH = 'D:\Chintan Data\Module 2\Research\Kernel Development\Okeechobee Data\S2A_MSIL2A_20200101T160511_N0213_R054_T17RNK_20200101T200214.SAFE\GRANULE\L2A_T17RNK_A023646_20200101T160506\IMG_DATA\R20m'
LOCS = os.listdir(PATH)

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

if __name__ == "__main__":
    '''
    driver function
    '''
    green = readBand('B03')[0]
    red = readBand('B04')[0]
    nir = readBand('B8A')[0]
    swir = readBand('B11')[0]
    
    classified_img = [[0 for j in range(5490)] for i in range(5490)]
    
    flag = False
    for row in tqdm(range(5490)):
        for col in range(5490):
            spectra = [green[row][col], red[row][col], nir[row][col], swir[row][col]]
            modulation = ""
            for x in range(len(spectra)):
                for y in range(x+1,len(spectra)):
                    if spectra[x] > spectra[y]:
                        modulation += '2'
                    elif spectra[y] < spectra[x]:
                        modulation += '1'
                    else:
                        modulation += '0'
            classified_img[row][col] = modulation
            
    with open('./classified_img.data', 'wb') as pf:
        pickle.dump(classified_img, pf)
            
                        
            
    
    