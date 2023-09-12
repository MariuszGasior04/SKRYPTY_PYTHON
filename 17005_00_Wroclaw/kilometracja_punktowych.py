#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do okreslania kilometrazu obiektow wzgledemi ich obiektow nadrzednych w bazie ewidencji wod.
#kilometrowane są wszystkie obiekty punktowe. Do programu nalezy wprowadzic jedynie obiekty tworzące ROUTE wzdlędem ktorego obiekty punktowe beda kilometrowane

import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True
import time
"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

arcpy.env.workspace=ws=ur'P:\Projekty_2017\17005_Baza_Wrocław\3. Etap I\4. Wytworzenie danych Ewidencji Wód\4_4_Produkcja\4_4_2_Baza_styki\jarzynowa2.gdb'                               #geobaza robocza

""" Podaj wszystkie warstwy ktore są uwzgledniane w kilometracji (nadrzedny_rur i syf musza byc zawsze podane bez wzgledu na to czy biora udzial w numerowaniu czy nie) """

# zeby kilometracja nie nadpisywała wczesniejszych iteracji najpierw nalezy kilometrowac wzgledem
## zbieraczy
## rowow
## ciekow
## kanalow
## rurociagow
## wałow

## stawow (ale nie wiem jak)

##'EWM_CiekNaturalny'
##'EWM_Zbieracz_drenarski'
##'EWM_Wal_przeciwpowodziowy'
##'EWM_RowSzczegolowy'
##'EWM_Kanal'

nadrzedny='EWM_Wal_przeciwpowodziowy'                                                              #warstwa liniowa do kilometracji
nadrzedny_rur='EWM_RurGrawPodst'
syf='EWM_Syfon'

start_time = time.time()

"""funkcja tworzaca klase route na podstawie wejsciowej geobazy oraz warstwy liniowej do kilometracji"""
def Route(workspace, in_features,rurociag,syfon):                                                                      #jako argumenty funkcji podajemy sciezke do geobazy oraz warstwe liniową do kilometracji
    arcpy.env.workspace=workspace

    selection_r=rurociag +'_sel'
    arcpy.Select_analysis(rurociag, selection_r)

    if rurociag=='EWM_RurGrawSzczeg':

        arcpy.CalculateField_management(selection_r, 'oznaczenie', '!oznaczenieRowu!', "PYTHON_9.3")
    elif rurociag=='EWM_RurGrawPodst':
        arcpy.CalculateField_management(selection_r, 'oznaczenie', '!oznaczenieCiekuUrzadzenia!', "PYTHON_9.3")
        arcpy.AddField_management(selection_r, 'numerOdcinka', 'LONG')
        arcpy.CalculateField_management(selection_r, 'numerOdcinka', '!nrOdcinka!', "PYTHON_9.3")

    selection_s=syfon +'_sel'
    arcpy.Select_analysis(syfon, selection_s)
    arcpy.AddField_management(selection_s, 'numerOdcinka', 'LONG')
    arcpy.AddField_management(selection_s, 'nrOdcinka', 'LONG')
    arcpy.CalculateField_management(selection_s, 'oznaczenie', '!oznaczenieCiekuUrzadzenia!', "PYTHON_9.3")
    arcpy.CalculateField_management(selection_s, 'numerOdcinka', '!NrOdcinkaCiekuUrzadz!', "PYTHON_9.3")
    arcpy.CalculateField_management(selection_s, 'nrOdcinka', '!NrOdcinkaCiekuUrzadz!', "PYTHON_9.3")

    merge=in_features +'_merge'
    arcpy.Merge_management([in_features,selection_r,selection_s], merge)
    arcpy.Delete_management(selection_r)
    arcpy.Delete_management(selection_s)

    if in_features=='EWM_CiekNaturalny' or in_features=='EWM_Kanal'or in_features=='EWM_BruzdNawStokowe'or in_features=='EWM_Grobla':
##        arcpy.CalculateField_management(merge, 'numerOdcinka', 0, "PYTHON_9.3")
        where_clause = '"numerOdcinka" <> 1 OR "sztucznyLacznik" <> 2'


    elif in_features=='EWM_RowSzczegolowy'or in_features=='EWM_Rurociag_deszczowniany'or in_features=='EWM_Zbieracz_drenarski':
