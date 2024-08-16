import arcpy
arcpy.env.overwriteOutput = True

def simplifyRiverGeom(riverGeom, riverIDField, riverWidthField, outputRiverGeometry, rFactor = 1.0):
    '''
    Funkcja upraszczająca geometrię rzeki przy uzyciu algorytmu Duglasa-Puckera (REMOVE POINT) przyjmująca jako współczynnik tolerancji szerokość koryta rzeki
    '''
    arcpy.AddMessage('INFO. Upraszczanie geometrii warstwy liniowej {} w oparciu o iloczyn atrybutu {} i współczynnika {}.'.format(riverGeom, riverWidthField, rFactor))
    riverWidths = []
    # tworzymy listę szerokości koryta
    arcpy.AddMessage('INFO. Grupowanie rzek według {}.'.format(riverWidthField))
    with arcpy.da.SearchCursor(riverGeom, [riverIDField, riverWidthField]) as search:
        for row in search:
            if row[1] is not None:
                riverWidths.append(row[1])

    widths = set(riverWidths)

    arcpy.AddMessage('INFO. Selekcja odcinków z przypisaną {}.'.format(riverWidthField))
    # tworzymy tymczasową warstwę z której będziemy wyjmować odcinki o tej samej szerokosci koryta
    river_temp1 = "in_memory/river_temp1"
    wc1 = riverWidthField + " IS NOT NULL"
    arcpy.MakeFeatureLayer_management(riverGeom,river_temp1,where_clause=wc1)
    river_temp2 = "in_memory/river_temp2"
    wc2 = riverWidthField + " IS NULL"
    arcpy.MakeFeatureLayer_management(riverGeom, river_temp2, where_clause=wc2)

    # upraszczamy geometrie odcinków o tej samej szerokości koryta, zapisujemy je do warstw tymczasowych
    inputs_temp = [river_temp2]
    arcpy.AddMessage('INFO. Upraszczanie geometrii odcinków.')

    for width in widths:
        wc3 = riverWidthField + " = " + str(width)
        arcpy.SelectLayerByAttribute_management(river_temp1,'NEW_SELECTION',where_clause = wc3)
        temp = "in_memory/simplified_"+str(width).replace('.','')
        arcpy.cartography.SimplifyLine(river_temp1,temp,"POINT_REMOVE",width*rFactor)
        inputs_temp.append(temp)

    #łączenie uproszczonych geometrii koryta z warstw tymczasowych i zapisanie warstwy wynikowej
    arcpy.AddMessage('INFO. Zapis warstwy wynikowej - {}.'.format(outputRiverGeometry))
    arcpy.Merge_management(inputs_temp,outputRiverGeometry)


    # przeliczenie w warstwie wynikowej liczby punktów węzłowych
    arcpy.AddMessage('INFO. Dodawanie do wynikowej warstwy {} informacji o liczbie werteksów w odcinku po uproszczeniu geometrii.'.format(outputRiverGeometry))
    temp_vertex = "in_memory/vertex"
    temp_table = "in_memory/table_count"
    arcpy.FeatureVerticesToPoints_management(outputRiverGeometry,temp_vertex)
    arcpy.analysis.Statistics(temp_vertex, temp_table, [[riverIDField, "COUNT"]], riverIDField)
    arcpy.JoinField_management(outputRiverGeometry, riverIDField, temp_table, riverIDField, 'COUNT_'+riverIDField)

if __name__ == '__main__':
    inRiver = 'E:\Waloryzajca_rzek_WWF\ROBOCZY_MAJ_2024\Zad3_Weryfikacja_odcinkow_rzeczywistych\Baza_bufory_odcinki.gdb\odcinki_rzek_2024'
    riverIDField = 'ID'
    riverBedWidthField = 'SZER_ODC_2'
    simplifiedRiver = 'E:\Waloryzajca_rzek_WWF\ROBOCZY_MAJ_2024\Zad3_Weryfikacja_odcinkow_rzeczywistych\Baza_bufory_odcinki.gdb\odcinki_rzek_2024_SZER_'

    # simplifyRiverGeom(inRiver, riverIDField, riverBedWidthField, simplifiedRiver + '03', 0.3)
    # simplifyRiverGeom(inRiver, riverIDField, riverBedWidthField, simplifiedRiver + '04', 0.4)
    simplifyRiverGeom(inRiver, riverIDField, riverBedWidthField, simplifiedRiver + '05', 0.5)