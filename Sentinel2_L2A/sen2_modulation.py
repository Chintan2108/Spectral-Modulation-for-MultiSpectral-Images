# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 01:05:30 2020

@author: Chintan Maniyar
"""


import sys, os
sys.path.append(os.path.abspath('D:\Chintan Data\GITHUB\Spectral-Modulation-for-MultiSpectral-Images'))
import util

temp = open('./../local_data/R_PATH_Sentinel.txt')
PATH = temp.read()

temp = open('./../local_data/W_PATH_Sentinel.txt')
W_PATH = temp.read()

if __name__ == "__main__":
    '''
    driver function
    '''
    
    #read band files
    green  = util.readBand('B03', PATH)
    red  = util.readBand('B04', PATH)
    nir  = util.readBand('B8A', PATH)
    swir  = util.readBand('B11', PATH)
    
    #perform spectral modulation and save output for each band file
    util.spectralModulation((green, red, nir,swir), W_PATH)
    