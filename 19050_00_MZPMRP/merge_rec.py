#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arcpy
import os

def collect_layers(dir, layerName, layerType):
    walk = arcpy.da.Walk(dir, datatype="FeatureClass", type=layerType)
    feature_classes = []
    for dirpath, dirnames, filenames in walk:
        for filename in filenames:
            if layerName in filename:
                feature_classes.append(os.path.join(dirpath, filename))

    return feature_classes


if __name__ == '__main__':
    layer = 'zaklady_przemyslowe'
    layer_type = 'Point'
    folder = ur"R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\4_Opracowanie_baz_danych\Baza z podzialem na RW i Dorzecza\Zbiorniki\mrp"
    folder_out = ur'R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\4_Opracowanie_baz_danych\Baza z podzialem na RW i Dorzecza\Zbiorniki\mrp_merge'

    try:
        arcpy.Merge_management(collect_layers(folder, layer, layer_type), os.path.join(folder_out, layer + '.shp'))
        print "Merge succeded {0}".format(layer)

    except Exception as e:
        raise e
