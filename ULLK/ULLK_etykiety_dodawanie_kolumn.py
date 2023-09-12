#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy

arcpy.env.overwriteOutput = True

"""parametry programu"""

workspace = arcpy.env.workspace = r"R:\OIIS_KR5\_PROJEKTY 2019\19004-00_Piekielko\33_ULLK\337_GIS\2_mapy\odc_E\baza_mapy_odcE.gdb"
warstwa = 'dzialki_ewidencyjne_zajecie_czasowe_diss'
for i in range(1,24):
    fieldName = 'ETYK'+str(i)
    arcpy.AddField_management(warstwa, fieldName, "TEXT", field_length=255)

print "dodano kolumny"