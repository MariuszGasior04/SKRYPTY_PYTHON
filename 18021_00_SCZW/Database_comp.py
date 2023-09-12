#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do porównania różnic między dwiema wersjami tej samej geobazy

import arcpy
import os

arcpy.env.overwriteOutput = True

def compareGdb(gdbSource, gdbUpdated):
    '''
    Funkcja porównująca tabele o takiej samej nazwie w dwóch geobazach, ale w innej wersji opracowania
    gdbSource - geobaza w wersji pierwotnej
    gdbUpdated - geobaza zaktualizowana
    compare_type - typ porównania (ALL —Compare all properties. This is the default. ATTRIBUTES_ONLY —Only compare the attributes and their values. SCHEMA_ONLY —Only compare the schema. Data Type STRING)
    '''

    arcpy.env.workspace = gdbUpdated
    for dirpathF, dirnamesF, filenamesF in arcpy.da.Walk(gdbUpdated):
        print dirpathF
        for fdsUpdated in filenamesF:
            fields = arcpy.ListFields(fdsUpdated)

            sort_field='OBJECTID'
            compare_type = 'ALL'
            ignore_option = "IGNORE_RELATIONSHIPCLASSES"
            continue_compare = "CONTINUE_COMPARE"
            attribute_tolerance = '#'
            omit_field = 'OBJECT_ID'
            compare_file = os.path.join(r"D:\DaneRobocze\SZCW_asysta", fdsUpdated + '_comp.txt')

            for dirpathS, dirnamesS, filenamesS in arcpy.da.Walk(gdbSource):
                for fdsSource in filenamesS:
                    if fdsUpdated == fdsSource:
                        # try:

                        arcpy.TableCompare_management(fdsUpdated, os.path.join(dirpathS, fdsSource),
                                                      sort_field,
                                                      compare_type,
                                                      ignore_option,
                                                      attribute_tolerance,
                                                      omit_field,
                                                      continue_compare,
                                                      compare_file)

                        #     print u"Porównało tabele " + str(fdsUpdated)
                        #
                        # except Exception as e:
                        #     print u"Nie porównano tabeli warstwy " + str(fdsUpdated)
                        #     raise e
    return

if __name__ == '__main__':

    geodatabaseSource = \
        ur'P:\Projekty_2017\18021-00_SZCW\08.Produkty\10.Przekazane\2019.05.31_CAŁOŚĆ\P6_Baza_danych\Baza danych wytworzonych\Baza SZCW.gdb'
    geodatabaseUpdated = \
        ur'P:\Projekty_2017\18021-00_SZCW\08.Produkty\10.Przekazane\ASYSTA_GWARANCJA\2020.11.17\Baza SZCW.gdb'

    compareGdb(geodatabaseSource, geodatabaseUpdated)
