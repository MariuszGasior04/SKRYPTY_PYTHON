#!/usr/bin/env python
# -*- coding: utf-8 -*-

# skrypt do synchronizacji warstwy punktow na przekrojach przedluzanych z punktami istniejacych przekroi z modelu MIKE. Finalnie po udanym przejsciu skryptu można połączyc tabelę warstwy punktow z tabela punktow przekroi z modelu MIKE

import arcpy

arcpy.CheckOutExtension("3D")
"""PARAMETR"""
workspace = arcpy.env.workspace = \
    r"R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\2_Opracowanie_danych_do_modeli\etap 3\2_przedluzone\Jeziorsko\3_iteracja\przedluzanie_przekroi.gdb"

"""PARAMETR"""
##punkty na przekrojach przedluzanych
pkt_prof = r'przedluzenia_WARTA_pkt'

pkt_prof_output = pkt_prof + '_2'

"""PARAMETR"""
##tabela z punktami na profilach z modelu MIKE
tab_RD_LP = r'WARTA_S10_RD_LP'

"""PARAMETR"""
# NMT
nmt = r'R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\_Dane_ref\NMT\NMT_ETAP3.gdb\Jeziorsko'

# Pokrycie BDOT Polska
# nie zmieniac
pk_BDOT = r'R:\OIIS_KR5\_BRANŻOWE\_GIS\BDOT10k\BDOT_PL.gdb\pokrycie_ter_pl_wspn'

## tabela ze wspolczynnikami szorstkosci
# nie zmieniac
n_tab = r'R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\1_Analiza_danych_OZ\przekroje\tabela_szorstkosci_pokrycia.dbf'

try:
    arcpy.AddField_management(pkt_prof, "DL", "DOUBLE", field_precision=13, field_scale=3)
    print "Dodano kolumne DL"
except:
    print "Nie dodano kolumny DL"
    pass

try:
    arcpy.CalculateField_management(pkt_prof, 'DL', '!cngmetry!', "PYTHON_9.3")
    print "Przeliczono kolumne DL"
except:
    print "Nie przeliczono kolumny DL"
    pass

try:
    arcpy.AddXY_management(pkt_prof)
    print "Przeliczono i dodano kolumny: POINT_X, POINT_Y, POINT_Z"
except:
    print "NIE dodano i NIE przeliczono kolumn: POINT_X, POINT_Y, POINT_Z"
    pass

arcpy.Intersect_analysis([pkt_prof, pk_BDOT], pkt_prof_output, "NO_FID")
print "Przeliczono i dodano kolumne WSP_n"

arcpy.AddSurfaceInformation_3d(pkt_prof_output, nmt, "Z", "LINEAR")
print "Przeliczono i dodano kolumne Z"

tab_RD_LP_stat = tab_RD_LP + '_stat'
statsFields = [["RID", "COUNT"]]

try:
    joinedField = ['RIVER', 'TOPO_ID', 'CHAINAGE', 'COORDINATES', 'COORD_X1', 'COORD_Y1', 'COORD_X2', 'COORD_Y2',
                   'FLOW_DIR', 'PROTECTION_DATA', 'DATUM', 'CLOSED_SECTION', 'RADIUS_TYPE', 'DIVIDE_X_SECTION',
                   'SECTION_ID', 'INTERPOLATED', 'ANGLE', 'RESIST_NO', 'PROFILE', 'LEVEL_PARAMS', 'RID']
    arcpy.Statistics_analysis(tab_RD_LP, tab_RD_LP_stat, statsFields, joinedField)
except:
    joinedField = ['RIVER', 'TOPO_ID', 'CHAINAGE', 'COORDINATES', 'COORD_X1', 'COORD_Y1', 'COORD_X2', 'COORD_Y2',
                   'FLOW_DIR', 'PROTECTION_DATA', 'DATUM', 'CLOSED_SECTION', 'RADIUS_TYPE', 'DIVIDE_X_SECTION',
                   'SECTION_ID', 'INTERPOLATED', 'ANGLE', 'ANGLE_X', 'ANGLE_Y', 'RESIST_NO', 'PROFILE', 'LEVEL_PARAMS',
                   'RID']
    arcpy.Statistics_analysis(tab_RD_LP, tab_RD_LP_stat, statsFields, joinedField)

try:
    arcpy.AddField_management(tab_RD_LP_stat, "XS_DL", "TEXT", field_length=15)
    arcpy.AddField_management(tab_RD_LP_stat, "XS_Z", "TEXT", field_length=15)
    arcpy.AddField_management(tab_RD_LP_stat, "XS_N", "TEXT", field_length=15)
    arcpy.AddField_management(tab_RD_LP_stat, "XS_MARKER", "TEXT", field_length=15)
    arcpy.AddField_management(tab_RD_LP_stat, "XS_UNK1", "TEXT", field_length=15)
    arcpy.AddField_management(tab_RD_LP_stat, "XS_UNK2", "TEXT", field_length=15)
    arcpy.AddField_management(tab_RD_LP_stat, "XS_UNK3", "TEXT", field_length=15)
    print "Dodano kolumny XS"
    try:
        arcpy.CalculateField_management(tab_RD_LP_stat, 'XS_DL', "'0.0'", "PYTHON_9.3")
        arcpy.CalculateField_management(tab_RD_LP_stat, 'XS_Z', "'0.0'", "PYTHON_9.3")
        arcpy.CalculateField_management(tab_RD_LP_stat, 'XS_N', "'0.0'", "PYTHON_9.3")
        arcpy.CalculateField_management(tab_RD_LP_stat, 'XS_MARKER', "'<#0>'", "PYTHON_9.3")
        arcpy.CalculateField_management(tab_RD_LP_stat, 'XS_UNK1', "'0.0'", "PYTHON_9.3")
        arcpy.CalculateField_management(tab_RD_LP_stat, 'XS_UNK2', "'0.0'", "PYTHON_9.3")
        arcpy.CalculateField_management(tab_RD_LP_stat, 'XS_UNK3', "'0.0'", "PYTHON_9.3")
        print "Przeliczono kolumny XS"

    except:
        print "Nie przeliczono kolumn XS"
        pass

except:
    print "Nie dodano kolumn XS"
    pass

layerName = pkt_prof_output + 'layer'
arcpy.MakeFeatureLayer_management(pkt_prof_output, layerName)

arcpy.AddJoin_management(layerName, "RID", tab_RD_LP_stat, "RID")

outFeature = pkt_prof_output + '_opracowane'
arcpy.CopyFeatures_management(layerName, outFeature)

fieldList = arcpy.ListFields(outFeature)
for field in fieldList:
    try:
        arcpy.AlterField_management(outFeature, field.name, field.aliasName)
    except:
        print 'Nie zaktualizowano kolumny ' + field.name
        pass

print 'koniec ', pkt_prof
