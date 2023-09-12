#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do zmiany nagłowkow tabeli wykazu dzialek i podmiotow wyeksportowanej z swd do dbf. Narzędzie działa tylko na tabelach zaimportowanych do geobazy

import arcpy
import os
import shutil
import zipfile

arcpy.env.overwriteOutput = True

"""PARAMETRY PROGRAMU"""

def zip_extract(zip_dir, output_dir, phrase):
    ''' Funkcja pozwala wypakować tylko te pliki z paczki zip, które zawierają okresloną nazwę lub jej fragment.
        zip_dir - lokalizacja (folder) z plikami zip
        output_dir - lokalizacja w której mają zostać wypakowane pliki
        phraze - część nazwy pliku który chcemy wypakować '''

    for root, dirs, files in os.walk(zip_dir, topdown=False):
        for zip_name in files:
            if os.path.splitext(zip_name)[1] == '.zip':
                with zipfile.ZipFile(os.path.join(root, zip_name), 'r') as zipObject:
                   listOfFileNames = zipObject.namelist()
                   # print listOfFileNames

                   for fileName in listOfFileNames:
                       if phrase in fileName:
                            zipObject.extract(fileName, output_dir)

    return

def create_dir(env, tab, kolumna, output_dir):
    """ Funkcja pozwala na utworzenie serii folderów na podstawie tebeli
        env - lokalizacja robocza (geobaza lub folder
        tab - warstwa/tabela zawierajaca informacje o folderach do utworzenia
        kolumna - kolumna w tabeli/warstwie w która zawiera nazwy folderów do utworzenia
        output_dir - lokalizacja w której mają zostać uworzone foldery """

    arcpy.env.workspace = env
    with arcpy.da.SearchCursor(tab, [kolumna])as cur:
        for row in cur:
            path = os.path.join(output_dir, str(row[0]))
            try:
                os.mkdir(path)
            except OSError as error:
                print(error)

    del cur
    return

def copy_maps(map_dir_input, map_dir_output):
    ''' Funkcja pozwala na kopiowanie map *.pdf z ich lokalizacji do konkretnego folderu w strukturze bazy publikacyjnej
        map_dir_input - główny folder map
        map_dir_output - główny folder map bazy publikacyjnej '''

    for root, dirs, files in os.walk(map_dir_input, topdown=False):
        for name in files:
            if os.path.splitext(name)[1] == '.pdf':
                shutil.copy2(os.path.join(root, name), os.path.join(map_dir_output, name[:6]))
    return

def extract_key(link):
    ''' Funkcja do zamiany hyperlinka mapy ISOK na identyfikator
        hyperlink - hyperlink do mapy (np. http://mapy.isok.gov.pl/pdf/M33006/M33006Ab2_RL_10_2019v1.pdf)'''
    id_key = link.split('/')[-1].split('.')[0][:-7]

    return id_key

def extract_godlo(input):
    ''' Funkcja do generowania godła z nazwy mapy pdf
        input - nazwa mapy'''
    g1 = input.split('_')[0]
    if g1[3:6][0] == '0':
        if g1[3:6][1] == '0':
            godlo = g1[0] + '-' + g1[1:3] + '-' + g1[5:6] + '-' + g1[6] + '-' + g1[7] + '-' + g1[8]
        else:
            godlo=g1[0] + '-' + g1[1:3] + '-' + g1[4:6] + '-' + g1[6] + '-' + g1[7] + '-' + g1[8]
    else:
        godlo = g1[0]+'-'+g1[1:3]+'-'+g1[3:6]+'-'+g1[6]+'-'+g1[7]+'-'+g1[8]

    return godlo

