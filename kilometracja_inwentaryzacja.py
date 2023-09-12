#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do okreslania kilometrazu obiektow zinwentaryzowanych wzgledem trasy route.

import arcpy
import os
from arcpy import env
arcpy.env.overwriteOutput = True
import time
"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

def Kilometracja(workspace,in_point, in_route):
    arcpy.env.workspace=workspace
    table='locate.dbf'
    arcpy.LocateFeaturesAlongRoutes_lr(in_point, in_route, 'LK', "250.0 Meters", table, "LK POINT measure",distance_field="DISTANCE", in_fields='NO_FIELDS')
    return table

def Kilometracja_polig(workspace,in_point, in_route):
    arcpy.env.workspace=workspace
    table='locate.dbf'
    arcpy.LocateFeaturesAlongRoutes_lr(in_point, in_route, 'LK', "170.0 Meters", table, "LK POINT measure",distance_field="DISTANCE", in_fields='FIELDS')
    return table

arcpy.env.workspace = ws = ur'P:\Projekty_2017\17052-00 E 75\33_ULLK\339_GIS\1_roboczy\shp\inwentaryzacja\test'

route = ur'P:\Projekty_2017\17052-00 E 75\33_ULLK\339_GIS\1_roboczy\shp\route\route_odc5_38_41.shp'
fcs = arcpy.ListFeatureClasses()

for input in fcs:

    if arcpy.Describe(input).shapeType =='Point' or arcpy.Describe(input).shapeType =='Multipoint':

        tab=Kilometracja(ws,input,route)
        try:
            arcpy.AddField_management(input, 'KM', 'FLOAT')
        except:
            pass
        try:
            arcpy.AddField_management(input, 'ODL', 'FLOAT')
        except:
            pass
        try:
            arcpy.AddField_management(input, 'STRONA', 'TEXT')
        except:
            pass

        arcpy.JoinField_management (input, 'FID', tab, 'INPUTOID', ['measure','Distance'])

        with arcpy.da.UpdateCursor(input,['KM','measure','Distance','STRONA','ODL'])as cur:
            for row in cur:
                if row[1] is not None:
                    row[0]=round(float(row[1])/1000,3)
                    if row[2]<0:
                        row[3]='prawa'
                        row[4]=round(row[2]*(-1),1)
                    elif row[2]>0:
                        row[3]='lewa'
                        row[4]=round(row[2],1)
                    elif row[2]==0:
                        row[3]='na osi trasy'
                        row[4]=round(row[2],1)
                    cur.updateRow(row)
        del cur

        arcpy.Delete_management(tab)
        arcpy.DeleteField_management(input, ['measure','Distance'])

    elif arcpy.Describe(input).shapeType =='Polyline':
        line_start='line_start.shp'
        line_end='line_end.shp'
        arcpy.AddField_management(input, 'START', 'FLOAT')
        arcpy.AddField_management(input, 'END', 'FLOAT')
        arcpy.AddField_management(input, 'ODLs', 'FLOAT')
        arcpy.AddField_management(input, 'STRONAs', 'TEXT')
        arcpy.AddField_management(input, 'ODLe', 'FLOAT')
        arcpy.AddField_management(input, 'STRONAe', 'TEXT')
        arcpy.FeatureVerticesToPoints_management(input, line_end, "END")
        arcpy.FeatureVerticesToPoints_management(input, line_start, "START")
        arcpy.DeleteField_management(input, ['START','END','STRONAs','STRONAe','ODLe','ODLs'])

        vertexy=[line_start,line_end]
        for point in vertexy:
            tab=Kilometracja(ws,point,route)

            arcpy.JoinField_management (point, 'FID', tab, 'INPUTOID', ['measure','LK','Distance'])

            if point ==line_start:
                kol =['START','measure','Distance','STRONAs','ODLs']
            elif point ==line_end:
                kol =['END','measure','Distance','STRONAe','ODLe']

            with arcpy.da.UpdateCursor(point,kol)as cur:
                for row in cur:
                    if row[1] is not None:
                        row[0]=round(float(row[1])/1000,3)
                        if row[2]<0:
                            row[3]='prawa'
                            row[4]=round(row[2]*(-1),1)
                        elif row[2]>0:
                            row[3]='lewa'
                            row[4]=round(row[2],1)
                        elif row[2]==0:
                            row[3]='na osi trasy'
                            row[4]=round(row[2],1)
                        cur.updateRow(row)

            del cur
            arcpy.Delete_management(tab)

            if point ==line_start:
               ## arcpy.JoinField_management (input, 'FID', point, 'ORIG_FID', ['START','STRONAs','ODLs'])
                arcpy.JoinField_management (input, 'FID', point, 'ORIG_FID', ['START'])
            elif point ==line_end:
              ##  arcpy.JoinField_management (input, 'FID', point, 'ORIG_FID', ['END','STRONAe','ODLe'])
               arcpy.JoinField_management (input, 'FID', point, 'ORIG_FID', ['END'])
            arcpy.Delete_management(point)

    elif arcpy.Describe(input).shapeType =='Polygon':

        werteksy = 'werteksy.shp'
        tab_stat = 'locate_stat.dbf'
        near_tab = 'near.dbf'
        arcpy.FeatureVerticesToPoints_management(input, werteksy, "ALL")

        tab = Kilometracja_polig(ws,werteksy,route)

        arcpy.Delete_management(werteksy)

        arcpy.Statistics_analysis(tab, tab_stat, statistics_fields = [["measure", "MIN"],["measure", "MAX"]], case_field = "ORIG_FID")

        try:
            arcpy.AddField_management(input, 'KM_START', 'FLOAT')
            arcpy.AddField_management(input, 'KM_END', 'FLOAT')
            arcpy.AddField_management(input, 'ODL', 'FLOAT')
        except:
            pass

        arcpy.Delete_management(tab)
        arcpy.JoinField_management (input, 'FID', tab_stat, 'ORIG_FID', ['MIN_measur','MAX_measur'])
        arcpy.Delete_management(tab_stat)

        arcpy.GenerateNearTable_analysis(input, route, near_tab, search_radius = '150 Meters')
        arcpy.JoinField_management (input, 'FID', near_tab, 'IN_FID', ['NEAR_DIST'])
        arcpy.Delete_management(near_tab)
        with arcpy.da.UpdateCursor(input,['KM_START','KM_END','MIN_measur','MAX_measur','ODL','NEAR_DIST'])as cur:
            for row in cur:
                if row[2] is not None:
                    row[0]=round(float(row[2])/1000,3)
                    row[1]=round(float(row[3])/1000,3)
                    row[4]=round(row[5],1)
                    cur.updateRow(row)
        del cur



        arcpy.DeleteField_management(input, ['MIN_measur','MAX_measur','NEAR_DIST'])

    print 'koniec', input

