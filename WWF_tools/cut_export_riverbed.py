#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy, os

def read_idHyd(riverBedShp, idhydr):
    idHydList = []
    with arcpy.da.SearchCursor(riverBedShp, [idhydr]) as search:
        for row in search:
            idHydList.append(row[0])
    del search

    idHydSet = set(idHydList)

    return idHydSet

def cutRiverBed(riverBedShp, riverBedIdhydr, cutLinesShp, cutLineIdhydr, idHydList, outFolder):
    i = 0
    arcpy.MakeFeatureLayer_management(riverBedShp, "river_bed")
    arcpy.MakeFeatureLayer_management(cutLinesShp, "linia_ciecia")
    for item in idHydList:
        i += 1
        riverQuery = riverBedIdhydr +'='+ "'" + item + "'"
        # liniQuery = "identyfika" +'='+ "'" + item + "'"
        liniQuery = cutLineIdhydr + '=' + "'" + item + "'"

        output = 'id_' + item + '.shp'
        arcpy.SelectLayerByAttribute_management("river_bed", "NEW_SELECTION", riverQuery)
        arcpy.SelectLayerByAttribute_management("linia_ciecia", "NEW_SELECTION", liniQuery)
        inFeatures = ["river_bed", "linia_ciecia"]
        outFeatureClass = os.path.join(outFolder, output)
        arcpy.FeatureToPolygon_management(inFeatures, outFeatureClass)
        arcpy.CalculateField_management(outFeatureClass, riverBedIdhydr, item, "PYTHON_9.3")
        arcpy.AddMessage("koryto {0} z {2} o id {1}".format(i, item, len(idHydList)))
    return

if __name__ == '__main__':
    koryta = r'E:\Waloryzajca_rzek_WWF\ROBOCZY_LIPIEC_SIERPIEN_2023\08_Ciecie_buforow_dolinowych\Bufory_i_rzeki\bufory_dolinowe\bufor_dolinowy_RW_16.shp'
    atrIdhyd = 'ID_HYD_R_1'
    linieCiecia = r'E:\Waloryzajca_rzek_WWF\ROBOCZY_LIPIEC_SIERPIEN_2023\08_Ciecie_buforow_dolinowych\Linie_ciecia\Merge\linie_ciecia_merge_1_3_4_9.shp'
    atrIdhyd2 = 'id_mphp'
    folder_wynikowy = r'E:\Waloryzajca_rzek_WWF\ROBOCZY_LIPIEC_SIERPIEN_2023\08_Ciecie_buforow_dolinowych\Ciecie\poprawki'
    # koryta = arcpy.GetParameterAsText(0)
    # atrIdhyd = arcpy.GetParameterAsText(1)
    # linieCiecia = arcpy.GetParameterAsText(2)
    # atrIdhyd2 = arcpy.GetParameterAsText(3)
    # folder_wynikowy = arcpy.GetParameterAsText(4)

    lista_id = read_idHyd(koryta, atrIdhyd)
    cutRiverBed(koryta, atrIdhyd, linieCiecia, atrIdhyd2, lista_id, folder_wynikowy)
