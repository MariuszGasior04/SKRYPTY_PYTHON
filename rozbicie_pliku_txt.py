#-*- coding: utf-8 -*-
import os
import csv


#podaj scieżkę do pliku csv w ktorym maja zostac zapisane wszystkie odczytane pliki
txt_file=ur"R:\OIIS_KR5\_PROJEKTY 2019\19004-00_Piekielko\33_ULLK\337_GIS\1_roboczy\cad\odcinek_B_pas300m.txt"
txt_file2=ur"R:\OIIS_KR5\_PROJEKTY 2019\19004-00_Piekielko\33_ULLK\337_GIS\1_roboczy\cad\odcinek_B_pas300m_2.txt"
txt_file3=ur"R:\OIIS_KR5\_PROJEKTY 2019\19004-00_Piekielko\33_ULLK\337_GIS\1_roboczy\cad\odcinek_B_pas300m_3.txt"
txt_file4=ur"R:\OIIS_KR5\_PROJEKTY 2019\19004-00_Piekielko\33_ULLK\337_GIS\1_roboczy\cad\odcinek_B_pas300m_4.txt"
txt_file5=ur"R:\OIIS_KR5\_PROJEKTY 2019\19004-00_Piekielko\33_ULLK\337_GIS\1_roboczy\cad\odcinek_B_pas300m_5.txt"
txt_file6=ur"R:\OIIS_KR5\_PROJEKTY 2019\19004-00_Piekielko\33_ULLK\337_GIS\1_roboczy\cad\odcinek_B_pas300m_6.txt"

# otwieramy plik txt i csv oraz zapisujemy nagłowki tworzonych zestawien
txt_2=open(txt_file2,'w')
txt_3=open(txt_file3,'w')
txt_4=open(txt_file4,'w')
txt_5=open(txt_file5,'w')
txt_6=open(txt_file6,'w')
i=0

with open(txt_file,'r') as zmienna:
    for line in zmienna:
        i+=1
        linia = line.replace('.',',')
        if i < 1000000:
            txt_2.write(linia)
        elif i >=1000000 and i < 2000000:
            txt_3.write(linia)
        elif i >=2000000 and i < 3000000:
            txt_4.write(linia)
        elif i >=3000000 and i < 4000000:
            txt_5.write(linia)
        elif i >=4000000:
            txt_6.write(linia)

txt_2.close()
txt_3.close()
txt_4.close()
txt_5.close()
txt_6.close()