#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do okreslania kilometrazu obiektow wzgledemi ich obiektow gazociagu.

import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True
import time

"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

arcpy.env.workspace=ws=ur'P:\Projekty_2017\18021-00_SZCW\07.GIS\02_Analizy\_Wyznaczenie_SZCW_screening_automatyczny\wyzn_SCZW.gdb'

char_JCWP_aPGW='Charakterystyka_JCWP_rzeczne_aPGW'
stat_JCWP_aPGW='Status_JCWP_rzeczne'
ods_JCWP_aPGW='Presja_ryzyko_odstępstwa_JCWP_rzeczne'
ocena_JCWP_aPGW='Ocena_stanu_JCWP_rzeczne'
monit='monit_2016'
monit_2017='monit_2017'
JCWP='JCWP_rzeczne_3test'
ocena_JCWP_2017='stan_pot_2017'

"""KROK 1"""
def Krok1(JCWP):
    print "realizuje Krok 1"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    with arcpy.da.UpdateCursor(JCWP,kol)as cur:
        for row in cur:
            if row[kol.index('TYP')]==u'typu nie określa się' and row[kol.index('KROK')] is None:
                row[kol.index('KROK')]=10
                cur.updateRow(row)
    del cur

    print "zakonczono Krok 1 - ", round((time.time() - start_time)/60, 2), "min " # 0.05 min
    return

"""KROK 2"""
def Krok2(JCWP,char_JCWP_aPGW):
    print "realizuje Krok 2"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    with arcpy.da.SearchCursor(char_JCWP_aPGW,['KOD_JCWP','TYP_JCW'])as cur2:
        for row2 in cur2:
            if row2[1]=='0':
                with arcpy.da.UpdateCursor(JCWP,kol)as cur:
                    for row in cur:
                        if row2[0] in [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]] and row[kol.index('KROK')] is None:
                            row[kol.index('KROK')]=2
                            cur.updateRow(row)
                del cur
    del cur2
    print"redukcja 2"
    with arcpy.da.UpdateCursor(JCWP,kol) as cur:
        for row in cur:
            if row[kol.index('KROK')]=='2':
                lista = [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]]
                dl_nat=0
                dl_szcw=0
                with arcpy.da.SearchCursor(char_JCWP_aPGW,['KOD_JCWP','DL_KM','Status_os']) as cur2:
                    for row2 in cur2:
                        for jcwp in lista[0:row[kol.index('IL_JCWP_aPGW')]]:
                            if str(jcwp) == str(row2[0]) and str(row2[2])=='NAT':
                                dl_nat = dl_nat + row2[1]

                            elif str(jcwp) == str(row2[0]) and str(row2[2])=='SZCW':
                                dl_szcw = dl_szcw + row2[1]

                            elif str(jcwp) == str(row2[0]) and str(row2[2])=='SCW':
                                dl_szcw = dl_szcw + row2[1]

                    if dl_nat + dl_szcw > 0 and dl_nat*100/(dl_nat+dl_szcw) < 75:
                        row[kol.index('KROK')] = '10_2'
                        cur.updateRow(row)

                    elif dl_nat + dl_szcw > 0 and dl_nat*100/(dl_nat+dl_szcw) >= 75:
                        row[kol.index('KROK')] = 4
                        cur.updateRow(row)
                del cur2
    del cur

    print "zakonczono Krok 2 - ", round((time.time() - start_time)/60, 2), "min " # 1.27 min
    return

