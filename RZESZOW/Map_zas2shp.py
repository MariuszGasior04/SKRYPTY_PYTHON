#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy

if __name__ == '__main__':
    """parametry programu"""
    dxf_directory = r'C:\robo\ZASADNICZA\mapa zasadnicza_1_500.dxf'
    output_gdb = r'P:\02_Pracownicy\Mariusz\RZESZOW\MAPA_ZASADNICZA\_mRzeszow_robo\robo.gdb'
    arcpy.CADToGeodatabase_conversion(dxf_directory, output_gdb,
                                      'M_rzeszow', 1000)