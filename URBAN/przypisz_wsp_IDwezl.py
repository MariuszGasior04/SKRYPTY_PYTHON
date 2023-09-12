#!/usr/bin/env python
#-*- coding: utf-8 -*-
#skrypt do przypisania współczynnika splywu z opracowane bazy danych do modelu w URBANIE

import arcpy

def wsp_splyw(msm_HMod, zlewnie):
    """
        Funkcja przypisująca współczynniki splywu do tabeli msm_HMod
    """
    zlew_dict = {}
    print("1-Tworzenie kolekcji ID zlewni, ID Wezlow i wspolczynnikow splywu")

    with arcpy.da.SearchCursor(zlewnie, ['ID', 'ws_splyw', 'ID_Wezla']) as search:
        for row in search:
            zlew_dict[row[0]] = [row[1], row[2]]
    del search

    print("2-Uzupełnianie wspolczynnikow splywu w tabeli msm_HMod")
    with arcpy.da.UpdateCursor(msm_HMod, ['CatchID', 'ImpArea'])as cur:
        for row in cur:
            if row[0] in zlew_dict:
                row[1] = round(float(zlew_dict[row[0]][0])*100, 2)
            cur.updateRow(row)
    del cur

    return zlew_dict

def powiazanie_zlewnia_wezel(msm_CtachCon, zlew_dict):
    """
        Funkcja do  uzupełniania tabeli łacznikowej ID Wezlów i ID zlewni
    """
    print("3-Czyszczenie, przygotowanie do załadaowania tabeli msm_CtachCon")
    arcpy.DeleteRows_management(msm_CtachCon)

    values = []
    for key in zlew_dict.keys():
        values.append((key, key, 1, zlew_dict[key][1], 1))

    print("4-Uzupełnianie tabeli msm_CtachCon")
    with arcpy.da.InsertCursor(msm_CtachCon, ['MUID', 'CatchID', 'TypeNo', 'NodeID', 'Fraction']) as insert:
        for row in values:
            insert.insertRow(row)
    del insert

if __name__ == '__main__':
    zlew = r'C:\robo\URBAN\MODELE\CZEKAJ_DOP2\DANE ZRODLOWE\DANE_URBAN_CZEKAJ_DOP2.gdb\siec\zlewnie'
    msm_Hmod = r'C:\robo\URBAN\MODELE\CZEKAJ_DOP2\CZEKAJ_DOP2_W0.gdb\msm_HModA'
    msm_CatchCon = r'C:\robo\URBAN\MODELE\CZEKAJ_DOP2\CZEKAJ_DOP2_W0.gdb\msm_CatchCon'

    powiazanie_zlewnia_wezel(msm_CatchCon, wsp_splyw(msm_Hmod, zlew))
