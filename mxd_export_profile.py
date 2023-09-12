#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy
import os

#skrypt do eksportowania map z projekcji przy pomocy DDP z jednoczesna zmianą profili w ramach każdego arkusza

mxd = arcpy.mapping.MapDocument("CURRENT")
folder_map = ur"P:\Projekty_2017\17051-00 Goleniów_Lwówek_DN1000\11_GIS\2_Mapy\Mapy_analiza_widocznosci\arkusze"

mxd.activeView = arcpy.mapping.ListDataFrames(mxd)[1].name

for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = pageNum
    pageName = mxd.dataDrivenPages.pageRow.PageNumber

    where_clause = '"PageNumber" = ' + str(pageName)
    arcpy.SelectLayerByAttribute_management(arcpy.mapping.ListLayers(mxd,data_frame = arcpy.mapping.ListDataFrames(mxd)[1])[0],'NEW_SELECTION',where_clause)
    arcpy.SelectLayerByAttribute_management(arcpy.mapping.ListLayers(mxd,data_frame = arcpy.mapping.ListDataFrames(mxd)[1])[1],'NEW_SELECTION',where_clause)
    arcpy.SelectLayerByAttribute_management(arcpy.mapping.ListLayers(mxd,data_frame = arcpy.mapping.ListDataFrames(mxd)[1])[2],'NEW_SELECTION',where_clause)

    arcpy.mapping.ExportToPDF(mxd, os.path.join(folder_map, "Ark" + str(pageName) + ".pdf"),resolution=200, image_quality = 'BEST', image_compression = 'LZW', georef_info=True)

del mxd

print "Koniec"

