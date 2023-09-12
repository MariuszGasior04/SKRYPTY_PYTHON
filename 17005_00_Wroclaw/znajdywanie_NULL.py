#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do okreslania kilometrazu odcinkow obiektow liniowych

import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True

"""Geobaza w ktorej sprawdzamy nulle"""
baza=arcpy.env.workspace =ur"P:\Projekty_2017\17005_Baza_Wrocław\3. Etap I\4. Wytworzenie danych Ewidencji Wód\4_4_Produkcja\4_4_2_Baza_styki\ostateczna.gdb"
ilosc_null=0

for sciezka, folder, datasets in arcpy.da.Walk(baza):     # przechodzimy przez kazdy obiekt w naszej geobazie w wyniku czego otrzymujemy liste list [[sciezka2], [folder2], [dataset2]]
    for fds in datasets:
        ilosc_nulli_warstwa=0
        kolumny=[]
        nulle=[]
        for field in arcpy.ListFields(fds):
            kolumny.append(str(field.name))

        with arcpy.da.SearchCursor(fds,kolumny)as cursor:
            for row in cursor:
                for i in range(0,len(kolumny)-1):
                    if row[i] is None:
                        ilosc_null+=1
                        ilosc_nulli_warstwa+=1
                        if  kolumny[i] not in nulle:
                            nulle.append(kolumny[i])
        if len(nulle)>0:
            print (str(fds)+' - {0} NULL w kolumnach:'.format(ilosc_nulli_warstwa))
            print nulle, '\n'
print "Ilosc wszystkich nulli {0}".format(ilosc_null)