#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("3D")

"""parametry programu"""

workspace = arcpy.env.workspace = \
    r"E:\Waloryzajca_rzek_WWF\ROBOCZY_KWIECIEN_2023\Zadanie3i4\Warstwy_robocze.gdb"

jcwpr = 'rzeki_glowne_JCWP'
wojtab = 'woj_Statis_dl'
nw = 'nw_Statis3'
zz = 'zz_Statis3'
def wojCount(jcwpr, wojtab):
    woj_jcwpr = {}
    with arcpy.da.SearchCursor(wojtab, ['MS_KOD', 'Nazwa_WOJ', 'SUM_geom_Length']) as cur:
        for row in cur:
            if row[0] not in woj_jcwpr:
                woj_jcwpr[row[0]] = [(row[1], round(row[2],))]
            else:
                i = 0
                for item in woj_jcwpr[row[0]]:
                    if row[2] < item[1]:
                        i += 1
                woj_jcwpr[row[0]].insert(i, (row[1], round(row[2],)))

    del cur
    print("slownik")
    with arcpy.da.UpdateCursor(jcwpr, ['MS_KOD', 'NAZ_WOJ1', 'DL_WOJ1', 'NAZ_WOJ2', 'DL_WOJ2', 'NAZ_WOJ3', 'DL_WOJ3']) as update:
        for row in update:
            if len(woj_jcwpr[row[0]]) == 1:
                row[1] = woj_jcwpr[row[0]][0][0]
                row[2] = woj_jcwpr[row[0]][0][1]
                row[3] = ""
                row[4] = 0
                row[5] = ""
                row[6] = 0
            elif len(woj_jcwpr[row[0]]) == 2:
                row[1] = woj_jcwpr[row[0]][0][0]
                row[2] = woj_jcwpr[row[0]][0][1]
                row[3] = woj_jcwpr[row[0]][1][0]
                row[4] = woj_jcwpr[row[0]][1][1]
                row[5] = ""
                row[6] = 0
            else:
                row[1] = woj_jcwpr[row[0]][0][0]
                row[2] = woj_jcwpr[row[0]][0][1]
                row[3] = woj_jcwpr[row[0]][1][0]
                row[4] = woj_jcwpr[row[0]][1][1]
                row[5] = woj_jcwpr[row[0]][2][0]
                row[6] = woj_jcwpr[row[0]][2][1]

            update.updateRow(row)

    del update
    return

def zznwCount(jcwpr, nwtab, zztab):
    nw_jcwpr = {}
    zz_jcwpr = {}
    with arcpy.da.SearchCursor(nwtab, ['MS_KOD', 'NW']) as cur:
        for row in cur:
            if row[0] not in nw_jcwpr:
                nw_jcwpr[row[0]] = [row[1]]
            else:
                nw_jcwpr[row[0]].append(row[1])
    del cur
    print("slownik_NW")

    with arcpy.da.SearchCursor(zztab, ['MS_KOD', 'ZZ']) as cur:
        for row in cur:
            if row[0] not in zz_jcwpr:
                zz_jcwpr[row[0]] = [row[1]]
            else:
                zz_jcwpr[row[0]].append(row[1])
    del cur

    print("slownik_ZZ")

    with arcpy.da.UpdateCursor(jcwpr, ['MS_KOD', 'NW_1', 'NW_2', 'NW_3', 'NW_4', 'NW_5', 'ZZ_1', 'ZZ_2']) as update:
        for row in update:
            lNW = len(nw_jcwpr[row[0]])
            lZZ = len(zz_jcwpr[row[0]])
            for i in range(0, lNW):
                row[1+i] = nw_jcwpr[row[0]][i]
            for j in range(0, lZZ):
                row[6+j] = zz_jcwpr[row[0]][j]

            update.updateRow(row)

    del update
    return

zznwCount(jcwpr, nw, zz)