import arcpy

def river_dict(baza_MPHP):
    """
        Funkcja zczytujaca liste rzek i ich dlugosci z mphp (po ID_HYD_R)
    """

    arcpy.env.workspace = baza_MPHP
    river_dict = {}

    with arcpy.da.SearchCursor('mphp10/rzeki_r', ['ID_HYD_R_10', 'DL_CIEK']) as search:
        for row in search:
            river_dict[row[0]] = [row[1]]
    del search

    return river_dict


def river_basin_dict(baza_MPHP):
    """
        Funkcja zczytujaca powierzchnie zlewni rzek z mphp (po ID_HYD_R)
    """

    arcpy.env.workspace = baza_MPHP
    basin_dict = {}

    with arcpy.da.SearchCursor('mphp10/zlew_el', ['ID_HYD_10', 'SHAPE_Area']) as search:
        for row in search:
            basin_dict[row[0]] = [row[1]]
    del search

    return basin_dict

def update_river_dict(river_dict, basin_dict):
    """
         Funkcja do przypisania zsumowanych powierzchni zlewni elementarnych
     """
    for id_hyd_r in river_dict.keys():
        river_basin_area = 0
        for id_hyd in basin_dict.keys():
            if id_hyd[:len(id_hyd_r)] == id_hyd_r:
                river_basin_area += basin_dict[id_hyd][0]
        river_dict[id_hyd_r].append(round(river_basin_area/1000000, 2))

    return

def update_river_MPHP(baza_MPHP, river_dict):

    arcpy.env.workspace = baza_MPHP
    with arcpy.da.UpdateCursor('mphp10/rzeki_r', ['ID_HYD_R_10', 'POW_ZLEW_km2'])as cur:
        for row in cur:
            row[1] = river_dict[row[0]][1]
            cur.updateRow(row)
    del cur

    return

if __name__ == '__main__':

    baza_MPHP = r"C:\robo\_warstwy_tymczasowe\mphp10v13.gdb"
    r_dict = river_dict(baza_MPHP)
    print("1 - rzeki")
    rb_dict = river_basin_dict(baza_MPHP)
    print("2 - zlewnie")
    update_river_dict(r_dict, rb_dict)
    print("3 - przypisanie powierzchni zlewni rzek do slownika")
    update_river_MPHP(baza_MPHP, r_dict)
    print("4 - przypisanie powierzchni zlewni rzek w mphp")
