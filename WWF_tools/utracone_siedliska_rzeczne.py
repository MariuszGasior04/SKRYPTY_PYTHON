import arcpy, math, statistics
import getElevation
arcpy.env.overwriteOutput = True

def calcSlope(lineLayer):
    '''
    Finkcja do oblicznia spadku obiektów w warstwie liniowej
    :return:
    '''
    i=0
    with arcpy.da.UpdateCursor(lineLayer, ['SPADEK', 'Shape_Length', 'SHAPE@']) as update:
        for row in update:
            if row[0] is None:
                i+=1
                lineGeom = list(row[2])
                y1 = lineGeom[0][0].X
                x1 = lineGeom[0][0].Y
                z1 = getElevation.getPointElevation(x1, y1)
                y2 = lineGeom[0][-1].X
                x2 = lineGeom[0][-1].Y
                z2 = getElevation.getPointElevation(x2, y2)
                try:
                    dh = z2 - z1
                    row[0] = round(dh*100/row[1], 2)
                    print("{} - Spadek {}% pomiedzy {} i {}".format(i, row[0], z2, z1))
                    update.updateRow(row)
                except TypeError:
                    continue
        del update
    return

def readReservoir(reservoirsLayer):
    reservoirs = {}
    '''zbiornik(identyfikator zbiornika) = lista parametrow zbiornika
                        lista parametrow zbiornika = [
                        0 identyfikator hydrograficzny głownego cieku zbiornika, 
                        1 indeks kolejnego odcinka cieku głównego w ramach całej sieci rzecznej, 
                        2 długosć osi geometrycznej zbiornika,
                        *kolejne parametry dodawane później
                        3 uśredniony współczynnik kierunkowy zbiornika na podstawie wkz dwóch odcinków poniżej i powyżej zbiornika
                        4 sumaryczna długość odcinków  odcinków poniżej i powyżej zbiornika
                        5 sumaryczna długość odcinków skorygowanych o spadek poniżej i powyżej zbiornika
                        6 skorygowana o sredni współczynnik kretości długosć osi geometrycznej zbiornika
                        7 utrata siedliska rzecznego
                        '''
    with arcpy.da.SearchCursor(reservoirsLayer, ['ID_HYD_R_1', 'ID_ZB', 'DL_OSI_GEOM']) as search:
        for row in search:
            if row[1] is not None and row[1] not in reservoirs:
                reservoirs[row[1]] = [row[0], 0, round(row[2])]
    return reservoirs