##        arcpy.CalculateField_management(merge, 'nrOdcinka', 0, "PYTHON_9.3")
        where_clause = '"nrOdcinka" <> 1 OR "sztucznyLacznik" <> 2'

    elif in_features=="EWM_Wal_przeciwpowodziowy":
        where_clause = '"nrOdcinka" > 0'

    elif in_features in ['EWM_RurGrawSzczeg','EWM_RurGrawPodst','EWM_Syfon']:
        where_clause = ''

    selection = in_features +'_sel'
    dissolve = in_features +'_diss'

    arcpy.Select_analysis(merge, selection, where_clause)
    arcpy.Dissolve_management(selection,dissolve,['oznaczenie'],multi_part='SINGLE_PART')
    arcpy.FlipLine_edit(dissolve)

    arcpy.AddField_management(dissolve, 'KM_start', 'FLOAT')
    arcpy.AddField_management(dissolve, 'KM_end', 'FLOAT')

    arcpy.CalculateField_management(dissolve, 'KM_start', '0', "PYTHON_9.3")
    arcpy.CalculateField_management(dissolve, 'KM_end', '!SHAPE.length!', "PYTHON_9.3")

    out_routes = in_features +'_route'
    arcpy.CreateRoutes_lr(dissolve, 'oznaczenie', out_routes, "TWO_FIELDS", 'KM_start', 'KM_end')
    out_routes2 = out_routes + '_2'
    arcpy.MultipartToSinglepart_management(out_routes, out_routes2)

    print "Utworzono klase route: "+ out_routes
    arcpy.Delete_management(selection)
    arcpy.Delete_management(dissolve)
    arcpy.Delete_management(merge)
    arcpy.Delete_management(out_routes)

    return out_routes2


"""funkcja tworząca tabele lokalizacji obiektow na obiektach nadrzednych na podstawie wejsciowej geobazy, warstwy punktowej oraz warstwy route"""
def Kilometracja(workspace,in_point, in_route):
    arcpy.env.workspace=workspace
    table=in_point+'_locate'
    arcpy.LocateFeaturesAlongRoutes_lr(in_point, in_route, 'oznaczenie', "1.0 Meters", table, "oznaczenie POINT measure",in_fields='NO_FIELDS')
    return table

route=Route(ws,nadrzedny,nadrzedny_rur,syf)


print 'Rozpoczeto lokalizowanie'

for dirpath, dirnames, filenames in arcpy.da.Walk(ws, datatype="FeatureClass", type="Point"):
        for filename in filenames:
##            if filename not in ['EWM_Hydrant','EWM_PompDeszcz','EWM_UjecieWodyGruntowej','EWM_StudzRurGraw']:
##            if filename in ['EWM_Wylot','EWM_StudzienkaDrenarska']:
            if filename in ['EWM_Przepust_walowy','EWM_Przewal']:
##            if filename in ['EWM_StudzRurGraw']:
##            if filename in ['EWM_Wylot','EWM_Przepust']:
                tabela=Kilometracja(ws,filename,route)
                arcpy.AddField_management(tabela, 'obiektNadrzedny_rob', 'TEXT')
                arcpy.AddField_management(tabela, 'lokalizacja_rob', 'TEXT')

                with arcpy.da.UpdateCursor(tabela,['INPUTOID','oznaczenie','measure','obiektNadrzedny_rob','lokalizacja_rob'])as cur:
                    for row in cur:
                        km=str(round(row[2]/1000,3)).replace('.','+')
                        lista=km.split('+')
                        while len(lista[1])<3:
                            lista[1]=lista[1]+'0'
                        km=lista[0]+'+'+lista[1]
                        row[4]=km
                        row[3]=row[1]
                        cur.updateRow(row)
                del cur

                print filename

                fieldList=['obiektNadrzedny_rob','lokalizacja_rob']
                arcpy.JoinField_management (filename, 'OBJECTID', tabela, 'INPUTOID', fieldList)

                with arcpy.da.UpdateCursor(filename,['OBJECTID','obiektNadrzedny','lokalizacja','obiektNadrzedny_rob','lokalizacja_rob'])as cur:
                    for row in cur:
                        if row[1]=='b/d' and row[3] is not None:
                            row[1]=row[3]
                            row[2]=row[4]
                            cur.updateRow(row)

                del cur

                arcpy.DeleteField_management(filename, fieldList)
                print 'Nadpisano lokalizacje na obiektach'
                arcpy.Delete_management(tabela)
                print 'Usunieto tabele lokalizacji obiektow punktowych -',tabela

arcpy.Delete_management(route)
print 'Usunieto klase route -',route

print "koniec programu",round((time.time() - start_time), 0), "sek "