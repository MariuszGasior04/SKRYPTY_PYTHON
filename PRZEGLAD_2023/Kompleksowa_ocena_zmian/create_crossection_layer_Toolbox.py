import arcpy
import os
arcpy.env.overwriteOutput = True

def create_densified_crossection_layer(event_table, river_route, id_hyd_r, km):
    '''
        Funkcja tworzaca warstwe punktową przekroi  do zagęszczenia na podstawie tabeli
    '''
    arcpy.AddMessage('INFO - Tworzenie warstwy punktowej przekroi zagęszczających pierwotną lokalizacje')
    output_temp = 'in_memory/temp'
    output = os.path.join(os.path.dirname(event_table), 'przekroje_dogeszczone')
    arcpy.MakeRouteEventLayer_lr(river_route, id_hyd_r, event_table,
                                 id_hyd_r + " POINT "+ km, output_temp)
    arcpy.CopyFeatures_management(output_temp,output)
    arcpy.AddMessage('INFO - Utworzono warstwe {}'.format(output))

    return

if __name__ == '__main__':

    crs_tab = arcpy.GetParameterAsText(0)
    r_route = arcpy.GetParameterAsText(1)
    id_hyd = arcpy.GetParameterAsText(2)
    km = arcpy.GetParameterAsText(3)

    create_densified_crossection_layer(crs_tab,r_route,id_hyd,km)