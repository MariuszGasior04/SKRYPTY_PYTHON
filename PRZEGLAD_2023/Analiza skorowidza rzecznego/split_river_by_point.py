import arcpy
import os


def splitLineByPoint(line, point, outputDir):
    list = []
    with arcpy.da.SearchCursor(line, ['ID_HYD_R','NAZWA_MPHP']) as cur:
        for row in cur:
            list.append((row[0], row[1]))
        del cur
    setList = set(list)
    print("1 - Utworzono zestaw ciekow IDHYDR...")

    layerRzeki = "cieki_temp"
    layerKm = "km_temp"
    arcpy.MakeFeatureLayer_management(line,layerRzeki)
    arcpy.MakeFeatureLayer_management(point, layerKm)
    print("2 - Utworzono layery robocze...")
    print("3 - Selekcja i dzielenie cieków w punktach kilometrazu...")
    i = 0
    for river in setList:
        i += 1
        where_clause_river = '"ID_HYD_R" = ' + "'"+river[0]+"'"
        # print(where_clause_river)
        arcpy.SelectLayerByAttribute_management(layerRzeki,"NEW_SELECTION", where_clause_river)
        where_clause_km = '"ID_HYD_R" = ' + "'"+river[0]+"'"
        arcpy.SelectLayerByAttribute_management(layerKm, "NEW_SELECTION", where_clause_km)

        outputRiver = river[1]+'_'+river[0]+'.shp'
        splitedRiver = os.path.join(outputDir, outputRiver)
        arcpy.SplitLineAtPoint_management(layerRzeki, layerKm, splitedRiver,"1 Meters")
        print("...podzielono i zapisano rzeke {} z {} - {}".format(i, len(setList), river))
    print("4 - Pocięto. Zagreguje to tera koleś...")
    return

def merge(dir):
    shpList = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.shp'):
                shpList.append(file)
    print(shpList)
    arcpy.env.workspace = dir
    arcpy.Merge_management(shpList, r"P:\02_Pracownicy\Mariusz\Przeglad_2023\01_Opracowanie wstepne\Opracowanie_skorowidza_rzek\Opracowanie_skorowidza_rzek.gdb\cieki_pociete_ost")

    return

if __name__ == "__main__":
    line = r'P:\02_Pracownicy\Mariusz\Przeglad_2023\01_Opracowanie wstepne\Opracowanie_skorowidza_rzek\Opracowanie_skorowidza_rzek.gdb\cieki_kanaly_skorowidz_diss_v4'
    point = r'P:\02_Pracownicy\Mariusz\Przeglad_2023\01_Opracowanie wstepne\Opracowanie_skorowidza_rzek\Opracowanie_skorowidza_rzek.gdb\kilometraz_MZP_do_ustalenia_referencji_ost'
    outputDir = r'P:\02_Pracownicy\Mariusz\Przeglad_2023\01_Opracowanie wstepne\Opracowanie_skorowidza_rzek\Splited'

    # splitLineByPoint(line, point, outputDir)
    merge(outputDir)