# !/usr/bin/env python
# -*- coding: utf-8 -*-

# skrypt do kopiowania wybranych arkuszy mapowych do swojej przestrzeni roboczej

import arcpy
import shutil
import os
from arcpy.sa import *

# nasza przestrzen robocza [PARAMETR]
workspace= arcpy.env.workspace = ur'R:\OIIS_KR5\_PROJEKTY 2018\18035-00 LK201\21_Hydrotechnika (H)\112_GIS\warstwy_shp'
# warstwa (tabela) przechowywująca dane do lokalizacji plikow ktore chcemy przekopiowac [PARAMETR]
arkusze = 'arkusze_struga.shp'

# folder do ktorego przekopiowywujemy pliki [PARAMETR]
output=ur'R:\OIIS_KR5\_PROJEKTY 2018\18035-00 LK201\21_Hydrotechnika (H)\112_GIS\NMT'


"""Pętla przeszukujaca arkusze dotyczy zarchiwizowanych arkuszy na dysku koputera (serwera), ktory nalezy zmapowacj jako partycja Z:. Bez tego skrypt nie zadziała"""
with arcpy.da.SearchCursor(arkusze, ['NMT_asc','godlo'])as search: ## aby przekopiowywac ORTO nalezy podmienic 'NMT_tif' na 'ORTO_tif'
    for row in search:
##        print row[0]
        if os.path.isfile(row[0]):
            shutil.copy2(row[0],output)
            print row[0]

print 'Przekopiowano wszystkie wymienione pliki'