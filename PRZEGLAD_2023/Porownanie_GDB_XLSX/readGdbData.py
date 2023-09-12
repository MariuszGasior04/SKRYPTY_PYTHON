#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arcpy
import pandas as pd
import os

def getFeatureProperies(feature):
    fp = {}
    describe = arcpy.Describe(feature)
    fp['featureName'] = describe.baseName
    # fp['featureType'] = describe.featureType
    fp['shapeType'] = describe.shapeType
    fp['dataType'] = describe.dataType
    fp['fields'] = [(field.name, field.aliasName, field.type) for field in describe.fields]
    # print(fp)
    return fp

def xlsx2df(xlsx):
    df = pd.read_excel(xlsx, sheet_name=None, skiprows=4 )
    print(df)
    return df

def table_to_data_frame(in_table, input_fields=None, where_clause=None):
    """Funkcja konwertuje tabele na dataframe w pandas indeksowane, po ObjectID z wybranymi kolumnami uzywając arcpy.da.SearchCursor."""
    OIDFieldName = arcpy.Describe(in_table).OIDFieldName
    if input_fields:
        final_fields = [OIDFieldName] + input_fields
    else:
        final_fields = [field.aliasName for field in arcpy.ListFields(in_table)]
    data = [row for row in arcpy.da.SearchCursor(in_table, final_fields, where_clause=where_clause)]
    fc_dataframe = pd.DataFrame(data, columns=final_fields)
    fc_dataframe = fc_dataframe.set_index(OIDFieldName, drop=True)
    return fc_dataframe




if __name__ == '__main__':
    feature = r'P:\02_Pracownicy\Mariusz\Przeglad_2023\02_Baza_produkty\00_Schematy\3M_1_10_Skorowidze_przekroje_rzeki\3M_1_10_Schemat.gdb\Skorowidz_przekrojow'
    xlsx = r'P:\02_Pracownicy\Mariusz\Przeglad_2023\02_Baza_produkty\00_Schematy\3M_1_10_Skorowidze_przekroje_rzeki\0_Dane\aMZPiMRP 1.3.14.40 DII Zal 6.1-6.4 Zakres MZP i MRP 20220729 v1.02.xlsx'
    # getFeatureProperies(feature)
    xlsx2df(xlsx)