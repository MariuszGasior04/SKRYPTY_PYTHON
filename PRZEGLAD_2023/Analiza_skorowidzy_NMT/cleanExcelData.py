import pandas as pd
import arcpy

def cleanExcellData(excell):
    d = {}
    df = pd.read_excel(excell,sheet_name='Arkusz1')
    for row in df.values:
        d[row[9]] = []
    for row in df.values:
        d[row[9]].append(row[11])
        d[row[9]].append(row[12])
    print(d)
    for k in d:
        d[k] = set(d[k])
    print(d)
    return d


if __name__ == '__main__':
    excell_file = r"C:\robo\Przeglad_LOKAL_ROBO\wynikowy zbiorczy 2019.xlsx"
    warstwa = r'C:\robo\Przeglad_LOKAL_ROBO\Skorowidz_NMT\Opracowanie_skorowidzy_NMT_local.gdb\obszar_zagrozenia_pow_rzeki_WZ'
    d = cleanExcellData(excell_file)

    with arcpy.da.UpdateCursor(warstwa, ['ID_HYD_R', 'WERSJA', 'roboczy', 'NMT_ROK']) as update:
        for row in update:
            if row[1] == '2019v1':
                try:
                    row[2] = str(d[int(row[0])]).replace('{','').replace('}','')
                    update.updateRow(row)
                except KeyError as k:
                    print('Brak rzeki {} w słowniku'.format(row[0]))
                    pass

    del update