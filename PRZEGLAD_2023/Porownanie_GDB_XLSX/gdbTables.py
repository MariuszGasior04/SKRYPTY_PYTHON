import dataclasses
import arcpy
import os
from datetime import datetime

class ControlStructure:
    def __init__(self):
        self.report = []

    def reportFeatureStructureCorrectness(self, feature):
        '''
        Funkcja odczytuje parametry warstwy przestrzennej 'feature' nastepnie porównuje je z parametrami w schemacie.
        Efekt porównania zapisuje w formie raportu w pliku tekstowym .txt w folderze w którym znajduje się geobaza
        '''
        describe = arcpy.Describe(feature)
        errFields = False
        errDomains = False
        gdb = os.path.basename(os.path.dirname(feature))
        layer = os.path.basename(feature)
        self.report.append("{} - Kontrola zgodności warstwy --{}-- ze shematem bazodanowym".format(datetime.now(), os.path.join(gdb, layer)))
        if describe.baseName == self.baseName:
            self.report.append("OK - NAZWA WARSTWY - {}".format(describe.baseName))
        else:
            self.report.append("!! BŁĄD - NAZWA WARSTWY NIEZGODNA ZE SCHEMATEM. JEST --{}--, A POWINNO BYĆ --{}--".format(describe.baseName, self.baseName))

        if describe.shapeType == self.shapeType:
            self.report.append("OK - TYP GEOMETRII - {}".format(describe.shapeType))
        else:
            self.report.append("!! BŁĄD - TYP GEOMERII NIEZGODNY ZE SCHEMATEM. JEST --{}--, A POWINNO BYĆ --{}--".format(describe.shapeType, self.shapeType))

        if describe.dataType == self.dataType:
            self.report.append("OK - TYP DANYCH - {}".format(describe.dataType))
        else:
            self.report.append("!! BŁĄD - TYP DANYCH NIEZGODNY ZE SCHEMATEM. JEST --{}--, A POWINNO BYĆ --{}--".format(describe.dataType, self.dataType))

        if describe.spatialReference.name == self.spatialRefName:
            self.report.append("OK - ODNIESIENIE PRZESTRZENNE - {}".format(describe.spatialReference.name))
        else:
            self.report.append(
                "!! BŁĄD - ODNIESIENIE PRZESTRZENNE NIEZGODNE Z WYTYCZNYMI. JEST --{}--, A POWINNO BYĆ --{}--".format(
                    describe.spatialReference.name, self.spatialRefName))

        structure = [(field.name, field.aliasName, field.type, field.scale, field.precision, field.length, field.domain) for field in describe.fields]
        fields = [fields[:-1] for fields in structure]
        for field in fields:
            if field not in self.fields:
                errFields = True
                self.report.append("     - W STRUKTURZE ATRYBUTOWEJ POLE --{}-- NIEZGODNE ZE SCHEMATEM".format(field))

        for field in self.fields:
            if field not in fields:
                errFields = True
                self.report.append("     - W STRUKTURZE ATRYBUTOWEJ BRAKUJE POLA --{}--".format(field))

        if errFields:
            self.report.insert(5, "!! BŁĄD - STRUKTURA ATRYBUTOWA WARSTWY KONTROLOWANEJ --(NAZWA_POLA, ALIAS_NAZYW_POLA, TYP_DANYCH, SKALA, PRECYZJA, DŁUGOŚĆ)-- - NIEPOPRAWNA")
        else:
            self.report.append("OK - STRUKTURA ATRYBUTOWA WARSTWY KONTROLOWANEJ - POPRAWNA")

        didx= len(self.report)
        domains = [(domain[0], domain[6]) for domain in structure if domain[6] != '']
        for domain in domains:
            if domain not in self.domains:
                errDomains = True
                self.report.append("     - PODPIĘCIE SŁOWNIKA --{}-- W POLU --{}-- NADPROGRAMOWE LUB JEST NIEPOPRAWNE ".format(domain[1],domain[0]))

        for domain in self.domains:
            if domain not in domains:
                errDomains = True
                self.report.append("     - PODPIECIE SŁOWNIKA --{}-- W POLU --{}-- NIE WYSTĘPUJE LUB JEST NIEPOPRAWNE".format(domain[1],domain[0]))

        if errDomains:
            self.report.insert(didx, "!! BŁĄD - PODPIĘCIE SŁOWNIKÓW - NIEPOPRAWNE")
        else:
            self.report.append("OK - PODPIĘCIE SŁOWNIKów - POPRAWNE")

        report_dir = os.path.dirname(os.path.dirname(feature))
        report_name = "Raport z kontroli warstwy - "  + layer + '.txt'
        with open(os.path.join(report_dir,report_name), 'w') as f:
            f.write('\n'.join(self.report))

    def reportGdbStructureCorrectness(self, gdb):

        return

    def reportDomainStructureCorrectness(self, gdb):

        return