def prepare_tab_record(map_name):
    ''' Funkcja zwracająca tuple mająca być wsadem do zaktualizowanej tabeli konfiguracyjnej
        map_name - nazwa pliku mapy MZP/MRP '''

    mapa = map_name.split('.')[0]

    godlo = (extract_godlo(mapa[:-7]))
    hyperlink = 'http://mapy.isok.gov.pl/pdf/' + mapa[:6] + '/' + map_name + '.pdf'
    typ = mapa.split('_')[1][0]
    # podtyp, qh, typ_txt, podtyp_txt, qh_txt, opis,
    etykieta = None
    id_scen = None
    id_scen_txt = None
    kod_rzeki = None
    rzeka = None
    km = None
    brzeg = None
    nr_scen = None

    if len(mapa.split('_')) == 3:
        if mapa.split('_')[2] in ['10', '1', '02']:
            podtyp = mapa.split('_')[1]
            qh = mapa.split('_')[2]
        elif mapa.split('_')[2] in ['02M']:
            podtyp = mapa.split('_')[1] + mapa.split('_')[2][:-1]
            qh = mapa.split('_')[2][:2]
        elif mapa.split('_')[2] in ['1M', '1WZ', '1WZM']:
            podtyp = mapa.split('_')[1] + mapa.split('_')[2][1:]
            qh = mapa.split('_')[2][0]
    else:
        podtyp = mapa.split('_')[1] + mapa.split('_')[2]
        qh = ''

    if typ == 'R':
        typ_txt = 'Mapa ryzyka powodziowego'
    else:
        typ_txt = 'Mapa zagrożenia powodziowego'

    if podtyp == 'RL':
        podtyp_txt = 'Mapa ryzyka powodziowego – negatywne konsekwencje dla ludności oraz wartości potencjalnych strat powodziowych'
    elif podtyp == 'RLBP':
        podtyp_txt = 'Mapa ryzyka powodziowego – potencjalne negatywne skutki dla życia i zdrowia ludzi oraz wartości potencjalnych strat powodziowych – uszkodzenie lub zniszczenie budowli piętrzącej'
    elif podtyp == 'RLM':
        podtyp_txt = 'Mapa ryzyka powodziowego od strony morza, w tym morskich wód wewnętrznych – negatywne konsekwencje dla ludności oraz wartości potencjalnych strat powodziowych'
    elif podtyp == 'RLWZ':
        podtyp_txt = 'Mapa ryzyka powodziowego – negatywne konsekwencje dla ludności oraz wartości potencjalnych strat powodziowych - całkowite zniszczenie wału przeciwpowodziowego'
    elif podtyp == 'RLWZM':
        podtyp_txt = 'Mapa ryzyka powodziowego – negatywne konsekwencje dla ludności oraz wartości potencjalnych strat powodziowych - całkowite zniszczenie wału przeciwsztormowego'
    elif podtyp == 'RS':
        podtyp_txt = 'Mapa ryzyka powodziowego –  negatywne konsekwencje dla środowiska, dziedzictwa kulturowego i działalności gospodarczej'
    elif podtyp == 'RSBP':
        podtyp_txt = 'Mapa ryzyka powodziowego – potencjalne negatywne skutki dla środowiska, dziedzictwa kulturowego i działalności gospodarczej – uszkodzenie lub zniszczenie budowli piętrzącej'
    elif podtyp == 'RSM':
        podtyp_txt = 'Mapa ryzyka powodziowego od strony morza, w tym morskich wód wewnętrznych – negatywne konsekwencje dla środowiska, dziedzictwa kulturowego i działalności gospodarczej'
    elif podtyp == 'RSWZ':
        podtyp_txt = 'Mapa ryzyka powodziowego –  negatywne konsekwencje dla środowiska, dziedzictwa kulturowego i działalności gospodarczej - całkowite zniszczenie wału przeciwpowodziowego'
    elif podtyp == 'RSWZM':
        podtyp_txt = 'Mapa ryzyka powodziowego –  negatywne konsekwencje dla środowiska, dziedzictwa kulturowego i działalności gospodarczej - całkowite zniszczenie wału przeciwsztormowego'
    elif podtyp == 'ZG':
        podtyp_txt = 'Mapa zagrożenia powodziowego wraz z głębokością wody'
    elif podtyp == 'ZGBP':
        podtyp_txt = 'Mapa zagrożenia powodziowego z głębokością wody – uszkodzenie lub zniszczenie budowli piętrzącej'
    elif podtyp == 'ZGM':
        podtyp_txt = 'Mapa zagrożenia powodziowego od strony morza, w tym morskich wód wewnętrznych'
    elif podtyp == 'ZGWZ':
        podtyp_txt = 'Mapa zagrożenia powodziowego wraz z głębokością wody - całkowite zniszczenie wału przeciwpowodziowego'
    elif podtyp == 'ZGWZM':
        podtyp_txt = 'Mapa zagrożenia powodziowego wraz z głębokością wody - całkowite zniszczenie wału przeciwsztormowego'
    elif podtyp == 'ZP':
        podtyp_txt = 'Mapa zagrożenia powodziowego wraz z prędkościami przepływu wody i kierunkami przepływu wody'

    if qh == '10':
        qh_txt = 'prawdopodobieństwo wystąpienia powodzi 10% – raz na 10 lat'
    elif qh == '1':
        qh_txt = 'prawdopodobieństwo wystąpienia powodzi 1% – raz na 100 lat'
    elif qh == '02':
        qh_txt = 'prawdopodobieństwo wystąpienia powodzi 0,2% – raz na 500 lat'
    else:
        qh_txt = ''

    if 'BP' in podtyp or 'WZ' in podtyp:
        opis = podtyp_txt
    else:
        opis = podtyp_txt + ', ' + qh_txt

    dataimport = '22.06.2022'

    if 'BP' in podtyp:
        zb = map_name.split('_')[3:-1]
        naz = ''
        for item in zb:
            naz = naz + item +' '
        rzeka = 'Zbiornik '+ naz.strip()

    id_wersji = map_name.split('_')[-1]
    rok_wersji = id_wersji.split('v')[0]
    nr_wersji = id_wersji.split('v')[-1]

    return(godlo, unicode(hyperlink), typ, podtyp, qh, typ_txt, podtyp_txt, qh_txt, opis, etykieta, dataimport, id_scen, id_scen_txt, kod_rzeki, rzeka, km, brzeg, nr_scen, id_wersji, rok_wersji, nr_wersji)

