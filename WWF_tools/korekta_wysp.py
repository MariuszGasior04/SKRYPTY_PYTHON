import arcpy
import os

arcpy.env.overwriteOutput = True
def reclass2polig(in_raster, output_draft_gdb, output_gdb):
    '''Funkca reklasyfikujaca wartości rastra z Float na Long i przetworzenie go do postaci wektorowej'''

    output_draft_name = os.path.basename(in_raster).split('.')[0]
    raster = arcpy.sa.Raster(in_raster)

    min_pixel_value = arcpy.GetRasterProperties_management(raster, "MINIMUM")
    max_pixel_value = arcpy.GetRasterProperties_management(raster, "MAXIMUM")
    myRemapRange = arcpy.sa.RemapRange([[min_pixel_value, max_pixel_value, 1]])

    arcpy.AddMessage('RASTER. NKO - {}'.format(output_draft_name))
    outReclass = arcpy.sa.Reclassify(raster, "Value", myRemapRange, "NODATA")
    arcpy.AddMessage('INFO. 1 - Poszerzanie rastra {}'.format(output_draft_name))
    outExpand = arcpy.sa.Expand(outReclass, 10, [1, 1, 1],'DISTANCE')
    arcpy.AddMessage('INFO. 2 - Konwertowanie rastra {} na poligon'.format(output_draft_name))
    ras2polig =os.path.join(output_draft_gdb, output_draft_name + '_polig')
    arcpy.conversion.RasterToPolygon(outExpand, ras2polig, "NO_SIMPLIFY", "VALUE")
    arcpy.AddMessage('INFO. 3 - Wypelnianie dziur w poligonie poligon')
    poligElim = os.path.join(output_draft_gdb, output_draft_name + '_poligElim')
    arcpy.EliminatePolygonPart_management(ras2polig, poligElim, "AREA", 10000000000)
    arcpy.AddMessage('INFO. 4 - Upraszczanie geometrii poligonu')
    poligSimp = os.path.join(output_draft_gdb, output_draft_name + '_poligSim')
    arcpy.SimplifyPolygon_cartography(poligElim, poligSimp, "EFFECTIVE_AREA", 10, 400, "RESOLVE_ERRORS", "KEEP_COLLAPSED_POINTS")
    arcpy.AddMessage('INFO. 5 - Konwertowanie uproszczonego poligonu na raster')
    poligRas = os.path.join(output_draft_gdb, output_draft_name + '_poligRas')
    arcpy.conversion.PolygonToRaster(poligSimp, 'gridcode', poligRas, 'CELL_CENTER', 'NONE', 1)
    arcpy.AddMessage('INFO. 6 - Zawezenie uproszczonego rastra')
    ras2polig2 =os.path.join(output_gdb, output_draft_name + '_polig_FINAL')
    outShrink = arcpy.sa.Shrink(poligRas, 10, [1, 1, 1], 'DISTANCE')
    arcpy.AddMessage('INFO. 7 - Zapis przetworzonego rastra {}'.format(output_draft_name))
    arcpy.conversion.RasterToPolygon(outShrink, ras2polig2, "NO_SIMPLIFY", "VALUE")
    arcpy.AddField_management(in_table=ras2polig2, field_name='NKO_RZEKI', field_type='TEXT', field_length=50,)
    expression = "'"+output_draft_name+"'"
    arcpy.CalculateField_management(ras2polig2, 'NKO_RZEKI', expression, 'PYTHON3')
    # outReclass.save(os.path.join(output_gdb,output_draft_name))


if __name__ == '__main__':
    # input
    raster = r"E:\Waloryzajca_rzek_WWF\ROBOCZY_KWIECIEN_2024\Zad9_korekta_zarysow_wysp_LIDAR_odcinki\DANE_AERO_ROSLINNOSC_ZACIENIENIE\roslinnosc\Wisla\_2_320000.asc"
    raster_dir = r"E:\Waloryzajca_rzek_WWF\ROBOCZY_KWIECIEN_2024\Zad9_korekta_zarysow_wysp_LIDAR_odcinki\DANE_AERO_ROSLINNOSC_ZACIENIENIE\roslinnosc\Bug"
    worspace = r"E:\Waloryzajca_rzek_WWF\ROBOCZY_KWIECIEN_2024\Zad9_korekta_zarysow_wysp_LIDAR_odcinki\Korekta_wysp_robo.gdb"
    gdb_final = r"E:\Waloryzajca_rzek_WWF\ROBOCZY_KWIECIEN_2024\Zad9_korekta_zarysow_wysp_LIDAR_odcinki\Poligony_korekty_koryta.gdb"
    #output

    # reclass2polig(raster,worspace,gdb_final)

    for root, dirs, files in os.walk(raster_dir, topdown=False):
        #iteracja po plikach
        #print(u"Przeszukuję folder:"+"\n"+root)
        for name in files:
            #znajdywanie plikow zawierających okreslone rozszerzenie
            if name.endswith('asc'):
                # print(os.path.join(root, name) +'#'+name)
                raster = os.path.join(root, name)
                try:
                    reclass2polig(raster, worspace, gdb_final)
                except:
                    continue