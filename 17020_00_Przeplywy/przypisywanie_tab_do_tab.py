#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do okreslania kilometrazu obiektow wzgledemi ich obiektow gazociagu.

import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True
import time
"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

arcpy.env.workspace=ws=ur'P:\Projekty_2017\17020-00 Przepływy_Środowiskowe\08. Produkty I etapu 2017\Baza\shp'

shp='JED_HYDROMORF.shp'
tab='JED_HYDROMORF_tab.dbf'
kol1=[]
kol2=[]

for field in arcpy.ListFields(shp):
    kol1.append(str(field.name))

for field in arcpy.ListFields(tab):
    kol2.append(str(field.name))

kol1.index
with arcpy.da.UpdateCursor(shp,kol1)as cur:
    for row in cur:
        with arcpy.da.SearchCursor(tab,kol2)as cur2:
            for row2 in cur2:
                if row[kol1.index('NrOdcRef')]==row2[kol2.index('NrOdcRef')] and row[kol1.index('NrJHM')]==row2[kol2.index('NrJHM')]:
                    row[kol1.index('DataBad')]=row2[kol2.index('DataBad')]
                    row[kol1.index('SrGle')]=row2[kol2.index('SrGle')]
                    row[kol1.index('SrV')]=row2[kol2.index('SrV')]
                    row[kol1.index('ObeBioOdp')]=row2[kol2.index('ObeBioOdp')]
                    row[kol1.index('ObeBioGal')]=row2[kol2.index('ObeBioGal')]
                    row[kol1.index('ObeBioOsa')]=row2[kol2.index('ObeBioOsa')]
                    row[kol1.index('ObeBioRes')]=row2[kol2.index('ObeBioRes')]
                    row[kol1.index('ObeBioDeb')]=row2[kol2.index('ObeBioDeb')]
                    row[kol1.index('ObeBioMul')]=row2[kol2.index('ObeBioMul')]
                    row[kol1.index('KryRybMak')]=row2[kol2.index('KryRybMak')]
                    row[kol1.index('KryRybWeg')]=row2[kol2.index('KryRybWeg')]
                    row[kol1.index('KryRybPly')]=row2[kol2.index('KryRybPly')]
                    row[kol1.index('KryRybZwa')]=row2[kol2.index('KryRybZwa')]
                    row[kol1.index('KryRybKam')]=row2[kol2.index('KryRybKam')]
                    row[kol1.index('KryRybOci')]=row2[kol2.index('KryRybOci')]
                    row[kol1.index('Uwagi')]=row2[kol2.index('Uwagi')]
                    row[kol1.index('Seria')]=row2[kol2.index('Seria')]
                    cur.updateRow(row)
        del cur2
del cur

print 'koniec'