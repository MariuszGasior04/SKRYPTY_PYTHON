import arcpy
import os
from pathlib import Path

arcpy.env.overwriteOutput = True


def batchExtractByMask2(mask, out_folder):
    temp_mask = r'memory\mask'
    arcpy.MakeFeatureLayer_management(mask, temp_mask)

    with arcpy.da.UpdateCursor(mask, ['ID_ODC_RZ', 'STATUS', 'SCIEZKA']) as cur:
        for row in cur:
            if row[1] != 'EXTRACTED':
                try:
                    inRaster = arcpy.Raster(row[2])
                    nazwa = row[0]
                    # arcpy.Select_analysis(temp_mask,os.path.join(output_geodatabase, row[0]))
                    arcpy.AddMessage('INFO. Wycinanie rastra {}'.format(row[2]))

                    wc = 'ID_ODC_RZ' +' = '+ "'"+row[0]+"'"
                    arcpy.SelectLayerByAttribute_management(temp_mask, where_clause=wc)
                    arcpy.env.extent = 'MINOF'
                    outExtractByMask = arcpy.sa.ExtractByMask(inRaster, temp_mask)

                    out_dir = os.path.join(out_folder, nazwa + '.tif')
                    # Jeśli istnieje już plik o tej samej nazwie w docelowej lokalizacji
                    if os.path.exists(out_dir):
                        index = 1
                        while True:
                            # Modyfikuj nazwę pliku, dodając indeks przed rozszerzeniem
                            nowa_nazwa = f"{nazwa}__{index}.tif"
                            out_dir = os.path.join(out_folder, nowa_nazwa)
                            # Jeśli zmodyfikowana nazwa pliku nie istnieje w docelowej lokalizacji, przerwij pętlę
                            if not os.path.exists(out_dir):
                                break
                            index += 1

                    outExtractByMask.save(out_dir)
                    arcpy.AddMessage('INFO. Wyekstraktowano raster dla odcinka {}'.format(row[0]))
                    row[1] = 'EXTRACTED'
                    cur.updateRow(row)
                except arcpy.ExecuteError:
                    print(arcpy.GetMessages(2))
                    continue
                except Exception as ex:
                    print(ex.args[0])
                    continue

    return

def batchExtractByMask(mask, out_folder):
    temp_mask = r'memory\mask'
    arcpy.MakeFeatureLayer_management(mask,temp_mask)

    with arcpy.da.UpdateCursor(mask, ['ID_ODC_RZ', 'STATUS','SCIEZKA', 'GODLO'])as cur:
        for row in cur:
            if row[1] != 'EXTRACTED':
                try:
                    inRaster = arcpy.Raster(row[2])
                    nazwa = row[0]
                    # arcpy.Select_analysis(temp_mask,os.path.join(output_geodatabase, row[0]))
                    arcpy.AddMessage('INFO. Wycinanie rastra {}'.format(row[2]))

                    outExtractByMask = arcpy.sa.ExtractByMask(inRaster, mask)

                    out_dir = os.path.join(out_folder, nazwa+'.tif')
                    # Jeśli istnieje już plik o tej samej nazwie w docelowej lokalizacji
                    if os.path.exists(out_dir):
                        index = 1
                        while True:
                            # Modyfikuj nazwę pliku, dodając indeks przed rozszerzeniem
                            nowa_nazwa = f"{nazwa}__{index}.tif"
                            out_dir = os.path.join(out_folder, nowa_nazwa)
                            # Jeśli zmodyfikowana nazwa pliku nie istnieje w docelowej lokalizacji, przerwij pętlę
                            if not os.path.exists(out_dir):
                                break
                            index += 1

                    outExtractByMask.save(out_dir)
                    arcpy.AddMessage('INFO. Wyekstraktowano {} dla godla {}'.format(row[0], row[3]))
                    row[1] = 'EXTRACTED'
                    cur.updateRow(row)
                except arcpy.ExecuteError:
                    print(arcpy.GetMessages(2))
                    continue
                except Exception as ex:
                    print(ex.args[0])
                    continue

    return