"""KROK 3"""
def Krok3(JCWP,char_JCWP_aPGW,stat_JCWP_aPGW):
    print "realizuje Krok 3"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    with arcpy.da.SearchCursor(char_JCWP_aPGW,['KOD_JCWP','TYP_JCW'])as cur2:
        for row2 in cur2:
            if row2[1]=='1':
                with arcpy.da.SearchCursor(stat_JCWP_aPGW,['KOD_JCWP','Status_os'])as cur3:
                    for row3 in cur3:
                        if row3[0]==row2[0] and row3[1]==u'SZCW':
                            with arcpy.da.UpdateCursor(JCWP,kol)as cur:
                                for row in cur:
                                    if row2[0] in [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]] and (row[kol.index('KROK')] is None or row[kol.index('KROK')] == '4'):
                                        row[kol.index('KROK')]=3
                                        cur.updateRow(row)
                            del cur
                del cur3
    del cur2
    print "zakonczono Krok 3 - ", round((time.time() - start_time)/60, 2), "min " # 0.05 min
    return

"""KROK 4"""
def Krok4(JCWP,ods_JCWP_aPGW):
    print "realizuje Krok 4"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    with arcpy.da.SearchCursor(ods_JCWP_aPGW,['KOD_JCWP','ODST_47'])as cur2:
        for row2 in cur2:
            if row2[1]==u'4(7)':
                with arcpy.da.UpdateCursor(JCWP,kol)as cur:
                    for row in cur:
                        if row2[0] in [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]] and row[kol.index('KROK')] is None:
                            row[kol.index('KROK')]=4
                            cur.updateRow(row)
                del cur
    del cur2
    print "zakonczono Krok 4 - ", round((time.time() - start_time)/60, 2), "min " # 4.52 min
    return

"""KROK 5"""
def Krok5(JCWP,ocena_JCWP_aPGW):
    print "realizuje Krok 5"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    with arcpy.da.SearchCursor(ocena_JCWP_aPGW,['KOD_JCWP','S_P_eko'])as cur2:
        for row2 in cur2:
            if row2[1] in [u'BARDZO DOBRY', u'CO NAJMNIEJ DOBRY', u'DOBRY', u'DOBRY i POWYŻEJ DOBREGO', u'DOBRY I POWYŻEJ DOBREGO']:
                with arcpy.da.UpdateCursor(JCWP,kol)as cur:
                    for row in cur:
                        if row2[0] in [row[kol.index('ST_KOD_1')]] and row[kol.index('ST_KOD_2')]==u'' and (row[kol.index('KROK')] is None or row[kol.index('KROK')] == '4'):
                            row[kol.index('KROK')]=5
                            cur.updateRow(row)
                del cur
    del cur2

    with arcpy.da.UpdateCursor(JCWP,kol) as cur:
        for row in cur:
            if row[kol.index('KROK')]=='5':
                lista = [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]]
                war = []
                for jcwp in lista[0:row[kol.index('IL_JCWP_aPGW')]]:
                    with arcpy.da.SearchCursor(ocena_JCWP_aPGW,['KOD_JCWP','DL','DETER'])as cur2:
                        for row2 in cur2:
                            if jcwp == row2[0] and row2[2] == 1:
                                war.append(1)
                    del cur2
                if len(war) == len(lista[0:row[kol.index('IL_JCWP_aPGW')]]):
                    row[kol.index('KROK')]=5
                    cur.updateRow(row)
                else:
                    row[kol.index('KROK')]=4
                    cur.updateRow(row)
    del cur
    print "zakonczono Krok 5 - ", round((time.time() - start_time)/60, 2), "min " # 10.20 min
    return