def readRiverReservoir(riverSections, reservoirs):
    '''
    :param riverSections: warstwa posortowanych odcinków cieków po identyfikatorach rzek oraz kilometrazu, kilometrażem, współczynnikiem krętości i ID zbiorników odcinków do wyznaczenia
    :return: zwraca kolekcje odcinków rzek dla którch wyliczany będzie wskaźnik utraconego siedliska rzecznego. Wyliczenie będzie dotyczyło znanego ID zbiornika
    '''
    rivers = {}

    with arcpy.da.SearchCursor(riverSections, ['identyfika', 'kmsrodek', 'wspzwykly', 'przebiegwz', 'ID_ZB', 'Shape_Length','SHAPE@','DL_KORYG']) as search:
        for row in search:
            if row[1] is not None:
                lineGeom = list(row[6])
                x1 = lineGeom[0][0].X
                x2 = lineGeom[0][-1].X
                y1 = lineGeom[0][0].Y
                y2 = lineGeom[0][-1].Y
                gLength = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2-y1), 2))
                if row[0] not in rivers:
                    '''rzeka(identyfikator hydrograficzny) = lista odcinkow rzeki
                    lista odcinkow rzeki = [
                    0 identyfikator zbiornika jezeli odcinek przechodzi przez zbiornik, 
                    1 kilometraz srodka odcinka rzeki, 
                    2 wspolczynnik kierunkowy zwykly,
                    3 czy odcinek przebiega przez zbiornik (tak/nie)
                    4 długość odcinka
                    5 os odcinka - odległość w lini prostej pomiędzy poczatkiem a końcem odcinka}]
                    6 dlugosc odcinka skorygowana o spadek terenu
                    '''
                    rivers[row[0]] = [[row[4], row[1], row[2], row[3], round(row[5]), round(gLength),row[7]]]
                    i=0
                else:
                    i+=1
                    rivers[row[0]].append([row[4], row[1], row[2], row[3], round(row[5]), round(gLength),row[7]])
                if row[4] is not None and row[4] not in reservoirs:
                    reservoirs[row[4]] = [row[0], i, round(row[5])]
                elif row[4] is not None and row[4] in reservoirs:
                    reservoirs[row[4]][1] = i
    del search

    utrataSiedFront = {}
    utrataSiedBack = {}
    for reservoir in reservoirs:
        '''Ta pętla sczytuje max 3 odcinki rzeczne poniżej zbiornikowego i max 2 odcinki powyżej (z pominieciem odcinków zbiornikowych, sierot, ramion bocznych).  
        Nie sczyta poniżej ujścia rzeki i oczywiście powyżej źródła'''
        frontRiverSections = []
        backRiverSections = []
        idHydR = reservoirs[reservoir][0]
        idXf = reservoirs[reservoir][1]
        idXb = reservoirs[reservoir][1]
        idR = rivers[idHydR]

        while idXf>0 and len(frontRiverSections) < 2:
            idXf-=1
            if len(frontRiverSections) == 0 and idR[idXf][0] is None and idR[idXf][2] is not None:
                idXf -= 1
                if idXf > 0:
                    frontRiverSections = [idR[idXf]]
            elif len(frontRiverSections) > 0 and idR[idXf][0] is None and idR[idXf][2] is not None:
                frontRiverSections.append(idR[idXf])

        while idXb < (len(idR)-1) and len(backRiverSections) < 2:
            idXb+=1
            # print(idXb)
            if len(backRiverSections) == 0 and idR[idXb][0] is None and idR[idXb][2] is not None:
                backRiverSections = [idR[idXb]]
            elif len(backRiverSections) > 0 and idR[idXb][0] is None and idR[idXb][2] is not None:
                backRiverSections.append(idR[idXb])
        utrataSiedFront[reservoir] = frontRiverSections
        utrataSiedBack[reservoir] = backRiverSections

    # print(dict(sorted(reservoirs.items())))
    for reservoir in reservoirs:
        wkz = []
        dl_odc_koryt = []
        dl_skor_odc_koryt = []
        '''Ta pętla odczytuje zapisane odcinki rzeczne. Wyliczna na ich podstawie średni współczynnik krętości i przy znanej odoległości punktów na końcach osi geometrycznej zbiornika
        obliczana jest długość koryta rzecznego przed zalaniem zbiornika.'''
        # print(reservoir, utrataSiedFront[reservoir])
        for itemF in utrataSiedFront[reservoir]:
            try:
                wkz.append(itemF[2])
                dl_odc_koryt.append(itemF[4])
                dl_skor_odc_koryt.append(itemF[6])
            except IndexError:
                print("Zbiornik {} nie posaida legitnych odcinkow rzecznych ponizej zapory".format(reservoir))
                continue
        for itemB in utrataSiedBack[reservoir]:
            try:
                wkz.append(itemB[2])
                dl_odc_koryt.append(itemB[4])
                dl_skor_odc_koryt.append(itemB[6])
            except IndexError:
                print("Zbiornik {} nie posaida legitnych odcinkow rzecznych powyzej cofki".format(reservoir))
                continue
        # print(reservoir, wkz, statistics.mean(wkz))
        # print(reservoir, dl_odc_koryt, sum(dl_odc_koryt))
        # print(reservoir, dl_skor_odc_koryt, sum(dl_skor_odc_koryt))
        reservoirs[reservoir].append(round(statistics.mean(wkz),4))
        reservoirs[reservoir].append(sum(dl_odc_koryt))
        reservoirs[reservoir].append(round(sum(dl_skor_odc_koryt)))
        reservoirs[reservoir].append(round(reservoirs[reservoir][5]*reservoirs[reservoir][2]/reservoirs[reservoir][4],2))
        reservoirs[reservoir].append(round(reservoirs[reservoir][6]*reservoirs[reservoir][3],2))
    # print(dict(sorted(utrataSied.items())))
    # print(dict(sorted(reservoirs.items())))
    # print(dict(sorted(reservoirs.items())))
    for reservoir in dict(sorted(reservoirs.items())):
        print("{};{};{};{};{};{};{};{};{}".format(reservoir, reservoirs[reservoir][0], reservoirs[reservoir][1], reservoirs[reservoir][2], reservoirs[reservoir][3], reservoirs[reservoir][4], reservoirs[reservoir][5], reservoirs[reservoir][6], reservoirs[reservoir][7]))
    return

if __name__ == '__main__':
    inWarstwaRzek = r'E:\Waloryzajca_rzek_WWF\ROBOCZY_LIPIEC_SIERPIEN_2023\01_06_Pilotazowa_ocena_utraty_siedliska_rzecznego\Ocena_ciaglosci_BOBR.gdb\odcinki_rzek_05_2023_SORT'
    inWarstwaZbiornikow = r'E:\Waloryzajca_rzek_WWF\ROBOCZY_LIPIEC_SIERPIEN_2023\01_06_Pilotazowa_ocena_utraty_siedliska_rzecznego\Ocena_ciaglosci_BOBR.gdb\zbiorniki_sztuczne_MPHP_2017'
    # calcSlope(inWarstwaRzek)
    readRiverReservoir(inWarstwaRzek, readReservoir(inWarstwaZbiornikow))
