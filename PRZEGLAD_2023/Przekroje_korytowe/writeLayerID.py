import arcpy

arcpy.env.overwriteOutput = True

def updateIDPrzek(layer, id_field, id_hyd_r):
    idHyd_dict = {}
    i = 0
    with arcpy.da.UpdateCursor(layer, [id_field, id_hyd_r])as cur:
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

    pzekroje = r'C:\robo\Przeglad_LOKAL_ROBO\KOMPLEKSOWA_OCENA\wyznaczane_przekroje.gdb\przekroje_pkt_P1_P2'
    updateIDPrzek(pzekroje)
