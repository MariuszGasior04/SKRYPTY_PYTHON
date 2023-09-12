#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy
import os

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("3D")

"""parametry programu"""

##create tin
##nmpw
##raster calc
##poligon glebokosci
##wygladzanie_poligonow

#geobaza robocza

workspace = arcpy.env.workspace = \
    r"D:\FolderRoboczy\Strefy_testy\OLDZA\v12\robo"
tiny = \
    r"D:\FolderRoboczy\Strefy_testy\OLDZA\v12\robo\tiny"
tab_wynik = \
    'Wyniki_H.dbf'

# warianty = \
#     ['RZED_PB_W1', 'RZED_PB_W2', 'RZED_PL_W1', 'RZED_PL_W2']
warianty = \
    ['RZED_10','RZED_1', 'RZED_02']
# warianty = \
    # ['RZED_PB']
# warianty = \
#     ['RZED_W2_10','RZED_W2_1','RZED_W2_02']


def addRes(tab, workspace, warianty):
    walk = arcpy.da.Walk(workspace, datatype = "FeatureClass", type = "Polyline")
    for dirpath, dirnames, filenames in walk:
        for layer in filenames:
            # try:
            #     arcpy.AddField_management(layer, 'KM_ID', "TEXT", field_length = 50)
            # except:
            #     pass
            #
            # expression = "'" + str(layer[:-13]) + "'" + "+' '+" + 'str(!KM_PKT!)'
            # arcpy.CalculateField_management(layer, 'KM_ID', expression,"PYTHON_9.3")
            try:
                arcpy.JoinField_management (layer, 'RID', tab, 'RID', warianty)
                print layer[:-13], ' - OK'
            except:
                print "Nie dodalo kolumn do ", layer


    return

def createTINs(shp_fold, tin_fold, warianty):
    inputs = {}
    walk = arcpy.da.Walk(shp_fold, datatype = "FeatureClass", type=['Polygon', 'Polyline'])
    for dirpath, dirnames, filenames in walk:
        for filename in filenames:
            if inputs.has_key(filename[:-len(filename.split('_')[-1])]):
                if filename.split('_')[-1] == 'dolinowe.shp':
                    inputs[filename[:-len(filename.split('_')[-1])]].insert(0,filename)
                else:
                    inputs[filename[:-len(filename.split('_')[-1])]].append(filename)
            else:
                inputs[filename[:-len(filename.split('_')[-1])]] = list()
                inputs[filename[:-len(filename.split('_')[-1])]].append(filename)

    for item in inputs.iteritems():
        try:
            if len(item[1])>1:
                print item
                for rzedna in warianty:
                    out_tin = os.path.join(tin_fold, str(item[0]) + rzedna)
                    spatial = "PROJCS['ETRS_1989_Poland_CS92',GEOGCS['GCS_ETRS_1989',DATUM['D_ETRS_1989',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',-5300000.0],PARAMETER['Central_Meridian',19.0],PARAMETER['Scale_Factor',0.9993],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
                    arcpy.ddd.CreateTin(out_tin, spatial, [[str(item[1][0]), rzedna, 'Hard_Line', '<None>'], [str(item[1][1]), '<None>', 'Soft_Clip', '<None>']] )
        except:
            print item, ' nie przetworzony'

    return


def renameBranch(workspace):
    walk = arcpy.da.Walk(workspace, datatype="FeatureClass", type="Polyline")
    for dirpath, dirnames, filenames in walk:
        for layer in filenames:
            with arcpy.da.UpdateCursor(layer, ['Branch_km']) as cur:
                for row in cur:
                    row[0] = str(row[0]).replace("-", "_")
                    cur.updateRow(row)

            print layer

    return


def searchZeros(workspace):
    print "Przeszukiwanie zerowych rzednych"+'\n'
    walk = arcpy.da.Walk(workspace, datatype="FeatureClass", type="Polyline")
    for dirpath, dirnames, filenames in walk:
        for layer in filenames:
            # print layer
            if layer.split("_")[-1] =='dolinowe.shp':
                with arcpy.da.SearchCursor(layer, ['RID', 'RZED_PL']) as cur:
                    for row in cur:
                        # if row[1] == 0 or row[2] == 0:
                        if row[1] == 0:
                            print "WARSTWA - ", layer
                            print row[0]

    return


# addRes(tab_wynik, workspace, warianty)
# searchZeros(workspace)
createTINs(workspace, tiny, warianty)
