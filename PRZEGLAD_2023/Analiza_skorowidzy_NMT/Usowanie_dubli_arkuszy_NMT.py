import os
import arcpy

def clearDTMdubles(featureDataset):
    wykaz = {}
    kol = [str(field.name) for field in arcpy.ListFields(featureDataset)]
    # print(kol)
    with arcpy.da.SearchCursor(featureDataset, kol) as cur:
        for row in cur:
            if row[kol.index('godlo')] in wykaz:
                wykaz[row[kol.index('godlo')]].append([row[kol.index('OBJECTID')],row[kol.index('akt_data')],row[kol.index('format')],row[kol.index('blad_sr_wy')],0])
            else:
                wykaz[row[kol.index('godlo')]] = [[row[kol.index('OBJECTID')],row[kol.index('akt_data')],row[kol.index('format')],row[kol.index('blad_sr_wy')],0]]
        del cur

    # print(wykaz)
    for key in wykaz.keys():
        a = wykaz[key]
        if len(a) == 3:
            a[0][4] = (1 if a[0][3] > a[1][3] else 0)
            a[1][4] = (1 if a[0][3] < a[1][3] else 0)
            a[0][4] = (1 if a[0][3] > a[2][3] else 0)
            a[2][4] = (1 if a[0][3] < a[2][3] else 0)
            a[1][4] = (1 if a[1][3] > a[2][3] else 0)
            a[2][4] = (1 if a[1][3] < a[2][3] else 0)
        elif len(a) == 2:
            a[0][4] = (1 if a[0][3] > a[1][3] else 0)
            a[1][4] = (1 if a[0][3] < a[1][3] else 0)
            if a[0][3] == a[1][3] and a[0][2] == 'ASCII XYZ GRID':
                a[0][4] = 1
            if a[0][3] == a[1][3] and a[1][2] == 'ASCII XYZ GRID':
                a[1][4] = 1

    l = []
    for value in wykaz.values():
        for record in value:
            if record[4] == 1:
                l.append(record[0])

    print(len(l))

    with arcpy.da.UpdateCursor(featureDataset, kol) as cursor:
        for row in cursor:
            if row[kol.index('OBJECTID')] in l:
                print(row[kol.index('OBJECTID')])
                cursor.deleteRow()
    del cursor

    return
if __name__ == "__main__":
    layer = r'P:\02_Pracownicy\Mariusz\Przeglad_2023\01_Opracowanie wstepne\Analiza skorowidzy NMT\Skorowidze.gdb\skorowidz_NMT_data_xy2000_filtr'
    clearDTMdubles(layer)