import arcpy, os

def read_idHyd(riverLineShp, idhydr):
    idHydList = []
    with arcpy.da.SearchCursor(riverLineShp, [idhydr]) as search:
        for row in search:
            # if row[0] == '2':
            idHydList.append(row[0])
    del search

    idHydSet = set(idHydList)

    return idHydSet

def cutRiverLine(riverLineShp, riverLineIdhydr, cutLinesShp, cutLineIdhydr, idHydList, outputLayer):
    i = 0
    temp_list = []
    arcpy.MakeFeatureLayer_management(riverLineShp, "river_line")
    arcpy.MakeFeatureLayer_management(cutLinesShp, "punkty_ciecia")
    for item in idHydList:
        i += 1
        riverQuery = riverLineIdhydr + '=' + "'" + item + "'"
        # liniQuery = "identyfika" +'='+ "'" + item + "'"
        pointQuery = cutLineIdhydr + '=' + "'" + item + "'"

        arcpy.SelectLayerByAttribute_management("river_line", "NEW_SELECTION", riverQuery)
        arcpy.SelectLayerByAttribute_management("punkty_ciecia", "NEW_SELECTION", pointQuery)

        outFeatureClass = 'memory\cut_'+'id_' + item
        searchRadius = '1 Meters'
        arcpy.management.SplitLineAtPoint("river_line", "punkty_ciecia", outFeatureClass,
                                          searchRadius)
        temp_list.append(outFeatureClass)
        # arcpy.CalculateField_management(outFeatureClass, riverLineIdhydr, item, "PYTHON_9.3")
        arcpy.AddMessage("koryto {0} z {2} o id {1}".format(i, item, len(idHydList)))

    arcpy.management.Merge(temp_list, outputLayer)
    arcpy.AddMessage("Zapisano warstwe {0} ".format(outputLayer))
    return

if __name__ == '__main__':
    koryta = r'E:\Waloryzajca_rzek_WWF\ROBOCZY_LISTOPAD_2023\Nowa warstwa odcinkow rzek\Robocze.gdb\_4_rzeki_integracja_ramiona_boczne'
    atrIdhyd = 'ID_HYD_R_10'
    linieCiecia = r'E:\Waloryzajca_rzek_WWF\ROBOCZY_LISTOPAD_2023\Nowa warstwa odcinkow rzek\Robocze.gdb\START_END_odcinki_stare_ramiona_boczne'
    atrIdhyd2 = 'ID_HYD_R_10_rzeki'
    arstwa_wynik = r'E:\Waloryzajca_rzek_WWF\ROBOCZY_LISTOPAD_2023\Nowa warstwa odcinkow rzek\Robocze.gdb\_5_pociete_ramiona_boczne_a'

    lista_id = read_idHyd(koryta, atrIdhyd)

    cutRiverLine(koryta, atrIdhyd, linieCiecia, atrIdhyd2, lista_id, arstwa_wynik)
