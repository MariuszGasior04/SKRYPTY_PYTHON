#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do obracania kierunku rysowania linii sieci uzbrojenia terenu w kierunku wylotu

import arcpy
arcpy.env.overwriteOutput = True

def createFlippedLineGeom(workspace, line, line_flip):
    """
    Funkcja tworząca kolekcje id linii o obróconej geometrii gdzie wspołrzędne są kluczem, a identyfikator wartością
    """
    arcpy.env.workspace = workspace
    arcpy.Copy_management(line, line_flip)
    arcpy.FlipLine_edit(line_flip)
    line_geom = {}
    with arcpy.da.SearchCursor(line_flip, ['SHAPE@', 'OID@']) as cur:
        for row in cur:
            line_geom[row[1]] = row[0]
    arcpy.Delete_management(line_flip)
    return line_geom

def readEndpoint(workspace, point):
    """
    Funkcja tworząca kolekcje id punktów wylotowych gdzie wspołrzędne są kluczem, a identyfikator wartością
    """
    dictPointID = {}

    arcpy.env.workspace = workspace  # geobza w ktorej obliczamy kat obrotu figury
    with arcpy.da.SearchCursor(point, ['SHAPE@X', 'SHAPE@Y', 'OID@']) as cur:
        for row in cur:
            dictPointID[(round(row[0], 3), round(row[1], 3))] = row[2]
    del cur
    return dictPointID

def flipNetwork(workspace, point, siec):
    """
    Funkcja mająca na celu
    1) obrócenie ostatniego, wylotowego kolektora w kierunkuw ujscia z sieci
    2) budowanie kolekcji kolektorów o poprawnym kierunku
    3) obracanie kolektorów w sieci w kierunku ostatniego wylotu z sieci
    Informacja o uzgodnieniu obrotu jest zalisywana w atrybucie 'kierunek'.
    Analizowane są tylko te kolektory które nie posiadają wartosci 'UZGODNIONY' w atrybucie 'kierunek'
    """
    arcpy.env.workspace = workspace
    siec_flip = siec + '_flip'

    arcpy.AddField_management(siec, field_name="kierunek", field_type="TEXT", field_length=20)

    print 'Tworzenie geometrii odwrotnej do istniejacej...'
    flipped_line_geom = createFlippedLineGeom(workspace, siec, siec_flip)

    print 'Przygotowywanie warstwy wylotow...'
    wyloty = readEndpoint(workspace, point)


    print "Obracanie kolektorów bezpośrednio dotykających wyloty..."
    with arcpy.da.UpdateCursor(siec, ['SHAPE@', 'OID@', 'kierunek']) as cur:
        for row in cur:
            (xs, ys) = (round(row[0].firstPoint.X, 3), round(row[0].firstPoint.Y, 3))
            if (xs, ys) in wyloty:
                row[0] = flipped_line_geom[row[1]]
                row[2] = 'UZGODNIONY'
                cur.updateRow(row)
    del cur

    siec_count = 0
    kolektory_poprawne = {}

    print 'Budowanie kolekcji kolektorów wylotowych...'
    with arcpy.da.UpdateCursor(siec, ['SHAPE@', 'OID@', 'kierunek']) as cur:
        for row in cur:
            siec_count += 1
            (xs, ys) = (round(row[0].firstPoint.X, 3), round(row[0].firstPoint.Y, 3))
            (xe, ye) = (round(row[0].lastPoint.X, 3), round(row[0].lastPoint.Y, 3))
            if (xe, ye) in wyloty:
                kolektory_poprawne[row[1]] = (row[0], (xs, ys), (xe, ye))
                row[2] = 'UZGODNIONY'
                cur.updateRow(row)
            if row[2] == 'UZGODNIONY' and row[1] not in kolektory_poprawne:
                kolektory_poprawne[row[1]] = (row[0], (xs, ys), (xe, ye))

    del cur

    print 'Uzgadnianie kierunków na całej sieci (ilosc obiektów sieci - {0})...'.format(siec_count)
    przyrost_kontrolny = 1
    while przyrost_kontrolny > 0:
        kol_temp = kolektory_poprawne.copy()
        stan_p = len(kolektory_poprawne)
        with arcpy.da.UpdateCursor(siec, ['SHAPE@', 'OID@', 'kierunek']) as cur:
            for row in cur:
                if row[1] not in kolektory_poprawne:
                    (xe, ye) = (round(row[0].lastPoint.X, 3), round(row[0].lastPoint.Y, 3))
                    (xs, ys) = (round(row[0].firstPoint.X, 3), round(row[0].firstPoint.Y, 3))
                    for item in kol_temp.iteritems():
                        if (xe, ye) == item[1][1]:
                            kolektory_poprawne[row[1]] = (row[0], (xs, ys), (xe, ye))
                            row[2] = 'UZGODNIONY'
                            cur.updateRow(row)
                        elif (xs, ys) == item[1][1]:
                            row[0] = flipped_line_geom[row[1]]
                            kolektory_poprawne[row[1]] = (row[0], (xe, ye), (xs, ys))
                            row[2] = 'UZGODNIONY'
                            cur.updateRow(row)
        del cur
        przyrost_kontrolny = len(kolektory_poprawne) - stan_p

        print 'Poprawnie zorientowanych odcinków sieci - {0} - {1}%'.format(len(kolektory_poprawne), round(float(len(kolektory_poprawne))*100/siec_count, 2))
    return

if __name__ == '__main__':
    """parametry programu"""
    workspace = r"P:\02_Pracownicy\Mariusz\RZESZOW\DO_MODELOWANIA\Flip.gdb"
    wyloty = 'wyloty_sieci_do_modelowania'
    network = 'Przewody_kan_wylotow_modelowanych'
    flipNetwork(workspace, wyloty, network)
