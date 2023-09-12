# !/usr/bin/env python
# -*- coding: utf-8 -*-

# skrypt do generowania konturow (warstwic) wybranych arkuszy mapowych do swojej przestrzeni roboczej

import arcpy
import os

arcpy.CheckOutExtension("Spatial")

# nasza przestrzen robocza [PARAMETR]
workspace= arcpy.env.workspace = ur'E:\FolderRoboczy\19004_00_Piekielko\warstwice_c'

# warstwa przechowywująca dane do okreslenia dla ktorych arkuszy generujemy kontury [PARAMETR]
arkusze = 'arkusze.shp'

output=ur'E:\FolderRoboczy\19004_00_Piekielko\warstwice_c'

with arcpy.da.SearchCursor(arkusze, ['NMT_asc','godlo','area'])as search:
    for row in search:

            print row[0]
            arcpy.sa.Contour(row[0],os.path.join(output,row[1]+'.shp'),0.5,0)

print 'Przetworzono wszystkie wymienione arkusze'