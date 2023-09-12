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
JCWP='JCWP_rzeczne_3test'


def Sum_ocena(JCWP,stat_JCWP_aPGW):
    print "realizuje sumowanie JCWP z aPGW po wskaznikach i1, i2, i3, m3, eks"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    with arcpy.da.UpdateCursor(JCWP,kol)as cur:
        for row in cur:
            wst=[]
            ost=[]
            sum_i1 = 0
            sum_i2 = 0
            sum_i3 = 0
            sum_m3 = 0
            eks = 0
            aPGW = [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]]

            for jcwp in aPGW[0:row[kol.index('IL_JCWP_aPGW')]]:
                with arcpy.da.SearchCursor(stat_JCWP_aPGW,['KOD_JCWP','Status_wst','Status_os','DL','i1','i2','i3','m3','eks'])as cur2:
                    for row2 in cur2:
                        if row2[0] == jcwp:
                            if row2[4] == 1:
                                sum_i1 = sum_i1 + row2[3]
                            if row2[5] == 1:
                                sum_i2 = sum_i2 + row2[3]
                            if row2[6] == 1:
                                sum_i3 = sum_i3 + row2[3]
                            if row2[7] == 1:
                                sum_m3 = sum_m3 + row2[3]
                            if row2[8] == 1:
                                eks = eks + row2[3]

                del cur2

            row[kol.index('i1')] = sum_i1
            row[kol.index('i2')] = sum_i2
            row[kol.index('i3')] = sum_i3
            row[kol.index('m3')] = sum_m3
            row[kol.index('eks')] = eks

            cur.updateRow(row)
    del cur

    print "zakonczono sumowanie dlugosci rzek na podstawie - ", round((time.time() - start_time)/60, 2), "min " # 5.04 min
    return

Sum_ocena(JCWP,stat_JCWP_aPGW)
