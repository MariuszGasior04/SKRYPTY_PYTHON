#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do okreslania kilometrazu pkt na profilu.

import arcpy
import os
from arcpy import env
arcpy.env.overwriteOutput = True
import time
"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

arcpy.env.workspace=ws=ur'R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\1_Analiza_danych_OZ\przekroje\Etap 1\2_przedluzone\Dobczyce'

pkt_prof ='S01_Raba_przekroje_przedluzone_pkt_5m.shp'
route = 'S01_Raba_przekroje_przedluzane_route.shp'

def Kilometracja(workspace,in_point, in_route):
    arcpy.env.workspace=workspace
    table='locate.dbf'
    arcpy.LocateFeaturesAlongRoutes_lr(in_point, in_route, 'RID', "0.1 Meters", table, "RID POINT measure",distance_field="DISTANCE", in_fields='NO_FIELDS')
    return table

tab=Kilometracja(ws,pkt_prof,route)

try:
    arcpy.AddField_management(pkt_prof, 'METR', 'FLOAT')
except:
    pass

arcpy.JoinField_management (pkt_prof, 'FID', tab, 'INPUTOID', ['measure'])

with arcpy.da.UpdateCursor(pkt_prof,['METR','measure'])as cur:
    for row in cur:
        if row[1] is not None:
            row[0]=round(float(row[1]),3)

            cur.updateRow(row)
del cur
##        arcpy.CalculateField_management(pkt_prof, 'KM', 'round(!measure!/1000,3)', "PYTHON_9.3")
##        arcpy.CalculateField_management(pkt_prof, 'ODL', '!Distance!', "PYTHON_9.3")
arcpy.Delete_management(tab)
arcpy.DeleteField_management(pkt_prof, ['measure'])

print 'koniec', pkt_prof





