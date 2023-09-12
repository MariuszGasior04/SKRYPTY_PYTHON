#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy, os

def loadShp(dir, gdbFinal):
    '''Funkcja ładująca warstwy przestrzenne *.shp o takiej samej nazwie i strukturze atrybutowej z folderu do geobazy'''
    arcpy.env.workspace = gdbFinal
    for dirpathF, dirnamesF, filenamesF in arcpy.da.Walk(gdbFinal):
        for fdsF in filenamesF:
            for dirpathS, dirnamesS, filenamesS in os.walk(dir, topdown=False):
                for fdsS in filenamesS:
                    if fdsS.split('.')[-1] == 'shp' and fdsF == fdsS.split('.')[0]:
                        try:
                            arcpy.Append_management(os.path.join(dirpathS, fdsS), fdsF, "NO_TEST", "", "")
                            print u"Zaladowalo klase " + str(fdsF)
                        except:
                            print u"Nie załadowano warstwy " + str(fdsF)
    return

def loadGdb(gdbSource, gdbFinal):
    '''Funkcja ładująca warstwy przestrzenne o takiej samej nazwie i strukturze atrybutowej z geobazy do geobazy'''
    arcpy.env.workspace = gdbFinal
    for dirpathF, dirnamesF, filenamesF in arcpy.da.Walk(gdbFinal):
        for fdsF in filenamesF:

            for dirpathS, dirnamesS, filenamesS in arcpy.da.Walk(gdbSource):
                for fdsS in filenamesS:
                    if fdsF == fdsS:
                        try:
                            arcpy.Append_management(os.path.join(dirpathS, fdsS), fdsF, "NO_TEST", "", "")
                            print u"Zaladowalo klase " + str(fdsF)
                        except:
                            print u"Nie załadowano warstwy " + str(fdsF)
    return

if __name__ == '__main__':
    folderShp = \
        ur'R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\4_Opracowanie_baz_danych\_DO PRZEKAZANIA\BUDOWLE PIETRZACE\OBSZARY DORZECZA\OD ODRY\MZP'
    geodatabaseFinal = \
        ur'R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\4_Opracowanie_baz_danych\_DO PRZEKAZANIA\GEOBAZA\MZP.gdb'

    loadShp(folderShp, geodatabaseFinal)