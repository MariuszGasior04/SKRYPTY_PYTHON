import arcpy

def extractXYZ2txt(infc, txt):
    f = open(txt, "w")
    # Enter for loop for each feature
    for row in arcpy.da.SearchCursor(infc, ["OID@", "SHAPE@"]):
        # the current polygon or polyline's ID
        f.write("ID, X, Y, Z\n")
        partnum = 0

        # Step through each part of the feature
        for part in row[1]:
            # the part number
            # f.write("Part {}:".format(partnum))

            # Step through each vertex in the feature
            for pnt in part:
                if pnt:
                    # x,y,z coordinates of current point
                    try:
                        f.write("{}, {}, {}, {}\n".format(row[0], pnt.X, pnt.Y, pnt.Z))
                    except:
                        f.write("{}, {}, {}, {}\n".format(row[0], pnt.X, pnt.Y, 'brak wsp Z'))
                else:
                    # If pnt is None, this represents an interior ring
                    f.write("Interior Ring:")

            partnum += 1
    arcpy.AddMessage("Zapisano wspolrzedne wezlow warstwy {0} do pliku tekstowego {1}".format(infc, txt))

if __name__ == '__main__':
    infc = arcpy.GetParameterAsText(0)
    txt = arcpy.GetParameterAsText(1)

    extractXYZ2txt(infc, txt)
