#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy, os

#parametr
baza= ur'R:\OIIS_KR5\_PROJEKTY 2019\19050-00_Mapy_Budowle\07.GIS\4_Opracowanie_baz_danych\_Baza_zbiorniki\1_zb_dobromierz\MZP\MZP.gdb'            #geobaza w ktorej znajduje się głowna baza projektu
glebokosc = 'glebokosc_BP'

robocza = arcpy.env.workspace = ur'R:\OIIS_KR5\_PROJEKTY 2019\19050-00_Mapy_Budowle\07.GIS\4_Opracowanie_baz_danych\_roboczy\pokrycie\topo_all.gdb'    #geobaza w ktorej znajdują się dane z obrębu do załadowania danych
pokrycie = 'pokrycie_BDOT10k_all'
print(baza)
inputF = [os.path.join(baza,glebokosc),pokrycie]
outputF = 'pokrycie_gleb'
arcpy.Intersect_analysis(inputF, outputF)

outputFDiss1 = 'uzytkowanie_gleb_diss'
outputFDiss2 = 'uzytkowanie_gleb_straty_diss'
dissolveFields1 = ['ZBIORNIK','CHARAKT','ID_KLAS']
dissolveFields2 = ['ZBIORNIK','GLEBOKOSC','CHARAKT','ID_KLAS']
arcpy.Dissolve_management(outputF, outputFDiss1, dissolveFields1, "","SINGLE_PART")
arcpy.Dissolve_management(outputF, outputFDiss2, dissolveFields2, "","SINGLE_PART")
arcpy.AddField_management(outputFDiss2, 'STRATY', "DOUBLE")
arcpy.AddField_management(outputFDiss2, 'STRATY_2', "DOUBLE")
print "pyklo"