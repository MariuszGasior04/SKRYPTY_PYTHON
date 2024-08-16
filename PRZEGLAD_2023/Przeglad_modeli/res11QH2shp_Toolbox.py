#!/usr/bin/env python
#-*- coding: utf-8 -*-

# koniecznosc podania nazwy rzeki, tzn ciągu znaków przed cyframi prawdopodobieństawa w nazwie pliku .res11
# nazwa brancha nie moze zaczynac sie od cyfry
# w przypadku zdublowanych punktach na przekrojach z floodplainami, przeplyw na terasie jest wartoscia wyzsza,
# w korycie nizsza atrybut w shp "type" oznacza punkty wyinterpolowane

import os
import arcpy
from subprocess import Popen
import pandas as pd

arcpy.env.overwriteOutput = True

##rzeka="S03_Wisla_"

rzeka = arcpy.GetParameterAsText(0)
res_input = arcpy.GetParameterAsText(1)
res_exe = arcpy.GetParameterAsText(2)

res_list = res_input.split(';')

path = os.path.dirname(res_list[0])
bat_file = os.path.join(path,'res11read.bat')

arcpy.AddMessage(res_list)
arcpy.AddMessage(path)
arcpy.AddMessage(bat_file)

def rename(i, rozszerzenie):
    i = i.replace(rzeka, "")
    if ".res11" in i:
        i = i.replace(".res11", rozszerzenie)
    elif "-max1" in i:
        i = i.replace("-max1", "")
        new_txt = 'Hmax'+ os.path.basename(i)
        dir = os.path.dirname(i)
        i = os.path.join(dir, new_txt)
    elif "-min1" in i:
        i = i.replace("-min1", "")
        new_txt = 'Hmin' + os.path.basename(i)
        dir = os.path.dirname(i)
        i = os.path.join(dir, new_txt)
    elif "-max2" in i:
        i = i.replace("-max2", "")
        new_txt = 'Qmax' + os.path.basename(i)
        dir = os.path.dirname(i)
        i = os.path.join(dir, new_txt)
    elif "-min2" in i:
        i = i.replace("-min2", "")
        new_txt = 'Qmin' + os.path.basename(i)
        dir = os.path.dirname(i)
        i = os.path.join(dir, new_txt)
    return i

def batRun(res_list, zmienna_res):
    txt_output_list = []
    for i in res_list:
        # stworzenie pliku .bat do obslugi res11read
        arcpy.AddMessage(i)
        txt_output = os.path.join(os.path.dirname(i), os.path.basename(i).split('.')[0] + zmienna_res+'.txt')
        arcpy.AddMessage(txt_output)
        txt_output = rename(txt_output, ".txt")
        bat = open(bat_file, 'w')
        # res_exe = r'C:\Program Files (x86)\DHI\2020\bin\x64\res11read.exe'
        bat.writelines('{0} {1} -DHIASCII -silent {2} {3}'.format('"'+res_exe+'"', zmienna_res, '"'+i+'"', '"'+txt_output+'"'))
        bat.close()
        # uruchomienie pliku .bat
        p = Popen(bat_file, shell = True)
        stdout, stderr = p.communicate()
        p.wait()
        txt_output_list.append(txt_output)

    return txt_output_list

def txtPtsRead(txt_pkt, nazwa_coor):
    txt = open(txt_pkt, "r").read()
    rows = txt.split("\n")
    
    os.remove(txt_pkt)  # usuwa plik txt

    csv_coor = "{}\\{}.csv".format(path, nazwa_coor)

    csv = open(csv_coor, "w")
    csv.writelines("x;y;branch;km;typ\n")

    for row in rows[1:-1]:
        i = -1
        for s in row:
            if s.isdigit():
                i += 1
            elif s == " ":
                i += 1
            elif s == ".":
                i += 1
            else:
                break

        coor = (row[:i].split())
        x = coor[0]
        y = coor[1]
        rest = row[i+1:].split()
        branch = rest[0]
        km = rest[1]
        typ = rest[2]
        pkt = "{};{};{};{};{}".format(x, y, branch, km, typ)

        csv.writelines(pkt+"\n")
    csv.close()

