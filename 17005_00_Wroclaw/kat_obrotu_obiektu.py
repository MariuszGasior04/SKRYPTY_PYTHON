#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do okreslania kątu obrotu obiektu na podstawie podanego metrowego odcinka cieku na ktorym znajduje sie

import arcpy
import math
from arcpy import env
arcpy.env.overwriteOutput = True

'''parametry programu'''
ws=ur"P:\Projekty_2017\17005_Baza_Wrocław\3. Etap I\4. Wytworzenie danych Ewidencji Wód\4_4_Produkcja\4_4_2_Baza_styki\Baza_ewidencji_wod_CZ3.gdb"                               #geobaza robocza

#warstwa liniowa do kilometracji

'''funkcja obliczajaca kat obrotu symboli wzgledem ich obiektow nadrzednych, na podstawie wejsciowej geobazy, warstwy punktowej oraz warstwy liniowej'''
def KatObr(workspace,in_point,in_liniowy):
    arcpy.env.workspace=workspace           #geobza w ktorej obliczamy kat obrotu figury
    arcpy.Buffer_analysis(in_point,"in_memory/buf",1)
    inFeatures = ["in_memory/buf",in_liniowy]
    arcpy.Intersect_analysis(inFeatures, "in_memory/int", output_type = "LINE")
    i=0

    with arcpy.da.SearchCursor("in_memory/int",['SHAPE@','ORIG_FID','katObr'])as cur:
        for row in cur:
            if row[2] is None:
                Xs=row[0].firstPoint.X
                Xe=row[0].lastPoint.X
                Ys=row[0].firstPoint.Y
                Ye=row[0].lastPoint.Y
                dX=Xe-Xs
                dY=Ye-Ys
                i+=1

                if dY==0:
                    dY=0.000001
                if dX==0:
                    dX=0.000001

                az = math.degrees(math.atan2(dX,dY))

                with arcpy.da.UpdateCursor(in_point,['OBJECTID','katObr'])as cur2:
                    for row2 in cur2:
                        if row2[0]==row[1] and row2[1] is None:
                            if in_point=='EWM_Brod'or in_point=='EWM_Stopien':
                                row2[1]= az+270
                            elif in_point=='EWM_Wylot'and (in_liniowy=='EWM_CiekNaturalny' or in_liniowy== 'EWM_RowSzczegolowy'):
                                row2[1]= az+90
                            elif in_liniowy=='EWM_Zbieracz_drenarski' and in_point=='EWM_Wylot':
                                row2[1]= az+180
                            elif in_liniowy=='EWM_Wal_przeciwpowodziowy' and in_point=='EWM_Przepust_walowy':
                                row2[1]= az+180
                            elif in_point=='EWM_Jaz'or in_point=='EWM_Brod'or in_point=='EWM_Zastawka'or in_point=='EWM_Stopien'or in_point=='EWM_Most'or in_point=='EWM_Prog'or in_point=='EWM_Bystrotok':
                                row2[1]= az+90
                            else:
                                row2[1]= az

                            cur2.updateRow(row2)
                            print in_point+' nadpisano kat: OBJECTID ',row2[0]

                del cur2
    del cur
    return

list_pod=['EWM_Przepust','EWM_Wylot','EWM_Jaz','EWM_Zastawka','EWM_Stopien', 'EWM_Kladka','EWM_Prog','EWM_Przepust_walowy', 'EWM_Most','EWM_PrzepustZPietrzeniem','EWM_Bystrotok','EWM_Mnich','EWM_Brod']
##list_pod=['EWM_Przepust','EWM_Jaz','EWM_Zastawka','EWM_Stopien', 'EWM_Kladka','EWM_Prog','EWM_Przepust_walowy', 'EWM_Most','EWM_PrzepustZPietrzeniem','EWM_Bystrotok','EWM_Mnich','EWM_Brod']
list_nad=['EWM_Wal_przeciwpowodziowy','EWM_RurGrawSzczeg','EWM_RowSzczegolowy','EWM_CiekNaturalny','EWM_Kanal','EWM_Zbieracz_drenarski','EWM_RurGrawPodst']

for podrzedny in list_pod:
    for nadrzedny in list_nad:
        KatObr(ws,podrzedny,nadrzedny)

print 'koniec programu'
