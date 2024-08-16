import os
import arcpy
import networkx

arcpy.env.overwriteOutput = True

def shp2longestPathNetwork(shpFile):
    '''Funkcja zamieniająca warstwe liniową shp na DAG network. Zwraca network najdłuższej sciezki z shp wejsciowego'''

    network = networkx.read_shp(shpFile, simplify=False, geom_attrs=True, strict=True)
    longestPathNetwork = networkx.DiGraph(networkx.dag_longest_path(network))

    return longestPathNetwork

def longestPaths2Shp(shpFile, catchmentField, outWorkspace, outLongestStream):
    '''Funkcja zapisująca najdłuższe scieżki spływu danej sieci rzecznej do nowej warstwy liniowej z atrybutem ID zlewni'''

    arcpy.env.workspace = outWorkspace

    arcpy.AddMessage("1 - Sczytywanie zlewni...")
    catchList = set()
    with arcpy.da.SearchCursor(shpFile, [catchmentField]) as cur:
        for row in cur:
            catchList.add(row[0])

    i = 1
    arcpy.AddMessage("2 - Tworzenie pustej warstwy wynikowej {}".format(outLongestStream))
    arcpy.CreateFeatureclass_management(outWorkspace, outLongestStream, 'POLYLINE')
    arcpy.AddField_management(outLongestStream, catchmentField, 'TEXT', field_length = 100)

    arcpy.AddMessage("3 - Przetwarzanie sciezek splywu dla {} zlewni...".format(len(catchList)))
    for catchmentID in catchList:
        arcpy.AddMessage("...przetwarzanie zlewni nr {} o ID {} i dodawanie najdluzszej sciezki splywu do {}".format(i, catchmentID, outLongestStream))

        temp_shp = os.path.join(os.path.dirname(shpFile), 'temp.shp')
        where_clause = '"'+catchmentField+'"'+'=' + str(catchmentID)
        arcpy.Select_analysis(shpFile, temp_shp, where_clause)
        network = shp2longestPathNetwork(temp_shp)

        wsp = []
        for node in network.edges:
            wsp.append(arcpy.Point(node[0], node[1]))
        array = arcpy.Array(wsp)
        polyline = arcpy.Polyline(array)

        # dodawanie geometrii najdłuzszej sciezki splywu do wynikowej warstwy
        cursor = arcpy.da.InsertCursor(outLongestStream, ['SHAPE@', catchmentField])
        cursor.insertRow([polyline, str(catchmentID)])
        i += 1
        del cursor

        arcpy.Delete_management(temp_shp)

if __name__ == '__main__':
    # r"C:\robo\_warstwy_tymczasowe\rzeszow\zlewnie\sciezki_splywu_zlewnie.shp"
    inShp = arcpy.GetParameterAsText(0)
    cField = arcpy.GetParameterAsText(1)
    oWorkspace = arcpy.GetParameterAsText(2)
    oLayer = arcpy.GetParameterAsText(3)

    longestPaths2Shp(inShp, catchmentField=cField, outWorkspace=oWorkspace, outLongestStream=oLayer)