def txtMaxRead(res_list, txt_max_list):
    dict = {k: v for k, v in zip(res_list, txt_max_list)}
    for i, j in dict.items():
        txt = open(j, 'r').read()
        rows = txt.split('\n')
        j = j.replace(".txt", "")
        col_name = rename(j, "")
        # csv_max = "{}\\{}.csv".format(path, col_name)
        csv_max = col_name +'.csv'
        csv = open(csv_max, "w")
        csv.writelines(col_name+"\n")
        for row in rows[2:-1]:
            row = row.split()
            max = row[2]
            max = round(float(max)*100, 0)/100
            csv.writelines(str(max)+"\n")
        csv.close()

        os.remove(j+".txt")

def mergedCsv(coor, QH):
    csv_list = []
    for i in res_list:
        i = rename(i, ".csv")
        dir = os.path.dirname(i)
        qh = QH + os.path.basename(i)

        i = os.path.join(dir,qh)
        csv_list.append(i)
        print(i)
        
    csv_list.sort(reverse=True)
    csv_list.insert(0, coor)
    print(csv_list)

    csv_data = []
    for csv in csv_list:
        if csv.endswith('csv'):  # nie wiem,czemu bez tego nie dziala
            csv_path = os.path.join(path, csv)
            arcpy.AddMessage(csv_path)
            data = pd.read_csv(csv_path, sep=';')
            csv_data.append(data)

    csv_data = pd.concat(csv_data, axis=1, join='inner')
    merged_csv = "{}{}_csv.csv".format(rzeka, QH)
    merged_csv_file = os.path.join(path, merged_csv)

    if os.path.exists(merged_csv_file):
        os.remove(merged_csv_file)
    csv_data.to_csv(merged_csv_file, index=False, sep=";")

    for csv in csv_list:
        os.remove(csv)
    
    return merged_csv_file

def createShp(merged_csv_file, QH,col):
    xy_lyr = "xy_lyr"
    pkt_lyr = "pkt_lyr"
    shp_wynik = os.path.join(path,"{}{}.shp".format(rzeka, QH))
    shp_roboczy = os.path.join(path,"{}roboczy.shp".format(rzeka))

    arcpy.MakeXYEventLayer_management(merged_csv_file, "x", "y", xy_lyr, "2180")
    # eliminacja punktow z kanalow polaczeniowych
    arcpy.MakeFeatureLayer_management(xy_lyr, pkt_lyr, "\"branch\" NOT LIKE 'KP_%'")
    arcpy.CopyFeatures_management(pkt_lyr, os.path.join(path, shp_roboczy))

    # stworzenie listy zdublowanych elementów (na podstawie x i y) do_usuniecia
    cursor = arcpy.SearchCursor(shp_roboczy)
    do_usuniecia = []
    i = 0
    p_coor = ""
    for row in cursor:
        current = row
        coor = current.getValue("x"), current.getValue("y")
        if coor == p_coor:
            do_usuniecia.append(i)
        p_coor = coor
        i += 1

    # usuniecie zdublowanych elementow, na podstawie listy do_usuniecia; usuniecie elementow type==1
    i = 0
    cursor = arcpy.UpdateCursor(shp_roboczy)
    for row in cursor:
        if i in do_usuniecia:
            cursor.deleteRow(row)
        i += 1
        if row.getValue("typ") == 1:
            cursor.deleteRow(row)            
    del cursor, row

    arcpy.DeleteField_management(shp_roboczy, "typ")
    arcpy.CopyFeatures_management(shp_roboczy, os.path.join(path, shp_wynik))
    arcpy.Delete_management(shp_roboczy)

    arcpy.AddField_management(shp_wynik,col,"DOUBLE","","",0)
    arcpy.AddField_management(shp_wynik,"ID_HYD_R","TEXT","","",22)
    arcpy.AddField_management(shp_wynik,"NAZWA_MPHP","TEXT","","",0)
    arcpy.AddField_management(shp_wynik,"KM_PKT","DOUBLE","","",0)
    arcpy.CalculateField_management(shp_wynik,"KM_PKT",'!km!','PYTHON')
    arcpy.AddField_management(shp_wynik,"TERASA_ZAL","TEXT","","",25)
    arcpy.AddField_management(shp_wynik,"OPIS","TEXT","","",0)
    arcpy.CalculateField_management(shp_wynik,"OPIS",'!branch!','PYTHON')
    arcpy.AddField_management(shp_wynik,"WERSJA","TEXT","","",25)
    # arcpy.CalculateField_management(shp_wynik,"WERSJA",'"2018v1"','PYTHON')

    arcpy.DeleteField_management(shp_wynik,["km","branch","x","y"])
    
    os.remove(merged_csv_file)