def extractByMaskTAB(mask, out_folder):
    with arcpy.da.UpdateCursor(mask, ['ID_ODC_RZ', 'STATUS','SCIEZKA_SHP', 'SCIEZKA_RASTER'])as cur:
        for row in cur:
            if row[1] != 'EXTRACTED':
                try:
                    inRaster = arcpy.Raster(row[3])
                    nazwa = row[0]
                    # arcpy.Select_analysis(temp_mask,os.path.join(output_geodatabase, row[0]))
                    arcpy.AddMessage('INFO. Wycinanie rastra {}'.format(row[2]))
                    arcpy.env.extent = row[2]
                    outExtractByMask = arcpy.sa.ExtractByMask(inRaster, row[2])

                    out_dir = os.path.join(out_folder, nazwa+'.tif')
                    # Jeśli istnieje już plik o tej samej nazwie w docelowej lokalizacji
                    if os.path.exists(out_dir):
                        index = 1
                        while True:
                            # Modyfikuj nazwę pliku, dodając indeks przed rozszerzeniem
                            nowa_nazwa = f"{nazwa}__{index}.tif"
                            out_dir = os.path.join(out_folder, nowa_nazwa)
                            # Jeśli zmodyfikowana nazwa pliku nie istnieje w docelowej lokalizacji, przerwij pętlę
                            if not os.path.exists(out_dir):
                                break
                            index += 1

                    outExtractByMask.save(out_dir)
                    arcpy.AddMessage('INFO. Wyekstraktowano raster {} dla odcinka {}'.format(row[3], row[0]))
                    row[1] = 'EXTRACTED'
                    cur.updateRow(row)
                except arcpy.ExecuteError:
                    print(arcpy.GetMessages(2))
                    continue
                except Exception as ex:
                    print(ex.args[0])
                    continue

    return

def batchMosaicToNewRaster(in_folder, out_folder):
    rastry={}
    for root, dirs, files in os.walk(in_folder, topdown=False):
        #iteracja po plikach
        #print(u"Przeszukuję folder:"+"\n"+root)
        for name in files:
            #znajdywanie plikow zawierających okreslone rozszerzenie
            if name.endswith('.tif'):
                file = os.path.join(root, name)
                corename = Path(file).stem
                odc = corename.split('__')[0]
                if odc in rastry:
                    rastry[odc].append(file)
                else:
                    rastry[odc]=[file]
    print(rastry)
    wkt= '''
    PROJCS["ETRS_1989_Poland_CS92",GEOGCS["GCS_ETRS_1989",DATUM["D_ETRS_1989",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",-5300000.0],PARAMETER["Central_Meridian",19.0],PARAMETER["Scale_Factor",0.9993],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]
    '''
    sr = arcpy.SpatialReference(text=wkt)
    for odc in rastry.keys():
        try:
            arcpy.env.extent = 'MINOF'
            arcpy.MosaicToNewRaster_management(rastry[odc], out_folder, odc+'.tif',
                                           sr, pixel_type = "32_BIT_FLOAT", cellsize = 1, number_of_bands = 1, mosaic_method = "LAST", mosaic_colormap_mode = "FIRST")
            arcpy.AddMessage('INFO. Zmoizaikowano raster odcinka {} '.format(odc))

        except arcpy.ExecuteError:
            print(arcpy.GetMessages(2))

        except Exception as ex:
            print(ex.args[0])
    return

if __name__ == '__main__':
    mask = r'C:\robo\Przeglad_LOKAL_ROBO\Analiza_szkod_gorniczych\Analiza_szkod_gorniczych.gdb\MASKA_AKTUALIZACJA_4'
    maskTab = r'C:\robo\Przeglad_LOKAL_ROBO\Analiza_szkod_gorniczych\Analiza_szkod_gorniczych.gdb\MASKA_ODCINKOW'
    # raster = r'C:\robo\Przeglad_LOKAL_ROBO\Analiza_szkod_gorniczych\Rastry.gdb\ROZNICOWE_1992'
    outputg = r'C:\robo\Przeglad_LOKAL_ROBO\Analiza_szkod_gorniczych\Roznice_NMT\Rastry_roznicowe_wycinanie\extr_mask'
    produkt = r'C:\robo\Przeglad_LOKAL_ROBO\Analiza_szkod_gorniczych\Roznice_NMT\Rastry_roznicowe_wycinanie\P2'
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.AddMessage("Checking out Spatial")
        arcpy.CheckOutExtension("Spatial")
    else:
        raise arcpy.ExecuteError("Spatial Analyst extension is not available.")

    # batchExtractByMask(mask,outputg)
    # batchExtractByMask2(mask, outputg)
    # batchMosaicToNewRaster(outputg,produkt)
    extractByMaskTAB(maskTab, produkt)
