#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

folder_map = ur"R:\OIIS_KR5\_PROJEKTY 2019\19050-00_Mapy_Budowle\07.GIS\5_Opracowanie_kartograficzne\MAPY\OD WISŁY\MRP"

for plik in os.listdir(folder_map):
    print (os.path.splitext(plik))
##    os.rename(os.path.join(folder_map,plik),os.path.join(folder_map,plik_nowy))