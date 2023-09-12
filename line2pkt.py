#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy
import  os

shp = 'profil.shp'
arcpy.env.workspace=ws=ur'P:\Projekty_2017\17051-00 Goleniów_Lwówek_DN1000\11_GIS\_warstwy_robo\analizy_widocznosci'

with arcpy.da.SearchCursor(shp, ['SHAPE@'])as search:
    for row in search:
        for part in row[0]:
            for pnt in part:
                x = pnt.X
                y = pnt.Y
                z = pnt.Z
                print (x, y, z)