# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 01:05:30 2020

@author: Chintan Maniyar
"""

import osr, gdal
import os
import numpy as np
from tqdm import tqdm

def readBand(band, PATH):
    '''
    This function reads the jp2/tif file for the said band
    args: band (str) --> band no. eg: 'B7' in case of Landsat, 'B07' in case of Sentinel
          PATH (str) --> Path to folder containing band files
    '''
    path = ''
    LOCS = os.listdir(PATH)
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
    args: array --> numpy array containing DN values
          geoTransform --> affine transformation coefficients
          projection --> projection info
          filename --> output filepath
    '''
    
    pixels_x = array.shape[1]
    pixels_y = array.shape[0]
    
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
    

#if __name__ == "__main__":
def spectralModulation(bands, outputPath):
    '''
    This function performs modulation for the spectra of TBD bands for feature based classification 
    args: bands --> a tuple of bands on which spectral modulation is to be performed
          outputPath --> Path to output directory
    NOTE: The order for the bands must be maintained same as the ordinality desired for modulation
    '''
#    green = readBand('B03')
#    red = readBand('B04')
#    nir = readBand('B8A')
#    swir = readBand('B11')
    
    rows, cols = bands[0][0].shape
    
    classified_img = np.zeros((rows,cols),dtype=np.float16)
    
    for row in tqdm(range(rows)):
        for col in range(cols):
            spectra = []
            for band in bands:
                spectra.append(band[0][row][col])
            #spectra = [green[0][row][col], red[0][row][col], nir[0][row][col], swir[0][row][col]]
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
            
            
    writeBand(classified_img, bands[0][2], bands[0][1], outputPath + '/wb_s2_msi_l2a_swir_th_90.tiff')
                        
            
    
    