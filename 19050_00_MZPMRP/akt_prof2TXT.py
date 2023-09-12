#!/usr/bin/env python
# -*- coding: utf-8 -*-

# skrypt do utworzenia raportu z posortowanej tabeli zaktualizowanych przekroi

import os
import arcpy

workspace = \
    arcpy.env.workspace = \
    r"R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\2_Opracowanie_danych_do_modeli\etap 3\2_przedluzone\Jeziorsko\3_iteracja\przedluzanie_przekroi.gdb"

tab = 'przedluzenia_WARTA_tab_SORT2'
tab_HL = 'WARTA_S10_HL'

file_dir =\
    r"R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\2_Opracowanie_danych_do_modeli\etap 3\2_przedluzone\Jeziorsko\3_iteracja\S10_Warta_aktualizacja_27012021.txt"

f = open(file_dir, "w")

fields = []
for field in arcpy.ListFields(tab):
    fields.append(str(field.name))
prof_disc = {}

with arcpy.da.SearchCursor(tab, fields) as search:
    for row in search:

        if prof_disc.has_key(str(row[fields.index('RID')])):
            if float(row[fields.index('XS_DL')]) > prof_disc[str(row[fields.index('RID')])][0]:
                prof_disc[str(row[fields.index('RID')])][0] = row[fields.index('XS_DL2')]

        else:
            prof_disc[str(row[fields.index('RID')])] = [
                row[fields.index('XS_DL2')],
                str(row[fields.index('RIVER')]),
                str(row[fields.index('TOPO_ID')]),
                str(row[fields.index('CHAINAGE')]),
                str(row[fields.index('COORDINATES')]),
                str(row[fields.index('FLOW_DIR')]),
                str(row[fields.index('PROTECTION_DATA')]),
                str(row[fields.index('DATUM')]),
                str(row[fields.index('CLOSED_SECTION')]),
                str(row[fields.index('RADIUS_TYPE')]),
                str(row[fields.index('DIVIDE_X_SECTION')]),
                str(row[fields.index('SECTION_ID')]),
                str(row[fields.index('INTERPOLATED')]),
                str(row[fields.index('ANGLE')]),
                str(row[fields.index('RESIST_NO')]),
                str(row[fields.index('PROFILE')]),
                str(row[fields.index('LEVEL_PARAMS')])
            ]
del search

fields_hl = []
for field in arcpy.ListFields(tab_HL):
    fields_hl.append(str(field.name))

hl_dict = {}
with arcpy.da.SearchCursor(tab_HL, fields_hl) as search:
    for row in search:
        if hl_dict.has_key(str(row[fields_hl.index('RID')])):
            hl_dict[str(row[fields_hl.index('RID')])].append(str(row[fields_hl.index('H_LEVEL')]))

        else:
            hl_dict[str(row[fields_hl.index('RID')])] = list()
            hl_dict[str(row[fields_hl.index('RID')])].append(str(row[fields_hl.index('H_LEVEL')]))

del search

print '1 - utworzono slownik z danymi z tabeli punktow profili i tabeli h - levels'


for item in prof_disc.iteritems():
    if item[1][8] == 'NIE DOTYCZY':
        f.write(
            item[1][2] + '\n' +
            item[1][1] + '\n' +
            item[1][3] + '\n' +
            'COORDINATES' + '\n' + item[1][4] + '\n' +
            'FLOW DIRECTION' + '\n' + item[1][5] + '\n' +
            'PROTECT DATA' + '\n' + item[1][6] + '\n' +
            'DATUM' + '\n' + item[1][7] + '\n' +
            'RADIUS TYPE' + '\n' + item[1][9] + '\n' +
            'DIVIDE X-Section' + '\n' + item[1][10] + '\n' +
            'SECTION ID' + '\n' + item[1][11] + '\n' +
            'INTERPOLATED' + '\n' + item[1][12] + '\n' +
            'ANGLE' + '\n' + item[1][13] + '\n' +
            'RESISTANCE NUMBERS' + '\n' + item[1][14] + '\n' +
            'PROFILE' + '  ' + item[1][15] + '\n'
        )
        with arcpy.da.SearchCursor(tab, fields) as search:
            for row in search:
                if item[0] == str(row[fields.index('RID')]):
                    f.write(str(row[fields.index('XS_DL')]) + '  ' + str(row[fields.index('XS_Z')]) + '  ' + str(
                        row[fields.index('XS_N')]) + '  ' + str(row[fields.index('XS_MARKER')]) + '  ' + str(
                        row[fields.index('XS_UNK1')]) + '  ' + str(row[fields.index('XS_UNK2')]) + '  ' + str(
                        row[fields.index('XS_UNK3')]) + '\n')
        del search

        if hl_dict.has_key(item[0]):
            f.write('LEVEL PARAMS' + '\n' + item[1][16] + '\n')
            f.write('H-LEVELS' + '       ' + str(len(hl_dict[item[0]])) + '\n')
            for level in hl_dict[item[0]]:
                f.write(level + '\n')
        else:
            f.write('LEVEL PARAMS' + '\n' + item[1][16] + '\n')
        f.write('*******************************' + '\n')
    else:
        f.write(
            item[1][2] + '\n' +
            item[1][1] + '\n' +
            item[1][3] + '\n' +
            'COORDINATES' + '\n' + item[1][4] + '\n' +
            'FLOW DIRECTION' + '\n' + item[1][5] + '\n' +
            'PROTECT DATA' + '\n' + item[1][6] + '\n' +
            'DATUM' + '\n' + item[1][7] + '\n' +
            'CLOSED SECTION' + '\n' + item[1][8] + '\n' +
            'RADIUS TYPE' + '\n' + item[1][9] + '\n' +
            'DIVIDE X-Section' + '\n' + item[1][10] + '\n' +
            'SECTION ID' + '\n' + item[1][11] + '\n' +
            'INTERPOLATED' + '\n' + item[1][12] + '\n' +
            'ANGLE' + '\n' + item[1][13] + '\n' +
            'RESISTANCE NUMBERS' + '\n' + item[1][14] + '\n' +
            'PROFILE' + '  ' + item[1][15] + '\n'
        )
        with arcpy.da.SearchCursor(tab, fields) as search:
            for row in search:
                if item[0] == str(row[fields.index('RID')]):
                    f.write(str(row[fields.index('XS_DL')]) + '  ' + str(row[fields.index('XS_Z')]) + '  ' + str(
                        row[fields.index('XS_N')]) + '  ' + str(row[fields.index('XS_MARKER')]) + '  ' + str(
                        row[fields.index('XS_UNK1')]) + '  ' + str(row[fields.index('XS_UNK2')]) + '  ' + str(
                        row[fields.index('XS_UNK3')]) + '\n')
        del search

        if hl_dict.has_key(item[0]):
            f.write('LEVEL PARAMS' + '\n' + item[1][16] + '\n')
            f.write('H-LEVELS' + '       ' + str(len(hl_dict[item[0]])) + '\n')
            for level in hl_dict[item[0]]:
                f.write(level + '\n')
        else:
            f.write('LEVEL PARAMS' + '\n' + item[1][16] + '\n')
        f.write('*******************************' + '\n')
f.close()

print 'koniec ', tab
