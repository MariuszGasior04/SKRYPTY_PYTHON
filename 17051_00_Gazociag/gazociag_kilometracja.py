#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do okreslania kilometrazu obiektow wzgledemi ich obiektow gazociagu.

import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True
import time
"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

arcpy.env.workspace=ws=ur'P:\Projekty_2017\17051-00 Goleniów_Lwówek_DN1000\11_GIS\_warstwy_robo\analizy_robocze'

point=''
line='os_dzialki.shp'

##routs=['Gaz_DN1000_route_01.shp','Gaz_DN1000_route_wariant_.shp','Gaz_DN1000_route_wariant_04W1.shp','Gaz_DN1000_route_wariant_04W2.shp','Gaz_DN1000_route_wariant_04W3.shp']
routs=['Gaz_DN1000_rek_01_route.shp']

def Kilometracja(workspace,in_point, in_route):
    arcpy.env.workspace=workspace
    table='locate.dbf'
    arcpy.LocateFeaturesAlongRoutes_lr(in_point, in_route, 'REV', "10.0 Meters", table, "REV POINT measure",distance_field="DISTANCE", in_fields='NO_FIELDS')
    return table

if point !='':
    for route in routs:
        tab=Kilometracja(ws,point,route)

        arcpy.AddField_management(tab, 'WAR_route', 'TEXT')
        arcpy.CalculateField_management(tab, 'WAR_route', '!REV!', "PYTHON_9.3")

        arcpy.JoinField_management (point, 'FID', tab, 'INPUTOID', ['measure','WAR_route'])

        with arcpy.da.UpdateCursor(point,['KM','measure'])as cur:
            for row in cur:
                if row[1] is not None:
                    row[0]=round(float(row[1])/1000,3)
                    cur.updateRow(row)
        del cur

        arcpy.Delete_management(tab)
        arcpy.DeleteField_management(point, ['measure','WAR_route'])

if line != '':
    line_start='line_start.shp'
    line_end='line_end.shp'
    arcpy.AddField_management(line, 'START', 'FLOAT')
    arcpy.AddField_management(line, 'END', 'FLOAT')
    arcpy.FeatureVerticesToPoints_management(line, line_end, "END")
    arcpy.FeatureVerticesToPoints_management(line, line_start, "START")
    arcpy.DeleteField_management(line, ['START','END'])

    for route in routs:
        vertexy=[line_start,line_end]
        for point in vertexy:
            tab=Kilometracja(ws,point,route)

            arcpy.AddField_management(tab, 'WAR_route', 'TEXT')
            arcpy.CalculateField_management(tab, 'WAR_route', '!REV!', "PYTHON_9.3")

            arcpy.JoinField_management (point, 'FID', tab, 'INPUTOID', ['measure','WAR_route'])

            if point ==line_start:
                kol =['START','measure','WAR_route']
            elif point ==line_end:
                kol =['END','measure','WAR_route']

            with arcpy.da.UpdateCursor(point,kol)as cur:
                for row in cur:
                    if row[1] is not None:
                        row[0]=round(float(row[1])/1000,3)
                        cur.updateRow(row)
            del cur
            arcpy.Delete_management(tab)

            if point ==line_start:
                arcpy.JoinField_management (line, 'FID', point, 'ORIG_FID', ['START'])
            elif point ==line_end:
                arcpy.JoinField_management (line, 'FID', point, 'ORIG_FID', ['END'])
            arcpy.Delete_management(point)

print 'koniec', line, point

