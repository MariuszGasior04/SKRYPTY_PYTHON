#!/usr/bin/env python
#-*- coding: utf-8 -*-

import arcpy

arcpy.env.overwriteOutput = True

def id_hyd_filter(rec_dict, id_hyd_r):
    filtered_dict = dict(filter(lambda item: item[1][0] == id_hyd_r, rec_dict.items()))
    return filtered_dict

def km_filter(rec_dict, km_river):
    filtered_dict = dict(filter(lambda item: item[1][2] > km_river, rec_dict.items()))
    return filtered_dict

def odc_filter(rec_dict, km_start, km_end):
    filtered_dict = dict(filter(lambda item: item[1][2] < km_end and item[1][2] > km_start, rec_dict.items()))
    return filtered_dict

def sort_lists_in_dict(dict):
    for key in dict:
        dict[key].sort(key=lambda x: x[1])  # Sortuj po drugim elemencie
    return dict

def find_idx_by_id(dict, szukane_id):
    for key in dict:
        for indeks, (id, _) in enumerate(dict[key]):
            if id == szukane_id:
                return indeks
    return None

def calc_dist(workspace, bud):
    arcpy.env.workspace = workspace

    pkt_dict = {}
    with arcpy.da.SearchCursor(bud, ['ID_HYD_R_1', 'KM_RZEKI', 'ODL_KOL_BUD', 'ID_NEW']) as search:
        for row in search:

            if row[0] in pkt_dict:
                pkt_dict[str(row[0])].append((row[3], row[1]))
            else:
                pkt_dict[str(row[0])] = [(row[3], row[1])]

    sort_lists_in_dict(pkt_dict)
    del search

    print("Utworzono słownik")
    # print(pkt_dict['254'])
    id_hyd_r = ''
    i=1
    with arcpy.da.UpdateCursor(bud, ['ID_HYD_R_1', 'KM_RZEKI', 'ODL_KOL_BUD', 'UWAGA_ODL','ID_NEW','ODL_DO_ZRD']) as cur:
        for row in cur:
            if row[2] is None:
                id = find_idx_by_id(pkt_dict, row[4])
                try:
                    row[2] = pkt_dict[row[0]][id+1][1] - row[1]
                except IndexError:
                    row[3] = 'Ostatnia budowla na cieku.Odleglość do źródła.'
                    row[2] = row[5]
                cur.updateRow(row)
    del cur
    return

def calc_river_length_above(workspace, bud, river_o):
    arcpy.env.workspace = workspace
    river_o_layer = 'river_o_layer'

    print("Tworzymy layer rzek_o...")
    arcpy.MakeFeatureLayer_management(river_o, river_o_layer)

    print("Zapisywanie sumarycznej długości rzek do warstwy budowli...")
    i = 0
    with arcpy.da.UpdateCursor(bud, ['ID_NEW', 'ID_HYD_10', 'ID_HYD_R_1', 'DL_RZEK_POW', 'ODL_DO_ZRD']) as cur:
        for row in cur:
            if row[3] is None:
                i += 1
                id_zlew = row[1]
                id_rzek = row[2]
                temp_tab = 'in_memory/temp_tab'
                where_clause = 'ID_HYD_10' + ' LIKE ' + "'" + id_zlew + "%'"
                arcpy.SelectLayerByAttribute_management(river_o_layer, "NEW_SELECTION", where_clause)

                while id_zlew != id_rzek:
                    try:
                        if id_zlew[-1] == '0':
                            id_zlew = id_zlew[:-1]
                        else:
                            id_zlew = id_zlew[:-1] + str(int(id_zlew[-1]) - 1)
                            where_clause = 'ID_HYD_10' + ' LIKE ' + "'" + id_zlew + "%'"
                            arcpy.SelectLayerByAttribute_management(river_o_layer, "ADD_TO_SELECTION", where_clause)
                    except:
                        row[3] = 0
                        break

                if row[3] is None:
                    where_clause = 'ID_HYD_R_10' + ' = ' + "'" + id_rzek + "'"
                    arcpy.SelectLayerByAttribute_management(river_o_layer, "REMOVE_FROM_SELECTION", where_clause)
                    arcpy.Statistics_analysis(river_o_layer, temp_tab, [["SHAPE_Length", "SUM"]])
                    with arcpy.da.SearchCursor(temp_tab, ['SUM_SHAPE_Length']) as cur2:
                        for row2 in cur2:
                            row[3] = round(row2[0]/1000, 3) + row[4]

                    del cur2


                print(i, row[0], row[1], row[3])
            cur.updateRow(row)

        del cur

    return

