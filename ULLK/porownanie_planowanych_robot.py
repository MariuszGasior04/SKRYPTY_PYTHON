#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do porównania różnic między dwiema wersjami tej samej geobazy

import arcpy
import os

arcpy.env.overwriteOutput = True

def compareLayer(tabSource, tabUpdated, tabSourceId, tabUpdatedId, comparedFields, raport):
    '''
    Funkcja porównująca tabele z wykazu działek, ale w innej wersji opracowania
    tabSource - geobaza w wersji pierwotnej
    tabUpdated - geobaza zaktualizowana
    compare_type - typ porównania (ALL —Compare all properties. This is the default. ATTRIBUTES_ONLY —Only compare the attributes and their values. SCHEMA_ONLY —Only compare the schema. Data Type STRING)
    '''
    
    return