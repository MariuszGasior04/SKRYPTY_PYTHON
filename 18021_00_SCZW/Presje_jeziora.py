#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do zbierania informacji o prasjach JCWP jezior na podstawie bazy HYMO.

import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True
import time

"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

arcpy.env.workspace=ws=ur'P:\Projekty_2017\18021-00_SZCW\07.GIS\02_Analizy\_wskazniki_dla_jezior\Analizy.gdb'

jez='JCWP_jeziorne_2'
bud_p='BUD_P'
kol=[]
kol_budp=[]

for field in arcpy.ListFields(jez):
        kol.append(str(field.name))

for field in arcpy.ListFields(bud_p):
        kol_budp.append(str(field.name))

with arcpy.da.SearchCursor(jez,kol) as cur:
    for row in cur:
        if  row[kol.index('WYNIK_SCREENING')]==1:

            with arcpy.da.SearchCursor(bud_p,kol_budp) as curbudp:
                for row_budp in curbudp:
                    if  row[kol.index('KOD')]==row_budp[kol_budp.index('KOD_JCWP_jez')]:

                        if row_budp[kol_budp.index('ID_BP')] is None:
                            ID_BP='0'
                        else:
                            ID_BP=row_budp[kol_budp.index('ID_BP')]

                        BP='1'

                        if row_budp[kol_budp.index('funk_ob')] is None:
                            FUN_BP='brak danych'
                        else:
                            FUN_BP=row_budp[kol_budp.index('funk_ob')]

                        if row_budp[kol_budp.index('RODZ_BUD')] is None:
                            RODZ_BP='brak danych'
                        else:
                            RODZ_BP=row_budp[kol_budp.index('RODZ_BUD')]

                        if row_budp[kol_budp.index('WYS_P')] is None:
                            WYS_BP='brak danych'
                        else:
                            WYS_BP=row_budp[kol_budp.index('WYS_P')]

                        if row_budp[kol_budp.index('max_pp')] is None or row_budp[kol_budp.index('nor_pp')] is None:
                            WAH_BP='brak danych'

                        else:
                            WAH_BP=row_budp[kol_budp.index('max_pp')]-row_budp[kol_budp.index('nor_pp')]


                        print row[kol.index('KOD')],"&",row[kol.index('NAZWA')],"&",row[kol.index('RZGW')],"&",row[kol.index('ZZ_miasto')],"&", ID_BP,"&", BP,"&", FUN_BP,"&", RODZ_BP,"&", WYS_BP,"&", WAH_BP
