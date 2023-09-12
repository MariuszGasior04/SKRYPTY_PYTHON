#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do okreslania kilometrazu obiektow liniowych wzgledemi ich obiektow nadrzednych
""" Żeby przypisało recypienta w kolumnach ObiektNadrzedny oraz lokalizacja musza byc wypelnione wartosciami <Null>"""
import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True
import time

"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

ws=ur'D:\DaneTymczasowe\Baza_ewidencji_wod.gdb'                              #geobaza robocza

""" Podaj wszystkie warstwy ktore są uwzgledniane w kilometracji (podrzedny_rur i podrzedny_syf musza byc zawsze podane bez wzgledu na to czy biora udzial w kilometrazu czy nie) """

podrzedny='EWM_RowSzczegolowy'                                                                  #warstwa liniowa do kilometracji
podrzedny_rur='EWM_RurGrawSzczeg'
podrzedny_syf='EWM_Syfon'

##'EWM_CiekNaturalny'
##'EWM_Kanal'
##'EWM_RurGrawPodst'
##'EWM_RurGrawSzczeg'
##'EWM_Syfon'
##'EWM_RowSzczegolowy'
##'EWM_Zbieracz_drenarski'

""" Podaj wszystkie warstwy liniowe ktore są uwzgledniane w tworzeniu ROUTE'a recypienta (nadrzedny_rur i nadrzedny_syf musza byc zawsze podane bez wzgledu na to czy biora udzial w kilometrazu czy nie) """

nadrzedny= 'EWM_CiekNaturalny'                                                               #warstwa liniowa recypienta
nadrzedny_rur='EWM_RurGrawPodst'
nadrzedny_syf='EWM_Syfon'
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
    arcpy.CalculateField_management(selection_s, 'oznaczenie', '!oznaczenieCiekuUrzadzenia!', "PYTHON_9.3")

    merge=in_features +'_merge'
    arcpy.Merge_management([in_features,selection_r,selection_s], merge)
    arcpy.Delete_management(selection_r)
    arcpy.Delete_management(selection_s)

    if in_features=='EWM_CiekNaturalny' or in_features=='EWM_Kanal'or in_features=='EWM_BruzdNawStokowe'or in_features=='EWM_Grobla':
##        arcpy.CalculateField_management(merge, 'numerOdcinka', 0, "PYTHON_9.3")
        where_clause = '"numerOdcinka" <> 1 OR "sztucznyLacznik" <> 2'


    elif in_features=='EWM_RowSzczegolowy'or in_features=='EWM_Rurociag_deszczowniany'or in_features=="EWM_Wal_przeciwpowodziowy" or in_features=='EWM_Zbieracz_drenarski':
##        arcpy.CalculateField_management(merge, 'nrOdcinka', 0, "PYTHON_9.3")
        where_clause = '"nrOdcinka" <> 1 OR "sztucznyLacznik" <> 2'

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

def Route_pod(workspace, in_features,rurociag,syfon):                                                                      #jako argumenty funkcji podajemy sciezke do geobazy oraz warstwe liniową do kilometracji
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
    arcpy.CalculateField_management(selection_s, 'oznaczenie', '!oznaczenieCiekuUrzadzenia!', "PYTHON_9.3")

    merge=in_features +'_merge'
    arcpy.Merge_management([in_features,selection_r,selection_s], merge)
    arcpy.Delete_management(selection_r)
    arcpy.Delete_management(selection_s)

    if in_features=='EWM_CiekNaturalny' or in_features=='EWM_Kanal'or in_features=='EWM_BruzdNawStokowe'or in_features=='EWM_Grobla':
##        arcpy.CalculateField_management(merge, 'numerOdcinka', 0, "PYTHON_9.3")
        where_clause = '"numerOdcinka" > 0'


    elif in_features=='EWM_RowSzczegolowy'or in_features=='EWM_Rurociag_deszczowniany'or in_features=="EWM_Wal_przeciwpowodziowy" or in_features=='EWM_Zbieracz_drenarski':
##        arcpy.CalculateField_management(merge, 'nrOdcinka', 0, "PYTHON_9.3")
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

"""funkcja tworzaca klase punktowa end_point na podstawie wejsciowej geobazy oraz warstwy liniowej do kilometracji"""
def Ujscie(workspace, in_features,rurociag,syfon):                                                                      #jako argumenty funkcji podajemy sciezke do geobazy oraz warstwe liniową do kilometracji
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
    arcpy.CalculateField_management(selection_s, 'oznaczenie', '!oznaczenieCiekuUrzadzenia!', "PYTHON_9.3")

    merge=in_features +'_merge'
    arcpy.Merge_management([in_features,selection_r,selection_s], merge)
    arcpy.Delete_management(selection_r)
    arcpy.Delete_management(selection_s)

    if in_features=='EWM_CiekNaturalny' or in_features=='EWM_Kanal'or in_features=='EWM_BruzdNawStokowe'or in_features=='EWM_Grobla':
##        arcpy.CalculateField_management(merge, 'numerOdcinka', 0, "PYTHON_9.3")
        where_clause = '"numerOdcinka" > 0'


    elif in_features=='EWM_RowSzczegolowy'or in_features=='EWM_Rurociag_deszczowniany'or in_features=="EWM_Wal_przeciwpowodziowy" or in_features=='EWM_Zbieracz_drenarski':
