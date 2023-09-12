#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do zmiany nagłowkow tabeli wykazu dzialek i podmiotow wyeksportowanej z swd do dbf. Narzędzie działa tylko na tabelach zaimportowanych do geobazy

import arcpy
import os
from arcpy import env
arcpy.env.overwriteOutput = True
import time
"""PARAMETRY PROGRAMU"""

arcpy.env.workspace = ws = r'R:\OIIS_KR5\_PROJEKTY 2019\19004-00_Piekielko\33_ULLK\337_GIS\1_roboczy\shp\dzialki_ewidencyjne\BAZA SWD\odc E\uzupelnienie_30092020\robo.gdb'

tab = 'gmina_elk_wykaz'

fieldList = arcpy.ListFields(tab)
for field in fieldList:

    if field.name.upper() == 'TEXT10':
        arcpy.AlterField_management(tab, field.name, new_field_name = 'ID_DZ')
    if field.name.upper() == 'TEXT21':
        arcpy.AlterField_management(tab, field.name, new_field_name = 'POW_HA')
    if field.name.upper() == 'TEXT22':
        arcpy.AlterField_management(tab, field.name, new_field_name = 'AM')
    if field.name.upper() == 'TEXT20':
        arcpy.AlterField_management(tab, field.name, new_field_name = 'OBREB')
    if field.name.upper() == 'TEXT14':
        arcpy.AlterField_management(tab, field.name, new_field_name = 'JED_EW')
    if field.name.upper() == 'TEXT15':
        arcpy.AlterField_management(tab, field.name, new_field_name = 'JED_REJ')
    if field.name.upper() == 'TEXT16':
        arcpy.AlterField_management(tab, field.name, new_field_name = 'WLAS')
    if field.name.upper() == 'TEXT17':
        arcpy.AlterField_management(tab, field.name, new_field_name = 'KW')
    if field.name.upper() == 'TEXT18':
        arcpy.AlterField_management(tab, field.name, new_field_name = 'KLASO_UZ')

print tab