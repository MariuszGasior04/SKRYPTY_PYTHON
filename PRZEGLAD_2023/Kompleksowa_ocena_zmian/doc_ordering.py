import arcpy, os, shutil

def readLayerUwInw(layer):
    '''Funkcja do czytania ID_UW i ID_INW z atrybutów warstwy P18b'''
    dict_inw = {}
    dict_uw = {}
    with arcpy.da.SearchCursor(layer, ['ID_ODC_RZ', 'ID_INW_A','ID_UW_A']) as search:
        for row in search:
            if row[1] != 'Nie dotyczy' and row[1] is not None:
                if row[0] not in dict_inw:
                    if row[1].split(';') != ['']:
                        dict_inw[row[0]] = row[1].split(';')
                else:
                    if row[1].split(';') != ['']:
                        dict_inw[row[0]] + row[1].split(';')

            if row[2] != 'Nie dotyczy' and row[2] is not None:
                if row[0] not in dict_uw:
                    if row[2].split(';') != ['']:
                        dict_uw[row[0]] = row[2].split(';')
                else:
                    if row[2].split(';') != ['']:
                        dict_uw[row[0]] + row[2].split(';')
    for k in dict_inw:
        dict_inw[k] = [item.strip() for item in dict_inw[k] if item]
    for k in dict_uw:
        dict_uw[k] = [item.strip() for item in dict_uw[k] if item]
    u = 0
    j = 0
    for k in dict_inw:
        for i in dict_inw[k]:
            print(i)
            j+=1
    for k in dict_uw:
        for i in dict_uw[k]:
            print(i)
            u += 1
    arcpy.AddMessage('{} - {}'.format(j, dict_inw))
    arcpy.AddMessage('{} - {}'.format(u, dict_uw))
    return

def readLayerWaBa(layer):
    '''Funkcja do czytania WSKAZ_A z atrybutów warstwy P18b'''
    dict_wa = []
    dict_ba = []
    with arcpy.da.SearchCursor(layer, ['ID_ODC_RZ', 'WSKAZ_A']) as search:
        for row in search:
            if row[1] == 'WA':
                dict_wa.append(row[0])
            else:
                dict_ba.append(row[0])

    return dict_wa, dict_ba

def find_move_file(in_folder, out_folder, phrase):

    for root, dirs, files in os.walk(in_folder, topdown=False):
        #iteracja po plikach
        # print(u"Przeszukuję folder:"+"\n"+root)
        for name in files:
          ###print(os.path.join(root, name))
        #znajdywanie plikow zawierających okreslona fraze i kopiowanie ich do nowej loklaizacji
          if phrase in name:
            shutil.move(os.path.join(root, name),out_folder)

if __name__ == '__main__':
    layer = r'P:\02_Pracownicy\Mariusz\Przeglad_2023\02_Baza_produkty\05_Produkty\CALOSC\2.01\PRZEGLAD_MZPiMRP.gdb\P18b_Wyniki_Przeglad_rzeki_v201'
    tif_in_folder = r'C:\robo\Przeglad_LOKAL_ROBO\KOMPLEKSOWA_OCENA\ZMIANY NMT II PARTIA\3M.1.12a'
    tif_out_folder_WA = r'C:\robo\Przeglad_LOKAL_ROBO\KOMPLEKSOWA_OCENA\ZMIANY NMT II PARTIA\ZMIANY_NMT_WA'
    tif_out_folder_BA = r'C:\robo\Przeglad_LOKAL_ROBO\KOMPLEKSOWA_OCENA\ZMIANY NMT II PARTIA\ZMIANY_NMT_BA'

    wa, ba = readLayerWaBa(layer)
    arcpy.AddMessage('INFO - Przenoszenie tifów odcinków WSKAZANYCH do aktualizacji')
    for odc_akt in wa:
        find_move_file(tif_in_folder, tif_out_folder_WA, odc_akt)

    arcpy.AddMessage('INFO - Przenoszenie tifów odcinków NIE WSKAZANYCH do aktualizacji')
    for odc_nakt in ba:
        find_move_file(tif_in_folder, tif_out_folder_BA, odc_nakt)
