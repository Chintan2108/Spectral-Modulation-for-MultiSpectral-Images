# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 12:27:20 2020

@author: mrg19-02144103
"""

REFLECTANCE_MULT = [(0.0011966, 0.0025008, 0.0021282, 0.0025759, 0.0017441, 0.0024211),
                    (0.0011984, 0.0025045, 0.0021314, 0.0025797, 0.0017467, 0.0024247)]

REFLECTANCE_ADD = [(-0.003572, -0.007405, -0.004513, -0.007016, -0.007106, -0.007961),
                   (-0.003577, -0.007416, -0.004520, -0.007026, -0.007117, -0.007973)]


import sys, os
sys.path.append(os.path.abspath(open('./../local_data/ACTIVEX.txt').readlines()[0].split('\n')[0]))
import util
import numpy as np
from tqdm import tqdm

PATH = open('./../local_data/R_PATH_Landsat.txt').readlines()
W_PATH = open('./../local_data/W_PATH_Landsat.txt').readlines()

def level2Corr(bands, inputPath, outputPath):
    '''
    This function performs level 2 correction on the level 0 Landsat 5 TM data and saves the corrected bands as tif rasters
    args: bands (tuple)    --> This is a tuple containing identifier of band name for correction. eg - ('B1','B5')
          inputPath (str)  --> This is the path to directory containing the level 1 data
          outputPath (str) --> This is the path to directory where the level 2 data is to be saved
     '''
    Radiance_bands = []
    for band in bands:
        Radiance_bands.append(util.readBand(band, inputPath))
    
    #performing correction upto level 2: DN -> Radiance -> Reflectance
    for band_name, band, mult, add in zip(bands, Radiance_bands, REFLECTANCE_MULT[0][1:-1], REFLECTANCE_ADD[0][1:-1]):
        tqdm.write('Correcting %s... ' % band_name, end='')
        rows, cols = band[0].shape
        corrected_img = np.zeros((rows,cols),dtype=np.float64)
        for row in tqdm(range(rows)):
            for col in range(cols):
                corrected_img[row][col] = mult*band[0][row][col] + add
        util.writeBand(corrected_img, band[2], band[1], os.path.join(outputPath, band_name + '.tif'))
        print('Done')
     

if __name__ == "__main__":
    '''
    driver function
    '''
    #perform correction using header file for DN to Reflectance conversion
    bands = ('B2','B3','B4','B5')
    #level2Corr(bands, PATH[2].split('\n')[0], W_PATH[2].split('\n')[0])
    
    #read corrected bands
    TOA_bands = []
    for band in bands:
        TOA_bands.append(util.readBand(band, PATH[3].split('\n')[0]))
    
    #perform modulation
    util.spectralModulation(tuple(TOA_bands), W_PATH[0].split('\n')[0])        
        
    
    
