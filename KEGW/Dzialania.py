#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("3D")


def przypiszZlewnie(rob, kol_rob, dzialania_polig, kol_dzial):
    '''
    Funkcja do przypisania wielu rekordów do jednego (wypisując po przecinku) w przypadku relacji dwóch warstw jeden do wielu.

    '''
    lista_robot_dzialki = []
    with arcpy.da.SearchCursor(rob, kol_rob) as cur2:
        for row2 in cur2:
            lista_robot_dzialki.append([row2[0], row2[1]])
    del cur2

    with arcpy.da.UpdateCursor(dzialania_polig, kol_dzial) as update:
        for row in update:
            print(row[0])
            row[1] = ''
            for item in lista_robot_dzialki:
                if row[0] == item[0]:
                    if row[1] == '':
                        # row[1] = unicode(item[1])
                        row[1] = item[1]
                    else:
                        row[1] = str(row[1]) + '\n' + str(item[1])
                        # row[1] = unicode(row[1]) + ', ' + unicode(item[1])

            print(row[1])
            print(len(row[1]))
            update.updateRow(row)

    del update

    return

if __name__ == '__main__':
    """parametry programu"""
    # geobaza robocza
    workspace = arcpy.env.workspace = \
        r"P:\02_Pracownicy\Mariusz\KEGW\DDP_nowe.gdb"
    # warstwa robocza po wykonaniu Spatial Join w relacji One to Many
    # dzialania_liniowe_Sort , dzialania_poligonowe_Sort , dzialania_punktowe_Sort
    rob = 'dzialania_liniowe_Sort'

    # kolumny warstwy roboczej przechowywujące ID obiektu, któremu przypisujemy wartość oraz kolumnę z której wartosci chcemy zgrupować (po przecinku)
    kol_rob = ['PageNumber', 'ETYK']

    # warstwa ostateczna z dodaną kolumną w której będą wpisywane rekordy
    dzialania_polig = 'arkusze_A2_3000_DDP'

    # kolumny warstwy ostatecznej przechowywujące ID (do identyfikacji) oraz kolumna do której wprowadzamy zgrupowane wartosci
    # ETYK_POLIG , ETYK_PKT , ETYK_LINE
    kol_dzial = ['PageNumber', 'ETYK_LINE']

    przypiszZlewnie(rob, kol_rob, dzialania_polig, kol_dzial)
