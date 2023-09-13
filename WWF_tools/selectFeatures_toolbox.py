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

    try:
        arcpy.analysis.Select(inFeauture, outFeature, whereClause)
        arcpy.AddMessage("Utworzono warstwe {} wyselekcjonowanych {} obiektow".format(outFeature, count))
    except:
        arcpy.AddMessage("Selekcja nie powiodla sie")
    return

if __name__ == '__main__':
    inWarstwa = arcpy.GetParameterAsText(0)
    outWarstwa = arcpy.GetParameterAsText(3)
    count = arcpy.GetParameterAsText(1)
    idFiledName = arcpy.GetParameterAsText(2)

    selectRandom(inWarstwa, outWarstwa, int(count), idFiledName)