def calc_river_length_above2(workspace, bud, rec_tab):
    arcpy.env.workspace = workspace

    print("Tworzymy słownik punktów ujsciowych wszystkich rzek...")
    rec_dict = {}
    with arcpy.da.SearchCursor(rec_tab, ['ID_HYD_R_10', 'ID_HYD_RC_10', 'KM_UJSCIA', 'ODL_DO_1BUD', 'DL_CIEK']) as search:
        for row in search:

            if row[0] not in rec_dict:
                rec_dict[row[0]] = [row[1], row[0], row[2], row[3], row[4]]
            else:
                rec_dict[str(row[0])] = [row[1]]
    del search

    print("Zapisywanie sumarycznej długości rzek do warstwy budowli...")
    i = 0
    with arcpy.da.UpdateCursor(bud, ['ID_NEW', 'ID_HYD_10', 'ID_HYD_R_1', 'DL_RZEK_POW', 'ODL_DO_ZRD', 'KM_RZEKI']) as cur:
        for row in cur:
            if row[3] is None:
                i += 1
                r = km_filter(id_hyd_filter(rec_dict, row[2]), row[5])
                rc = r.copy()
                a = len(r)
                b = a - 1
                while a > b:
                    b = len(r)
                    for key in rc:
                        r.update(id_hyd_filter(rec_dict, key))
                    a = len(r)

                suma = sum(r[item][4] for item in r)

                row[3] = suma + row[4]

                # print(i, row[0], row[1], row[3])

            cur.updateRow(row)

        del cur

    return

def calc_unobstacled_river_length_above(workspace, bud, rec_tab):
    arcpy.env.workspace = workspace

    print("Tworzymy słownik punktów ujsciowych wszystkich rzek...")
    rec_dict = {}
    with arcpy.da.SearchCursor(rec_tab, ['ID_HYD_R_10', 'ID_HYD_RC_10', 'KM_UJSCIA', 'ODL_DO_1BUD', 'DL_CIEK']) as search:
        for row in search:

            if row[0] not in rec_dict:
                rec_dict[row[0]] = [row[1], row[0], row[2], row[3], row[4]]
            else:
                rec_dict[str(row[0])] = [row[1]]
    del search

    print("Zapisywanie sumarycznej długości nieprzegrodzonych rzek do warstwy budowli...")
    i = 0
    with arcpy.da.UpdateCursor(bud, ['ID_NEW', 'ID_HYD_10', 'ID_HYD_R_1', 'DL_RZEK_N_POW', 'ODL_KOL_BUD', 'KM_RZEKI']) as cur:
        for row in cur:
            if row[3] is None:
                i += 1
                r = odc_filter(id_hyd_filter(rec_dict, row[2]), row[5], row[5]+row[4])
                rc = r.copy()
                a = len(r)
                b = a - 1
                while a > b:
                    b = len(r)
                    for value in rc.values():
                        if len(id_hyd_filter(rec_dict, value[1])) > 0 and value[3] is not None:
                            r.update(odc_filter(id_hyd_filter(rec_dict, value[1]), 0, value[3]))
                        elif len(id_hyd_filter(rec_dict, value[1])) > 0 and value[3] is None:
                            r.update(id_hyd_filter(rec_dict, value[1]))
                    a = len(r)

                suma = 0
                for value in r.values():
                    if value[3] is not None:
                        suma += value[3]
                    else:
                        suma += value[4]

                row[3] = suma + row[4]

                # print(i, row[0], row[1], row[3])

            cur.updateRow(row)

        del cur

    return

if __name__ == '__main__':
    # workspace = 'E:\Waloryzajca_rzek_WWF\PPH2\ew\PPH2_10_12_22.gdb'
    # budowle = 'bud_p_id_odc'
    tabela_recypientow = 'rzeki_r_PKT_UJSCIOWE_Locate'
    workspace = 'D:\ZLECENIA_2023\ROBOCZY_CZERWIEC_2023\Ocena_ciaglosci_BOBR.gdb'
    budowle = 'Obiekty_hydro_calosc'
    # calc_dist(workspace,budowle)
    # tabela_recypientow = 'rzeki_r_PKT_UJSCIOWE_Locate'
    calc_unobstacled_river_length_above(workspace, budowle, tabela_recypientow)
    # calc_river_length_above2(workspace, budowle, tabela_recypientow)
    # calc_dist(workspace, budowle)