import arcpy, requests

def getPointElevation(x, y):
    url = f'https://services.gugik.gov.pl/nmt/?request=GetHByXY&x={x}&y={y}'
    
    response = requests.get(url)
    if response.status_code == 200:
        elevation_data = response.json()
        return elevation_data
    else:
        print(f"Nie uzyskoano danych wysokościowych. Status code: {response.status_code}")
        return None


def getPointsElevation(listXY):
    url = f'https://services.gugik.gov.pl/nmt/?request=GetHByPointList&list={listXY}'
    # 'https: // services.gugik.gov.pl / nmt /?request = GetHByPointList & list = 563800 243490, 563950 243490, 563950 243400'

    response = requests.get(url)
    if response.status_code == 200:
        elevation_data = response.text
        return elevation_data
    else:
        print(f"Nie uzyskoano danych wysokościowych. Status code: {response.status_code}")
        return None

def calcZ(pointLayer):
    '''
    Funkcja do oblicznia Z
    :return:
    '''
    i=0
    with arcpy.da.UpdateCursor(pointLayer, ['Z', 'SHAPE@X', 'SHAPE@Y','OID@']) as update:
    # with arcpy.da.UpdateCursor(lineLayer, ['SPADEK', 'Shape_Length', 'SHAPE@','Wkp','ROZNICA_WYS']) as update:
        for row in update:
            if row[0] is None:

                y1 = row[1]
                x1 = row[2]
                z1 = getPointElevation(x1, y1)
                row[0] = z1
                print(row[3])
                update.updateRow(row)

        del update
    return

if __name__ == "__main__":
    x = 486617
    y = 637928
    listCoordinates = '563800.2 243490, 563950 243490.56, 563910.11 243400.255'
    pointlayer = r'E:\Waloryzajca_rzek_WWF\ROBOCZY_CZERWIEC_2024\Zad_03_Poprawa budowli\OB_HYDRO_MOST.gdb\Obiekty_hydro_PointsAlongLines2'
    calcZ(pointlayer)
    # elevation = getPointElevation(x, y)
    # elevations = getPointsElevation(listCoordinates)
    #
    # if elevation is not None:
    #     print(f"Wysokość w punkcie o współrzędnych ({x}, {y}): {elevation} metrów nad poziomem morza")
    #     print(elevations)
    # else:
    #     print("Nie uzyskano danych wysokościowych.")