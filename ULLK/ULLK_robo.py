#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do tworzenia wsadu do wniosku

import os
import arcpy
import docx
from docx.shared import Pt
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

arcpy.env.overwriteOutput = True

"""parametry programu"""

roboty = {'121002_2.0009':['1/18','1/59','1/65'],
        '121002_2.0014':['123','124']}

workspace = arcpy.env.workspace = r"R:\OIIS_KR5\_PROJEKTY 2019\19004-00_Piekielko\33_ULLK\337_GIS\2_mapy\odc_E\baza_mapy_odcE.gdb\dzialki_ewidencyjne_zajecie_czasowe_diss"

dzialki_czas = 'dzialki_ewidencyjne_zajecie_czasowe_diss'
kol = []

for field in arcpy.ListFields(dzialki_czas):
        kol.append(str(field.name))

with arcpy.da.SearchCursor(dzialki_czas, kol)as search: ## aby przekopiowywac ORTO nalezy podmienic 'NMT_tif' na 'ORTO_tif'
    for row in search:
        row[kol.index('ID_DZ')] =

del search


for ob in roboty:
    print ob
    roboty.get(ob).append('aaa')
    print roboty.get(ob)
