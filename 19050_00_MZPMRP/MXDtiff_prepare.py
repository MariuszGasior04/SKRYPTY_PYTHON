#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do porównania różnic między dwiema wersjami tej samej geobazy

import arcpy
import os

arcpy.env.overwriteOutput = True


def mxdCopy(folder_mxd, folder_output):
    i = 0
    wydrukowane_lista=[]

    for mapa in os.listdir(folder_output):
        wydrukowane_lista.append(os.path.splitext(mapa)[0])

    wydruki = set(wydrukowane_lista)

    for plik in os.listdir(folder_mxd):
            if (os.path.isfile(os.path.join(folder_mxd, plik)) and os.path.splitext(plik)[1] == '.mxd') and os.path.splitext(plik)[0] not in wydruki:
                i+=1
                mxd = arcpy.mapping.MapDocument(os.path.join(folder_mxd, plik))
                print str(i) +' - '+ plik

                mxd.saveACopy(os.path.join(folder_output, plik),'10.3')

    return

if __name__ == '__main__':

    folder_input = \
        ur'R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\5_Opracowanie_kartograficzne\BAZA_Mapy\PROJEKCJE_ETAP3_106\MZP\PDF'
    folder_output = \
        ur'R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\5_Opracowanie_kartograficzne\BAZA_Mapy\PROJEKCJE_ETAP3\MZP\PDF'

    mxdCopy(folder_input, folder_output)