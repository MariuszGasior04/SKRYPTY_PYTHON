#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("3D")

"""parametry programu"""


workspace = arcpy.env.workspace = \
    r"R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\5_Opracowanie_kartograficzne\BAZA_Mapy\_robo.gdb"

ark = 'arkusze_all'
ark_WOJ = 'arkusze_do_WOJ_Sort'

# walk = arcpy.da.Walk(workspace, datatype="FeatureClass", type="Polygon")
# for dirpath, dirnames, filenames in walk:
#     for layer in filenames:
#         nazwa = layer.split("_")[-1][:-4]
#
#         arcpy.CalculateField_management(layer, 'ZBIORNIK', '"' + nazwa + '"', "PYTHON_9.3")

fields = []
for field in arcpy.ListFields(ark_WOJ):
    fields.append(str(field.name))
dict = {}

with arcpy.da.SearchCursor(ark_WOJ, fields) as search:
    for row in search:
        if dict.has_key(str(row[fields.index('Godlo_1')])):
            dict[str(row[fields.index('Godlo_1')])].append(row[fields.index('NAZWA_1')])
        else:
            dict[str(row[fields.index('Godlo_1')])] = [
                (row[fields.index('NAZWA_1')])
            ]
del search

print "Utworzyło słownik Województw"

fields = []
for field in arcpy.ListFields(ark):
    fields.append(str(field.name))

with arcpy.da.UpdateCursor(ark, fields) as update:
    for row in update:
        # print len(dict[str(row[fields.index('Godlo')])])
        # print dict[str(row[fields.index('Godlo')])]
        counterWOJ = 0
        for woj in dict[str(row[fields.index('Godlo')])]:
            # print woj
            counterWOJ += 1
            row[fields.index('WOJ'+str(counterWOJ))] = woj
            update.updateRow(row)
del update

print 'Nadpisano stukture warstwy ' + ark