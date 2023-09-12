#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do naprawy geometri warstw shp

import arcpy
import os

arcpy.env.overwriteOutput = True

workspace = arcpy.env.workspace = r"R:\OIIS_KR5\_PROJEKTY 2019\19050-00_Mapy_Budowle\07.GIS\4_Opracowanie_baz_danych\_Baza_zbiorniki"

walk = arcpy.da.Walk(workspace, datatype="FeatureClass")
for dirpath, dirnames, filenames in walk:
    print(dirpath)
    for filename in filenames:
        warstwa = os.path.join(dirpath,filename)
        listSet=[]
        kol=[]
        for field in arcpy.ListFields(warstwa):
            kol.append(str(field.name))

        try:
            if 'ZBIORNIK' in kol:
                with arcpy.da.SearchCursor(warstwa, ['ZBIORNIK'])as cur:
                    for row in cur:
                        listSet.append(row[0])
                print(filename)
                print(set(listSet))
        except:
            print(filename + " nie posiada atrybutu 'ZBIORNIK' ")