"""KROK 6"""
def Krok6(JCWP,ocena_JCWP_aPGW):
    print "realizuje Krok 6"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    with arcpy.da.UpdateCursor(JCWP,kol)as cur:
        for row in cur:
            if (row[kol.index('KROK')] is None or row[kol.index('KROK')]== '4'):
                aPGW = [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]]
                war=[]
                for st_kod in aPGW:
                    if st_kod !='':
                        with arcpy.da.SearchCursor(ocena_JCWP_aPGW,['KOD_JCWP','S_P_eko'])as cur2:
                            for row2 in cur2:
                                if row2[1] in [u'BARDZO DOBRY', u'CO NAJMNIEJ DOBRY', u'DOBRY', u'DOBRY i POWYŻEJ DOBREGO', u'DOBRY I POWYŻEJ DOBREGO'] and row2[0]==st_kod:
                                    war.append(1)
                                elif row2[1] not in [u'BARDZO DOBRY', u'CO NAJMNIEJ DOBRY', u'DOBRY', u'DOBRY i POWYŻEJ DOBREGO', u'DOBRY I POWYŻEJ DOBREGO'] and row2[0]==st_kod:
                                    war.append(0)
                        del cur2
                if 0 not in war and len(war)>0:
                    row[kol.index('KROK')]=6
                    cur.updateRow(row)
    del cur

    with arcpy.da.UpdateCursor(JCWP,kol) as cur:
        for row in cur:
            if row[kol.index('KROK')]=='6':
                lista = [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]]
                war = []
                for jcwp in lista[0:row[kol.index('IL_JCWP_aPGW')]]:
                    with arcpy.da.SearchCursor(ocena_JCWP_aPGW,['KOD_JCWP','DL','DETER'])as cur2:
                        for row2 in cur2:
                            if jcwp == row2[0] and row2[2] == 1:
                                war.append(1)
                    del cur2
                if len(war) == len(lista[0:row[kol.index('IL_JCWP_aPGW')]]):
                    row[kol.index('KROK')]=6
                    cur.updateRow(row)
                else:
                    row[kol.index('KROK')]=4
                    cur.updateRow(row)
    del cur

    print "zakonczono Krok 6 - ", round((time.time() - start_time)/60, 2), "min " # 6.32 min
    return

"""KROK 7"""
def Krok7(JCWP,ocena_JCWP_aPGW):
    print "realizuje Krok 7"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    with arcpy.da.UpdateCursor(JCWP,kol)as cur:
        for row in cur:
            if row[kol.index('KROK')] is None or row[kol.index('KROK')]== '4':
                aPGW = [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]]
                war_dobry=0
                war_zly=0
                for st_kod in aPGW:
                    if st_kod !='':
                        with arcpy.da.SearchCursor(ocena_JCWP_aPGW,['KOD_JCWP','S_P_eko','DL'])as cur2:
                            for row2 in cur2:
                                if row2[1] in [u'BARDZO DOBRY', u'CO NAJMNIEJ DOBRY', u'DOBRY', u'DOBRY i POWYŻEJ DOBREGO', u'DOBRY I POWYŻEJ DOBREGO'] and row2[0]==st_kod:
                                    war_dobry = war_dobry + row2[2]
                                elif row2[1] not in [u'BARDZO DOBRY', u'CO NAJMNIEJ DOBRY', u'DOBRY', u'DOBRY i POWYŻEJ DOBREGO', u'DOBRY I POWYŻEJ DOBREGO'] and row2[0]==st_kod:
                                    war_zly = war_zly + row2[2]
                        del cur2
                if war_dobry+war_zly==0:
                    continue
                elif war_dobry*100/(war_dobry+war_zly)>75:
                    row[kol.index('KROK')]=7
                    cur.updateRow(row)
    del cur

    with arcpy.da.UpdateCursor(JCWP,kol) as cur:
        for row in cur:
            if row[kol.index('KROK')]=='7':
                lista = [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]]
                war = []
                dl_d=0
                dl_z=0
                for jcwp in lista[0:row[kol.index('IL_JCWP_aPGW')]]:
                    with arcpy.da.SearchCursor(ocena_JCWP_aPGW,['KOD_JCWP','DL','DETER'])as cur2:
                        for row2 in cur2:
                            if jcwp == row2[0] and row2[2] == 1:
                                dl_d = dl_d + row2[1]
                            else:
                                dl_z = dl_z + row2[1]
                    del cur2
                if dl_d*100/(dl_d+dl_z) > 75:
                    row[kol.index('KROK')]=7
                    cur.updateRow(row)
                else:
                    row[kol.index('KROK')]=4
                    cur.updateRow(row)
    del cur

    print "zakonczono Krok 7 - ", round((time.time() - start_time)/60, 2), "min " # 6.14 min
    return

