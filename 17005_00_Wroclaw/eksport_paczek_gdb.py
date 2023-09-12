#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy
import os
import sys
import time
arcpy.env.overwriteOutput = True
start_time = time.time()
"""PARAMETRY PROGRAMU"""

"""Geobaza do ktorej wgrywamy obiekty z poszczegolnych oddzialow"""
baza_oddzialy=arcpy.env.workspace =ur"P:\Projekty_2017\17005_Baza_Wrocław\3. Etap I\4. Wytworzenie danych Ewidencji Wód\4_4_Produkcja\4_4_2_Baza_styki\Baza_ewidencji_wod_CZ3.gdb"

"""Geobaza robocza (zawierajacą obiekty ze wszystkich gmin)"""
workspace=arcpy.env.workspace=ur"P:\Projekty_2017\17005_Baza_Wrocław\3. Etap I\4. Wytworzenie danych Ewidencji Wód\4_4_Produkcja\4_4_2_Baza_styki\20180701_Baza_ewidencji_wod.gdb"

"""Plik SHP z gminami ktory sluzy do przeszukiwania i Bazy i zapisywania warstw do poszczsegolnych oddzialow"""
gminy=r"P:\Projekty_2017\17005_Baza_Wrocław\3. Etap I\_warstwy_robocze\gminy_oddzialy.shp"

"""Lista oddzialow z ktorego eksportujemy warstwy do geobazy (nazwa oddziału musi byc podana w formie unikodu)"""
oddzial=[u'Baza 3']

for part in oddzial:
    print part
    where_clause= '"ODDZIAL" = '+"'"+part+"'"
    arcpy.MakeFeatureLayer_management(gminy,'gmina_temp',where_clause)
    for dirpath, dirnames, filenames in arcpy.da.Walk(workspace, datatype="FeatureClass"):
        for filename in filenames:
            temp=filename+'_temp'
            output=filename+'_out'
            arcpy.MakeFeatureLayer_management(filename,temp)
            with arcpy.da.SearchCursor(gminy,['ODDZIAL', 'KOD_POW', 'POWIAT', 'KOD_GM', 'GMINA'])as cursor:
                for row in cursor:
                    if filename!='EWM_ObiektMelioracyjny' and part==row[0]:
                        expr = '"numerTerytObrebu" LIKE '+"'"+row[3]+"%'"
                        arcpy.SelectLayerByAttribute_management (temp, "ADD_TO_SELECTION", expr)
                    elif filename=='EWM_ObiektMelioracyjny' and part==row[0]:
                        arcpy.SelectLayerByLocation_management(temp, 'WITHIN', 'gmina_temp',selection_type="ADD_TO_SELECTION")
            del cursor
            arcpy.Select_analysis(temp,output)
            arcpy.Delete_management(temp)
            print filename

            for sciezka2, folder2, datasets2 in arcpy.da.Walk(baza_oddzialy):     # przechodzimy przez kazdy obiekt w naszej geobazie w wyniku czego otrzymujemy liste list [[sciezka2], [folder2], [dataset2]]
                for fds2 in datasets2:
                    if filename==fds2:
                        arcpy.Append_management(os.path.join(workspace,output),os.path.join(baza_oddzialy,fds2), "NO_TEST", "", "")
                        print "Zaladowalo klase "+ str(filename)

                arcpy.Delete_management(os.path.join(workspace,output))

    arcpy.Delete_management('gmina_temp')
print 'koniec programu',round((time.time() - start_time)/60, 2), "min "
