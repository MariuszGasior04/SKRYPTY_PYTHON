#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do porównania różnic między dwiema wersjami tej samej geobazy

import arcpy
import os

arcpy.env.overwriteOutput = True


dict = {}



def getArkusze(warstwa_arkuszy):
    fields = []
    for field in arcpy.ListFields(warstwa_arkuszy):
        fields.append(str(field.name))

    dictArkusze = {}
    with arcpy.da.SearchCursor(warstwa_arkuszy, fields) as search:
        for row in search:
                dictArkusze[str(row[fields.index('Godlo')])] = [
                    (row[fields.index('Lewy_g_y_')]),
                    (row[fields.index('Lewy_g_x_')]),
                    (row[fields.index('Prawy_g_y')]),
                    (row[fields.index('Prawy_g_x')]),
                    (row[fields.index('Prawy_d_y')]),
                    (row[fields.index('Prawy_d_x')]),
                    (row[fields.index('Lewy_d_y_')]),
                    (row[fields.index('Lewy_d_x_')]),
                    (row[fields.index('AKT_ORTO')]),
                    (row[fields.index('WARIANT')]),
                    (row[fields.index('WOJ1')]),
                    (row[fields.index('WOJ2')]),
                    (row[fields.index('WOJ3')]),
                    (row[fields.index('NR_ZZ1_1')]),
                    (row[fields.index('ZZ1_1')]),
                    (row[fields.index('NR_ZZ1_2')]),
                    (row[fields.index('ZZ1_2')]),
                    (row[fields.index('NR_ZZ1_3')]),
                    (row[fields.index('ZZ1_3')]),
                    (row[fields.index('NR_ZZ1_4')]),
                    (row[fields.index('ZZ1_4')]),
                    (row[fields.index('NR_ZZ1_5')]),
                    (row[fields.index('ZZ1_5')]),
                    (row[fields.index('NR_ZZ2_1')]),
                    (row[fields.index('ZZ2_1')]),
                    (row[fields.index('NR_ZZ2_2')]),
                    (row[fields.index('ZZ2_2')]),
                    (row[fields.index('RZGW1_NAZ')]),
                    (row[fields.index('RZGW2_NAZ')])
                ]
    del search

    return dictArkusze

def mxdTextSwap(folder_mxd, folder_output, arkusze, zbiornik):

    dict = getArkusze(arkusze)

    wydrukowane_lista=[]

    for mapa in os.listdir(folder_output):
        wydrukowane_lista.append(os.path.splitext(mapa)[0])

    wydruki = set(wydrukowane_lista)

    for plik in os.listdir(folder_mxd):
        if zbiornik == os.path.splitext(plik)[0].split('_')[-2]:
            if (os.path.isfile(os.path.join(folder_mxd, plik)) and os.path.splitext(plik)[1] == '.mxd') and os.path.splitext(plik)[0] not in wydruki:

                mxd = arcpy.mapping.MapDocument(os.path.join(folder_mxd, plik))

                elements = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")
                print str(mxd.dataDrivenPages.currentPageID) +' - '+ plik
                godlo = mxd.dataDrivenPages.pageRow.Godlo
                # print len(elements)
                # print elements

                for elm in elements:
                    if len(elm.text) > 3:
                        if 'Lewy_g_y_' in elm.text:
                            elm.text = dict[str(godlo)][0]
                        if 'Lewy_g_x_' in elm.text:
                            elm.text = dict[str(godlo)][1]
                        if 'Prawy_g_y' in elm.text:
                            elm.text = dict[str(godlo)][2]
                        if 'Prawy_g_x' in elm.text:
                            elm.text = dict[str(godlo)][3]
                        if 'Prawy_d_y' in elm.text:
                            elm.text = dict[str(godlo)][4]
                        if 'Prawy_d_x' in elm.text:
                            elm.text = dict[str(godlo)][5]
                        if 'Lewy_d_y_' in elm.text:
                            elm.text = dict[str(godlo)][6]
                        if 'Lewy_d_x_' in elm.text:
                            elm.text = dict[str(godlo)][7]
                        if 'AKT_ORTO' in elm.text:
                            elm.text = u'Aktualność podkładu topograficznego: '+ unicode(dict[str(godlo)][8]) +u' r.'
                        if 'WARIANT' in elm.text:
                            elm.text = dict[str(godlo)][9]
                        if 'WOJ1' in elm.text:
                            elm.text = u'<FNT name="Arial" size="6"> PODZIAŁ ADMINISTRACYJNY </FNT>' + '\n' + dict[str(godlo)][10] + ' ' +  dict[str(godlo)][11] + ' ' + dict[str(godlo)][12]

                        opis = u"OBSZAR DZIAŁANIA JEDNOSTEK ORGANIZACYJNYCH"+'\n'+u"PAŃSTWOWEGO GOSPODARSTWA WODNEGO WODY POLSKIE"

                        if (dict[str(godlo)][13] > 0):
                            opis = opis +"\n"+ dict[str(godlo)][27]
                        if (dict[str(godlo)][13] > 0):
                            opis = opis +"\n"+"    "+  dict[str(godlo)][14]
                        if (dict[str(godlo)][15] > 0):
                            opis = opis +"\n"+"    "+  dict[str(godlo)][16]
                        if (dict[str(godlo)][17] > 0):
                            opis = opis +"\n"+"    "+  dict[str(godlo)][18]
                        if (dict[str(godlo)][19] > 0):
                            opis = opis +"\n"+"    "+  dict[str(godlo)][20]
                        if (dict[str(godlo)][21] > 0):
                            opis = opis +"\n"+"    "+  dict[str(godlo)][22]
                        if (dict[str(godlo)][23] > 0):
                            opis = opis +"\n"+ dict[str(godlo)][28]
                        if (dict[str(godlo)][23] > 0):
                            opis = opis +"\n"+"    "+  dict[str(godlo)][24]
                        if (dict[str(godlo)][25] > 0):
                            opis = opis +"\n"+"    "+  dict[str(godlo)][26]

                        if 'expression' in elm.text:
                            elm.text = opis

                mxd.saveACopy(os.path.join(folder_output, plik))

                del mxd

    return

if __name__ == '__main__':

    folder_input = \
        ur'R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\5_Opracowanie_kartograficzne\PROJEKCJE ETAP3-SZABLONY\MRP_gotowe'
    folder_output = \
        ur'R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\5_Opracowanie_kartograficzne\BAZA_Mapy\PROJEKCJE_ETAP3\MRP\PDF'
    arkusze = r'R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\5_Opracowanie_kartograficzne\BAZA_Mapy\ETAP3\DEBE.gdb\arkusze_Dębe'
    zbiornik = u'Dębe'

    mxdTextSwap(folder_input, folder_output, arkusze, zbiornik)
