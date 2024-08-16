import arcpy
import os

arcpy.env.overwriteOutput = True

def przekPkt2Line(point_layer, sort_field, kod_terenu_field,  id_hyd_field, river_name_field, date_field):
    '''
    Funkcja konwertująca punktowe przekroje korytowe z pomiarów geodezyjnych na ich reprezentacje liniową
    '''
    prz_dict = {}
    arcpy.AddMessage("INFO. Odczytywanie warstwy przekroi {}".format(point_layer))

    with arcpy.da.SearchCursor(point_layer, ['SHAPE@XY', sort_field, river_name_field, id_hyd_field, date_field, kod_terenu_field]) as search:
        for row in search:
            if row[-1] != '' and row[-1] != ' ' and row[-1] is not None:
                if row[1].split('.')[0]+'_'+row[2] in prz_dict:
                    prz_dict[row[1].split('.')[0]+'_'+row[2]][2].append(row[0])
                else:
                    prz_dict[row[1].split('.')[0] + '_' + row[2]] = [row[3], row[4], [row[0]]]
    del search

    # tworzymy warstwe wynikową
    output_shp = os.path.basename(point_layer).split('.')[0] + '_liniowe_przeglad.shp'
    output_dir = os.path.dirname(point_layer)
    shp_path = os.path.join(output_dir, output_shp)

    arcpy.AddMessage("INFO. Tworzenie warstwy wynikowej {} w lokalizacji {}".format(output_shp, output_dir))

    arcpy.management.CreateFeatureclass(output_dir, output_shp, geometry_type='POLYLINE',
                                        spatial_reference='ETRS_1989_Poland_CS92')
    arcpy.management.AddField(shp_path, "ID_PRZEKR", 'TEXT', field_length=30)
    arcpy.management.AddField(shp_path, "ID_HYD_R", 'TEXT', field_length=30)
    arcpy.management.AddField(shp_path, "NAZ_RZEKI", 'TEXT', field_length=100)
    arcpy.management.AddField(shp_path, "DATA_POM", 'TEXT', field_length=12)
    arcpy.management.AddField(shp_path, "MODEL", 'TEXT', field_length=254)

    arcpy.AddMessage(
        "INFO. Zapis warstwy liniowej przekroi korytowych na warstwie {}".format(output_shp, output_dir))
    with arcpy.da.InsertCursor(shp_path, ["SHAPE@", "ID_PRZEKR", "ID_HYD_R", "NAZ_RZEKI", "DATA_POM", "MODEL"]) as przekCur:
        for przekroj in prz_dict:
            geom = arcpy.Polyline(arcpy.Array([arcpy.Point(x[0], x[1]) for x in prz_dict[przekroj][2]]))
            row = [geom, przekroj.split('_')[0], prz_dict[przekroj][0], przekroj.split('_')[1], prz_dict[przekroj][1], os.path.dirname(point_layer)]
            przekCur.insertRow(row)
    del przekCur

    return

def przekPkt2Line2(point_layer, sort_field, kod_terenu_field, river_name_field, date_field):
    '''
    Funkcja konwertująca punktowe przekroje korytowe z pomiarów geodezyjnych na ich reprezentacje liniową (nie uwzglednia IDHYDR)
    '''
    prz_dict = {}
    arcpy.AddMessage("INFO. Odczytywanie warstwy przekroi {}".format(point_layer))
    with arcpy.da.SearchCursor(point_layer, ['SHAPE@XY', sort_field, river_name_field, date_field, kod_terenu_field]) as search:
        for row in search:
            if row[-1] != '' and row[-1] != ' ' and row[-1] is not None:
                if row[1].split('.')[0] + '_' + row[2] in prz_dict:
                    prz_dict[row[1].split('.')[0]+'_'+row[2]][1].append(row[0])
                else:
                    prz_dict[row[1].split('.')[0] + '_' + row[2]] = [row[3], [row[0]]]
    del search

    # tworzymy warstwe wynikową
    output_shp = os.path.basename(point_layer).split('.')[0] + '_liniowe_przeglad.shp'
    output_dir = os.path.dirname(point_layer)
    shp_path = os.path.join(output_dir, output_shp)

    arcpy.AddMessage("INFO. Tworzenie warstwy wynikowej {} w lokalizacji {}".format(output_shp, output_dir))

    arcpy.management.CreateFeatureclass(output_dir, output_shp, geometry_type='POLYLINE',
                                        spatial_reference='ETRS_1989_Poland_CS92')
    arcpy.management.AddField(shp_path, "ID_PRZEKR", 'TEXT', field_length=30)
    arcpy.management.AddField(shp_path, "NAZ_RZEKI", 'TEXT', field_length=100)
    arcpy.management.AddField(shp_path, "DATA_POM", 'TEXT', field_length=12)
    arcpy.management.AddField(shp_path, "MODEL", 'TEXT', field_length=254)

    # print(prz_dict)
    arcpy.AddMessage(
        "INFO. Zapis warstwy liniowej przekroi korytowych na warstwie {}".format(output_shp, output_dir))
    with arcpy.da.InsertCursor(shp_path, ["SHAPE@", "ID_PRZEKR", "NAZ_RZEKI", "DATA_POM", "MODEL"]) as przekCur:
        for przekroj in prz_dict:
            geom = arcpy.Polyline(arcpy.Array([arcpy.Point(x[0], x[1]) for x in prz_dict[przekroj][1]]))
            row = [geom, przekroj.split('_')[0], przekroj.split('_')[1], prz_dict[przekroj][0], os.path.dirname(point_layer)]
            przekCur.insertRow(row)
    del przekCur

    return

