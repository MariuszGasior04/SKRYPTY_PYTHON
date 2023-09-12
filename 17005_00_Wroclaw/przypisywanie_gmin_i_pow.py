#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do przypisania gmin i powiatow na podstawie teryt

import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True

"""Geobaza w ktorej sprawdzamy TERYT"""
baza=arcpy.env.workspace =ur"P:\Projekty_2017\17005_Baza_Wrocław\3. Etap I\4. Wytworzenie danych Ewidencji Wód\4_4_Produkcja\4_4_2_Baza_styki\ostateczna.gdb"
obreby=ur"P:\Projekty_2017\17005_Baza_Wrocław\3. Etap I\_warstwy_robocze\obreby.shp"
fieldList=['POWIAT','GMINA']

for sciezka, folder, datasets in arcpy.da.Walk(baza):     # przechodzimy przez kazdy obiekt w naszej geobazie w wyniku czego otrzymujemy liste list [[sciezka2], [folder2], [dataset2]]
    for fds in datasets:
        kolumny=[]
        if fds!='EWM_ObiektMelioracyjny':
            for field in arcpy.ListFields(fds):
                kolumny.append(str(field.name))

            if 'ID_Powiat' not in kolumny:
                arcpy.AddField_management(fds, 'ID_Powiat', 'TEXT',field_length=50)
                kolumny.append('ID_Powiat')
            if 'ID_Gmina' not in kolumny:
                arcpy.AddField_management(fds, 'ID_Gmina', 'TEXT',field_length=50)
                kolumny.append('ID_Gmina')

            if 'ID_Powiat' in kolumny and 'ID_Gmina' in kolumny:
                arcpy.JoinField_management (fds, 'numerTerytObrebu', obreby, 'jpt_kod_je', fieldList)
                arcpy.CalculateField_management(fds, 'ID_Powiat', '!POWIAT!', "PYTHON_9.3")
                arcpy.CalculateField_management(fds, 'ID_Gmina', '!GMINA!', "PYTHON_9.3")
                arcpy.DeleteField_management(fds, fieldList)
                print 'Nadpisano',fds

print 'koniec'