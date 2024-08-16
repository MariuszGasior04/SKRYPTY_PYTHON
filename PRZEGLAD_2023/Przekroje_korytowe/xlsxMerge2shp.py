import pandas as pd
import os
import geopandas as gpd
from shapely.geometry import Point

def mergeExcellFiles(in_folder, output_xlsx):
    excl_list = []
    for root, dirs, files in os.walk(in_folder, topdown=False):
        #iteracja po plikach
        #print(u"Przeszukuję folder:"+"\n"+root)
        for file in files:
            #znajdywanie plikow zawierających okreslone rozszerzenie
            if file.endswith('.xls') or file.endswith('.xlsx'):
                file_path = os.path.join(root, file)
                excl_list.append(pd.read_excel(file_path))
    # create a new dataframe to store the
    # merged excel file.
    excl_merged = pd.DataFrame()

    for excl_file in excl_list:
        # appends the data into the excl_merged
        # dataframe.
        excl_merged = excl_merged._append(excl_file, ignore_index=True)

    return excl_merged.to_excel(os.path.join(in_folder, output_xlsx), index=False)

def excell2shp(in_folder, excell_file, kol_X, kol_Y):
    # exports the dataframe into excel file with
    # specified name.
    excell_df = pd.read_excel(os.path.join(in_folder, excell_file))
    geometry = [Point(xy) for xy in zip(excell_df[kol_Y],excell_df[kol_X])]
    gdf = gpd.GeoDataFrame(excell_df, crs= 'EPSG:2180', geometry = geometry)
    gdf.to_file(os.path.join(in_folder, excell_file.replace('.xlsx','.shp')), driver = 'ESRI Shapefile')

if __name__ == '__main__':
    in_folder = r'R:\Dane_PGW_WP_3M\10. Modele hydrauliczne\RW G-ZW\WILGA_21372_2019v1\1.3.14.27 RAPORT\WILGA_21372_API\SHP_korytowe'
    excell_file = 'WILGA_przekroje_korytowe.xlsx'

    # mergeExcellFiles(in_folder, excell_file)

    excell2shp(in_folder, excell_file, 'Wsp_X', 'Wsp_Y')