def update_conf_tab(env, map_dir_input):
    ''' Funkcja do aktualizowania tabel konfiguracyjnych
        env - lokalizacja robocza (geobaza lub folder)
        map_dir_input - główny folder map '''

    arcpy.env.workspace = env
    tab_zr = 'MAPY_ZR'
    tab_arch = 'MAPY_ZR_ARCH'
    fields = ['GODLO', 'HYPERLINK', 'TYP', 'PODTYP', 'Q_H', 'TYP_TEXT', 'PODTYP_TEXT', 'Q_H_TEXT', 'OPIS', 'ETYKIETA', 'DATAIMPORT', 'ID_SCEN', 'ID_SCEN_TXT', 'KOD_RZEKI', 'RZEKA', 'KM', 'BRZEG', 'NR_SCEN', 'ID_WERSJI', 'ROK_WERSJI', 'NR_WERSJI']
    dict_zr = {}

    with arcpy.da.SearchCursor(tab_zr, fields) as cur:
        for row in cur:
            dict_zr[extract_key(row[fields.index('HYPERLINK')])] = [row[fields.index('GODLO')], row[fields.index('HYPERLINK')], row[fields.index('TYP')], row[fields.index('PODTYP')], row[fields.index('Q_H')], row[fields.index('TYP_TEXT')], row[fields.index('PODTYP_TEXT')], row[fields.index('Q_H_TEXT')], row[fields.index('OPIS')], row[fields.index('DATAIMPORT')], row[fields.index('RZEKA')], row[fields.index('ID_WERSJI')], row[fields.index('ROK_WERSJI')], row[fields.index('NR_WERSJI')]]

        print 'UTWORZONO SLOWNIK Z AKTUALNEJ TABELI KONFIGURACYJNEJ'
    del cur

    for root, dirs, files in os.walk(map_dir_input, topdown=False):
        for name in files:
            if os.path.splitext(name)[1] == '.pdf' and os.path.splitext(name)[0].split('_')[-1] != 'archiwalna':
                dict_key = os.path.splitext(name)[0][:-7]
                # sprawdzamy czy mapa jest w tabeli konfiguracyjnej
                if dict_zr.has_key(dict_key):

                    #sprawdzmy czy mapa jest w nowszej wersji niż ta zapisana w tabeli konfiguracyjnej
                    if long(dict_zr[dict_key][12]) < long(os.path.splitext(name)[0].split('_')[-1].split('v')[0]):

                        # mapa jest w nowszej wersji. Dodajemy wpis do archwalnej tabeli konfiguracyjnej
                        cur = arcpy.da.InsertCursor(tab_arch, fields)
                        cur.insertRow((dict_zr[dict_key][0],
                                       dict_zr[dict_key][1].replace('.pdf', '_archiwalna.pdf'),
                                       dict_zr[dict_key][2],
                                       dict_zr[dict_key][3],
                                       dict_zr[dict_key][4],
                                       dict_zr[dict_key][5],
                                       dict_zr[dict_key][6],
                                       dict_zr[dict_key][7],
                                       dict_zr[dict_key][8],
                                       '',
                                       dict_zr[dict_key][9],
                                       '',
                                       '',
                                       '',
                                       dict_zr[dict_key][10],
                                       '',
                                       '',
                                       '',
                                       dict_zr[dict_key][11],
                                       dict_zr[dict_key][12],
                                       dict_zr[dict_key][13]))

                        del cur

                        # zmieniamy nazwę starej mapy (dodajemy dopisek _archiwalna)
                        old_map = os.path.join(root, dict_zr[dict_key][1].split('/')[-1])
                        new_name = dict_zr[dict_key][1].split('/')[-1]
                        new_map = os.path.join(root, new_name.replace('.pdf', '_archiwalna.pdf'))
                        os.rename(old_map, new_map)

                        # usówamy z tabeli konfiguracyjnej rekord starej mapy
                        with arcpy.da.UpdateCursor(tab_zr, fields) as cursor:
                            for row in cursor:
                                if row[1] == dict_zr[dict_key][1]:
                                    cursor.deleteRow()
                        del cursor

                        # dodajemy do tabeli konfiguracyjnej nową mapę
                        cur = arcpy.da.InsertCursor(tab_zr, fields)
                        cur.insertRow(prepare_tab_record(unicode(os.path.splitext(name)[0])))

                        del cur

                else:
                    # dodajemy do tabeli konfiguracyjnej nową mapę
                    cur = arcpy.da.InsertCursor(tab_zr, fields)
                    cur.insertRow(prepare_tab_record(unicode(os.path.splitext(name)[0])))

                    del cur
    return

def batch_rename(map_dir_input):
    for root, dirs, files in os.walk(map_dir_input, topdown=False):
        for name in files:
            if os.path.splitext(name)[1] == '.pdf':
                if u'Sulejów' in name:
                    print name
                    new_name = name[:16] + "Sulejow" + name[-11:]
                    os.rename(os.path.join(root, name), os.path.join(root, new_name))

    return

if __name__ == '__main__':
    env = r'D:\DaneRobocze\2_Hydroportal_PDF\MZPiMRP_pub.gdb'
    tab = 'Lista_folder_pdf.dbf'
    map_dir = r'R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\5_Opracowanie_kartograficzne\MAPY_ETAP3'
    map_dir2 = r'R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\9_Baza_publikacyjna\Publikacja_mzpimrp_bp\2_Hydroportal_PDF\pdf'
    zip_dir = r'R:\OIIS_KR5\_BRANŻOWE\_GIS\BDOT10k\BDOT10k_SHP_2'
    zip_output = r'D:\FolderRoboczy\BDOT_BUZM'
    # batch_rename(map_dir2)

    # update_conf_tab(env, map_dir2)
    zip_extract(zip_dir, zip_output, 'BUZM')