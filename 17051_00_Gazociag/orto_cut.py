# !/usr/bin/env python
# -*- coding: utf-8 -*-

# skrypt do kopiowania wybranych arkuszy mapowych do swojej przestrzeni roboczej

import arcpy
import shutil
import os
from arcpy.sa import *

arcpy.env.workspace=ws=ur'R:\OIIS_KR5\_PROJEKTY 2018\18042-00 Skoczów-Komorowice-Oświęcim\11_GIS\1_roboczy\shp\arkusze'
arkusz = 'orto_ark_2500.shp'
folder_out = ur'R:\OIIS_KR5\_PROJEKTY 2018\18042-00 Skoczów-Komorowice-Oświęcim\11_GIS\_ETAP_I_PW\MAPY\Ortofotomapa'
folder = ur"R:\OIIS_KR5\_PROJEKTY 2018\18042-00 Skoczów-Komorowice-Oświęcim\11_GIS\_ETAP_I_PW\MAPY\Ortofotomapa\New Folder"


with arcpy.da.SearchCursor(arkusz,['godlo2'])as cur:
    for row in cur:
        for sciezka, podkatalogi, pliki in os.walk(folder):
             a=sciezka,podkatalogi,pliki
             for plik in a[2]:
                if os.path.splitext(plik)[0]==row[0]:
                    print os.path.join(folder,plik)
                    where_clause = '"godlo2" = ' +"'"+ str(row[0])+"'"
                    out = row[0]+".shp"
                    out_feature_class = out.replace("-","_")
                    arcpy.Select_analysis(arkusz, out_feature_class, where_clause)

##                    outExtractByMask = ExtractByMask(os.path.join(folder,plik), out_feature_class)
##                    outExtractByMask.save(os.path.join(folder_out,row[0]+".tif"))
##                    arcpy.DeleteFeatures_management(out_feature_class)

del cur
