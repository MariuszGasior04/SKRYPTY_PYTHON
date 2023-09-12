# !/usr/bin/env python
# -*- coding: utf-8 -*-

# skrypt do kopiowania wybranych arkuszy mapowych do swojej przestrzeni roboczej

import arcpy
import shutil

# nasza przestrzen robocza [PARAMETR]
workspace = arcpy.env.workspace = r'D:\FolderRoboczy\Strefy_testy\_NMT'
# warstwa przechowywująca dane do lokalizacji plikow ktore chcemy przekopiowac [PARAMETR]
arkusze = 'arkusze.shp'

output = workspace

with arcpy.da.SearchCursor(arkusze, ['NMT_asc', 'godlo'])as search: ## aby przekopiowywac ORTO nalezy podmienic 'NMT_tif' na 'ORTO_tif'
    for row in search:
        shutil.copy2(row[0], output)
        print row[0]

del search

print 'Zakonczono kopiowanie'