##        arcpy.CalculateField_management(merge, 'nrOdcinka', 0, "PYTHON_9.3")
        where_clause = '"nrOdcinka" > 0'

    elif in_features in ['EWM_RurGrawSzczeg','EWM_RurGrawPodst','EWM_Syfon']:
        where_clause = ''

    selection = in_features +'_sel'
    dissolve = in_features +'_diss_ednpoint'
    end_point = in_features +'_end_point'

    arcpy.Select_analysis(merge, selection, where_clause)
    arcpy.Dissolve_management(selection,dissolve,['oznaczenie'],multi_part='SINGLE_PART')
    arcpy.FeatureVerticesToPoints_management(dissolve, end_point, "END")
    arcpy.AddField_management(end_point, 'ozn_rec', 'TEXT')
    arcpy.AddField_management(end_point, 'measure', 'FLOAT')
    print "Utworzona warstwe END POINT: "+ end_point
    arcpy.Delete_management(selection)
    arcpy.Delete_management(merge)
    arcpy.Delete_management(dissolve)
    return end_point

"""funkcja tworząca tabele lokalizacji obiektow na obiektach nadrzednych (INPUTOID i oznaczenie recypienta) na podstawie wejsciowej geobazy, warstwy punktowej oraz warstwy route"""
def Kilometracja(workspace,in_point, in_route):
    arcpy.env.workspace=workspace
    table=in_point+'_locate'
    arcpy.LocateFeaturesAlongRoutes_lr(in_point, in_route, 'oznaczenie', "0.5 Meters", table, "oznaczenie POINT measure",route_locations='ALL',zero_length_events='NO_ZERO',in_fields='NO_FIELDS')
    arcpy.Delete_management(in_route)
    print 'Usunieto klase route i utworzono tabele lokalizacji obiektow liniowych na recypientach'
    return table

print "1"

route=Route(ws,nadrzedny,nadrzedny_rur,nadrzedny_syf)
end_point=Ujscie(ws,podrzedny,podrzedny_rur,podrzedny_syf)

tabela=Kilometracja(ws,end_point,route)

print "2"

with arcpy.da.UpdateCursor(tabela,['measure'])as cur:
    for row in cur:
        if row[0]==0:
            cur.deleteRow()
del cur

with arcpy.da.UpdateCursor(end_point,['OBJECTID','oznaczenie','ozn_rec','measure'])as cur:
        for row in cur:

            with arcpy.da.SearchCursor(tabela,['INPUTOID','oznaczenie','measure'])as cur2:
                for row2 in cur2:
                    if row[0]==row2[0] and row2[2] is not None and row[2]!=row2[1]:

                        row[2]=row2[1]
                        row[3]=row2[2]
                    cur.updateRow(row)
            del cur2
del cur

arcpy.Delete_management(tabela)
print 'Usunieto tabele lokalizacji obiektow punktowych na obiekcie nadrzednym'
print 'Przypisano recypienta i kilometr ujsciowy do END POINT'

print "3"

route_pod=Route_pod(ws,podrzedny,podrzedny_rur,podrzedny_syf)
arcpy.AddField_management(route_pod, 'obiektNadrzedny_rob', 'TEXT')
arcpy.AddField_management(route_pod, 'lokalizacja_rob', 'TEXT')
route_pod2 = route_pod +'_2'

arcpy.MultipartToSinglepart_management(route_pod,route_pod2)
arcpy.Delete_management(route_pod)

list_end=[]
with arcpy.da.UpdateCursor(end_point,['SHAPE@XY','oznaczenie','ozn_rec','measure'])as cur:
    for row in cur:
        if row[2] is None:
            cur.deleteRow()
        else:
            km=str(round(row[3]/1000,3)).replace('.','+')
            lista=km.split('+')
            while len(lista[1])<3:
                lista[1]=lista[1]+'0'
            km=lista[0]+'+'+lista[1]
            list_end.append((row[0][0],row[0][1],row[1],row[2],km))
del cur

print "Przypisywanie recypienta do tymczasowego routa"
with arcpy.da.UpdateCursor(route_pod2,['SHAPE@','oznaczenie','obiektNadrzedny_rob','lokalizacja_rob'])as cur:
    for row in cur:
        for end_pkt in list_end:
            if row[0].firstPoint.X==end_pkt[0] and row[0].firstPoint.Y==end_pkt[1] and row[1]==end_pkt[2]:
                row[2]=end_pkt[3]
                row[3]=end_pkt[4]

                cur.updateRow(row)
del cur


with arcpy.da.UpdateCursor(route_pod2,['obiektNadrzedny_rob'])as cur:
    for row in cur:
        if row[0] is None:
            cur.deleteRow()
del cur

print "4"
out_spatialjoin=podrzedny+'_spatial'
arcpy.SpatialJoin_analysis(podrzedny, route_pod2, out_spatialjoin, match_option='SHARE_A_LINE_SEGMENT_WITH')
fieldList=['obiektNadrzedny_rob','lokalizacja_rob']

arcpy.JoinField_management (podrzedny, 'OBJECTID', out_spatialjoin, 'TARGET_FID', fieldList)

with arcpy.da.UpdateCursor(podrzedny,['obiektNadrzedny','lokalizacja','obiektNadrzedny_rob','lokalizacja_rob'])as cur:
    for row in cur:
        if row[2] is not None and row[0]=='b/d' or row[0]=='-9999':
            row[0]=row[2]
            row[1]=row[3]
            cur.updateRow(row)
del cur

print 'Przypisano recypienta i kilometr ujsciowy do liniowych obiektow podrzednych'

arcpy.Delete_management(end_point)
arcpy.Delete_management(route_pod2)
arcpy.Delete_management(out_spatialjoin)
arcpy.DeleteField_management(podrzedny, fieldList)

print "koniec programu -",podrzedny,round((time.time() - start_time), 0), "sek "

