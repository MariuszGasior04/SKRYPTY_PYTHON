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

    dictArkusze ={}
    with arcpy.da.SearchCursor(warstwa_arkuszy, fields) as search:
        for row in search:
                dictArkusze[str(row[fields.index('NUMER')])] = [
                    (row[fields.index('Lewy_g_y_')]),
                    (row[fields.index('Lewy_g_x_')]),
                    (row[fields.index('Prawy_g_y')]),
                    (row[fields.index('Prawy_g_x')]),
                    (row[fields.index('Prawy_d_y')]),
                    (row[fields.index('Prawy_d_x')]),
                    (row[fields.index('Lewy_d_y_')]),
                    (row[fields.index('Lewy_d_x_')]),
                    (row[fields.index('WARIANT_')]),
                    (row[fields.index('WOJ1')]),
                    (row[fields.index('WOJ2')]),
                    (row[fields.index('ZZ1_1')]),
                    (row[fields.index('ZZ1_2')]),
                    (row[fields.index('ZZ2_1')]),
                    (row[fields.index('ZZ2_2')]),
                    (row[fields.index('RZGW1_NAZ')]),
                    (row[fields.index('RZGW2_NAZ')])
                ]
    del search
    print 'utworzono slownik z arkuszy'
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
                godlo = mxd.dataDrivenPages.pageRow.NUMER
                # print len(elements)
                # print elements

                for elm in elements:
                    if len(elm.text) > 3:
                        print elm.text
                        if 'Lewy_g_y_' in elm.text:
                            elm.text=dict[str(godlo)][0]
                        if 'Lewy_g_x_' in elm.text:
                            elm.text=dict[str(godlo)][1]
                        if 'prawy_g_y' in elm.text:
                            elm.text=dict[str(godlo)][2]
                        if 'prawy_g_x' in elm.text:
                            elm.text=dict[str(godlo)][3]
                        if 'prawy_d_y' in elm.text:
                            elm.text=dict[str(godlo)][4]
                        if 'prawy_d_x' in elm.text:
                            elm.text=dict[str(godlo)][5]
                        if 'Lewy_d_y_' in elm.text:
                            elm.text=dict[str(godlo)][6]
                        if 'Lewy_d_x_' in elm.text:
                            elm.text=dict[str(godlo)][7]
                        if 'WARIANT_' in elm.text:
                            elm.text=dict[str(godlo)][8]
                        if 'WOJ1' in elm.text:
                            elm.text=u'<FNT name="Arial" size="6"> PODZIAŁ ADMINISTRACYJNY </FNT>' + '\n' + \
                                     dict[str(godlo)][9] + ' ' + dict[str(godlo)][10]

                        opis=u"OBSZAR DZIAŁANIA JEDNOSTEK ORGANIZACYJNYCH" + '\n' + u"PAŃSTWOWEGO GOSPODARSTWA WODNEGO WODY POLSKIE"

                        if (dict[str(godlo)][15] != ''):
                            opis = (opis + "\n" + dict[str(godlo)][15]).strip()
                            if (dict[str(godlo)][11] != ''):
                                opis = (opis + "\n" + "    " + dict[str(godlo)][11]).strip()
                            if (dict[str(godlo)][12] != ''):
                                opis = (opis + "\n" + "    " + dict[str(godlo)][12]).strip()
                        if (dict[str(godlo)][16] != ''):
                            opis = (opis + "\n" + dict[str(godlo)][16]).strip()
                            if (dict[str(godlo)][13] != ''):
                                opis = (opis + "\n" + "    " + dict[str(godlo)][13]).strip()
                            if (dict[str(godlo)][14] != ''):
                                opis = (opis + "\n" + "    " + dict[str(godlo)][14]).strip()

                        if 'expression' in elm.text:
                            elm.text = opis.strip()
                            elm.elementPositionX = 50.3997
                            elm.elementPositionY = 18.4

                # mxd.saveACopy(os.path.join(folder_output, plik))

                del mxd

    return

if __name__ == '__main__':

    folder_input = \
        ur'D:\DaneTymczasowe\PROJEKCJE\WISŁA\MZP_pdf'
    folder_output = \
        ur'D:\DaneTymczasowe\PROJEKCJE\WISŁA'
    arkusze = r'D:\DaneTymczasowe\_warstwy_pomocnicze_do_map\arkusze.shp'
    zbiornik = u'Przeczyce'

    mxdTextSwap(folder_input, folder_output, arkusze, zbiornik)
