#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("3D")

"""parametry programu"""


workspace = arcpy.env.workspace = \
    r"R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\5_Opracowanie_kartograficzne\BAZA_Mapy\_robo.gdb"

ark = 'arkusze_all'
ark_ZZ = 'arkusze_do_ZZ_Sort'

# walk = arcpy.da.Walk(workspace, datatype="FeatureClass", type="Polygon")
# for dirpath, dirnames, filenames in walk:
#     for layer in filenames:
#         nazwa = layer.split("_")[-1][:-4]
#
#         arcpy.CalculateField_management(layer, 'ZBIORNIK', '"' + nazwa + '"', "PYTHON_9.3")

fields = []
for field in arcpy.ListFields(ark_ZZ):
    fields.append(str(field.name))
dict = {}

with arcpy.da.SearchCursor(ark_ZZ, fields) as search:
    for row in search:
        if dict.has_key(str(row[fields.index('Godlo_1')])):
            dict[str(row[fields.index('Godlo_1')])].append([(row[fields.index('RZGW_KOD')]), (row[fields.index('ZZ_miasto')]), (row[fields.index('NR_ZZ')])])
        else:
            dict[str(row[fields.index('Godlo_1')])] = [[
                (row[fields.index('RZGW_KOD')]),
                (row[fields.index('ZZ_miasto')]),
                (row[fields.index('NR_ZZ')])]
            ]
del search

print "Utworzyło słownik ZZ"

fields = []
for field in arcpy.ListFields(ark):
    fields.append(str(field.name))

with arcpy.da.UpdateCursor(ark, fields) as update:
    for row in update:
        # print len(dict[str(row[fields.index('Godlo')])])
        # print dict[str(row[fields.index('Godlo')])]
        if len(dict[str(row[fields.index('Godlo')])]) == 1:
            zz = dict[str(row[fields.index('Godlo')])][0]
            row[fields.index('RZGW1')] = str(zz[0])
            row[fields.index('ZZ1_1')] = zz[1]
            row[fields.index('NR_ZZ1_1')] = str(zz[2])
            update.updateRow(row)
        else:
            counterZZ = 1
            counterRZ = 1
            for zz in dict[str(row[fields.index('Godlo')])]:
                rzgw = str(zz[0])
                if counterZZ == 1:
                    rzgw1 = rzgw
                    row[fields.index('RZGW'+str(counterRZ))] = str(zz[0])
                    row[fields.index('ZZ'+str(counterRZ)+'_'+str(counterZZ))] = zz[1]
                    row[fields.index('NR_ZZ'+str(counterRZ)+'_'+str(counterZZ))] = str(zz[2])
                    counterZZ += 1

                elif counterZZ > 1 and rzgw1 == str(zz[0]):
                    row[fields.index('RZGW' + str(counterRZ))] = str(zz[0])
                    row[fields.index('ZZ' + str(counterRZ) + '_' + str(counterZZ))] = zz[1]
                    row[fields.index('NR_ZZ' + str(counterRZ) + '_' + str(counterZZ))] = str(zz[2])
                    counterZZ += 1

                elif rzgw1 != str(zz[0]):
                    rzgw1 = rzgw
                    counterZZ = 1
                    counterRZ = 2
                    row[fields.index('RZGW' + str(counterRZ))] = str(zz[0])
                    row[fields.index('ZZ' + str(counterRZ) + '_' + str(counterZZ))] = zz[1]
                    row[fields.index('NR_ZZ' + str(counterRZ) + '_' + str(counterZZ))] = str(zz[2])
                    counterZZ += 1

            update.updateRow(row)

del update

print 'Nadpisano stukture warstwy ' + ark