import arcpy

arcpy.env.overwriteOutput = True

def mileage_crossection(crossection, river_route, id_hyd_r, id_corssection):
    '''
       Funkca nadająca kilometraż punktom na rzece zgodnie z IDHYD_R rzeki i ID_przekroi
    '''
    temp_tab = 'in_memory/temp_tab'
    arcpy.AddMessage('INFO Lokalizowanie punktow przekroi na rzekach')
    arcpy.LocateFeaturesAlongRoutes_lr(crossection, river_route, id_hyd_r, 1, temp_tab, "rkey POINT KM_RZEKI")

    arcpy.AddMessage('INFO Dostosowywanie struktury warstwy przekroi i kilometracja przekroi')
    arcpy.DeleteField_management(crossection,['KM_RZEKI'])
    arcpy.JoinField_management(crossection, id_corssection, temp_tab, id_corssection, ['KM_RZEKI'])
    arcpy.AddField_management(crossection, 'ODL_KOL_PRZEKR', 'DOUBLE')
    arcpy.CalculateField_management(crossection, 'KM_RZEKI', 'round(!KM_RZEKI!, 3)', "PYTHON3")

    return

if __name__ == '__main__':

    crossection = arcpy.GetParameterAsText(0)
    r_route = arcpy.GetParameterAsText(1)
    id_hyd = arcpy.GetParameterAsText(2)
    id_cross = arcpy.GetParameterAsText(3)

    mileage_crossection(crossection,r_route,id_hyd,id_cross)