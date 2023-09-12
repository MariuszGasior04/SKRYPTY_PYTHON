# !/usr/bin/env python
# -*- coding: utf-8 -*-

# skrypt do numeracji odcinkow liniowych w bazie melioracji
""" NUMERUJE TYLKO 0 """

import arcpy
import time

arcpy.env.overwriteOutput = True

"""PARAMETRY PROGRAMU"""

""" Podaj geobaze robocza """

ws = ur'D:\DaneTymczasowe\Baza_ewidencji_wod.gdb'

""" Podaj warstwe liniową do zanumerowania """

numerowany='EWM_RowSzczegolowy'
##'EWM_RowSzczegolowy'
##'EWM_Zbieracz_drenarski'
##'EWM_Wal_przeciwpowodziowy'
##'EWM_RowSzczegolowy'
##'EWM_Kanal'
""" Podaj wszystkie warstwy liniowe ktore są uwzgledniane w numerowaniu (rur i syf musza byc zawsze podane bez wzgledu na to czy biora udzial w numerowaniu czy nie) """

liniowy='EWM_RowSzczegolowy'
rur='EWM_RurGrawSzczeg'
syf='EWM_Syfon'

max_time = 3600
start_time = time.time()

def Numerate(workspace, in_features,rurociag,syfon):                                                                      #jako argumenty funkcji podajemy sciezke do geobazy oraz warstwe liniową do kilometracji
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
        arcpy.CalculateField_management(merge, 'numerOdcinka', 0, "PYTHON_9.3")
        where_clause = '"numerOdcinka" IS NOT null'
        kolumny =['oznaczenie', 'SHAPE@','numerOdcinka']

    elif in_features=='EWM_RowSzczegolowy'or in_features=='EWM_Rurociag_deszczowniany'or in_features=="EWM_Wal_przeciwpowodziowy" or in_features=='EWM_Zbieracz_drenarski':
        arcpy.CalculateField_management(merge, 'nrOdcinka', 0, "PYTHON_9.3")
        where_clause = '"nrOdcinka" IS NOT null'
        kolumny =['oznaczenie', 'SHAPE@','nrOdcinka']

    selection = in_features +'_sel'
    dissolve = in_features +'_diss'

    arcpy.Select_analysis(merge, selection, where_clause)

### Nadanie numeru 1 ujsciowemu odcinkowi w warstwie tymczasowej
    lista=[]
    nr=[]
    iteracja=[]
    with arcpy.da.SearchCursor(selection, kolumny) as search:
        for row in search:
            lista.append((row[0],(row[1].firstPoint.X,row[1].firstPoint.Y)))
            nr.append((row[0],(row[1].firstPoint.X,row[1].firstPoint.Y),row[2]))
            iteracja.append(row[2])
    del search

    with arcpy.da.UpdateCursor(selection, kolumny)as update:
        for row in update:
            war=(row[0],(row[1].lastPoint.X,row[1].lastPoint.Y))

            if war not in lista:
                row[2]=1
                update.updateRow(row)

    del update

### nadawanie kolejnych numerow odcinkom w warstwie tymczasowej
    while 0 in iteracja and (time.time() - start_time) < max_time:
        with arcpy.da.SearchCursor(selection, kolumny) as search:
            for row in search:
                nr.append((row[0],(row[1].firstPoint.X,row[1].firstPoint.Y),row[2]))
        del search

        iteracja=[]
        with arcpy.da.UpdateCursor(selection, kolumny)as update:
            for row in update:
                if row[2]==0:
                    war=(row[0],(row[1].lastPoint.X,row[1].lastPoint.Y),row[2])
                    for obiekt in nr:
                        if war[0]==obiekt[0] and war[1]==obiekt[1] and obiekt[2]<>0:
                            row[2]=obiekt[2]+1
                            update.updateRow(row)
                iteracja.append(row[2])
        del update

    arcpy.Delete_management(merge)
    print "Route ",in_features
    return selection

def Numerate_rur(workspace, in_features):                                                                      #jako argumenty funkcji podajemy sciezke do geobazy oraz warstwe liniową do kilometracji
    arcpy.env.workspace=workspace

    if in_features=='EWM_Syfon':
        arcpy.CalculateField_management(in_features, 'numerOdcinka', 0, "PYTHON_9.3")
        where_clause = '"numerOdcinka" IS NOT null'
        kolumny =['oznaczenie', 'SHAPE@','numerOdcinka']

    elif in_features=='EWM_RurGrawSzczeg'or in_features=='EWM_RurGrawPodst':
        arcpy.CalculateField_management(in_features, 'nrOdcinka', 0, "PYTHON_9.3")
        where_clause = '"nrOdcinka" IS NOT null'
        kolumny =['oznaczenie', 'SHAPE@','nrOdcinka']

