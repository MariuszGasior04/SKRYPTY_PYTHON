#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do sprawdzania poprawnosci wypelnienia terytu

import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True

"""Geobaza w ktorej sprawdzamy TERYT"""
baza=arcpy.env.workspace =ur"P:\Projekty_2017\17005_Baza_Wrocław\3. Etap I\4. Wytworzenie danych Ewidencji Wód\4_4_Produkcja\4_4_2_Baza_styki\ostateczna.gdb"
ilosc_szpot=0

for sciezka, folder, datasets in arcpy.da.Walk(baza):     # przechodzimy przez kazdy obiekt w naszej geobazie w wyniku czego otrzymujemy liste list [[sciezka2], [folder2], [dataset2]]
    for fds in datasets:
        print fds
        ilosc_szpot_warstwa=0
        kolumny=[]
        szpot=[]
        for field in arcpy.ListFields(fds):
            kolumny.append(str(field.name))

        with arcpy.da.SearchCursor(fds,kolumny)as cursor:
            for row in cursor:
                if fds!='EWM_ObiektMelioracyjny' and unicode(row[kolumny.index('numerTerytObrebu')])[:2]!='02':
                    ilosc_szpot+=1
                    ilosc_szpot_warstwa+=1

            print ilosc_szpot_warstwa
        del cursor

print "Ilosc wszystkich szpotow teryt {0}".format(ilosc_szpot)