def przekPkt2Line3(point_layer, sort_field, kod_terenu_field, river_name_field):
    '''
    Funkcja konwertująca punktowe przekroje korytowe z pomiarów geodezyjnych na ich reprezentacje liniową (nie uwzglednia IDHYDR)
    '''
    prz_dict = {}
    arcpy.AddMessage("INFO. Odczytywanie warstwy przekroi {}".format(point_layer))
    with arcpy.da.SearchCursor(point_layer, ['SHAPE@XY', sort_field, river_name_field, kod_terenu_field]) as search:
        for row in search:
            if row[-1] != '' and row[-1] != ' ' and row[-1] is not None:
                if row[1].split('.')[0] + '_' + row[2] in prz_dict:
                    prz_dict[row[1].split('.')[0]+'_'+row[2]][0].append(row[0])
                else:
                    prz_dict[row[1].split('.')[0] + '_' + row[2]] = [[row[0]]]
    del search

    # tworzymy warstwe wynikową
    output_shp = os.path.basename(point_layer).split('.')[0] + '_liniowe_przeglad.shp'
    output_dir = os.path.dirname(point_layer)
    shp_path = os.path.join(output_dir, output_shp)

    arcpy.AddMessage("INFO. Tworzenie warstwy wynikowej {} w lokalizacji {}".format(output_shp, output_dir))

    arcpy.management.CreateFeatureclass(output_dir, output_shp, geometry_type='POLYLINE',
                                        spatial_reference='ETRS_1989_Poland_CS92')
    arcpy.management.AddField(shp_path, "ID_PRZEKR", 'TEXT', field_length=30)
    arcpy.management.AddField(shp_path, "NAZ_RZEKI", 'TEXT', field_length=100)
    arcpy.management.AddField(shp_path, "MODEL", 'TEXT', field_length=254)

    # print(prz_dict)
    arcpy.AddMessage(
        "INFO. Zapis warstwy liniowej przekroi korytowych na warstwie {}".format(output_shp, output_dir))
    with arcpy.da.InsertCursor(shp_path, ["SHAPE@", "ID_PRZEKR", "NAZ_RZEKI", "MODEL"]) as przekCur:
        for przekroj in prz_dict:
            geom = arcpy.Polyline(arcpy.Array([arcpy.Point(x[0], x[1]) for x in prz_dict[przekroj][0]]))
            row = [geom, przekroj.split('_')[0], przekroj.split('_')[1], os.path.dirname(point_layer)]
            przekCur.insertRow(row)
    del przekCur

    return

def search(in_folder, file_ext):
    for root, dirs, files in os.walk(in_folder, topdown=False):
        #iteracja po plikach
        #print(u"Przeszukuję folder:"+"\n"+root)
        for name in files:
            #znajdywanie plikow zawierających okreslone rozszerzenie
            if name.endswith(file_ext):
                if 'liniowe_przeglad' not in name:
                    if 'obiekty_mostowe' in name or 'przekroje_koryto' in name or 'obiekty_hydrotechniczne' in name:
                        point_layer = os.path.join(root, name)
                        sort_field = 'NR_PKT'
                        kod_terenu_field = 'KOD_TERENU'
                        id_hyd_field = 'ID_HYD_R'
                        river_name_field = 'NAZWA'
                        date_field = 'DATA_POM'

                        field_names = [f.name for f in arcpy.ListFields(point_layer)]

                        if id_hyd_field in field_names and date_field in field_names:
                            print('Z warstwy {0} wyeksportowano przekroje liniowe z atrybutami {1} {2}'.format(point_layer,
                                                                                                               id_hyd_field,
                                                                                                               date_field))
                            przekPkt2Line(point_layer, sort_field, kod_terenu_field, id_hyd_field, river_name_field,
                                          date_field)
                        elif date_field in field_names:
                            print('Z warstwy {0} wyeksportowano przekroje liniowe z atrybutami {1}'.format(point_layer,
                                                                                                           date_field))
                            przekPkt2Line2(point_layer, sort_field, kod_terenu_field, river_name_field, date_field)
                        else:
                            print('Z warstwy {0} wyeksportowano przekroje liniowe bez IDHYD i DATY POMIARU'.format(
                                point_layer))
                            przekPkt2Line3(point_layer, sort_field, kod_terenu_field, river_name_field)


if __name__ == '__main__':
    in_folder = r'R:\Dane_PGW_WP_3M\10. Modele hydrauliczne\RW G-ZW\WISŁA_2_2019v1\1.3.14.27 RAPORT\WISLA_2_ISOK\PLIKI SHAPE'

    search(in_folder, '.shp')
