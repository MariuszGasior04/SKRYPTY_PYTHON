#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do porządkowania opisow sieci branzowych na warstwach działek ewidencyjnych

import arcpy

arcpy.env.overwriteOutput = True

"""parametry programu"""

workspace = arcpy.env.workspace = r"R:\OIIS_KR5\_PROJEKTY 2019\19004-00_Piekielko\33_ULLK\337_GIS\2_mapy\odc_5\baza_mapy_odc5.gdb"

tabela = 'E_dane_branzowe_dzialki_diss'
etyk_ost = 'dzialki_ewidencyjne_zajecie_czasowe'

kol = []

for field in arcpy.ListFields(tabela):
        kol.append(str(field.name))

#kolumn ETYK# musi byc tyl ile jest maksymalnie przewidzianych robot na jednej dzialce
###with arcpy.da.UpdateCursor(etyk_ost, ['ID_DZ', 'Rodz_ullk','ETYK1','ETYK2','ETYK3','ETYK4','ETYK5','ETYK6','ETYK7','ETYK8','ETYK9','ETYK10','ETYK11','ETYK12'])as cur:
with arcpy.da.UpdateCursor(etyk_ost, ['ID_DZ','ETYK1','ETYK2','ETYK3','ETYK4','ETYK5','ETYK6','ETYK7','ETYK8','ETYK9','ETYK10','ETYK11','ETYK12','ETYK13','ETYK14','ETYK15','ETYK16','ETYK17'])as cur:
    for row in cur:
        ###i=2
        i=1
        with arcpy.da.SearchCursor(tabela, kol)as cur2:
            for row2 in cur2:
                #w miejscu "ID_DZ" musi byc podana kolumna z identyfikatorem dzialki
                ###if row[0] == row2[kol.index('ID_DZ')] and row[1]== row2[kol.index('Rodz_ullk')]:
                if row[0] == row2[kol.index('ID_DZ')]:
                    row[i] = row2[kol.index('roboty')]
                    i+=1
        del cur2
        cur.updateRow(row)
del cur

print 'dodano branze'