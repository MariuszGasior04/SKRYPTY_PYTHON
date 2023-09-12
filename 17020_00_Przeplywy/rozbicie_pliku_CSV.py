#-*- coding: utf-8 -*-
import os
import csv


#podaj scieżkę do pliku csv w ktorym maja zostac zapisane wszystkie odczytane pliki
csv_file=ur"E:\FolderRoboczy\_roboczy\csv\B00050S_2018_08.csv"
csv_file2=ur"E:\FolderRoboczy\_roboczy\csv\B00050S_2018_08_1.csv"
csv_file3=ur"E:\FolderRoboczy\_roboczy\csv\B00050S_2018_08_2.csv"
csv_file4=ur"E:\FolderRoboczy\_roboczy\csv\B00050S_2018_08_3.csv"

# otwieramy plik txt i csv oraz zapisujemy nagłowki tworzonych zestawien
csv_2=open(csv_file2,'w')
csv_3=open(csv_file3,'w')
csv_4=open(csv_file4,'w')

i=0

with open(csv_file,'r') as zmienna:
    for line in zmienna:
        i+=1
        if i < 1000000:
            csv_2.write(line)
        elif i >=1000000 and i < 2000000:
            csv_3.write(line)
        elif i >= 2000000:
            csv_4.write(line)



csv_2.close()
csv_3.close()
csv_4.close()
