#-*- coding: utf-8 -*-
import os
import csv

# podaj folder ktory należy przeszukac
folder=ur'P:\Projekty_2017\17051-00 Goleniów_Lwówek_DN1000\05_Geodezja\Materiały z PODGiK\Nowy Tomyśl\2018-09-24\zasadnicza 20.09.18'

#podaj scieżkę do pliku txt w ktorym maja zostac zapisane wszystkie odczytane pliki
txt_file=ur"P:\Projekty_2017\17051-00 Goleniów_Lwówek_DN1000\05_Geodezja\Materiały z PODGiK\Nowy Tomyśl\2018-09-24\zasadnicza 20.09.18\test.txt"



def konwersja_bajtow(num):
    """
    funkcja konwertuje bajty na MB.... GB... itd
    """
    for x in ['bajty', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.3f %s" % (num, x)
        num /= 1024.0

def rozmiar_nazwa_pliku(sciezka):
    """
    funkcja zwroci rozmiar pliku i jego nazwe
    """
    if os.path.isfile(sciezka):
        file_info = os.stat(sciezka)
        return [os.path.split(sciezka)[1],konwersja_bajtow(file_info.st_size)]

# otwieramy plik txt i csv oraz zapisujemy nagłowki tworzonych zestawien
txt_=open(txt_file,"w")
txt_.write('Plik'+'\n')

"""
pętla przeszukuje kolejne foldery oraz podfoldery zadeklarowanej scieżki pierwszej,
pętla wewnętrzna rozpoznaje pliki, pobiera objetosci tych plikow (ewentualnie zapisuje je do pliku txt i csv)
"""

for sciezka, podkatalogi, pliki in os.walk(folder):
     a=sciezka,podkatalogi,pliki
     for plik in a[2]:

        if os.path.splitext(plik)[1]=='.pdf':

            txt_.write(str(plik)+'\n')

txt_.close()