#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy
import os
folder_mxd = r"P:\02_Pracownicy\Mariusz\PULAWSKA\MAPY\MXD\korekta_uwag_pNachlik"
folder_map = r"P:\02_Pracownicy\Mariusz\PULAWSKA\MAPY\JPG\Korekta_uwag_pNachlik"

for plik in os.listdir(folder_mxd):
    if os.path.isfile(os.path.join(folder_mxd, plik)) and os.path.splitext(plik)[1] == '.mxd':
        mxd = arcpy.mapping.MapDocument(os.path.join(folder_mxd, plik))
        for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):
            mxd.dataDrivenPages.currentPageID = pageNum
            pageName = mxd.dataDrivenPages.pageRow.NAZ_MAP
            arcpy.mapping.ExportToJPEG(mxd, os.path.join(folder_map, str(pageName) + ".jpg"), resolution=200, jpeg_quality=95)
        del mxd