"""KROK 8"""
def Krok8(JCWP,ods_JCWP_aPGW):
    print "realizuje Krok 8"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    with arcpy.da.SearchCursor(ods_JCWP_aPGW,['KOD_JCWP','RYZ'])as cur2:
        for row2 in cur2:
            if row2[1] in [u'niezagrożona']:
                with arcpy.da.UpdateCursor(JCWP,kol)as cur:
                    for row in cur:
                        if row2[0] in [row[kol.index('ST_KOD_1')]] and row[kol.index('ST_KOD_2')]==u'' and (row[kol.index('KROK')] is None or row[kol.index('KROK')]== '4'):
                            row[kol.index('KROK')]=8
                            cur.updateRow(row)
                del cur
    del cur2
    print "zakonczono Krok 8 - ", round((time.time() - start_time)/60, 2), "min "
    return

"""KROK 9"""
def Krok9(JCWP,ods_JCWP_aPGW):
    print "realizuje Krok 9"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    with arcpy.da.UpdateCursor(JCWP,kol)as cur:
        for row in cur:
            if row[kol.index('KROK')] is None or row[kol.index('KROK')]== '4':
                aPGW = [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]]
                war=[]
                for st_kod in aPGW:
                    if st_kod !='':
                        with arcpy.da.SearchCursor(ods_JCWP_aPGW,['KOD_JCWP','RYZ'])as cur2:
                            for row2 in cur2:
                                if row2[1] in [u'niezagrożona'] and row2[0]==st_kod:
                                    war.append(1)
                                elif row2[1] not in [u'niezagrożona'] and row2[0]==st_kod:
                                    war.append(0)
                        del cur2
                if 0 not in war and len(war)>0:
                    row[kol.index('KROK')]=9
                    cur.updateRow(row)
    del cur
    print "zakonczono Krok 9 - ", round((time.time() - start_time)/60, 2), "min "
    return

"""KROK 10"""
def Krok10(JCWP,ods_JCWP_aPGW):
    print "realizuje Krok 10"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    with arcpy.da.UpdateCursor(JCWP,kol)as cur:
        for row in cur:
            if row[kol.index('KROK')] is None or row[kol.index('KROK')]== '4':
                aPGW = [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]]
                war_dobry=0
                war_zly=0
                for st_kod in aPGW:
                    if st_kod !='':
                        with arcpy.da.SearchCursor(ods_JCWP_aPGW,['KOD_JCWP','RYZ','DL'])as cur2:
                            for row2 in cur2:
                                if row2[1] in [u'niezagrożona'] and row2[0]==st_kod:
                                    war_dobry = war_dobry + row2[2]
                                elif row2[1] not in [u'niezagrożona'] and row2[0]==st_kod:
                                    war_zly = war_zly + row2[2]
                        del cur2
                if war_dobry+war_zly==0:
                    continue
                elif war_dobry*100/(war_dobry+war_zly)>75:
                    row[kol.index('KROK')]=10
                    cur.updateRow(row)
    del cur
    print "zakonczono Krok 10 - ", round((time.time() - start_time)/60, 2), "min "
    return

