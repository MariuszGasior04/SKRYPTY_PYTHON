import math
import arcpy
import os

arcpy.env.overwriteOutput = True

def calculateAz(x1, y1, x2, y2):

    # Obliczanie azymutu w stopniach

    azymut = math.atan(abs((y2 - y1)/(x2 - x1)))
    azymut_stopnie = round(math.degrees(azymut), 2)

    # Określenie w której ćwiartce znajduje się azymut
    if x2 > x1:
        if y2 > y1:
            kwadrat = "I"
            azymut_xns = azymut_stopnie
        elif y2 < y1:
            kwadrat = "IV"
            azymut_xns = 360 - azymut_stopnie
        else:
            kwadrat = "Na osi X"
            azymut_xns = azymut_stopnie
    elif x2 < x1:
        if y2 > y1:
            kwadrat = "II"
            azymut_xns = 180 - azymut_stopnie
        elif y2 < y1:
            kwadrat = "III"
            azymut_xns = 180 + azymut_stopnie
        else:
            kwadrat = "Na osi X"
            azymut_xns = azymut_stopnie
    else:
        if y2 > y1:
            kwadrat = "Na osi Y"
            azymut_xns = azymut_stopnie
        elif y2 < y1:
            kwadrat = "Na osi Y"
            azymut_xns = 180 + azymut_stopnie
        else:
            kwadrat = "Punkt początkowy i końcowy są identyczne"
            azymut_xns = 0

    return azymut_xns, kwadrat

def getLineAz(line, id_przek):
    '''
    Funkcja obliczająca azymut przekroju korytowego
    '''
    az = {}
    # print([field.name for field in arcpy.ListFields(line)])

    arcpy.AddMessage('INFO. Obliczanie azymutów obiektów w wartwie - {}'.format(line))
    with arcpy.da.SearchCursor(line, ['SHAPE@', id_przek]) as search:
        for row in search:
            line_geom = row[0]

            # Pobieranie współrzędnych pierwszego i ostatniego punktu linii.
            # X i Y są celowo zamienione bo w naszych Polskich układach współrzednych osie układów nie są matematyczne
            try:
                x1, y1 = line_geom.firstPoint.Y, line_geom.firstPoint.X
                x2, y2 = line_geom.lastPoint.Y, line_geom.lastPoint.X
            except AttributeError:
                continue

            az[row[1]],k = calculateAz(x1, y1, x2, y2)
            # print(row[1], k)
    # print('Azymuty warstwy {} - {}'.format(line, az))
    return az

def findPointAz(point, river, id_przek):
    '''
    Funkcja obliczająca azymut punktu wzdłóż rzeki w buforze 20m
    '''

    buff_temp = r'memory\Buff'
    dist_buf = "10 Meters"
    arcpy.Buffer_analysis(point, buff_temp, dist_buf)
    in_obj2 = [river, buff_temp]
    intersect_temp_line = r'memory\Odcinki_rzek_przy_przekrojach'
    arcpy.Intersect_analysis(in_obj2, intersect_temp_line)
    az = getLineAz(intersect_temp_line, id_przek)

    return az

def calcRiverXnsCoord(point, river, id_przek):

    riverAz = findPointAz(point, river, id_przek)
    arcpy.AddField_management(point,"AZ","DOUBLE","","",0)
    arcpy.AddField_management(point, "UWAGA", 'TEXT', field_length=254)

    arcpy.AddMessage('INFO. Obliczanie azymutów kierunków punktów przekroi prostopadłych do osi rzeki {} z {}'.format(point, river))

    with arcpy.da.UpdateCursor(point, [id_przek, "AZ", "UWAGA"])as cur:
        for row in cur:
            try:
                pAz = round(abs(riverAz[row[0]]+90))
                row[1] = pAz
            except KeyError:
                arcpy.AddMessage('UWAGA! Dla przekroju/obiektu {} nie wyznaczono azymutu'.format(row[0]))
                row[2] = 'Nie określono kierunku prostopadłego do osi cieku'
            cur.updateRow(row)
    del cur


def lokPktPrzek2Line(point_layer, id_przek, szerokosc_koryta, output_layer_name):
    '''
    Funkcja konwertująca punktową warstw lokalizacji przekroju korytowego na reprezentacje liniową, prostopadła do osi cieku
    '''
    prz_dict = {}
    arcpy.AddMessage("INFO. Odczytywanie warstwy przekroi {}".format(point_layer))
    with arcpy.da.SearchCursor(point_layer, ['SHAPE@X','SHAPE@Y', id_przek, 'AZ', szerokosc_koryta]) as search:
        for row in search:
            # parametr 1.5 jest wilokrotnoscią koryta
            xp = row[0] + (row[4] * 1.5 * math.sin(math.radians(row[3])))
            yp = row[1] + (row[4] * 1.5 * math.cos(math.radians(row[3])))
            xk = row[0] + (row[4] * 1.5 * math.sin(math.radians(row[3]+180)))
            yk = row[1] + (row[4] * 1.5 * math.cos(math.radians(row[3]+180)))

            if row[2] not in prz_dict:
                prz_dict[row[2]] = (tuple((xp, yp)), tuple((xk, yk)))
    del search

    # tworzymy warstwe wynikową
    output_dir = os.path.dirname(point_layer)
    # if '.gdb' in output_dir:
    #     output_layer = os.path.basename(point_layer).split('.')[0] + '_korytowe_projektowane'
    # else:
    #     output_layer = os.path.basename(point_layer).split('.')[0] + '_korytowe_projektowane.shp'

    shp_path = os.path.join(output_dir, output_layer_name)

    arcpy.AddMessage("INFO. Tworzenie warstwy wynikowej {} w lokalizacji {}".format(output_layer_name, output_dir))

    arcpy.management.CreateFeatureclass(output_dir, output_layer_name, geometry_type='POLYLINE',
                                        spatial_reference='ETRS_1989_Poland_CS92')
    arcpy.management.AddField(shp_path, id_przek, 'TEXT', field_length=30)

    arcpy.AddMessage(
        "INFO. Zapis warstwy liniowej przekroi korytowych na warstwie {}".format(output_layer_name))
    with arcpy.da.InsertCursor(shp_path, ["SHAPE@", "ID_PRZEK"]) as przekCur:

        for przekroj in prz_dict:
            geom = arcpy.Polyline(arcpy.Array([arcpy.Point(x[0], x[1]) for x in prz_dict[przekroj]]))
            row = [geom, przekroj]
            przekCur.insertRow(row)
    del przekCur

    return

if __name__ =='__main__':

    crossection = arcpy.GetParameterAsText(0)
    river = arcpy.GetParameterAsText(1)
    id_crossection = arcpy.GetParameterAsText(2)
    river_width_field = arcpy.GetParameterAsText(3)
    output_layer_name = arcpy.GetParameterAsText(4)

    calcRiverXnsCoord(crossection, river, id_crossection)
    lokPktPrzek2Line(crossection,id_crossection,river_width_field, output_layer_name)
