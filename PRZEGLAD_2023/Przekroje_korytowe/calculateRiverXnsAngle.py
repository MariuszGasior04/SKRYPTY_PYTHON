import arcpy
import math

arcpy.env.overwriteOutput = True

def calculateAz(x1, y1, x2, y2):

    # Obliczanie azymutu w stopniach
    try:
        azymut = math.atan(abs((y2 - y1)/(x2 - x1)))
    except ZeroDivisionError:
        azymut = math.atan(abs((y2 - y1) / 0.0001))
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

def getRiverAz(xns, river, id_przek):
    '''
    Funkcja obliczająca azymut rzeki w buforze 10m od przecięcia z przekrojem
    '''
    in_obj1 = [xns, river]
    intersect_temp_point = r'memory\IntersectP'
    buff_temp = r'memory\Buff'
    arcpy.Intersect_analysis(in_obj1, intersect_temp_point, output_type = "POINT")

    dist_buf = "20 Meters"
    arcpy.Buffer_analysis(intersect_temp_point, buff_temp, dist_buf)

    in_obj2 = [river, buff_temp]
    intersect_temp_line = r'memory\Odcinki_rzek_przy_przekrojach'
    arcpy.Intersect_analysis(in_obj2, intersect_temp_line)

    return getLineAz(intersect_temp_line, id_przek)

def calcRiverXnsAngle(xns, river, id_przek):
    xnsAz = getLineAz(xns, id_przek)
    riverAz = getRiverAz(xns, river, id_przek)
    arcpy.AddField_management(xns,"ANGLE","DOUBLE","","",0)
    arcpy.AddField_management(xns, "UWAGA", 'TEXT', field_length=254)

    arcpy.AddMessage('INFO. Obliczanie kątów przecięcia warstwy {} z {}'.format(xns, river))

    with arcpy.da.UpdateCursor(xns, [id_przek, "ANGLE", "UWAGA"])as cur:
        for row in cur:

            try:
                angle = round(abs(riverAz[row[0]]-xnsAz[row[0]]))
                if angle > 200:
                    angle = angle - 180
                if angle >= 70 and angle <= 110:
                    row[1] = angle
                    row[2] = ''
                else:
                    row[1] = angle
                    row[2] = 'Kąt przecięcia przekroju z osią cieku przekracza wartości dopuszczalne'

            except KeyError:
                arcpy.AddMessage('UWAGA! Przekrój/Obiekt {} nie leży na osi cieku'.format(row[0]))
                row[2] = 'Przekrój nie leży na osi cieku'
            cur.updateRow(row)
    del cur

if __name__ =='__main__':

    xns = r'C:\robo\Przeglad_LOKAL_ROBO\Przekroje_geod\Analiza_przekroi_geodezyjnych.gdb\Lupawa_ISOK_przekroje_liniowe_przeglad'
    rzeki = r'C:\robo\Przeglad_LOKAL_ROBO\Przekroje_geod\Analiza_przekroi_geodezyjnych.gdb\zw_aMZPiMRP_skorowidz_rzeki_morze'
    id_kol = 'ID_PRZEKR'

    calcRiverXnsAngle(xns, rzeki, id_kol)
