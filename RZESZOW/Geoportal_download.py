#!/usr/bin/env python
#-*- coding: utf-8 -*-
#skrypt do pobierania danych GUGIK na podstawie skorowidzów
import os
import requests
import arcpy

def download_from_shp(env, shp, output_dir):
    arcpy.env.workspace = env
    i = 0
    out_data = os.path.join(env, shp)
    field_names = [f.name for f in arcpy.ListFields(out_data)]
    if 'status' not in field_names:
        arcpy.AddField_management(out_data, 'status', "TEXT", field_length=50)

    with arcpy.da.UpdateCursor(shp, ['godlo', 'url_do_pob', 'status'])as cur:
        for row in cur:

            if row[2] != 'pobrane':
                url = row[1]
                response = requests.get(url)
                filename = url.split('/')[-1]
                open(os.path.join(output_dir, filename), "wb").write(response.content)
                i += 1
                row[2] = 'pobrane'
                print(i, str(row[0]), str(filename))
            cur.updateRow(row)
    del cur

if __name__ == '__main__':
    workspace = r'C:\robo\_warstwy_tymczasowe\NMT\Podstawowa_osnowa_wysokosciowa'
    arkusze = r'powiaty.shp'
    folder_pobrane = r'C:\robo\_warstwy_tymczasowe\NMT\Podstawowa_osnowa_wysokosciowa\Pobrane'

    download_from_shp(workspace, arkusze, folder_pobrane)
