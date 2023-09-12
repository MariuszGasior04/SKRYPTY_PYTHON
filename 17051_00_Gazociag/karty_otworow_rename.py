#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do automatycznej zmiany nazw plikwow w folderze

import arcpy
import os
from arcpy import env
arcpy.env.overwriteOutput = True
import time
import shutil

"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

arcpy.env.workspace=ws=ur'P:\Projekty_2017\17051-00 Goleniów_Lwówek_DN1000\11_GIS\_warstwy_robo\Geologia_opracowanie_wyników\Geometria + karty otworów\V_zachodniopomorskie'
folder_sond=ur'P:\Projekty_2017\17051-00 Goleniów_Lwówek_DN1000\11_GIS\_warstwy_robo\Geologia_opracowanie_wyników\Geometria + karty otworów\_Karty sond\V\karty sond\Karty sond DPL'

tab = 'karty_sondy_v_sort'

for sciezka, podkatalogi, pliki in os.walk(folder_sond):
     a=sciezka,podkatalogi,pliki
     for b in a[2]:
        if os.path.isfile(os.path.join(a[0],b)):
            with arcpy.da.SearchCursor(tab, ['PDF','NAZ_OTW'])as search:
                for row in search:
                    if row[0] == b:
                        n_naz = row[1]+'.pdf'
                        print os.path.join(a[0],b)
                        try:
                            os.renames(os.path.join(a[0],b), os.path.join(a[0],n_naz))
                        except:
                            pass
