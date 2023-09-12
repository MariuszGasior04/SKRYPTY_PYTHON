#!/usr/bin/env python
#-*- coding: utf-8 -*-
#skrypt do pobierania danych GUGIK na podstawie skorowidzów
import os
import requests
import arcpy

def download_from_shp(skorowidz, output_dir):
    i = 0
    arcpy.AddMessage("Sprawdzanie atrybutow warstwy skorowidzy...")
    field_names = [f.name for f in arcpy.ListFields(skorowidz)]
    if 'STATUS' not in field_names:
        arcpy.AddField_management(skorowidz, field_name="STATUS", field_type="TEXT", field_length=50)
        arcpy.AddMessage("Dodanie atrybutu 'STATUS' do warstwy skorowidzy...")

    with arcpy.da.UpdateCursor(skorowidz, ['godlo', 'url_do_pob', 'STATUS'])as cur:
        for row in cur:
            if row[2] != 'pobrane':
                URL = row[1]
                response = requests.get(URL)
                filename = URL.split('/')[-1]
                open(os.path.join(output_dir, filename), "wb").write(response.content)
                i+=1
                row[2] = 'pobrane'
                arcpy.AddMessage("{0} Pobrano arkusz {1} o nazwie {2}".format(i, row[0], filename))
            cur.updateRow(row)
    del cur

if __name__ == '__main__':
    skorowidz = arcpy.GetParameterAsText(0)
    folder_pobrane = arcpy.GetParameterAsText(1)

    download_from_shp(skorowidz, folder_pobrane)
