#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arcpy

arcpy.env.overwriteOutput = True
arcpy.env.workspace = ws = ur'R:\OIIS_KR5\_PROJEKTY 2018\18042-00 Skoczów-Komorowice-Oświęcim\11_GIS\1_roboczy\shp\Dzialki'
dz_topo = 'Dzialki_godla.shp'
dz = 'Dzialki_11_02_2019.shp'


with arcpy.da.UpdateCursor(dz,['DZ_TERYT','ARKUSZE']) as cur:
    for row in cur:
        lista=[]

        with arcpy.da.SearchCursor(dz_topo,['DZ_TERYT','godlo'])as search:
            for row2 in search:
                if row[0] == row2[0]:
                    lista.append(row2[1])
        del search
        g = ''

        for godlo in lista:
            if len(lista) == 1:
                g = str(godlo)
                row[1] = g
                cur.updateRow(row)
            else:
                g = g + str(godlo)+', '
        row[1] = g
        cur.updateRow(row)
del cur