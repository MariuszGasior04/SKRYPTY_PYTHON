#!/usr/bin/env python
# -*- coding: utf-8 -*-

# skrypt do okreslania kilometrazu obiektow wzgledemi ich obiektow gazociagu.

import arcpy

arcpy.env.overwriteOutput = True

"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

arcpy.env.workspace = ws =\
    ur'P:\Projekty_2017\17052-00 E 75\33_ULLK\339_GIS\1_roboczy\shp\inwentaryzacja\WWY_E75\do uzupełnienia\inwent_podst'

routs = [
    r'P:\Projekty_2017\17052-00 E 75\33_ULLK\339_GIS\1_roboczy\shp\route\route_odc1_4_lk38_lk516.shp']


def Kilometracja(workspace, in_point, in_route):
    arcpy.env.workspace = workspace
    table = 'locate.dbf'
    arcpy.LocateFeaturesAlongRoutes_lr(in_point, in_route, 'LK', "1000.0 Meters", table, "LK POINT measure",
                                       distance_field="DISTANCE", in_fields='NO_FIELDS')
    return table

walk = arcpy.da.Walk(ws, datatype="FeatureClass", type=["Point", "Polyline"])
for dirpath, dirnames, filenames in walk:
    for input in filenames:

        if arcpy.Describe(input).shapeType == 'Point':
            for route in routs:
                tab = Kilometracja(ws, input, route)
                try:
                    arcpy.AddField_management(input, 'KM', 'FLOAT')
                except:
                    pass
                arcpy.AddField_management(input, 'ODL', 'FLOAT')
                arcpy.AddField_management(input, 'STRONA', 'TEXT')
                arcpy.JoinField_management(input, 'FID', tab, 'INPUTOID', ['measure', 'Distance'])

                with arcpy.da.UpdateCursor(input, ['KM', 'measure', 'Distance', 'STRONA', 'ODL'])as cur:
                    for row in cur:
                        if row[1] is not None:
                            row[0] = round(float(row[1]) / 1000, 3)
                            if row[2] < 0:
                                row[3] = 'prawa'
                                row[4] = round(row[2] * (-1), 1)
                            elif row[2] > 0:
                                row[3] = 'lewa'
                                row[4] = round(row[2], 1)
                            elif row[2] == 0:
                                row[3] = 'na osi trasy'
                                row[4] = round(row[2], 1)
                            cur.updateRow(row)
                del cur

                arcpy.Delete_management(tab)
                arcpy.DeleteField_management(input, ['measure', 'Distance'])

        elif arcpy.Describe(input).shapeType == 'Polyline':
            line_start = 'line_start.shp'
            line_end = 'line_end.shp'
            arcpy.AddField_management(input, 'START', 'FLOAT')
            arcpy.AddField_management(input, 'END', 'FLOAT')
            arcpy.AddField_management(input, 'ODLs', 'FLOAT')
            arcpy.AddField_management(input, 'STRONAs', 'TEXT')
            arcpy.AddField_management(input, 'ODLe', 'FLOAT')
            arcpy.AddField_management(input, 'STRONAe', 'TEXT')
            arcpy.FeatureVerticesToPoints_management(input, line_end, "END")
            arcpy.FeatureVerticesToPoints_management(input, line_start, "START")
            arcpy.DeleteField_management(input, ['START', 'END', 'STRONAs', 'STRONAe', 'ODLe', 'ODLs'])

            for route in routs:
                vertexy = [line_start, line_end]
                for point in vertexy:
                    tab = Kilometracja(ws, point, route)

                    arcpy.JoinField_management(point, 'FID', tab, 'INPUTOID', ['measure', 'REV', 'Distance'])

                    if point == line_start:
                        kol = ['START', 'measure', 'Distance', 'STRONAs', 'ODLs']
                    elif point == line_end:
                        kol = ['END', 'measure', 'Distance', 'STRONAe', 'ODLe']

                    with arcpy.da.UpdateCursor(point, kol)as cur:
                        for row in cur:
                            if row[1] is not None:
                                row[0] = round(float(row[1]) / 1000, 3)
                                if row[2] < 0:
                                    row[3] = 'prawa'
                                    row[4] = round(row[2] * (-1), 1)
                                elif row[2] > 0:
                                    row[3] = 'lewa'
                                    row[4] = round(row[2], 1)
                                elif row[2] == 0:
                                    row[3] = 'na osi trasy'
                                    row[4] = round(row[2], 1)
                                cur.updateRow(row)

                    del cur
                    arcpy.Delete_management(tab)

                    if point == line_start:
                        arcpy.JoinField_management(input, 'FID', point, 'ORIG_FID', ['START', 'STRONAs', 'ODLs'])
                    elif point == line_end:
                        arcpy.JoinField_management(input, 'FID', point, 'ORIG_FID', ['END', 'STRONAe', 'ODLe'])
                    arcpy.Delete_management(point)

        print 'koniec', input
