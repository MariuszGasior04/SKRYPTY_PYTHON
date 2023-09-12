#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("3D")

"""parametry programu"""


workspace = arcpy.env.workspace = \
    r"R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\5_Opracowanie_kartograficzne\BAZA_Mapy\robo_skorowidz.gdb"

pkt = 'akt_NMT'
ark = 'MZP_skorowidz'

with arcpy.da.UpdateCursor(ark, ['Godlo', 'AKT_NMT']) as update:
    for row in update:
        rok = ''
        with arcpy.da.SearchCursor(pkt, ['GODLO', 'ROKAKT']) as cur2:
            for row2 in cur2:
                if row[0] == row2[0]:
                    if rok == '':
                        rok = str(row2[1])
                    else:
                        rok = rok +', '+str(row2[1])
        del cur2
        row[1] = rok
        print row[0]
        update.updateRow(row)

del update
# kol = ['etyk1', 'etyk11', 'etyk12', 'etyk13']
# def etykiety(kol):
#     opis = kol[0]+'\n'
#
#     for e in range(len(kol)):
#         if kol[e] is not None:
#             if e > 0:
#                 opis = opis + kol[e] + '\n'
#     return opis[:-1]
#
# print etykiety(kol)
# print etykiety('etyk1', 'etyk11', 'etyk12', 'etyk13')[:-1]