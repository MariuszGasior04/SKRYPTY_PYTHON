#!/usr/bin/env python
# -*- coding: utf-8 -*-

# skrypt do utworzenia raportu z posortowanej tabeli zaktualizowanych przekroi

import os
import arcpy

workspace = \
    arcpy.env.workspace = \
    r"D:\FolderRoboczy\3_iteracja\robo.gdb"

tab = 'przedluzenia_WARTA_tab_sort'
tab_HL = 'WARTA_S10_HL'

file_dir =\
    r"D:\FolderRoboczy\3_iteracja\S10_Warta_aktualizacja_27012021.txt"

f = open(file_dir, "w")

fields = []
for field in arcpy.ListFields(tab):
    fields.append(str(field.name))
prof_disc = {}

with arcpy.da.SearchCursor(tab, ['OBJECTID', 'cngmetry', 'ROUTE_ID', 'RID', 'DL', 'POINT_X', 'POINT_Y', 'POINT_Z', 'POINT_M', 'x_kod', 'rodzaj', 'opis', 'WSP_n', 'Z', 'RIVER', 'TOPO_ID', 'CHAINAGE', 'COORDINATES', 'COORD_X1', 'COORD_Y1', 'COORD_X2', 'COORD_Y2', 'FLOW_DIR', 'PROTECTION_DATA', 'DATUM', 'CLOSED_SECTION', 'RADIUS_TYPE', 'DIVIDE_X_SECTION', 'SECTION_ID', 'INTERPOLATED', 'ANGLE', 'RESIST_NO', 'PROFILE', 'LEVEL_PARAMS', 'XS_DL', 'XS_Z', 'XS_N', 'XS_MARKER', 'XS_UNK1', 'XS_UNK2', 'XS_UNK3', 'XS_DL2', 'KM', 'ROBO']) as search:
    for row in search:
        print row[3]

        # if prof_disc.has_key(str(row[fields.index('RID')])):
        #     if float(row[fields.index('XS_DL')]) > prof_disc[str(row[fields.index('RID')])][0]:
        #         prof_disc[str(row[fields.index('RID')])][0] = row[fields.index('XS_DL2')]