#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy
import  os

def  BIT_RASTER(folder_tif, folder_bit):
    for plik in os.listdir(folder_tif):
        if os.path.isfile(os.path.join(folder_tif,plik)) and os.path.splitext(plik)[1]=='.tif':
            arcpy.CopyRaster_management(os.path.join(folder_tif,plik),os.path.join(folder_bit,plik),pixel_type = "1_BIT", nodata_value = "255",transform="Transform")
    return

def  BIT8_RASTER(folder_tif, folder_bit):
    for plik in os.listdir(folder_tif):
        if os.path.isfile(os.path.join(folder_tif,plik)) and os.path.splitext(plik)[1]=='.tif':
            arcpy.CopyRaster_management(os.path.join(folder_tif,plik),os.path.join(folder_bit,plik),pixel_type = "8_BIT_UNSIGNED", nodata_value = "255",transform="Transform")
    return

