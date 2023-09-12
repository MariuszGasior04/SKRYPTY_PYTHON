#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy
import os

arcpy.env.workspace = r'P:\02_Pracownicy\Monika\01.Puławska\02.GIS\13.Przekroje_pkt_korytowe_do_generacji\Przekroje_Pulawska_xns'
przekroje = r'przekroje_dolinowe_CALOSC.shp'
lista = []

with arcpy.da.SearchCursor(przekroje, ['TYP', 'nazwa']) as search:
    for row in search:
        lista.append((row[0], row[1]))
        unikalne = set(lista)
del search

przekroje_temp = r"in_memory\przekroje"
arcpy.MakeFeatureLayer_management(przekroje, przekroje_temp)

for item in unikalne:
    el1 = item[0]
    el2 = item[1]
    if el1 in ['K', 'US', 'DS']:
        where_clause = '"TYP" = ' +"'"+ el1 +"'"+ ' AND ' + '"nazwa" = ' +"'" + el2+"'"
        arcpy.SelectLayerByAttribute_management(przekroje_temp, "NEW_SELECTION", where_clause)
        przekroje_output = el2 +'_przekroje_'+ el1 + '.shp'
        # print(przekroje_output)
        arcpy.CopyFeatures_management(przekroje_temp, przekroje_output)