@dataclasses.dataclass
class SkorowidzNMT(ControlStructure):
    report = []
    baseName = 'Skorowidz_NMT'
    shapeType = 'Polygon'
    dataType = 'FeatureClass'
    spatialRefName = 'ETRS_1989_Poland_CS92'
    # struktura tabeli zapisana jako lista tupli o wartościach (nazwa, alias, typ danych, skala, precyzja, długość, domena)
    structure = [('OBJECTID', 'OBJECTID', 'OID', 0, 0, 4, ''),
                        ('Shape', 'Shape', 'Geometry',  0, 0, 0, ''),
                        ('godlo', 'godlo', 'String', 0, 0, 254, ''),
                        ('akt_rok', 'akt_rok', 'Integer', 0, 0, 4, ''),
                        ('akt_data', 'akt_data', 'String', 0, 0, 254, ''),
                        ('format', 'format', 'String', 0, 0, 254, 's_format'),
                        ('char_przes', 'char_przes', 'String', 0, 0, 254, ''),
                        ('blad_sr_wy', 'blad_sr_wy', 'Double', 0, 0, 8, ''),
                        ('uklad_h', 'uklad_h', 'String', 0, 0, 254, 's_uklad_h'),
                        ('url_do_pob', 'url_do_pob', 'String', 0, 0, 254, ''),
                        ('zrodlo_dan', 'zrodlo_dan', 'String', 0, 0, 254, 's_zrd_dan'),
                        ('Shape_Length', 'Shape_Length', 'Double', 0, 0, 8, ''),
                        ('Shape_Area', 'Shape_Area', 'Double', 0, 0, 8, '')]
    fields = [(fields[:-1]) for fields in structure]
    domains = [(domain[0],  domain[6]) for domain in structure if domain[6] != '']

    def reportFeatureStructureCorrectness(self, feature):
        ControlStructure.reportFeatureStructureCorrectness(self, feature)

@dataclasses.dataclass
class DomainFormat():
    report = []
    name = 's_format'
    type = 'Text'
    domainType = 'CodedValue'
    codedValues = {'ARC/INFO ASCII GRID': 'ARC/INFO ASCII GRID',
                   'ASCII XYZ GRID': 'ASCII XYZ GRID'}
    range = None

@dataclasses.dataclass
class DomainZrodloDanych():
    report = []
    name = 's_zrd_dan'
    type = 'Text'
    domainType = 'CodedValue'
    codedValues = {'Skaning laserowy': 'Skaning laserowy',
                   'Zdj. lotnicze': 'Zdj. lotnicze'}
    range = None

@dataclasses.dataclass
class DomainUkladH():
    report = []
    name = 's_uklad_h'
    type = 'Text'
    domainType = 'CodedValue'
    codedValues = {'TAK': 'TAK',
                   'NIE': 'NIE'}
    range = None



@dataclasses.dataclass
class GdbSkorowidze(ControlStructure):
    report = []
    featureClasses = [SkorowidzNMT.baseName]
    domains = [DomainUkladH(), DomainFormat(), DomainZrodloDanych()]

    def reportGdbStructureCorrectness(self, gdb):
        return

    def reportDomainStructureCorrectness(self, gdb):
        return