#!/usr/bin/env python
# -*- coding: utf-8 -*-

# skrypt do synchronizacji warstwy punktow na przekrojach przedluzanych z punktami istniejacych przekroi z modelu MIKE. Finalnie po udanym przejsciu skryptu można połączyc tabelę warstwy punktow z tabela punktow przekroi z modelu MIKE

import arcpy

workspace = arcpy.env.workspace = \
    r"R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\2_Opracowanie_danych_do_modeli\etap 3\2_przedluzone\Jeziorsko\3_iteracja\przedluzanie_przekroi.gdb"

##punkty na przekrojach przedluzanych !!! warstwa punktow profili przedluzanych musi posiadac wszystkie atrybuty tabeli z modelu MIKE
pkt_prof = 'przedluzenia_WARTA_pkt_2_opracowane'

##tabela z punktami na profilach z modelu MIKE
tab = 'WARTA_S10_RD_LP'

wsp_prof = {}

with arcpy.da.SearchCursor(pkt_prof, ['ROUTE_ID', 'WSP_n', 'DL', 'Z', 'POINT_X', 'POINT_Y'])as search:
    ## atrybut ROUTE_ID w PUNKTACH musi składac się z klucza RZEKA_KILOMETRAZ_BRZEG np. RABA_12345_LEWY
    for row in search:
        if str(row[0]).split('_')[-1] == 'LEWY':

            if len(wsp_prof.keys()) == 0:
                wsp_prof[str(row[0])] = [0, str(round(row[4], 3)).replace(',', '.'),
                                         str(round(row[5], 3)).replace(',', '.'), round(row[2], 3)]

            if wsp_prof.has_key(str(row[0])):
                if wsp_prof[str(row[0])][3] < row[2]:
                    wsp_prof[str(row[0])][3] = round(row[2], 3)

                if row[2] == 0:
                    wsp_prof[str(row[0])][1] = str(round(row[4], 3)).replace(',', '.')
                    wsp_prof[str(row[0])][2] = str(round(row[5], 3)).replace(',', '.')

            else:
                wsp_prof[str(row[0])] = [0, str(round(row[4], 3)).replace(',', '.'),
                                         str(round(row[5], 3)).replace(',', '.'), round(row[2], 3)]

        if str(row[0]).split('_')[-1] == 'PRAWY':

            if len(wsp_prof.keys()) == 0:
                wsp_prof[str(row[0])] = [0, str(round(row[4], 3)).replace(',', '.'),
                                         str(round(row[5], 3)).replace(',', '.'), round(row[2], 3)]

            if wsp_prof.has_key(str(row[0])):
                if wsp_prof[str(row[0])][3] < row[2]:
                    wsp_prof[str(row[0])][3] = round(row[2], 3)
                    wsp_prof[str(row[0])][1] = str(round(row[4], 3)).replace(',', '.')
                    wsp_prof[str(row[0])][2] = str(round(row[5], 3)).replace(',', '.')

            else:
                wsp_prof[str(row[0])] = [0, str(round(row[4], 3)).replace(',', '.'),
                                         str(round(row[5], 3)).replace(',', '.'), round(row[2], 3)]
del search

print '1 - utworzono slownik wspolrzednych koncy profili do zaktualizowania wspolrzednych i dlugosci w profilach MIKE'

fields = []
for field in arcpy.ListFields(tab):
    fields.append(str(field.name))

field_types = []
for field in arcpy.ListFields(tab):
    field_types.append((str(field.name), str(field.type)))