"""KROK 11"""
def Krok11(JCWP,monit):
    print "realizuje Krok 11"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    stJCWP=[]
    with arcpy.da.SearchCursor(monit,['KOD_JCWP'])as cur3:
        for row3 in cur3:
            stJCWP.append(row3[0])
    del cur3

    with arcpy.da.UpdateCursor(JCWP,kol)as cur:
        for row in cur:
            if row[kol.index('KROK')] is None or row[kol.index('KROK')]== '4':
                aPGW = [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]]
                war=[]
                for st_kod in aPGW:
                    if st_kod !='':
                        with arcpy.da.SearchCursor(monit,['KOD_JCWP','KLASA_BIOL','KLASA_BENT', 'KLASA_ICHT'])as cur2:
                            for row2 in cur2:
                                if row2[1] in [1,2] and row2[0]==st_kod:
                                    if row2[2] == 0 and row2[3] == 0:
                                        war.append(0)
                                    elif row2[2] < 3 and row2[3] in [1,2]:
                                        war.append(1)
                                    elif row2[3] < 3 and row2[2] in [1,2]:
                                        war.append(1)
                                elif row2[1] not in [1,2] and row2[0]==st_kod:
                                    war.append(0)
                                elif st_kod not in stJCWP:
                                    war.append(0)

                        del cur2
                if 0 not in war and len(war)>0:
                    row[kol.index('KROK')]=8
                    cur.updateRow(row)
    del cur
    print "zakonczono Krok 11 - ", round((time.time() - start_time)/60, 2), "min " # 7.78 min
    return

"""KROK 12"""
def Krok12(JCWP,monit):
    print "realizuje Krok 12"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    stJCWP=[]
    with arcpy.da.SearchCursor(monit,['KOD_JCWP'])as cur3:
        for row3 in cur3:
            stJCWP.append(row3[0])
    del cur3

    with arcpy.da.UpdateCursor(JCWP,kol)as cur:
        for row in cur:
            if row[kol.index('KROK')] is None or row[kol.index('KROK')]== '4':
                aPGW = [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]]
                war=[]
                for st_kod in aPGW:
                    if st_kod !='':
                        with arcpy.da.SearchCursor(monit,['KOD_JCWP','KLASA_BIOL','KLASA_BENT', 'KLASA_ICHT'])as cur2:
                            for row2 in cur2:
                                if row2[1] in [1,2] and row2[0]==st_kod:
                                    if row2[2] == 0 and row2[3] == 0:
                                        war.append(0)
                                    elif row2[2] < 3 and row2[3] in [1,2]:
                                        war.append(1)
                                    elif row2[3] < 3 and row2[2] in [1,2]:
                                        war.append(1)
                                elif row2[1] not in [1,2] and row2[0]==st_kod:
                                    war.append(0)
                                elif st_kod not in stJCWP:
                                    war.append(2)
                        del cur2
                if 0 not in war and 1 in war:
                    row[kol.index('KROK')]=9
                    cur.updateRow(row)
    del cur
    print "zakonczono Krok 12 - ", round((time.time() - start_time)/60, 2), "min " # 7.00 min
    return


"""KROK 11 2017"""
def Krok11_2017(JCWP,ocena_JCWP_2017):
    print "realizuje Krok 11 2017"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    stJCWP=[]
    with arcpy.da.SearchCursor(ocena_JCWP_2017,['KOD_JCWP'])as cur3:
        for row3 in cur3:
            stJCWP.append(row3[0])
    del cur3

    with arcpy.da.UpdateCursor(JCWP,kol)as cur:
        for row in cur:
            if row[kol.index('KROK')] is None or row[kol.index('KROK')]== '4':
                aPGW = [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]]
                war=[]
                for st_kod in aPGW:
                    if st_kod !='':
                        with arcpy.da.SearchCursor(ocena_JCWP_2017,['KOD_JCWP','KLASA_BIOL','KLASA_BENT', 'KLASA_ICHT'])as cur2:
                            for row2 in cur2:
                                if row2[1] in [1,2] and row2[0]==st_kod:
                                    if row2[2] == 0 and row2[3] == 0:
                                        war.append(0)
                                    elif row2[2] < 3 and row2[3] in [1,2]:
                                        war.append(1)
                                    elif row2[3] < 3 and row2[2] in [1,2]:
                                        war.append(1)
                                elif row2[1] not in [1,2] and row2[0]==st_kod:
                                    war.append(0)
                                elif st_kod not in stJCWP:
                                    war.append(0)

                        del cur2
                if 0 not in war and len(war)>0:
                    row[kol.index('KROK')]='8_0217'
                    cur.updateRow(row)
    del cur
    print "zakonczono Krok 11 2017 - ", round((time.time() - start_time)/60, 2), "min " # 7.78 min
    return

