import arcpy

arcpy.env.overwriteOutput = True

def updateIDcrossection(crossection, id_field, id_hyd_r):
    '''
    Funkca aktualizaująca ID przekroju
    '''
    idHyd_dict = {}
    i = 0
    arcpy.AddMessage('INFO Nadawanie identifikatora w polu {} na podstawie {}'.format(id_field, id_hyd_r))
    with arcpy.da.UpdateCursor(crossection, [id_field, id_hyd_r])as cur:
        for row in cur:
            if row[1] not in idHyd_dict:
                idHyd_dict[row[1]] = 1
            else:
                idHyd_dict[row[1]] += 1
            row[0] = row[1]+'_'+str(idHyd_dict[row[1]])
            i += 1
            print(i)
            cur.updateRow(row)
    del cur

if __name__ == '__main__':

    crossection = arcpy.GetParameterAsText(0)
    id_hyd =  arcpy.GetParameterAsText(2)
    id_cross = arcpy.GetParameterAsText(1)

    updateIDcrossection(crossection, id_cross, id_hyd)