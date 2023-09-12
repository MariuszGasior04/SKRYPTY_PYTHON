#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do zczytywania pliku cross section z MIKE11 do formatu DBF

import os
import arcpy

workspace = arcpy.env.workspace = r"R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\1_Analiza_danych_OZ\przekroje\Etap 1"
dbf = "test_rd.dbf"
file_dir = r"R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\1_Analiza_danych_OZ\przekroje\rd.txt"

counter = 0
profile_counter=0

def createDbfTab(direction, tab):
    if not os.path.exists(os.path.join(workspace,tab)):
        arcpy.CreateTable_management(workspace, tab)
        arcpy.AddField_management(tab, "River", "TEXT", field_length = 30)
        arcpy.AddField_management(tab, "Topo_ID", "TEXT", field_length = 30)
        arcpy.AddField_management(tab, "Chainage", "DOUBLE", field_precision = 13, field_scale = 2)
        arcpy.AddField_management(tab, "Coord", "TEXT", field_length = 80)
        arcpy.AddField_management(tab, "Flow_Dir", "LONG", field_precision = 9)
        arcpy.AddField_management(tab, "Prot_Data", "LONG", field_precision = 9)
        arcpy.AddField_management(tab, "Datum", "DOUBLE", field_precision = 13, field_scale = 2)
        arcpy.AddField_management(tab, "Rad_Type", "LONG", field_precision = 9)
        arcpy.AddField_management(tab, "Div_Xsec", "LONG", field_precision = 9)
        arcpy.AddField_management(tab, "Sec_ID", "TEXT", field_length = 30)
        arcpy.AddField_management(tab, "Inter", "LONG", field_precision = 9)
        arcpy.AddField_management(tab, "Angle", "TEXT", field_length = 30)
        arcpy.AddField_management(tab, "Resist_no", "TEXT", field_length = 80)
        arcpy.AddField_management(tab, "Profile", "LONG", field_precision = 9)
        arcpy.AddField_management(tab, "XS_Dl", "TEXT", field_length = 30)
        arcpy.AddField_management(tab, "XS_Z", "DOUBLE", field_precision = 13, field_scale = 3)
        arcpy.AddField_management(tab, "XS_n", "DOUBLE", field_precision = 13, field_scale = 3)
        arcpy.AddField_management(tab, "XS_mark", "TEXT", field_length = 10)
        arcpy.AddField_management(tab, "XS_unk1", "LONG", field_precision = 9)
        arcpy.AddField_management(tab, "XS_unk2", "DOUBLE", field_precision = 13, field_scale = 3)
        arcpy.AddField_management(tab, "XS_unk3", "LONG", field_precision = 9)
        arcpy.DeleteField_management(tab, ['Field1'])
    return

createDbfTab(workspace,dbf)
file_txt = open(file_dir, "r")
for line in file_txt:
    if line.rstrip('\n') == '*******************************':
        profile_counter += 1

print ('Liczba profili w pliku ' + str(profile_counter))
file_txt.close()

file_txt = open(file_dir, "r")
for line in file_txt:
    if line.rstrip('\n') != '*******************************':
        counter += 1
    else:
        counter = 0
        profile_counter -=1
        print (u'Pozostało ' + str(profile_counter))

    if line.rstrip('\n') == 'LEVEL PARAMS':
        counter = -1

    if counter == 1:
        topo_id = line.rstrip('\n')
    if counter == 2:
        river = line.rstrip('\n')
    if counter == 3:
        chainage = float(line.rstrip('\n').split()[0])
    if counter == 5:
        coordinates = line.rstrip('\n')
    if counter == 7:
        flow_dir = long(line.rstrip('\n').split()[0])
    if counter == 9:
        protection_data = long(line.rstrip('\n').split()[0])
    if counter == 11:
        datum = float(line.rstrip('\n').split()[0])
    if counter == 13:
        radius_type = long(line.rstrip('\n').split()[0])
    if counter == 15:
        divide_xsection = long(line.rstrip('\n').split()[0])
    if counter == 17:
        section_id = line.rstrip('\n')
    if counter == 19:
        interpolated = long(line.rstrip('\n').split()[0])
    if counter == 21:
        angle = line.rstrip('\n')
    if counter == 23:
        resist_no = line.rstrip('\n')
    if counter == 24:
        profile = long(line.rstrip('\n').split()[1])

#tutaj zaczyna się dodawanie do tabeli punktow z pliku txt na profilu
    if counter > 25:
        xs_dl = float(line.rstrip('\n').split()[0])
        xs_z = float(line.rstrip('\n').split()[1])
        xs_n = float(line.rstrip('\n').split()[2])
        xs_mark = line.rstrip('\n').split()[3]
        xs_unk1 = long(line.rstrip('\n').split()[4])
        xs_unk2 = float(line.rstrip('\n').split()[5])
        xs_unk3 = long(line.rstrip('\n').split()[6])

        with arcpy.da.InsertCursor(dbf, ['River','Topo_ID','Chainage','Coord','Flow_Dir','Prot_Data','Datum','Rad_Type','Div_Xsec','Sec_ID','Inter','Angle','Resist_no','Profile','XS_Dl','XS_Z','XS_n','XS_mark','XS_unk1','XS_unk2','XS_unk3'])as cur:
            row = (river, topo_id, chainage,  coordinates, flow_dir, protection_data, datum, radius_type, divide_xsection, section_id, interpolated, angle, resist_no, profile, xs_dl, xs_z, xs_n, xs_mark, xs_unk1, xs_unk2, xs_unk3)
            cur.insertRow(row)
        del cur

file_txt.close()