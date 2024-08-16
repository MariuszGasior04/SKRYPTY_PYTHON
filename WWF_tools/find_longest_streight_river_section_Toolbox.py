import arcpy
import math
import os

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

def calcGeomArrayLength(array):
    '''Funkcja obliczająca długość ze współrzędnych geometrii'''
    geomLength = 0
    for i in range (0, len(array)-1):
        try:
            y1 = array[i].X
            x1 = array[i].Y
            y2 = array[i+1].X
            x2 = array[i+1].Y
            gLength = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
            geomLength += gLength
        except IndexError:
            arcpy.AddMessage('Prekroczono maksymalny indeks geometrii przy oblicziu dlugosci geometrii')
        continue
    return geomLength

def readGeomToMemory(inLineGeom):
    '''Funkca zczytująca geometrię rzek i zwracająca kolekcje tej geometrii jako słownik'''
    dGeom = {}
    with arcpy.da.SearchCursor(inLineGeom, ['OID@', 'SHAPE@']) as search:
        for row in search:
            dGeom[row[0]]=list(row[1])
    arcpy.AddMessage('INFO. Zaczytano  geometrie odcinkow rzek do pamieci.')
    return dGeom

def findLongestStreightSection(dictGeom, azDiffBorderValue):
    '''Funkcja zwracająca najdłuzszy prosty odcinek w geometrii linii'''
    maxLength = 0
    maxGeom = {}
    for k in dictGeom:
        for array in dictGeom[k]:
            for i in range (0,len(array)-1):
                azDiff = 0
                try:
                    y1 = array[i].X
                    x1 = array[i].Y
                    y2 = array[i + 1].X
                    x2 = array[i + 1].Y
                    az0 = calculateAz(x1, y1, x2, y2)[0]
                    j = i+1
                    # Tutaj wprowadzamy graniczną różnicę azymutów wskazująca na meandrowanie odcinka rzeki
                    while azDiff < azDiffBorderValue and j < len(array)-1:
                        y3 = array[j + 1].X
                        x3 = array[j + 1].Y
                        az1 = calculateAz(x1, y1, x3, y3)[0]
                        azDiff = abs(az1 - az0)

                        j += 1
                    if k not in maxGeom:
                        maxGeom[k] = array[i:j+1]
                        lengthCon = calcGeomArrayLength(array[i:j + 1])

                    elif lengthCon < calcGeomArrayLength(array[i:j+1]):
                        maxGeom[k] = array[i:j+1]
                        lengthCon = calcGeomArrayLength(array[i:j + 1])

                except IndexError:
                    arcpy.AddMessage('Przeliczono azymuty wszystkich werteksow obiektu {}. Max{}. Int i {}. Int j {}'.format(k,len(array), i, j))
                    continue
        # print(k, len(maxGeom[k]), len(dictGeom[k][0]))
    arcpy.AddMessage('INFO. Zaczytano najdluzsze geometrie prostych odcinkow rzek')
    return maxGeom

def convertGeomToShp(geom, outputShpFilePath):
    '''Funkcja zamieniajaca kolekcję geometrii na shp'''
    output_dir = os.path.dirname(outputShpFilePath)
    output_shp = os.path.basename(outputShpFilePath).split('.')[0] + '.shp'
    arcpy.management.CreateFeatureclass(output_dir, output_shp, geometry_type = 'POLYLINE', spatial_reference = SPATIAL_REF)
    arcpy.AddField_management(os.path.join(output_dir, output_shp), 'ID', 'LONG')
    arcpy.AddMessage('INFO. Utworzono warstwe liniowa {} w lokalizacji {}'.format(output_shp,output_dir))
    for k in geom:
        polyline = arcpy.Polyline(geom[k])
        cursor = arcpy.da.InsertCursor(os.path.join(output_dir, output_shp),
                                       ['SHAPE@', 'ID'])

        cursor.insertRow([polyline, k])
    arcpy.AddMessage('INFO. Zaladowano geometrie prostych odcinkow rzek do warstwy liniowej {} w lokalizacji {}'.format(output_shp, output_dir))

if __name__ == '__main__':

    warstwa_rzek = arcpy.GetParameterAsText(0)
    output_shp = arcpy.GetParameterAsText(1)
    maks_odchylka_az = arcpy.GetParameterAsText(2)

    SPATIAL_REF = arcpy.Describe(warstwa_rzek).spatialReference
    geom = readGeomToMemory(warstwa_rzek)
    longestGeom = findLongestStreightSection(geom, float(maks_odchylka_az))
    convertGeomToShp(longestGeom, output_shp)