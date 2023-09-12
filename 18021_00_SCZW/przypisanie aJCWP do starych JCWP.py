#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True
import time

"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

arcpy.env.workspace=ws=ur'P:\Projekty_2017\18021-00_SZCW\07.GIS\02_Analizy\_wskazniki_dla_rzek\_Przypisanie_JCWP.gdb'

old_JCWP='JCWP_stare'
aJCWP='aJCWP_rzeczne'

def przyp(aJCWP,old_JCWP):
    kol=[]
    for field in arcpy.ListFields(aJCWP):
        kol.append(str(field.name))

    with arcpy.da.UpdateCursor(old_JCWP,['RWB_MS_CD','NOWA_JCWP'])as cur2:
        for row2 in cur2:
            with arcpy.da.SearchCursor(aJCWP,kol)as cur:
                for row in cur:
                    if row2[0] in [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]]:
                        row2[1] = row[kol.index('MS_KOD')]
                        cur2.updateRow(row2)
            del cur


    del cur2

    print "zakonczono przypis"
    return

przyp(aJCWP,old_JCWP)