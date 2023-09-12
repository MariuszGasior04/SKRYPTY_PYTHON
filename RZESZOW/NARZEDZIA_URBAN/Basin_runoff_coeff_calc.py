import arcpy

def calculate_basin_runoff_coeff(basin, buildings, landcover, coeff, ID_basin, ID_manhole, output):
    arcpy.AddMessage("1-Analiza zlewni poza budynkami modelowanymi")
    inMemory_basin1 = 'in_memory/basin1'
    arcpy.Erase_analysis(basin, buildings, inMemory_basin1)

    arcpy.AddMessage("2-Obliczanie powierzchni zlewni")
    inMemory_basin2 = 'in_memory/basin2'
    arcpy.Dissolve_management(inMemory_basin1, inMemory_basin2, [ID_basin, ID_manhole])
    arcpy.AddField_management(inMemory_basin2, "POW_ZLEW", "DOUBLE")
    arcpy.CalculateField_management(inMemory_basin2, "POW_ZLEW", '!shape.area!', "PYTHON_9.3")

    arcpy.AddMessage("3-Obliczanie powierzchni pokrycia terenu i wspolczynnika splywu")
    inMemory_basin3 = 'in_memory/basin3'
    arcpy.Intersect_analysis ([inMemory_basin2, landcover], inMemory_basin3)
    arcpy.AddField_management(inMemory_basin3, "POW_POK", "DOUBLE")
    arcpy.AddField_management(inMemory_basin3, "WSP_IL", "DOUBLE")
    arcpy.CalculateField_management(inMemory_basin3, "POW_POK", '!shape.area!', "PYTHON_9.3")
    expression = str("!"+coeff+"!*!POW_POK!/!POW_ZLEW!")
    arcpy.CalculateField_management(inMemory_basin3, "WSP_IL", expression, "PYTHON_9.3")

    arcpy.AddMessage("4-Sumowanie wspolczynnika splywu w zlewniach")
    inMemory_basin4 = 'in_memory/basin4'
    arcpy.Dissolve_management(inMemory_basin3, inMemory_basin4, [ID_basin, ID_manhole], [["WSP_IL", 'SUM']])

    arcpy.AddMessage("5-Agregacja zlewni kanalizacji ze zlewniami budynkow")
    inMemory_basin5 = 'in_memory/basin5'
    arcpy.Merge_management([inMemory_basin4, buildings], inMemory_basin5)

    arcpy.AddMessage("6-Porzadkowanie wynikow")
    expression = 'calc(!SUM_WSP_IL!)'
    codeblock = '''def calc(field):
    if field is None:
        return 0.9
    else:
        return round(field, 2)
    '''
    arcpy.CalculateField_management(inMemory_basin5, coeff, expression, "PYTHON_9.3", codeblock)

    arcpy.AddMessage("7-Zapisywanie warstwy wynikowej {0}".format(output))
    arcpy.Dissolve_management(inMemory_basin5, output, [ID_basin, ID_manhole, coeff])

    arcpy.AddMessage("8-Czyszczenie warstw...")
    arcpy.Delete_management(inMemory_basin1)
    arcpy.Delete_management(inMemory_basin2)
    arcpy.Delete_management(inMemory_basin3)
    arcpy.Delete_management(inMemory_basin4)
    arcpy.Delete_management(inMemory_basin5)
    return

if __name__ == '__main__':
    basin = arcpy.GetParameterAsText(0)
    buildings = arcpy.GetParameterAsText(3)
    landcover = arcpy.GetParameterAsText(4)
    coeff = arcpy.GetParameterAsText(5)
    idb = arcpy.GetParameterAsText(1)
    idm = arcpy.GetParameterAsText(2)
    output = arcpy.GetParameterAsText(6)

    calculate_basin_runoff_coeff(basin, buildings, landcover, coeff, idb, idm, output)