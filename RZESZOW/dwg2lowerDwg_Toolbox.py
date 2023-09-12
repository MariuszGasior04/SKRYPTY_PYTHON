#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy
import os

def prepareInputFeatures(dwg_file):
    dwg_features = []
    dwg_features.append(os.path.join(dwg_file, 'MultiPatch'))
    dwg_features.append(os.path.join(dwg_file, 'Annotation'))
    dwg_features.append(os.path.join(dwg_file, 'Polygon'))
    dwg_features.append(os.path.join(dwg_file, 'Polyline'))
    dwg_features.append(os.path.join(dwg_file, 'Point'))
    return dwg_features

def saveDwgVersion(input_folder_dwg, output_folder_dwg,output_type):
    for file in os.listdir(input_folder_dwg):
        if os.path.isfile(os.path.join(input_folder_dwg, file)) and os.path.splitext(file)[1] == '.dwg':
            dwg_file = os.path.join(input_folder_dwg, file)
            arcpy.AddMessage("Przetwarzanie pliku - ".format(file))
            dwg_features = prepareInputFeatures(dwg_file)
            output_file = os.path.join(output_folder_dwg, file)
            arcpy.ExportCAD_conversion(dwg_features, output_type, output_file)
            arcpy.AddMessage("Zapisano plik {0} do wersji {1} ".format(output_file, output_type))
    return

if __name__ == '__main__':
    input_folder_dwg = arcpy.GetParameterAsText(0)
    output_folder_dwg = arcpy.GetParameterAsText(1)
    dwg_version = arcpy.GetParameterAsText(2)

    saveDwgVersion(input_folder_dwg, output_folder_dwg, dwg_version)
