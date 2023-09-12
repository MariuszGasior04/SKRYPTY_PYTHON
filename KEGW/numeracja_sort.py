import arcpy

def dzialaniaSort(dzialania, gdb):
    arcpy.env.workspace = gdb
    i = 1
    a = 0
    with arcpy.da.UpdateCursor(dzialania, ['PageNumber', 'SORT']) as cur:
        for row in cur:
            if row[0] != a:
                i = 1
                row[1] = i
                a = row[0]
            elif row[0] == a:
                row[1] = i
            cur.updateRow(row)
            i+=1
    del cur

if __name__ == '__main__':
    gdb = r'P:\02_Pracownicy\Mariusz\KEGW\DDP_nowe.gdb'
    dzialania = 'dzialania_liniowe_Sort'
    dzialaniaSort(dzialania, gdb)
