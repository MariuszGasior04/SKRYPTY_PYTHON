import arcpy
import os

# arcpy.env.overwriteOutput = True

def reclassRaster(in_raster, out_folder):
    inRaster = arcpy.Raster(in_raster)
    min_pix = inRaster.minimum
    max_pix = inRaster.maximum
    if min_pix is not None and max_pix is not None:
        arcpy.AddMessage('INFO. Reklasyfikacja rastra {}'.format(in_raster))
        field = "VALUE"
        if min_pix < -1.0:
            remapString1 = str(min_pix) +" -1 1;-0.999 -0.5 2;-0.499 -0.15 3;-0.149"
        if max_pix > 1.0:
            remapString2 = " 0.15 4;0.151 0.5 3;0.501 1 2;1.001 " + str(max_pix) + " 1"
        if min_pix >= -1.0 and min_pix < -0.5:
            remapString1 = str(min_pix) + " -0.5 2;-0.499 -0.15 3;-0.149"
        if min_pix >= -0.5 and min_pix < -0.15:
            remapString1 = str(min_pix) + " -0.15 3;-0.149"
        if min_pix >= -0.15 and min_pix < 0.15:
            remapString1 = str(min_pix)
        if max_pix <= 1.0 and max_pix > 0.5:
            remapString2 = " 0.15 4;0.151 0.5 3;0.501 " + str(max_pix) + " 2"
        if max_pix <= 0.5 and max_pix > 0.15:
            remapString2 = " 0.15 4;0.151 " + str(max_pix) + " 3"
        if max_pix <= 0.15 and max_pix > -0.15:
            remapString2 = " " + str(max_pix) + " 4"
        try:
            remapString = remapString1 + remapString2
        except Exception as ex:
            print(ex.args[0])
            arcpy.AddMessage("min = {}; max = {}".format(min_pix, max_pix))

        outRaster = os.path.join(out_folder, os.path.basename(in_raster))
        try:
            arcpy.Reclassify_3d(inRaster, field, remapString, outRaster, "DATA")
            arcpy.AddMessage('INFO. Zreklasyfikowano {}'.format(in_raster))
        except arcpy.ExecuteError:
            print(arcpy.GetMessages(2))
        except Exception as ex:
            print(ex.args[0])
            arcpy.AddMessage("min = {}; max = {}".format(min_pix, max_pix))
    else:
        arcpy.AddMessage('ERROR. Ekstremalne wartosci rastra okreslone jako NONE. Reklasyfikacja rastra {} nieudana'.format(in_raster))

def raster2poligon(in_raster, out_folder):
    outPolig = os.path.join(out_folder, os.path.basename(in_raster)[:-4].replace(".","_")+'.shp').replace("-","_")
    # print(outPolig)
    field = "VALUE"
    arcpy.AddMessage('INFO. Przetwarzanie rastra {}'.format(in_raster))
    arcpy.RasterToPolygon_conversion(in_raster, outPolig, "NO_SIMPLIFY", field)

    return

def search(in_folder, out_folder, file_ext):
    i = 0
    for root, dirs, files in os.walk(in_folder, topdown=False):
        for name in files:
            if name.endswith(file_ext):
                i+=1
                print(i)
                reclassRaster(os.path.join(root,name), out_folder)

if __name__ == '__main__':
    rastry = r"C:\robo\Przeglad_LOKAL_ROBO\Analiza_szkod_gorniczych\Roznice_NMT\Rastry_roznicowe\uzup2"
    reclasy = r"C:\robo\Przeglad_LOKAL_ROBO\Analiza_szkod_gorniczych\Roznice_NMT\Rastry_reclass\Uzup_2024"
    shpy = r"C:\robo\Przeglad_LOKAL_ROBO\Analiza_szkod_gorniczych\Roznice_NMT\Shpy\Uzup_2024"
    # if arcpy.CheckExtension("Spatial") == "Available":
    #     arcpy.AddMessage("Checking out Spatial")
    #     arcpy.CheckOutExtension("Spatial")
    # else:
    #     raise arcpy.ExecuteError("Spatial Analyst extension is not available.")
    # search(rastry, reclasy, '.tif')
    i = 0
    i = 0
    for root, dirs, files in os.walk(reclasy, topdown=False):
        for name in files:
            if name.endswith('.tif'):
                if name[0:7] == 'M-34-78':
                    i += 1
                    print(i)
                    # print(name[0:8])
                    raster2poligon(os.path.join(root,name), shpy)