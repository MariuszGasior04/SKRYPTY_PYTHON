import arcpy, random
arcpy.env.overwriteOutput = True

def selectRandom(inFeauture, outFeature, count, objectIdFieldName):
    oidList = []
    with arcpy.da.SearchCursor(inFeauture, ['OID@']) as search:
        for row in search:
            oidList.append(row[0])
    del search

    selList = random.sample(oidList, k=count)
    whereClause  = objectIdFieldName + ' in ' + str(tuple(selList))
    print(whereClause)
    try:
        arcpy.analysis.Select(inFeauture, outFeature, whereClause)
        print("OK")
    except:
        print("Nie pykło")
    return

if __name__ == '__main__':
    inWarstwa = r'E:\Waloryzajca_rzek_WWF\ROBOCZY_LIPIEC_SIERPIEN_2023\01_06_Pilotazowa_ocena_utraty_siedliska_rzecznego\przekazano_do_analizy_deepsense\zbior_obiektow.shp'
    outWarstwa = r'E:\Waloryzajca_rzek_WWF\ROBOCZY_LIPIEC_SIERPIEN_2023\01_06_Pilotazowa_ocena_utraty_siedliska_rzecznego\przekazano_do_analizy_deepsense\zbior_obiektow_SELECT.shp'
    selectRandom(inWarstwa, outWarstwa, 1000, 'FID')
