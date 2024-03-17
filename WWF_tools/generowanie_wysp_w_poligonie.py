import arcpy

arcpy.env.overwriteOutput = True

def getHoleGeometry(polygon_name, workspace, output_polygon, output_polyline):
    arcpy.env.workspace = workspace

    #  Create new polygone dataset
    arcpy.CreateFeatureclass_management(workspace, output_polygon, 'POLYGON')
    arcpy.AddField_management(output_polygon,'ID_HYD_R','TEXT',field_length=25)

    #  Create new polyline dataset
    arcpy.CreateFeatureclass_management(workspace, output_polyline, 'POLYLINE')
    arcpy.AddField_management(output_polyline, 'ID_HYD_R', 'TEXT', field_length=25)

    # Initialize empty nodes dataset
    node_dict = {}
    p=0
    with arcpy.da.SearchCursor(polygon_name, ['SHAPE@','OID@','ID_HYD_R_10']) as cursor:
        for row in cursor:
            polygon = row[0]
            i=0
            holeBool = False

            # reading polygon geometry
            for part in polygon:
                for point in part:
                    # getting geometry of polygon's hole element and saving it to nodes dataset
                    if point is None:
                        p += 1
                        holeBool = True
                    if holeBool and point:
                        if p not in node_dict:
                            node_dict[p]= [point]
                        else:
                            node_dict[p].append(point)

            # inserting polygon's hole geometry to new polygon dataset
            with arcpy.da.InsertCursor(output_polygon, ['SHAPE@','ID_HYD_R']) as cursorPolig:
                for key in node_dict:
                    cursorPolig.insertRow([arcpy.Polygon(arcpy.Array(node_dict[key])), row[2]])
            del cursorPolig

            # inserting polygon's hole geometry to new polyline dataset
            with arcpy.da.InsertCursor(output_polyline, ['SHAPE@','ID_HYD_R']) as cursorPolyline:
                for key in node_dict:
                    cursorPolyline.insertRow([arcpy.Polyline(arcpy.Array(node_dict[key])), row[2]])
            del cursorPolyline

            node_dict = {}

            print('{} - Zapisano wyspy dla rzeki id = {}'.format(row[1], row[2]))

    del cursor

    return

def getHoleGeometryAll(polygon_name, workspace, output_polygon, output_polyline):
    arcpy.env.workspace = workspace

    #  Create new polygone dataset
    arcpy.CreateFeatureclass_management(workspace, output_polygon, 'POLYGON',spatial_reference=polygon_name)
    arcpy.AddField_management(output_polygon, 'ORIG_FID', 'LONG')
    #  Create new polyline dataset
    arcpy.CreateFeatureclass_management(workspace, output_polyline, 'POLYLINE', spatial_reference=polygon_name)
    arcpy.AddField_management(output_polyline, 'ORIG_FID', 'LONG')
    # Initialize empty nodes dataset
    node_dict = {}
    p=0
    with arcpy.da.SearchCursor(polygon_name, ['SHAPE@','OID@']) as cursor:
        for row in cursor:
            polygon = row[0]
            i=0
            holeBool = False

            # reading polygon geometry
            for part in polygon:
                for point in part:
                    # getting geometry of polygon's hole element and saving it to nodes dataset
                    if point is None:
                        p += 1
                        holeBool = True
                    if holeBool and point:
                        if p not in node_dict:
                            node_dict[p]= [point]
                        else:
                            node_dict[p].append(point)

            # inserting polygon's hole geometry to new polygon dataset
            with arcpy.da.InsertCursor(output_polygon, ['SHAPE@','ORIG_FID']) as cursorPolig:
                for key in node_dict:
                    cursorPolig.insertRow([arcpy.Polygon(arcpy.Array(node_dict[key])), row[1]])
            del cursorPolig

            # inserting polygon's hole geometry to new polyline dataset
            with arcpy.da.InsertCursor(output_polyline, ['SHAPE@','ORIG_FID']) as cursorPolyline:
                for key in node_dict:
                    cursorPolyline.insertRow([arcpy.Polyline(arcpy.Array(node_dict[key])), row[1]])
            del cursorPolyline

            node_dict = {}

            print('{} - Zapisano wyspy'.format(row[1]))

    del cursor

    return

if __name__ == '__main__':
    # input
    rzeki = r"bufory_dolinowe_pociete_PL6000_po_korekcie"
    worspace = r"E:\Waloryzajca_rzek_WWF\ROBOCZY_PAZDZIERNIK_2023\Zad5\Dane do manualnej korekty ciecia buforow.gdb"
    #output
    output_polig = "wyspy_polig"
    output_polyline = "wyspy_polyline"

    getHoleGeometryAll(rzeki, worspace, output_polig, output_polyline)