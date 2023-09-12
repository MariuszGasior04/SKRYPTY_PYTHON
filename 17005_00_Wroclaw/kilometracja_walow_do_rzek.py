#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do okreslania kilometrazu odcinkow obiektow liniowych

import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True
import time

"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

ws=ur'P:\Projekty_2017\17005_Baza_Wrocław\3. Etap I\4. Wytworzenie danych Ewidencji Wód\4_4_Produkcja\4_4_2_Baza_styki\jarzynowa.gdb'                                #geobaza robocza

""" Podaj wal """

wal='EWM_Wal_przeciwpowodziowy'

""" Podaj wszystkie warstwy liniowe ktore są uwzgledniane w tworzeniu ROUTE'a (nadrzedny_rur i syf musza byc zawsze podane bez wzgledu na to czy biora udzial w kilometrazu czy nie) """
##'EWM_Kanal'
##'EWM_RowSzczegolowy'
##'EWM_CiekNaturalny'
ciek= 'EWM_CiekNaturalny'                                                                    #warstwa liniowa do kilometracji
ruraciag='EWM_RurGrawPodst'
syfon='EWM_Syfon'

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

#   TUTEJ!!! REGULUJA SIĘ BUFUR W KTORYM KILOMETRUJEMY WALY NA CIEKACH        ↓↓↓        DIFOLTOWO JEST 500 metruf                                                                   PARAMETR
    arcpy.LocateFeaturesAlongRoutes_lr(in_point, in_route, 'oznaczenie', "1600 Meters", table, "oznaczenie POINT measure",in_fields='NO_FIELDS',route_locations='ALL')
    arcpy.Delete_management(in_route)
    return table

route=Route(ws,ciek,ruraciag,syfon)

lista=[]
with arcpy.da.SearchCursor(wal,['oznaczenieCiekuKanaluObwal'])as cur:
    for row in cur:
        lista.append(row[0])
del cur

with arcpy.da.UpdateCursor(route,['oznaczenie'])as cur:
        for row in cur:
            if row[0] not in lista:
                cur.deleteRow()
del cur

wal_pkt = wal+"_pkt"
arcpy.FeatureVerticesToPoints_management(wal, wal_pkt, "BOTH_ENDS")

tabela=Kilometracja(ws,wal_pkt,route)                                         #wywołanie funkcji


kolumny =['OBJECTID','odcinekCiekuKanaluObwal','oznaczenieCiekuKanaluObwal']

with arcpy.da.UpdateCursor(wal_pkt,kolumny)as cur:
        for row in cur:

            with arcpy.da.SearchCursor(tabela,['INPUTOID','oznaczenie','measure'])as cur2:
                for row2 in cur2:
                    if row[0]==row2[0] and row[2]==row2[1]:
                        km=str(round(row2[2]/1000,3)).replace('.','+')
                        lista_od=km.split('+')
                        while len(lista_od[1])<3:
                            lista_od[1]=lista_od[1]+'0'
                        km=lista_od[0]+'+'+lista_od[1]
                        row[1]=km

                        cur.updateRow(row)


            del cur2
del cur

print "Przypisano kilometr rzeki do START i END pointow walu"

with arcpy.da.UpdateCursor(wal,['SHAPE@','odcinekCiekuKanaluObwal','oznaczenieCiekuKanaluObwal'])as cur:
    for row in cur:
        od='b/d'
        do='b/d'
        if row[1]=='b/d' or row[1] =='-9999' or row[1] is None:
            with arcpy.da.SearchCursor(wal_pkt,['SHAPE@XY','odcinekCiekuKanaluObwal','oznaczenieCiekuKanaluObwal'])as cur2:
                for row2 in cur2:
                    if (row[0].lastPoint.X,row[0].lastPoint.Y)==row2[0] and row[2]==row2[2]:
                        od = row2[1]
                    elif (row[0].firstPoint.X,row[0].firstPoint.Y)==row2[0]and row[2]==row2[2]:
                        do = row2[1]

            if od != 'b/d' and do != 'b/d':
                row[1]= od +" - "+ do

                cur.updateRow(row)

            del cur2
del cur

print "Przypisano kilometr rzeki do walu"

arcpy.Delete_management(tabela)
arcpy.Delete_management(wal_pkt)
arcpy.Delete_management(route)

print "koniec programu", wal, round((time.time() - start_time), 0), "sek "