import arcpy
import collections

arcpy.env.overwriteOutput = True

def findTouchingVerticles(polygon_name, workspace, output_points):
    arcpy.env.workspace = workspace

    # Initialize empty nodes dataset
    node_list = []
    with arcpy.da.SearchCursor(polygon_name, ['SHAPE@','OID@']) as cursor:
        for row in cursor:
            polygon = row[0]
            i=0
            for part in polygon:
                print(list(part))
                for point in part[1:-2]:
                    if point:
                        node = (row[1], point.X, point.Y)
                        node_list.append(node)  
                    else:
                        node_list.pop()
                        break              
    del cursor

    doublesList = [item for item, count in collections.Counter(node_list).items() if count > 1]
    # print(doublesList)
    point = arcpy.Point()
    pointGeometryList = []
    for node in doublesList:
        point.X = node[1]
        point.Y = node[2]
        pointGeometry = arcpy.PointGeometry(point)
        pointGeometryList.append(pointGeometry)

    # Create new point dataset
    arcpy.CreateFeatureclass_management(workspace, output_points, 'POINT')

    # Inserting nodes to new point dataset
    with arcpy.da.InsertCursor(output_points, ['SHAPE@']) as cursor:
        for point in pointGeometryList:
            cursor.insertRow([point])
    del cursor

    arcpy.AddMessage("New point dataset {} created".format(output_points))
    return

if __name__ == '__main__':
    # polig = arcpy.GetParameterAsText(0)
    # in_gdb = arcpy.GetParameterAsText(1)
    # point_name = arcpy.GetParameterAsText(2)
    polig = r"C:\Users\gasiorm6406\OneDrive - ARCADIS\Documents\ArcGIS\Projects\ICM.gdb\TouchingPoly"
    in_gdb = r"C:\Users\gasiorm6406\OneDrive - ARCADIS\Documents\ArcGIS\Projects\ICM.gdb"
    point_name = "Duble2"
    findTouchingVerticles(polig, in_gdb, point_name)