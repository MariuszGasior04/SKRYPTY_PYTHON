#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do zmiany nagłowkow tabeli wykazu dzialek i podmiotow wyeksportowanej z swd do dbf. Narzędzie działa tylko na tabelach zaimportowanych do geobazy

import arcpy
import os
from arcpy import env
arcpy.env.overwriteOutput = True

"""PARAMETRY PROGRAMU"""

arcpy.env.workspace = ws = ur'R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\9_Baza_publikacyjna\roboczy'

tab = 'Lista_folder_pdf.dbf'

with arcpy.da.SearchCursor(tab, ['FOLDER'])as cur:
    for row in cur:
        path = os.path.join(ur'R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\03.DaneOZ\20211123_Publikacja_MZPiMRP_BP\2_Hydroportal_PDF\pdf',str(row[0]))
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)


del cur