xyh = batRun([res_list[0]], "-xyh")
txtPtsRead(xyh[0], "coor_H")
max1 = batRun(res_list, "-max1")
txtMaxRead(res_list, max1)
min1 = batRun(res_list, "-min1")
txtMaxRead(res_list, min1)

for i in res_list:
    i = rename(i, ".csv")
    arcpy.AddMessage(i+' csv')

    dir = os.path.dirname(i)
    hmax = 'Hmax' + os.path.basename(i)
    hmin = 'Hmin' + os.path.basename(i)
    h = 'H' + os.path.basename(i)
    hmax_dir= os.path.join(dir,hmax)
    hmin_dir = os.path.join(dir, hmin)
    h_dir = os.path.join(dir, h)

    Hmax_csv=open(hmax_dir,"r").read()
    Hmin_csv=open(hmin_dir,"r").read()
    H_csv=open(h_dir,"w")

    col_name = "H_"+os.path.basename(i).replace(".csv", "")
    if "1000" in col_name:
        col_name=col_name.replace("1000","01")
    elif "500" in col_name:
        col_name=col_name.replace("500","02")
    elif "100" in col_name:
        col_name=col_name.replace("100","1")    
    elif "010" in col_name:
        col_name=col_name.replace("010","10")


    H_csv.writelines(col_name+"\n")
    
    rows_Hmax = Hmax_csv.split('\n')
    rows_Hmax = rows_Hmax[1:-1]
    rows_Hmin = Hmin_csv.split('\n')
    rows_Hmin = rows_Hmin[1:-1]
    for j, max in enumerate(rows_Hmax):
##        print(max, abs(float(rows_Hmin[j])))
        if float(max)==float(rows_Hmin[j]):
            H=-7777
        if float(max)>float(rows_Hmin[j]):
            H=max

        H_csv.writelines(str(H)+"\n")
    H_csv.close()
    os.remove(hmax_dir)
    os.remove(hmin_dir)

merged_csv_file = mergedCsv(os.path.join(path,"coor_H.csv"), "H")
createShp(merged_csv_file, "H","H_WZ")
os.remove(bat_file)

xyq = batRun([res_list[0]], "-xyq")
txtPtsRead(xyq[0], "coor_Q")
max2 = batRun(res_list, "-max2")
txtMaxRead(res_list, max2)
min2 = batRun(res_list, "-min2")
txtMaxRead(res_list, min2)

for i in res_list:
    i = rename(i, ".csv")
    arcpy.AddMessage(i)
    dir = os.path.dirname(i)
    qmax = 'Qmax' + os.path.basename(i)
    qmin = 'Qmin' + os.path.basename(i)
    q = 'Q' + os.path.basename(i)
    qmax_dir = os.path.join(dir, qmax)
    qmin_dir = os.path.join(dir, qmin)
    q_dir = os.path.join(dir, q)

    Qmax_csv=open(qmax_dir,"r").read()
    Qmin_csv=open(qmin_dir,"r").read()
    
    Q_csv=open(q_dir,"w")
    col_name = "Q_"+os.path.basename(i).replace(".csv", "")

    if "1000" in col_name:
        col_name = col_name.replace("1000", "01")
    elif "500" in col_name:
        col_name=col_name.replace("500","02")
    elif "100" in col_name:
        col_name=col_name.replace("100","1")    
    elif "010" in col_name:
        col_name=col_name.replace("010","10")


    Q_csv.writelines(col_name+"\n")
    
    rows_Qmax = Qmax_csv.split('\n')
    rows_Qmax = rows_Qmax[1:-1]
    rows_Qmin = Qmin_csv.split('\n')
    rows_Qmin = rows_Qmin[1:-1]    
    for j, max in enumerate(rows_Qmax):
##        print(max, abs(float(rows_Qmin[j])))
        if float(max)>=abs(float(rows_Qmin[j])):
            Q=max
##            print(Q)
        if abs(float(rows_Qmin[j]))>float(max):
            Q=rows_Qmin[j]
##            print(Q)
        Q_csv.writelines(Q+"\n")
    Q_csv.close()
    os.remove(qmax_dir)
    os.remove(qmin_dir)

merged_csv_file = mergedCsv(os.path.join(path,"coor_Q.csv"), "Q")
createShp(merged_csv_file, "Q","Q_WZ")
os.remove(bat_file)

arcpy.AddMessage("Zakończono i wwygenerowano warstwy przestrzenne Q i H z wynikami")

