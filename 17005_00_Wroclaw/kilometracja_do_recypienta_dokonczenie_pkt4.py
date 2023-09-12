#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do okreslania kilometrazu obiektow liniowych wzgledemi ich obiektow nadrzednych
""" Żeby przypisało recypienta w kolumnach ObiektNadrzedny oraz lokalizacja musza byc wypelnione wartosciami <Null>"""
import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True
import time

"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

arcpy.env.workspace=ur'P:\Projekty_2017\17005_Baza_Wrocław\3. Etap I\4. Wytworzenie danych Ewidencji Wód\4_4_Produkcja\4_4_2_Baza_styki\Baza_ewidencji_wod_Wroclaw_PD.gdb'                              #geobaza robocza

""" Podaj wszystkie warstwy ktore są uwzgledniane w kilometracji (podrzedny_rur i podrzedny_syf musza byc zawsze podane bez wzgledu na to czy biora udzial w kilometrazu czy nie) """

podrzedny= 'EWM_Zbieracz_drenarski'

print "4"

out_spatialjoin=podrzedny+'_spatial'

fieldList=['obiektNadrzedny_rob','lokalizacja_rob']

arcpy.JoinField_management (podrzedny, 'OBJECTID', out_spatialjoin, 'TARGET_FID', fieldList)

with arcpy.da.UpdateCursor(podrzedny,['obiektNadrzedny','lokalizacja','obiektNadrzedny_rob','lokalizacja_rob'])as cur:
    for row in cur:
        if row[2] is not None or row[2]=='b/d' or row[2]=='-9999':
            row[0]=row[2]
            row[1]=row[3]
            cur.updateRow(row)
del cur

print 'Przypisano recypienta i kilometr ujsciowy do liniowych obiektow podrzednych'

arcpy.Delete_management(out_spatialjoin)
arcpy.DeleteField_management(podrzedny, fieldList)

print "koniec programu -",podrzedny