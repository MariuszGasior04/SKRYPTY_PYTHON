#!/usr/bin/env python
#-*- coding: utf-8 -*-


import arcpy
import os

arcpy.env.overwriteOutput = True

def mxdExport(file_mxd, folder_map):
    mxd = arcpy.mapping.MapDocument(file_mxd)
    for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):

        mxd.dataDrivenPages.currentPageID = pageNum
        pageName = mxd.dataDrivenPages.pageRow.PageNumber
        elements = arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT")

        for elm in elements:
            if elm.name == 'PODGIK - 3 do 6':
                elm.elementWidth = 9.8
            if elm.name == 'PODGIK - 1 do 2_6a do 12_171 do 175':
                elm.elementWidth = 10.8
            if 'KODGIK' in elm.name:
                elm.elementWidth = 7.8

        arcpy.mapping.ExportToPDF(mxd, os.path.join(folder_map, 'zalacznik 1 odc 1 arkusz ' + str(pageName) + ".pdf")
                                  , resolution=300
                                  , image_compression='ADAPTIVE'
                                  , picture_symbol='RASTERIZE_BITMAP'
                                  , layers_attributes='NONE'
                                  , jpeg_compression_quality=85
                                  , georef_info=True)

        print ('zalacznik 1 odc 1 arkusz {0}.pdf').format(pageName)

    del mxd

    return

if __name__ == '__main__':

    mxd_input = \
        ur'R:\OIIS_KR5\_PROJEKTY 2018\18035-00 LK201\33_ULLK\337_GIS\2_mapy\Projekcje\ODC1\wersja_bez_podpisów\ODC1_ULLK_kolejowa_126x594_zal1.mxd'

    folder_map = \
        ur"R:\OIIS_KR5\_PROJEKTY 2018\18035-00 LK201\33_ULLK\337_GIS\2_mapy\Pdf\ODC1\ZALACZNIK1"

    mxdExport(mxd_input, folder_map)