with arcpy.da.UpdateCursor(tab, fields) as update:
    ## atrybut RID w TABELI musi składac się z klucza RZEKA_KILOMETRAZ np. RABA_12345
    for row in update:
        if wsp_prof.has_key(str(row[fields.index('RID')]) + '_LEWY'):
            X1 = wsp_prof[str(row[fields.index('RID')]) + '_LEWY'][1]

            if ('XS_DL', 'String') in field_types:
                row[fields.index('XS_DL')] = str(
                    float(row[fields.index('XS_DL')]) + wsp_prof[str(row[fields.index('RID')]) + '_LEWY'][3])
            elif ('XS_DL', 'Double') in field_types:
                dl = float(row[fields.index('XS_DL')]) + wsp_prof[str(row[fields.index('RID')]) + '_LEWY'][3]
                row[fields.index('XS_DL')] = dl
        else:
            X1 = str(row[fields.index('COORD_X1')])

        if wsp_prof.has_key(str(row[fields.index('RID')]) + '_LEWY'):
            Y1 = wsp_prof[str(row[fields.index('RID')]) + '_LEWY'][2]
        else:
            Y1 = str(row[fields.index('COORD_Y1')])

        if wsp_prof.has_key(str(row[fields.index('RID')]) + '_PRAWY'):
            X2 = wsp_prof[str(row[fields.index('RID')]) + '_PRAWY'][1]
        else:
            X2 = str(row[fields.index('COORD_X2')])

        if wsp_prof.has_key(str(row[fields.index('RID')]) + '_PRAWY'):
            Y2 = wsp_prof[str(row[fields.index('RID')]) + '_PRAWY'][2]
        else:
            Y2 = str(row[fields.index('COORD_Y2')])

        row[fields.index('COORDINATES')] = '%5d  %10s  %10s  %10s  %10s' % (2, X1, Y1, X2, Y2)

        update.updateRow(row)

del update

print '2 - zaktualizowano XS_DL i COORDINATES w tabeli profili MIKE'

akt_dl = {}
with arcpy.da.SearchCursor(tab, fields)as search:
    for row in search:

        if akt_dl.has_key(str(row[fields.index('RID')])):
            if float(row[fields.index('XS_DL')]) > akt_dl[str(row[fields.index('RID')])][0]:
                akt_dl[str(row[fields.index('RID')])] = [float(row[fields.index('XS_DL')]),
                                                         row[fields.index('COORDINATES')]]
        else:
            akt_dl[str(row[fields.index('RID')])] = [float(row[fields.index('XS_DL')]),
                                                     row[fields.index('COORDINATES')]]

del search

print '3 - utworzono slownik wspolrzednych koncy profili i dlugosci do zaktualizowania prawych wydluzen profili'

fields = []
for field in arcpy.ListFields(pkt_prof):
    fields.append(str(field.name))

field_types = []
for field in arcpy.ListFields(pkt_prof):
    field_types.append((str(field.name), str(field.type)))

with arcpy.da.UpdateCursor(pkt_prof, fields) as update:
    for row in update:
        row[fields.index('XS_MARKER')] = '<#0>'

        if ('XS_N', 'String') in field_types:
            row[fields.index('XS_N')] = str(row[fields.index('WSP_n')])

        else:
            row[fields.index('XS_N')] = round(float(row[fields.index('WSP_n')]), 3)

        if ('XS_Z', 'String') in field_types:
            row[fields.index('XS_Z')] = str(round(row[fields.index('Z')], 3))

        else:
            row[fields.index('XS_Z')] = float(round(row[fields.index('Z')], 3))

        row[fields.index('COORDINATES')] = akt_dl[str(row[fields.index('RID')])][1]

        if str(row[fields.index('ROUTE_ID')]).split('_')[-1] == 'LEWY':
            if ('XS_DL', 'String') in field_types:
                row[fields.index('XS_DL')] = str(round(row[fields.index('DL')], 3))

            else:
                row[fields.index('XS_DL')] = float(round(row[fields.index('DL')], 3))
        else:
            if ('XS_DL', 'String') in field_types:
                row[fields.index('XS_DL')] = str(
                    round(row[fields.index('DL')] + akt_dl[str(row[fields.index('RID')])][0], 3))

            else:
                row[fields.index('XS_DL')] = float(
                    round(row[fields.index('DL')] + akt_dl[str(row[fields.index('RID')])][0], 3))

        update.updateRow(row)

del update

print '4 - zakonczono synchronizacje - ', pkt_prof, tab