"""KROK 12 2017"""
def Krok12_2017(JCWP,ocena_JCWP_2017):
    print "realizuje Krok 12 2017"
    start_time = time.time()
    kol=[]
    for field in arcpy.ListFields(JCWP):
        kol.append(str(field.name))

    stJCWP=[]
    with arcpy.da.SearchCursor(ocena_JCWP_2017,['KOD_JCWP'])as cur3:
        for row3 in cur3:
            stJCWP.append(row3[0])
    del cur3

    with arcpy.da.UpdateCursor(JCWP,kol)as cur:
        for row in cur:
            if row[kol.index('KROK')] is None or row[kol.index('KROK')]== '4':
                aPGW = [row[kol.index('ST_KOD_1')], row[kol.index('ST_KOD_2')], row[kol.index('ST_KOD_3')],row[kol.index('ST_KOD_4')],row[kol.index('ST_KOD_5')],row[kol.index('ST_KOD_6')],row[kol.index('ST_KOD_7')],row[kol.index('ST_KOD_8')],row[kol.index('ST_KOD_9')], row[kol.index('ST_KOD_10')],row[kol.index('ST_KOD_11')],row[kol.index('ST_KOD_12')],row[kol.index('ST_KOD_13')],row[kol.index('ST_KOD_14')],row[kol.index('ST_KOD_15')]]
                war=[]
                for st_kod in aPGW:
                    if st_kod !='':
                        with arcpy.da.SearchCursor(ocena_JCWP_2017,['KOD_JCWP','KLASA_BIOL','KLASA_BENT', 'KLASA_ICHT'])as cur2:
                            for row2 in cur2:
                                if row2[1] in [1,2] and row2[0]==st_kod:
                                    if row2[2] == 0 and row2[3] == 0:
                                        war.append(0)
                                    elif row2[2] < 3 and row2[3] in [1,2]:
                                        war.append(1)
                                    elif row2[3] < 3 and row2[2] in [1,2]:
                                        war.append(1)
                                elif row2[1] not in [1,2] and row2[0]==st_kod:
                                    war.append(0)
                                elif st_kod not in stJCWP:
                                    war.append(2)
                        del cur2
                if 0 not in war and 1 in war:
                    row[kol.index('KROK')]='9_2017'
                    cur.updateRow(row)
    del cur
    print "zakonczono Krok 12 2017- ", round((time.time() - start_time)/60, 2), "min " # 7.00 min
    return

##Krok1(JCWP)
##Krok2(JCWP,char_JCWP_aPGW)
##Krok3(JCWP,char_JCWP_aPGW,stat_JCWP_aPGW)
##Krok4(JCWP,ods_JCWP_aPGW)
##Krok5(JCWP,ocena_JCWP_aPGW)
##Krok6(JCWP,ocena_JCWP_aPGW)
##Krok7(JCWP,ocena_JCWP_aPGW)
##Krok5_2017(JCWP,ocena_JCWP_2017)
####Krok6_2017(JCWP,ocena_JCWP_2017)
####Krok7_2017(JCWP,ocena_JCWP_2017)
####Krok8(JCWP,ods_JCWP_aPGW)
####Krok9(JCWP,ods_JCWP_aPGW)
####Krok10(JCWP,ods_JCWP_aPGW)
Krok11(JCWP,monit)
Krok12(JCWP,monit)
Krok11_2017(JCWP, monit_2017)
Krok12_2017(JCWP, monit_2017)

with arcpy.da.UpdateCursor(JCWP,['KROK'])as cur:
    for row in cur:
        if row[0] is None or row[0] == '4':
            row[0] = 10
            cur.updateRow(row)
del cur