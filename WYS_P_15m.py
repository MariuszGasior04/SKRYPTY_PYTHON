#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy

arcpy.env.overwriteOutput = True

arcpy.env.workspace = ws =\
    r'D:\FolderRoboczy\budowle_pietrzace\bud_p_marian2.gdb'

budowle = 'ddp2'
pkt_prof = 'Odcinki_rzek_budowli_all_pkt_sort'


#tworzenie słownika z profilami (szybciej dziala niz operacje na tabeli w geobazie)
pkt_dict = {}
with arcpy.da.SearchCursor(pkt_prof, ['ID_NEW', 'cngmetry','Z'])as search:
    for row in search:

        # if pkt_dict.has_key(str(row[0])):
        #     pkt_dict[str(row[0])].append([row[1], round(row[2], 2)])
        # else:
        #     pkt_dict[str(row[0])] = [[row[1], round(row[2], 2)]]
        if pkt_dict.has_key(str(row[0])):
            pkt_dict[str(row[0])].append(round(row[2], 2))
        else:
            pkt_dict[str(row[0])] = [round(row[2], 2)]

del search

def findPP(id_new, profile):
    wys_p = 0
    for i in range(0, len(profile[id_new])-8):
        zakres = max(profile[id_new][i:i+8])-min(profile[id_new][i:i+8])
        if zakres > wys_p:
            wys_p = zakres
    return wys_p


with arcpy.da.UpdateCursor(budowle,
                           ['ID_NEW', 'ANALIZ_PROFIL', 'WYS_P2'])as cur:
    for row in cur:
        if row[1] == 1:
            row[2] = findPP(str(row[0]), pkt_dict)
        print(row[0], row[2])
        cur.updateRow(row)

del cur