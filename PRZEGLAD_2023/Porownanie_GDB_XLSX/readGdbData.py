import os.path

import arcpy
import pandas as pd
from gdbTables import SkorowidzNMT

def getFeatureProperies(feature):
    fp = {}
    describe = arcpy.Describe(feature)
    fp['featureName'] = describe.baseName
    # fp['featureType'] = describe.featureType
    fp['shapeType'] = describe.shapeType
    fp['dataType'] = describe.dataType
    fp['spatialRef'] = describe.spatialReference.name
    fp['fields'] = [(field.name, field.aliasName, field.type, field.scale, field.precision, field.length, field.domain) for field in describe.fields]
    # print(fp)
    return fp

def getDomainProperies(gdb):
    dpList = []
    dp = {}
    domains = arcpy.da.ListDomains(gdb)
    for domain in domains:
        dp['name'] = domain.name
        dp['type'] = domain.type
        dp['domainType'] = domain.domainType
        if domain.domainType == "CodedValue":
            dp['codedValues'] = domain.codedValues
            dp['range'] = None
        elif domain.domainType == "Range":
            dp['codedValues'] = None
            dp['range'] = domain.range
        dpCopy = dp.copy()
        dpList.append(dpCopy)
    return dpList

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
    feature = r'P:\02_Pracownicy\Mariusz\Przeglad_2023\02_Baza_produkty\01_Analiza_danych_do_opracowania_produktow\3M_1_09_Skorowidze_NMT\02_Analizy\Skorowidze_NMT_GUGIK_agregacja_selekcja.gdb\skorowidz_NMT_data'
    xlsx = r'P:\02_Pracownicy\Mariusz\Przeglad_2023\02_Baza_produkty\00_Schematy\3M_1_10_Skorowidze_przekroje_rzeki\0_Dane\aMZPiMRP 1.3.14.40 DII Zal 6.1-6.4 Zakres MZP i MRP 20220729 v1.02.xlsx'
    # print(getFeatureProperies(feature))
    print(getDomainProperies(os.path.dirname(feature)))
    # skorowidz = SkorowidzNMT()
    # skorowidz.reportFeatureStructureCorrectness(feature)

    # xlsx2df(xlsx)