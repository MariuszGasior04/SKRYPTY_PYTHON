import arcpy
import math
import os
arcpy.env.overwriteOutput = True

def find_tuple_index(input_list, first_value):
    for index, item in enumerate(input_list):
        if item[0] == first_value:
            return index
    return None


def calc_dist(crossection, id_hyd_r, id_corssection, km, dist):
    '''
    Funkca wylicająca odległości pomiędzy punkatmi na warstwie rzece
    '''
    arcpy.AddMessage('INFO - Sortowanie przekroi')
    pkt_dict = {}
    pkt_dict_sort = {}
    with arcpy.da.SearchCursor(crossection, [id_hyd_r, km, id_corssection]) as search:
        try:
            for row in search:
                if row[0] in pkt_dict:
                    pkt_dict[str(row[0])].append((row[2],row[1]))
                else:
                    pkt_dict[str(row[0])] = [(row[2],row[1])]
        except AttributeError as e:
            arcpy.AddError(e)

    del search

    for id_hyd in pkt_dict:
        pkt_dict_sort[id_hyd] = sorted(pkt_dict[id_hyd],key = lambda x: x[1])

    arcpy.AddMessage('INFO - Przypisywanie odleglosci pomiedzy przekrojami')
    with arcpy.da.UpdateCursor(crossection, [id_hyd_r, id_corssection, dist]) as cur:
        for row in cur:
            if len(pkt_dict_sort[row[0]]) > 1:
                i = find_tuple_index(pkt_dict_sort[row[0]],row[1])
                if i == 0:
                    row[2] = 0
                else:
                    row[2] = pkt_dict_sort[row[0]][i][1] - pkt_dict_sort[row[0]][i-1][1]
                cur.updateRow(row)
    del cur
    return

def create_densified_crossection_tab(crossection,id_corssection, id_hyd_r, km, dist, frequency = 0.6, planned_frequency = 0.5):
    '''
    Funkcja sprawdzająca odległości miedzy przekrojami i tworząca tabele do zagęszczenia liczby przekroi na rzece
    '''
    arcpy.AddMessage('INFO - Tworzymy kolekcje przekroi do zageszczenia')
    event_table = {}
    i = 1
    with arcpy.da.SearchCursor(crossection, [id_hyd_r, km, dist, id_corssection]) as search:
        for row in search:
            try:
                if row[2] > frequency:
                    count_new_crossection = math.ceil(row[2]/planned_frequency)
                    new_dist = row[2]/count_new_crossection
                    for n in range(1,count_new_crossection):
                        event_table[row[0]+'_0'+str(i)] = [row[0], row[1]- (new_dist*n), new_dist]
                        i += 1
            except TypeError as e:
                arcpy.AddError(e)
                arcpy.AddMessage('UWAGA - Przekrój "{}" nie ma przeliczonych odległości. Nie dogęszczono przy nim przekroi'.format(row[3]))
                continue

    arcpy.AddMessage('INFO - Tworzenie tabeli z lokalizacją nowych przekroi')
    table_workspace = os.path.dirname(crossection)
    table_name = os.path.basename(crossection)+'_event_tab'
    arcpy.CreateTable_management(table_workspace, table_name, crossection)

    cursor = arcpy.da.InsertCursor(os.path.join(table_workspace, table_name), [id_hyd_r, id_corssection, km, dist,])
    for id in event_table:
        arcpy.AddMessage('INFO - dodanie przekroju {}'.format(id))
        cursor.insertRow([event_table[id][0], id, event_table[id][1], event_table[id][2]])

    event_table_path = os.path.join(table_workspace, table_name)

    return event_table_path

def create_densified_crossection_layer(event_table, river_route, id_hyd_r, km, output_name):
    '''
        Funkcja tworzaca warstwe punktową przekroi  do zagęszczenia na podstawie tabeli
    '''
    arcpy.AddMessage('INFO - Tworzenie warstwy punktowej przekroi zagęszczających pierwotną lokalizacje')
    output_temp = 'in_memory/temp'
    output = os.path.join(os.path.dirname(event_table), output_name)
    arcpy.MakeRouteEventLayer_lr(river_route, id_hyd_r, event_table,
                                 id_hyd_r + " POINT "+ km, output_temp)
    arcpy.CopyFeatures_management(output_temp,output)
    arcpy.AddMessage('INFO - Utworzono warstwe {}'.format(output))

    return

if __name__ == '__main__':

    crossection = arcpy.GetParameterAsText(0)
    r_route = arcpy.GetParameterAsText(1)
    id_hyd = arcpy.GetParameterAsText(2)
    id_cross = arcpy.GetParameterAsText(3)
    km = arcpy.GetParameterAsText(4)
    dist = arcpy.GetParameterAsText(5)

    fr = float(arcpy.GetParameterAsText(6)) #optional
    pl_fr = float(arcpy.GetParameterAsText(7)) #optional

    output_name = arcpy.GetParameterAsText(8)

    calc_dist(crossection,id_hyd, id_cross, km, dist)
    event_tab = create_densified_crossection_tab(crossection, id_cross, id_hyd, km, dist, fr, pl_fr)
    create_densified_crossection_layer(event_tab, r_route, id_hyd, km, output_name)