import arcpy
import shutil
import os

arcpy.env.overwriteOutput = True

def kr2Am(nmt_kr, nmt_roznicowe, out_folder):
    raster1 = arcpy.Raster(nmt_kr)
    raster2 = arcpy.Raster(nmt_roznicowe)

    expression = "R1 + R2"
    outraster = arcpy.ia.RasterCalculator([raster1, raster2], ["R1","R2"], expression, "FirstOf", 'FirstOf')

    output_raster_path = os.path.join(out_folder, os.path.basename(nmt_kr)[:-4] + '.tif')
    outraster.save(output_raster_path)
    return

def roznicaNmt(skorowidz, out_folder):

    i = 0
    with arcpy.da.SearchCursor(skorowidz, ['GODLO', 'SCIEZKA', 'SCIEZKA_AR'])as cur:
        for row in cur:
            i += 1
            try:
                raster1 = arcpy.Raster(row[1])
                raster2 = arcpy.Raster(row[2])

                expression = "R1 - R2"
                outraster = arcpy.ia.RasterCalculator([raster1, raster2], ["R1","R2"], expression, "FirstOf", 'FirstOf')

                output_raster_path = os.path.join(out_folder, row[0] + '.tif')
                outraster.save(output_raster_path)
                print("{} - Odjęto arkusze {} i {}".format(i, row[1], row[2]))

            except Exception as ex:
                print(ex.args[0])
                continue
    return

def checkNMT(skorowidz, nmt_roznicowe, out_folder):
    '''
    Funkcja do przetwarzania arkuszy NMT w układzie Krondsztad 86 na układ wysokościowy Amsterdam
    '''
    i = 0
    dsc = arcpy.Describe(skorowidz)
    coord_sys = dsc.spatialReference
    with arcpy.da.SearchCursor(skorowidz, ['GODLO', 'UKL_WYS', 'SCIEZKA', 'UKL_WSP'])as cur:
        for row in cur:
            if row[2] is not None:
                i += 1
                if row[1] == 'PL-KRON86-NH':
                    kr2Am(row[2],nmt_roznicowe, out_folder)
                    print("{} - Przeliczono arkusz {} na Amsterdam".format(i, row[0]))

                if row[1] == 'PL-EVRF2007-NH':
                    shutil.copy2(row[2], out_folder)
                    print("{} - Przekopiowano arkusz {}".format(i, row[0]))

    return

def batchDefineProjection(skorowidz):
    '''
    Ta funkcja nie jest dopracowana. Nadaje wszystkim rastrom układ skorowidza
    '''
    i = 0
    dsc = arcpy.Describe(skorowidz)
    coord_sys = dsc.spatialReference

    with arcpy.da.SearchCursor(skorowidz, ['GODLO', 'UKL_WYS', 'SCIEZKA', 'UKL_WSP'])as cur:
        for row in cur:
            # if row[1] == 'PL-EVRF2007-NH':
                i += 1
                try:
                    arcpy.DefineProjection_management(row[2], coord_sys)
                    print(arcpy.GetMessages(0))

                except arcpy.ExecuteError:
                    print(arcpy.GetMessages(2))
                    continue
                except Exception as ex:
                    print(ex.args[0])
                    continue

if __name__ == '__main__':
    skorowidz = r"C:\robo\Przeglad_LOKAL_ROBO\Analiza_szkod_gorniczych\Analiza_szkod_gorniczych.gdb\Skorowidz_NMT_nowe_LUTY_1992a"
    out_folder = r'C:\robo\Przeglad_LOKAL_ROBO\Analiza_szkod_gorniczych\Roznice_NMT\Roznice_luty\1992_v2'
    nmt_roznicowe = r'C:\robo\Przeglad_LOKAL_ROBO\Analiza_szkod_gorniczych\Moder_roznic_wys_evrf2007_kr86.gdb\model_roz_evrf2007_kr86_BUF'

    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.AddMessage("Checking out Spatial")
        arcpy.CheckOutExtension("Spatial")
    else:
        raise arcpy.ExecuteError("Spatial Analyst extension is not available.")

    # checkNMT(skorowidz,nmt_roznicowe, out_folder)
    # batchDefineProjection(skorowidz)
    roznicaNmt(skorowidz,out_folder)