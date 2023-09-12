#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("3D")

"""parametry programu"""

workspace = arcpy.env.workspace = \
    r"R:\OIIS_KR5\_PROJEKTY 2018\18035-00 LK201\33_ULLK\337_GIS\1_roboczy\shp\pliki_branzowe\ODC_1\ODC_1_24022022.gdb"

dzialki_czasowe = 'dzialki_ewidencyjne_zakres_lk201_ROBOTY_ODC1_czasowe'
roboty = 'pliki_branzowe_dz_czasowe_dissolve2_sort'

lista_robot_dzialki = []
with arcpy.da.SearchCursor(roboty, ['Identyfika', 'PLANOWANE_ROBOTY']) as cur2:
    for row2 in cur2:
        lista_robot_dzialki.append([row2[0], row2[1]])
        # lista_robot_dzialki = set(lista_robot_dzialki)
del cur2

with arcpy.da.UpdateCursor(dzialki_czasowe, ['Identyfika', 'PLANOWANE_ROBOTY']) as update:
    for row in update:
        print row[0]
        row[1] = ''
        for item in lista_robot_dzialki:
            if row[0] == item[0]:
                if row[1] == '':
                    row[1] = item[1]
                else:
                    row[1] = row[1] + '\n' + item[1]

        print row[1]
        print len(row[1])
        update.updateRow(row)

del update