#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy
import  os
import mbitRasterTo1bitRaster

folder_mxd=ur"P:\Projekty_2017\17051-00 Goleniów_Lwówek_DN1000\11_GIS\_warstwy_robo\Nadlesnictwa\Mapy_PUL_surowe\Bolewice"
folder_bit=ur"P:\Projekty_2017\17051-00 Goleniów_Lwówek_DN1000\11_GIS\_warstwy_robo\Nadlesnictwa\Mapy_PUL_kalibracja\Bolewice"
folder_map = folder_mxd

for plik in os.listdir(folder_mxd):
    if os.path.isfile(os.path.join(folder_mxd,plik)) and os.path.splitext(plik)[1]=='.mxd':
        mxd = arcpy.mapping.MapDocument(os.path.join(folder_mxd,plik))
        for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):
            mxd.dataDrivenPages.currentPageID = pageNum
            pageName = mxd.dataDrivenPages.pageRow.NAZWA

            arcpy.mapping.ExportToPDF(mxd, os.path.join(folder_map,str(pageName) + ".pdf"),resolution=400, image_quality = 'BEST', image_compression = 'LZW', georef_info=True)

            arcpy.PDFToTIFF_conversion(os.path.join(folder_map,str(pageName) + ".pdf"), os.path.join(folder_map,str(pageName) + ".tif"), resolution =400, color_mode = 'RGB_PALETTE', tiff_compression ='LZW', geotiff_tags = True)
        del mxd

mbitRasterTo1bitRaster.BIT_RASTER(folder_map,folder_bit)
##mbitRasterTo1bitRaster.BIT8_RASTER(folder_map,folder_bit)

print "Koniec", folder_mxd

#df_export_width=640, df_export_height=480, geoTIFF_tags=True