### Nadanie numeru 1 ujsciowemu odcinkowi w warstwie
    lista=[]
    nr=[]
    iteracja=[]
    with arcpy.da.SearchCursor(in_features, kolumny) as search:
        for row in search:
            lista.append((row[0],(row[1].firstPoint.X,row[1].firstPoint.Y)))
            nr.append((row[0],(row[1].firstPoint.X,row[1].firstPoint.Y),row[2]))
            iteracja.append(row[2])
    del search

    with arcpy.da.UpdateCursor(in_features, kolumny)as update:
        for row in update:
            war=(row[0],(row[1].lastPoint.X,row[1].lastPoint.Y))

            if war not in lista:
                row[2]=1
                update.updateRow(row)

    del update

### nadawanie kolejnych numerow odcinkom w warstwie
    while 0 in iteracja and (time.time() - start_time) < max_time:
        with arcpy.da.SearchCursor(in_features, kolumny) as search:
            for row in search:
                nr.append((row[0],(row[1].firstPoint.X,row[1].firstPoint.Y),row[2]))
        del search

        iteracja=[]
        with arcpy.da.UpdateCursor(in_features, kolumny)as update:
            for row in update:
                if row[2]==0:
                    war=(row[0],(row[1].lastPoint.X,row[1].lastPoint.Y),row[2])
                    for obiekt in nr:
                        if war[0]==obiekt[0] and war[1]==obiekt[1] and obiekt[2]<>0:
                            row[2]=obiekt[2]+1
                            update.updateRow(row)
                iteracja.append(row[2])
        del update
    print "Zanumerowalo ",in_features
    return

if liniowy=='EWM_CiekNaturalny' or liniowy=='EWM_Kanal'or liniowy=='EWM_BruzdNawStokowe'or liniowy=='EWM_Grobla':
    kolumny =['oznaczenie', 'SHAPE@','numerOdcinka']
elif liniowy=='EWM_RowSzczegolowy'or liniowy=='EWM_Rurociag_deszczowniany'or liniowy=="EWM_Wal_przeciwpowodziowy" or liniowy=='EWM_Zbieracz_drenarski':
    kolumny =['oznaczenie', 'SHAPE@','nrOdcinka']

nr=[]
temp=Numerate(ws,liniowy,rur,syf)

with arcpy.da.SearchCursor(temp, kolumny) as search:
    for row in search:
        nr.append((row[0],(row[1].centroid.X,row[1].centroid.Y),row[2]))
del search

if numerowany=='EWM_CiekNaturalny' or numerowany=='EWM_Kanal'or numerowany=='EWM_BruzdNawStokowe'or numerowany=='EWM_Grobla':
    kolumny_numerowanego =['oznaczenie', 'SHAPE@','numerOdcinka']
elif numerowany=='EWM_RowSzczegolowy'or numerowany=='EWM_Rurociag_deszczowniany'or numerowany=="EWM_Wal_przeciwpowodziowy" or numerowany=='EWM_Zbieracz_drenarski':
    kolumny_numerowanego =['oznaczenie', 'SHAPE@','nrOdcinka']
elif numerowany=='EWM_RurGrawSzczeg':
    kolumny_numerowanego =['oznaczenie', 'SHAPE@','nrOdcinkaRowu']
elif numerowany=='EWM_Syfon':
    kolumny_numerowanego =['oznaczenie', 'SHAPE@','NrOdcinkaCiekuUrzadz']
elif numerowany=='EWM_RurGrawPodst':
    kolumny_numerowanego =['oznaczenie', 'SHAPE@','NrOdcinkaCieku']


with arcpy.da.UpdateCursor(numerowany, kolumny_numerowanego)as update:
    for row in update:
        war=(row[0],(row[1].centroid.X,row[1].centroid.Y),row[2])
        if row[2]==0 or row[2] is None or row[2]==-9999:
            for obiekt in nr:
                if  war[1]==obiekt[1] and obiekt[2]<>0:
                    row[2]=obiekt[2]
                    update.updateRow(row)

del update

arcpy.Delete_management(temp)

if numerowany in ['EWM_Akwedukt','EWM_RurGrawPodst','EWM_RurGrawSzczeg','EWM_Syfon']:
    Numerate_rur(ws, numerowany)


print "koniec programu", round((time.time() - start_time), 0), "sek "

