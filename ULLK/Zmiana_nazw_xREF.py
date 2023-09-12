#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import string

def odkoduj(tekst):
    polskie={"\xc4\x84": "A", "\xc4\x86": "C",
             "\xc4\x98": "E", "\xc5\x81": "L", "\xc5\x83": "N", "\xc3\x93": "O",
             "\xc5\x9a": "S", "\xc5\xb9": "Z", "\xc5\xbb": "Z", "\xc4\x85": "a",
             "\xc4\x87": "c", "\xc4\x99": "e", "\xc5\x82": "l", "\xc5\x84": "n",
             "\xc3\xB3": "o", "\xc5\x9b": "s", "\xc5\xba": "z", "\xc5\xbc": "z",
             "-": "_"}
    for x in tekst:
        if polskie.has_key(x):
            tekst=string.replace(tekst, x, polskie[x])

    return tekst

def renameXREF(dir):
    '''Funkcja do standaryzacji nazw plików xREF (zamiana polskich znaków i znaków specjalnych'''
    for dirpath, dirnames, filenames in os.walk(dir, topdown=False):
        for xref in filenames:
            os.rename(os.path.join(dir, xref), os.path.join(dir, odkoduj(xref)))
    return


if __name__ == '__main__':
    folderxREF = \
        ur'R:\OIIS_KR5\_PROJEKTY 2018\18035-00 LK201\33_ULLK\337_GIS\5_xref_ULLK\xref_odc.1'

    renameXREF(folderxREF)
