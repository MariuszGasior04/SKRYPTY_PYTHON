#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy
import os

folder_mxd = ur"R:\OIIS_KR5\_PROJEKTY 2019\19050-00_Mapy_Budowle\07.GIS\5_Opracowanie_kartograficzne\PROJEKCJE\ODRA\MRP_gotowe"
folder_map = ur"R:\OIIS_KR5\_PROJEKTY 2019\19050-00_Mapy_Budowle\07.GIS\5_Opracowanie_kartograficzne\MAPY\OD ODRY\MRP"
i=0
wydrukowane_lista=[]

for mapa in os.listdir(folder_map):
    wydrukowane_lista.append(os.path.splitext(mapa)[0])

wydruki = set(wydrukowane_lista)

for plik in os.listdir(folder_mxd):
    if (os.path.isfile(os.path.join(folder_mxd,plik)) and os.path.splitext(plik)[1]=='.mxd') and os.path.splitext(plik)[0] not in wydruki:
        mxd = arcpy.mapping.MapDocument(os.path.join(folder_mxd,plik))

        if plik[10:12] == 'RS':
            i+=1
            arcpy.mapping.ExportToPDF(mxd, os.path.join(folder_map,os.path.splitext(plik)[0] + ".pdf")
            ,resolution=300
            ,image_compression = 'ADAPTIVE'
            ,picture_symbol = 'RASTERIZE_BITMAP'
            ,layers_attributes = 'NONE'
            ,jpeg_compression_quality=85
            ,georef_info=True)

            print (os.path.splitext(plik)[0] +" - nr {0}").format(i)

            del mxd


print "Koniec", folder_mxd

#df_export_width=640, df_export_height=480, geoTIFF_tags=True