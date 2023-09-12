#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import PyPDF4
import csv
import math


def pdfsizecounter(folder_pdf, copies_no):
    a3_length = 0
    a2_length = 0
    a1_length = 0
    a0_length = 0
    with open(os.path.join(folder_pdf, 'spis_rysunkow.csv'), mode='w') as csv_file:
        csv_rowlist = [['Nazwa_pliku', 'wymiary [cm]', 'A3_297 [mm]', 'A2_420 [mm]', 'A1_594 [mm]', 'A0_841 [mm]']]
        writer = csv.writer(csv_file, dialect='excel', delimiter='\t')

        for plik_pdf in os.listdir(folder_pdf):
            if os.path.splitext(plik_pdf)[-1] == '.pdf':
                # print(os.path.join(folder_pdf, plik_pdf))
                pdf = open(os.path.join(folder_pdf, plik_pdf), 'rb')

                reader = PyPDF4.PdfFileReader(pdf,
                                              strict=False,
                                              warndest=None,
                                              overwriteWarnings=True)
                pagehight = round(float(reader.getPage(0).mediaBox[3]) * 0.035274, 1)
                pagelength = round(float(reader.getPage(0).mediaBox[2]) * 0.035274, 1)
                # print(reader.documentInfo)
                pdf.close()

                if pagehight <= pagelength:
                    hight = pagehight
                    length = pagelength
                else:
                    hight = pagelength
                    length = pagehight

                if hight == 21.0:
                    csv_rowlist.append([plik_pdf, 'A4', 0, 0, 0, 0])

                elif hight == 29.7:
                    csv_rowlist.append([plik_pdf, str(hight) + ' x ' + str(length), length * 10, 0, 0, 0])
                    a3_length += length * 10

                elif hight == 42.0:
                    csv_rowlist.append([plik_pdf, str(hight) + ' x ' + str(length), 0, length * 10, 0, 0])
                    a2_length += length * 10

                elif hight == 59.4:
                    csv_rowlist.append([plik_pdf, str(hight) + ' x ' + str(length), 0, 0, length * 10, 0])
                    a1_length += length * 10

                elif hight == 84.1:
                    csv_rowlist.append([plik_pdf, str(hight) + ' x ' + str(length), 0, 0, 0, length * 10])
                    a0_length += length * 10

                else:
                    csv_rowlist.append([plik_pdf, str(hight) + ' x ' + str(length), 'niestandartowy wymiar', 'niestandartowy wymiar', 'niestandartowy wymiar', 'niestandartowy wymiar'])


        csv_rowlist.append(['Sumaryczna dlugosc wydrukow', ' ', a3_length, a2_length, a1_length, a0_length])
        csv_rowlist.append(
            ['Metry bierzace rolki dla ' + str(copies_no) + ' kopii', ' ', int(math.ceil(a3_length * float(copies_no) / 1000)),
             int(math.ceil(a2_length * float(copies_no) / 1000)), int(math.ceil(a1_length * float(copies_no) / 1000)),
             int(math.ceil(a0_length * float(copies_no) / 1000))])
        writer.writerows(csv_rowlist)

    csv_file.close()
    return


if __name__ == '__main__':

    folder = input('Wklej sciezke do folderu z plikami PDF:')
    # in_folder = unicode(folder)
    copies_count = input('Podaj liczbe kopii:')
    try:
        copies_count = int(copies_count)
        while type(copies_count) is not int:
            copies_count = input('Podaj liczbe kopii:')

        try:
            pdfsizecounter(folder, copies_count)
        except Exception as e:
            raise e

    except Exception as e:
        raise e
    print('Utworzono plik "spis_rysunkow.csv" w lokalizacji {0}. Obliczenia wykonano dla {1} kopii rysunkow'.format(
        folder, copies_count))
