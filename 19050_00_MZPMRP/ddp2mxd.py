#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy
import os

war = "MRP"

# list_mrp = ['MRP_RL_BP_Tresna.mxd']

# list_mrp =[ 'MRP_RL_BP_Debe.mxd',
#             'MRP_RL_BP_Jeziorsko_UTM34.mxd',
#             'MRP_RL_BP_Jeziorsko_UTM33.mxd',
#             'MRP_RL_BP_Wloclawek_UTM34.mxd',
#             'MRP_RL_BP_Wloclawek_UTM33.mxd',
#             'MRP_RL_BP_Sulejow.mxd',
#             'MRP_RL_BP_Pakosc_UTM34.mxd',
#             'MRP_RL_BP_Pakosc_UTM33.mxd',
#             'MRP_RL_BP_Mylof.mxd',
#             'MRP_RL_BP_Koronowo_UTM34.mxd',
#             'MRP_RL_BP_Koronowo_UTM33.mxd'
#             ]
# list_mzp = [
#             'MZP_ZG_BP_Goczalkowice.mxd', 'MZP_ZG_BP_Tresna.mxd'
#             ]
# list_mrp = [
#             'MRP_RS_BP_Goczalkowice.mxd', 'MRP_RS_BP_Tresna.mxd', 'MRP_RL_BP_Goczalkowice.mxd', 'MRP_RL_BP_Tresna.mxd'
#             ]
list_mrp = [
            'MRP_RS_BP_Goczalkowice_Geotiff.mxd', 'MRP_RS_BP_Tresna_Geotiff.mxd', 'MRP_RL_BP_Goczalkowice_Geotiff.mxd', 'MRP_RL_BP_Tresna_Geotiff.mxd'
            ]



if war == 'MRP':
    list_mxd = list_mrp
    folder_mxd = ur"R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\5_Opracowanie_kartograficzne\PROJEKCJE ETAP1-SZABLONY\MRP_roboczo_geotiff"
elif war == 'MZP':
    list_mxd = list_mzp
    folder_mxd = ur"R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\5_Opracowanie_kartograficzne\PROJEKCJE ETAP1-SZABLONY\MZP_roboczo"

for projekcja in list_mxd:
    mxd = arcpy.mapping.MapDocument(os.path.join(r"R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\5_Opracowanie_kartograficzne\PROJEKCJE ETAP1-SZABLONY", projekcja))
    for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):
         mxd.dataDrivenPages.currentPageID = pageNum
         pageName = mxd.dataDrivenPages.pageRow.Godlo.replace('-', '')

         if len(pageName) < 8:
            pageName = pageName[:3]+'00'+pageName[3:]

         if len(pageName) < 9:
            pageName = pageName[:3]+'0'+pageName[3:]

         zbior = mxd.dataDrivenPages.pageRow.ZBIORNIK.replace(' ', '_')
         print(pageName + projekcja[3:10]+zbior+"_2022v1")
         mxd.saveACopy(os.path.join(folder_mxd, pageName + projekcja[3:10]+zbior+"_2022v1.mxd"))

del mxd