#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do przypisania ID studzienki modelowanej sieci kanalizacji do punktów zlewni (kratek lub dachów)

import arcpy

def idStud(workspace, studnie):
    """
    Funkcja tworząca kolekcje id studzienek gdzie wspołrzędne są kluczem, a identyfikator wartością
    """
    dictStudID = {}

    arcpy.env.workspace = workspace  # geobza w ktorej obliczamy kat obrotu figury
    with arcpy.da.SearchCursor(studnie, ['SHAPE@X', 'SHAPE@Y', 'OID@']) as cur:
        for row in cur:
            dictStudID[(round(row[0], 3), round(row[1], 3))] = row[2]
    del cur
    return dictStudID

def idKolektor(workspace, siec):
    """
    Funkcja tworząca dwie kolekcje
    1) id kolektorów gdzie wspołrzędne początku i konca odcinka sieci są kluczem, a lista identyfikatorów wartością
    2) id kolektorów gdzie id odcinków sieci są kluczem a tupla wspołrzędnych początku i konca odcinka sieci jest wartością
    """
    dictSiecID = {}
    dictSiecWsp = {}
    arcpy.env.workspace = workspace
    with arcpy.da.SearchCursor(siec, ['SHAPE@', 'OID@']) as cur:
        for row in cur:
            (xs, ys) = (round(row[0].firstPoint.X, 3), round(row[0].firstPoint.Y, 3))
            (xe, ye) = (round(row[0].lastPoint.X, 3), round(row[0].lastPoint.Y, 3))

            if (xs, ys) not in dictSiecID:
                dictSiecID[(xs, ys)] = [row[1]]
            else:
                dictSiecID[(xs, ys)].append(row[1])

            if (xe, ye) not in dictSiecID:
                dictSiecID[(xe, ye)] = [row[1]]
            else:
                dictSiecID[(xe, ye)].append(row[1])

            dictSiecWsp[row[1]] = ((xs, ys), (xe, ye))
    del cur
    return dictSiecID, dictSiecWsp

def updateStudID(workspace, studnie, siec, kratki):
    """
    Funkcja mająca za zadanie przypisać identyfikatory studzienek na sieci modelowanej obiektom na warstwie kratek
    warstwa kratek musi posiadać atrybut ID_STUDZIENKI. Identyfiakotory sa przypisywane obiektom które w atrybucie ID_STUDZIENEK posiadają wartość NULL
    """
    dStudnie = idStud(workspace, studnie)
    print ("1 - Zbudowano kolekcje ID studzienek modelowanych")
    dKolektorID, dKolektorWsp = idKolektor(workspace, siec)
    print ("2 - Zbudowano kolekcje ID kolektorów analizowanej sieci")

    arcpy.env.workspace = workspace

    arcpy.AddField_management(kratki, field_name = "ID_STUDZIENKI", field_type = "LONG")

    print ("3 - Rozpoczącie przypisywania identyfikatorów studzienek do kratek")

    with arcpy.da.UpdateCursor(kratki, ['SHAPE@X', 'SHAPE@Y', 'OID@', 'ID_STUDZIENKI']) as cur:
        for row in cur:
            if row[3] is None:
                print (row[2])
                wspKratki = (round(row[0], 3), round(row[1], 3))
                if wspKratki in dStudnie:
                    row[3] = dStudnie[wspKratki]
                    print ("Przypisano ID studzienki modelowanej do obiektu o ID {0}".format(row[2]))
                elif wspKratki in dKolektorID:
                    id = dKolektorID[wspKratki][0]
                    ommitIdList = [id]
                    if dKolektorWsp[id][0] in dStudnie or dKolektorWsp[id][1] in dStudnie:
                        try:
                            row[3] = dStudnie[dKolektorWsp[id][0]]
                            print ("Przypisano ID studzienki modelowanej do obiektu o ID {0}".format(row[2]))
                        except KeyError:
                            row[3] = dStudnie[dKolektorWsp[id][1]]
                            print ("Przypisano ID studzienki modelowanej do obiektu o ID {0}".format(row[2]))
                    else:
                        IDlist = list(set(dKolektorID[dKolektorWsp[id][0]] + dKolektorID[dKolektorWsp[id][1]]))
                        try:
                            IDlist.remove(id)
                        except ValueError:
                            pass
                        i = 0
                        while row[3] is None and i < 500:
                            # print IDlist
                            i+=1
                            for id in IDlist:
                                ommitIdList.append(id)
                                ommitIdList = list(set(ommitIdList))
                                if dKolektorWsp[id][0] in dStudnie or dKolektorWsp[id][1] in dStudnie:
                                    try:
                                        row[3] = dStudnie[dKolektorWsp[id][0]]
                                        print ("Przypisano ID studzienki modelowanej do obiektu o ID {0}".format(row[2]))
                                        IDlist.remove(id)
                                        break
                                    except KeyError:
                                        row[3] = dStudnie[dKolektorWsp[id][1]]
                                        print ("Przypisano ID studzienki modelowanej do obiektu o ID {0}".format(row[2]))
                                        IDlist.remove(id)
                                        break
                                else:
                                    IDlist = list(set(IDlist + dKolektorID[dKolektorWsp[id][0]] + dKolektorID[
                                        dKolektorWsp[id][1]]))
                                    try:
                                        for id in ommitIdList:
                                            IDlist.remove(id)
                                    except ValueError:
                                        if IDlist == []:
                                            break
            cur.updateRow(row)
    del cur
    return

if __name__ == '__main__':
    """parametry programu"""
    workspace = r"P:\02_Pracownicy\Mariusz\RZESZOW\DO_MODELOWANIA\Dane_opracowane.gdb\network"
    kratka = 'Odwodnienie_liniowe_pkt1m_00'
    studnie = 'wezly_sieci_modelowanej_01'
    siec = 'Przewody_kan_wylotow_modelowanych'

    updateStudID(workspace, studnie, siec, kratka)
