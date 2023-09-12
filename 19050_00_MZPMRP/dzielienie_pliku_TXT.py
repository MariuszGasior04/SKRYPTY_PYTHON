#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do rozdzielania liku tekstowego na dwa
import os

file_input = r"R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\2_Opracowanie_danych_do_modeli\etap 2\2_przedluzone\Otmuchow_Nysa\S01_Nysa_Klodzka_przetworzone_RD.txt"
file_output_1 = os.path.join(os.path.dirname(file_input),os.path.basename(file_input).split('.')[0]+'_1.txt')
file_output_2 = os.path.join(os.path.dirname(file_input),os.path.basename(file_input).split('.')[0]+'_2.txt')
f1 = open(file_output_1, "w")
f2 = open(file_output_2, "w")

file_txt = open(file_input, "r")
counter = 0

for line in file_txt:
    if counter == 0:
        header = line
    counter+=1

file_txt.close()

f2.write(header)

file_txt = open(file_input, "r")
counter2 = 0

for line in file_txt:
    counter2 += 1
    counter -= 1
    if counter2 < counter/2:
        f1.write(line)
    else:
        f2.write(line)

f1.close()
f2.close()