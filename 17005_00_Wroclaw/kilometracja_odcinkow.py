#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do okreslania kilometrazu odcinkow obiektow liniowych

import arcpy
from arcpy import env
import time
arcpy.env.overwriteOutput = True

"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

ws = ur'D:\DaneTymczasowe\Baza_ewidencji_wod.gdb'                            #geobaza robocza

""" Podaj warstwe liniową do kilometrowania """

kilometrowany='EWM_RowSzczegolowy'
##'EWM_CiekNaturalny'
##'EWM_Zbieracz_drenarski'
##'EWM_Wal_przeciwpowodziowy'
##'EWM_RowSzczegolowy'
##'EWM_Kanal'
##'EWM_Grobla'
""" Podaj wszystkie warstwy liniowe ktore są uwzgledniane w tworzeniu ROUTE'a (nadrzedny_rur i syf musza byc zawsze podane bez wzgledu na to czy biora udzial w kilometrazu czy nie) """

ob_liniowy='EWM_RowSzczegolowy'                                                  #warstwa liniowa do kilometracji
nadrzedny_rur='EWM_RurGrawSzczeg'
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
    arcpy.AddField_management(selection_s, 'nrOdcinka', 'LONG')
    arcpy.CalculateField_management(selection_s, 'numerOdcinka', '2', "PYTHON_9.3")
    arcpy.CalculateField_management(selection_s, 'nrOdcinka', '2', "PYTHON_9.3")
    arcpy.CalculateField_management(selection_s, 'oznaczenie', '!oznaczenieCiekuUrzadzenia!', "PYTHON_9.3")

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

"""funkcja tworzaca klase route na podstawie wejsciowej geobazy oraz warstwy liniowej do kilometracji dla rurociągow"""
def Route_rur(workspace, in_features):                                                                      #jako argumenty funkcji podajemy sciezke do geobazy oraz warstwe liniową do kilometracji
    arcpy.env.workspace=workspace

    dissolve = in_features +'_diss_rur'

    arcpy.Dissolve_management(in_features,dissolve,['oznaczenie'],multi_part='SINGLE_PART')
    arcpy.FlipLine_edit(dissolve)

    arcpy.AddField_management(dissolve, 'KM_start', 'FLOAT')
    arcpy.AddField_management(dissolve, 'KM_end', 'FLOAT')

    arcpy.CalculateField_management(dissolve, 'KM_start', '0', "PYTHON_9.3")
    arcpy.CalculateField_management(dissolve, 'KM_end', '!SHAPE.length!', "PYTHON_9.3")

    out_routes = in_features +'_route_rur'
    arcpy.CreateRoutes_lr(dissolve, 'oznaczenie', out_routes, "TWO_FIELDS", 'KM_start', 'KM_end')
    print "Utworzono klase route rurociagu: "+ out_routes
    arcpy.Delete_management(dissolve)

    return out_routes

"""funkcja tworząca tabele lokalizacji obiektow na obiektach nadrzednych na podstawie wejsciowej geobazy, warstwy punktowej oraz warstwy route"""
def Kilometracja(workspace,in_line, in_route):
    arcpy.env.workspace=workspace
    table=in_line+'_locate'
    arcpy.LocateFeaturesAlongRoutes_lr(in_line, in_route, 'oznaczenie', "0 Meters", table, "oznaczenie LINE OD DO",in_fields='NO_FIELDS')
    arcpy.Delete_management(in_route)
    print 'Usunieto klase route oraz utworzono tabele kilometracji odcinkow obiektow liniowych'
    return table

print "1"
tabela=Kilometracja(ws,kilometrowany,Route(ws,ob_liniowy,nadrzedny_rur,syf))                                         #wywołanie funkcji

if kilometrowany in ['EWM_CiekNaturalny','EWM_Kanal','EWM_BruzdNawStokowe','EWM_Grobla','EWM_RowSzczegolowy','EWM_Rurociag_deszczowniany','EWM_Wal_przeciwpowodziowy','EWM_Zbieracz_drenarski']:
    kolumny =['OBJECTID','kilometrPoczatkowy','kilometrKoncowy','dlugosc']
