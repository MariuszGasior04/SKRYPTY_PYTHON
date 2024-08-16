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

if __name__ == '__main__':
    # point_layer = arcpy.GetParameterAsText(0)
    # sort_field = arcpy.GetParameterAsText(1)
    # kod_terenu_field = arcpy.GetParameterAsText(2)
    # id_hyd_field = arcpy.GetParameterAsText(4)
    # river_name_field = arcpy.GetParameterAsText(3)
    # date_field = arcpy.GetParameterAsText(5)

    point_layer = r'R:\Dane_PGW_WP_3M\10. Modele hydrauliczne\RW G-WW\SĘKÓWKA_21826_2019v1\1.3.14.27 RAPORT\SEKOWKA_21826_API\SHP\SEKOWKA_przekroje_punkty.shp'
    sort_field = 'NR_PKT'
    kod_terenu_field = 'RZEKA'
    id_hyd_field = 'ID_HYD_R'
    river_name_field = 'RZEKA'
    date_field = None

    if id_hyd_field and date_field:
        przekPkt2Line(point_layer, sort_field, kod_terenu_field,  id_hyd_field, river_name_field, date_field)
    elif date_field:
        przekPkt2Line2(point_layer, sort_field, kod_terenu_field, river_name_field, date_field)
    else:
        przekPkt2Line3(point_layer, sort_field, kod_terenu_field, river_name_field)