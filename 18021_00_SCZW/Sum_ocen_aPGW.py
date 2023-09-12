#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True
import time

"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

arcpy.env.workspace=ws=ur'P:\Projekty_2017\18021-00_SZCW\07.GIS\02_Analizy\_Wyznaczenie_SZCW_screening_automatyczny\wyzn_SCZW.gdb'

stat_JCWP_aPGW='Status_JCWP_rzeczne'
JCWP='JCWP_rzeczne_2'


def Sum_ocena(JCWP,stat_JCWP_aPGW):
    print "realizuje sumowanie ocen stanu JCWP z aPGW"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    with arcpy.da.UpdateCursor(JCWP,kol)as cur:
        for row in cur:
            wst=[]
            ost=[]
            with arcpy.da.SearchCursor(stat_JCWP_aPGW,['KOD_JCWP','Status_wst','Status_os'])as cur2:
                for row2 in cur2:
                    if row2[0] in [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]]:
                        ost.append(row2[2])
                        wst.append(row2[1])
            del cur2
            row[kol.index('WST_NAT')]=wst.count('NAT')
            row[kol.index('WST_SCW')]=wst.count('SCW')
            row[kol.index('WST_SZCW')]=wst.count('SZCW')
            row[kol.index('OST_NAT')]=ost.count('NAT')
            row[kol.index('OST_SCW')]=ost.count('SCW')
            row[kol.index('OST_SZCW')]=ost.count('SZCW')
            cur.updateRow(row)
    del cur

    print "zakonczono sumowanie ocen stanu JCWP z aPGW - ", round((time.time() - start_time)/60, 2), "min " # 5.04 min
    return

Sum_ocena(JCWP,stat_JCWP_aPGW)