elif kilometrowany=='EWM_Akwedukt':
    kolumny =['OBJECTID','kilometrPoczOdcinkaCiekuUrzadzenia','kilometrKoncOdcinkaCiekuUrzadzenia','dlugosc']
elif kilometrowany=='EWM_RurGrawPodst':
    kolumny =['OBJECTID','kilometrPoczatkowyCieku','kilometrKoncowyCieku','dlugosc']
elif kilometrowany=='EWM_RurGrawSzczeg':
    kolumny =['OBJECTID','kilometrPoczatkowyRowu','kilometrKoncowyRowu','dlugosc']
elif kilometrowany=='EWM_Syfon':
    kolumny =['OBJECTID','kilometrPoczatkowyCiekuUrzadzenia','kilometrKoncowyCiekuUrzadzenia','dlugoscSyfonu']

with arcpy.da.UpdateCursor(kilometrowany,kolumny)as cur:
        for row in cur:
            if row[1]=='b/d'or row[1]=='0' or row[1]=='-9999':
                with arcpy.da.SearchCursor(tabela,['INPUTOID','oznaczenie','OD','DO'])as cur2:
                    for row2 in cur2:
                        if row[0]==row2[0]:
                            km_od=str(round(row2[2]/1000,3)).replace('.','+')
                            lista_od=km_od.split('+')
                            while len(lista_od[1])<3:
                                lista_od[1]=lista_od[1]+'0'
                            km_od=lista_od[0]+'+'+lista_od[1]
                            row[1]=km_od

                            km_do=str(round(row2[3]/1000,3)).replace('.','+')
                            lista_do=km_do.split('+')
                            while len(lista_do[1])<3:
                                lista_do[1]=lista_do[1]+'0'
                            km_do=lista_do[0]+'+'+lista_do[1]
                            row[2]=km_do

                            row[3]=row2[3]-row2[2]
                            cur.updateRow(row)


                del cur2
del cur

if kilometrowany in ['EWM_Akwedukt','EWM_RurGrawPodst','EWM_RurGrawSzczeg','EWM_Syfon']:
    tabela_rur=Kilometracja(ws,kilometrowany,Route_rur(ws,kilometrowany))

    if kilometrowany=='EWM_Akwedukt':
        kolumny =['OBJECTID','kilometrPoczAkweduktu','kilometrKoncAkweduktu','dlugosc']
    elif kilometrowany=='EWM_RurGrawPodst':
        kolumny =['OBJECTID','kilometrPoczatkowy','kilometrKoncowy','dlugosc']
    elif kilometrowany=='EWM_RurGrawSzczeg':
        kolumny =['OBJECTID','kilometrPoczatkowyRurociagu','kilometrKoncowyRurociagu','dlugosc']
    elif kilometrowany=='EWM_Syfon':
        kolumny =['OBJECTID','kilometrPoczatkowySyfonu','kilometrKoncowySyfonu','dlugoscSyfonu']
    with arcpy.da.UpdateCursor(kilometrowany,kolumny)as cur:
        for row in cur:

            with arcpy.da.SearchCursor(tabela_rur,['INPUTOID','oznaczenie','OD','DO'])as cur2:
                for row2 in cur2:
                    if row[0]==row2[0]:
                        km_od=str(round(row2[2]/1000,3)).replace('.','+')
                        lista_od=km_od.split('+')
                        while len(lista_od[1])<3:
                            lista_od[1]=lista_od[1]+'0'
                        km_od=lista_od[0]+'+'+lista_od[1]
                        row[1]=km_od

                        km_do=str(round(row2[3]/1000,3)).replace('.','+')
                        lista_do=km_do.split('+')
                        while len(lista_do[1])<3:
                            lista_do[1]=lista_do[1]+'0'
                        km_do=lista_do[0]+'+'+lista_do[1]
                        row[2]=km_do

                        row[3]=row2[3]-row2[2]
                        cur.updateRow(row)


            del cur2
    del cur
    arcpy.Delete_management(tabela_rur)

print 'Nadpisano kilometraz odcinkow'

arcpy.Delete_management(tabela)

print "koniec programu",round((time.time() - start_time), 0), "sek ", kilometrowany