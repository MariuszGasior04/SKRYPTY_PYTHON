# !/usr/bin/env python
# -*- coding: utf-8 -*-

import arcpy

precision = 1 #number of decimals to round coordinates when matching points to polygon vertices
point_fc = ur'E:\FolderRoboczy\_smietnik\MC\swinoujscie\Marian\budynki_ger_1_vert0.shp'
polygon_fc = ur'E:\FolderRoboczy\_smietnik\MC\swinoujscie\Marian\budynki_ger_1.shp'

polycopy = r'E:\FolderRoboczy\_smietnik\MC\swinoujscie\Marian\bud_copy2.shp'
arcpy.CopyFeatures_management(in_features=polygon_fc, out_feature_class=polycopy)

points = [(round(i[0][0],precision),round(i[0][1],precision)) for i in arcpy.da.SearchCursor(point_fc,'SHAPE@XY')]

#Recreate each polygon with all vertices but the ones matching the points
with arcpy.da.UpdateCursor(polycopy,'SHAPE@') as cursor:
    for row in cursor:
        polylist = []
        for part in row[0]:
            partlist = []
            for pnt in part:
                try:
                    if (round(pnt.X,precision), round(pnt.Y,precision)) not in points:
                        partlist.append(pnt)
                except AttributeError:
                    pass
            polylist.append(partlist)
        row[0] = arcpy.Polygon(arcpy.Array(polylist))
        cursor.updateRow(row)
del cursor