# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 12:27:20 2020

@author: mrg19-02144103
"""

REFLECTANCE_MULT = (0.0011966, 0.0025008, 0.0021282, 0.0025759, 0.0017441, 0.0024211)
REFLECTANCE_ADD = (-0.003572, -0.007405, -0.004513, -0.007016, -0.007106, -0.007961)

import sys, os
sys.path.append(os.path.abspath(open('./../local_data/ACTIVEX.txt').readlines()[0].split('\n')[0]))
import util
import numpy as np
from tqdm import tqdm

PATH = open('./../local_data/R_PATH_Landsat.txt').readlines()

W_PATH = open('./../local_data/W_PATH_Landsat.txt').readlines()

if __name__ == "__main__":
    '''
    driver function
    '''
    #read band files
    bands = ('B2','B3','B4','B5')
    Radiance_bands = []
    for band in bands:
        Radiance_bands.append(util.readBand(band, PATH[0].split('\n')[0]))
    
    
    
    #performing correction upto level 2: DN -> Radiance -> Reflectance
    TOA_bands = []
    for band_name, band, mult, add in zip(bands, Radiance_bands, REFLECTANCE_MULT[1:-1], REFLECTANCE_ADD[1:-1]):
        tqdm.write('Correcting %s... ' % band_name, end='')
        rows, cols = band[0].shape
        corrected_img = np.zeros((rows,cols),dtype=np.float64)
        for row in tqdm(range(rows)):
            for col in range(cols):
                corrected_img[row][col] = mult*band[0][row][col] + add
        util.writeBand(corrected_img, band[2], band[1], os.path.join(W_PATH[1].split('\n')[0], band_name + '.tif'))
        print('Done')
        
        
    
    
