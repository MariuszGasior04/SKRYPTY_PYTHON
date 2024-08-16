import os
import sys

try:
    import arcpy

    arcpy.env.overwriteOutput = True
except:
    # komunikaty przy braku arcpy
    class arcpy:
        def AddWarning(msg):
            print(msg)

        def AddMessage(msg):
            print(msg)

        def AddError(msg):
            print(msg)


def checkPrerequisites():
    '''
    Funkcja sprawdza, czy sa zainstalowane potrzebne moduly i ew. licencje
    Input:
        brak
    Output:
        True/False - czy sa spelnione wszystkie wymagania do odpalenia skryptu
    '''
    # wynik sprawdzenia
    result = True

    # sprawdzenie wersji Pythona
    if sys.version_info.major != 3:
        result = False
        arcpy.AddWarning("WARNING. Wymagany jest Python 3")

    return result

def getNetworkData(networkFile):
    '''
    Funkcja do odczytywania geometrii branchy z pliku NWK MIKE11
    input: scieżka do pliku *.nwk11
    output: słowniki z branchami, weirsami, culvertami i bridgami
    '''
    pointsFull = {}
    pointsCoord = {}
    branches = {}
    weirs = {}
    culverts = {}
    bridges = {}
    # w tej sekcji następuje zaczytanie branczy, struktur i współrzędnych punktów budujących branche do słowników
    if networkFile.endswith('.nwk11'):
        print(networkFile)
        pointBool = False
        branchBool = False
        weirBool = False
        culvertBool = False
        culvertGeomBool = False
        bridgeBool = False
        resMarkBool = False
        irrBool = False
        resistance = ''
        arcpy.AddMessage("INFO. Rozpoczęto przetwarzanie networka - {}".format(networkFile))
        with open(networkFile, 'r') as f:
            try:
                for line in f:
                    # w tej cześci nastepuje zczytywanie punktów tworzacych obiekty w pliku *nwk11
                    if '[POINTS]' in line:
                        pointBool = True
                    if 'EndSect  // POINTS' in line:
                        pointBool = False
                    if pointBool and 'point' in line:
                        rsline = line.rstrip('\n').lstrip().replace(',','')
                        sl = rsline.split(" ")
                        # [NR punktu] = (wspolrzedna X, wspolrzedna Y, kilometraz, ? 0, ? 0)
                        try:
                            # [NR punktu] = (wspolrzedna X, wspolrzedna Y, kilometraz)
                            pointsFull[sl[2]] = (sl[3], sl[4], sl[6])
                            # [NR punktu] = (wspolrzedna X, wspolrzedna Y)
                            pointsCoord[sl[2]] = (sl[3], sl[4])
                        except IndexError as e:
                            arcpy.AddError(e)

                    # w tej cześci nastepuje zczytywanie branchy tworzacych obiekty w pliku *nwk11
                    if '[branch]' in line:
                        branchBool = True
                    if 'EndSect  // branch' in line:
                        branchBool = False
                    if branchBool:
                        if 'definitions' in line:
                            rsline = line.rstrip('\n').lstrip()
                            sl = rsline.replace('definitions = ','').split(",")
                            bTemp = sl[0]
                            branches[sl[0]] = [sl[1], sl[2], sl[3]]
                        if 'points' in line:
                            rsline = line.rstrip('\n').lstrip().replace(',', '')
                            sl = rsline.split(" ")
                            branches[bTemp].append(sl[2:])
                        if '[linkchannel]' in line:
                            branches[bTemp].append('link chanel')

                    # w tej cześci nastepuje zczytywanie weirsów tworzacych obiekty w pliku *nwk11
                    if '[weir_data]' in line:
                        weirBool = True
                    if 'EndSect  // weir_data' in line:
                        weirBool = False
                    if weirBool:
                        if 'Location' in line:
                            rsline = line.rstrip('\n').lstrip()
                            sl = rsline.replace('Location = ','').split(",")
                            # [weirID] = [branch, chainage, topoID]
                            weirs[sl[2]] = [sl[0], sl[1]]

                    # w tej cześci nastepuje zczytywanie culvertów tworzacych obiekty w pliku *nwk11
                    if '[culvert_data]' in line:
                        culvertBool = True
                        culvertIrr = ''
                    if 'EndSect  // culvert_data' in line:
                        culverts[currCulvert].append(culvertIrr)
                        culvertBool = False
                    if culvertBool:
                        if 'Location' in line:
                            rsline = line.rstrip('\n').lstrip()
                            sl = rsline.replace('Location = ', '').split(",")
                            # [culvertID] = [branch, chainage]
                            currCulvert = sl[2].lstrip()
                            culverts[sl[2].lstrip()] = [sl[0].lstrip(), sl[1].lstrip()]
                        if 'Attributes' in line:
                            rsline = line.rstrip('\n').lstrip()
                            sl = rsline.replace('Attributes = ', '').split(",")
                            culverts[currCulvert].append(sl[0].lstrip()) #rzedna1
                            culverts[currCulvert].append(sl[1].lstrip()) #rzedna2
                            culverts[currCulvert].append(sl[2].lstrip()) #dlugosc
                            culverts[currCulvert].append(sl[3].lstrip()) #maning
                            # [culvertID] = [branch, chainage, rzedna1, rzedna2, dlugosc, maning]
                    if '[Geometry]' in line and culvertBool:
                        culvertGeomBool = True
                    if 'EndSect  // Geometry' in line and culvertBool:
                        culvertGeomBool = False
                    if culvertGeomBool:
                        if 'Type' in line:
                            rsline = line.rstrip('\n').lstrip()
                            sl = rsline.replace('Type = ', '').split(",")
                            culverts[currCulvert].append(sl[0].lstrip())  # culvertType
                        if 'Rectangular' in line:
                            rsline = line.rstrip('\n').lstrip()
                            sl = rsline.replace('Rectangular = ', '').split(",")
                            culverts[currCulvert].append(sl[0].lstrip())  # culvertWys
                            culverts[currCulvert].append(sl[1].lstrip())  # culvertSzer
                        if 'Cicular_Diameter' in line:
                            rsline = line.rstrip('\n').lstrip()
                            sl = rsline.replace('Cicular_Diameter = ', '').split(",")
                            culverts[currCulvert].append(sl[0].lstrip())  # culvertDiameter
                        if '[Irregular]' in line:
                            irrBool = True
                        if 'EndSect  // Irregular' in line:
                            irrBool = False
                        if irrBool:
                            if 'Data = -1e-155' in line:
                                culvertIrr = ''
                            elif 'Data =' in line:
                                culvertIrr = 'kształt nieregularny'


                        # [culvertID] = [branch, chainage, rzedna1, rzedna2, dlugosc, maning, culvertType, culvertWys, culvertSzer, culvertDiameter, culvertIrr]

                    # w tej cześci nastepuje zczytywanie bridgy tworzacych obiekty w pliku *nwk11
                    if '[bridge_data]' in line:
                        bridgeBool = True
                    if bridgeBool:
                        if 'BranchName' in line:
                            rsline = line.rstrip('\n').lstrip()
                            sl = rsline.replace('BranchName = ', '').split(",")
                            bridge_branch = sl[0].lstrip() # bridge branch
                        if 'Chainage' in line:
                            rsline = line.rstrip('\n').lstrip()
                            sl = rsline.replace('Chainage = ', '').split(",")
                            bridge_chainage = sl[0].lstrip()  # bridge chainage
                        if 'ID' in line:
                            rsline = line.rstrip('\n').lstrip()
                            if rsline[:2] == 'ID':
                                sl = rsline.replace('ID = ', '').split(",")
                                bridgeID = sl[0].lstrip() # bridgeID
                        if 'Type' in line:
                            rsline = line.rstrip('\n').lstrip()
                            if rsline[:4] == 'Type':
                                sl = rsline.replace('Type = ', '').split(",")
                                bridge_type = sl[0].lstrip()  # bridgeType

                        if '[XZResMark]' in line:
                            resMarkBool = True
                            resistance = 'OK - wszystkie współczynniki strat BRIDGa mają wartości równe 1'
                        if 'EndSect  // XZResMark' in line:
                            resMarkBool = False
                        if resMarkBool and 'Row' in line:
                            rsline = line.rstrip('\n').lstrip()
                            sl = rsline.replace('Row = ', '').split(",")
                            if sl[2] != ' 1':
                                resistance = 'UWAGA - współczynniki strat BRIDGa mają wartości różne od 1'

                        if 'EndSect  // bridge_data' in line:
                            bridgeBool = False
                            bridges[bridgeID] = [bridge_branch, bridge_chainage, bridge_type, resistance]
            except:
                arcpy.AddError("ERROR! Problem z przetworzeniem networka {} w linii '{}'".format(networkFile, line))

        # w tej sekcji następuje zastąpienie punktów w słowniku branches współrzędnymi tych punktów
        # print(branches)
        branches_copy = branches.copy()
        for branch in branches:
            for point in pointsFull:
                try:
                    i = branches[branch][3].index(point)
                    branches_copy[branch][3][i] = pointsFull[point]
                except ValueError:
                    continue
                except IndexError:
                    continue


        # w tej sekcji następuje dodanie współrzednych X Y do słowników weirsów, culvertów i bridgy
        try:
            for weir in weirs:
                weirs[weir].append(getLocation(branches, weirs[weir][0], float(weirs[weir][1])))
        except:
            arcpy.AddError("ERROR! Problem z przypisaniem współrzednych dla weir {}".format(weir))
        try:
            for culvert in culverts:
                culverts[culvert].append(getLocation(branches, culverts[culvert][0], float(culverts[culvert][1])))
        except:
            arcpy.AddError("ERROR! Problem z przypisaniem współrzednych dla culvert {}".format(culvert))
        try:
            for bridge in bridges:
                bridges[bridge].append(getLocation(branches, bridges[bridge][0], float(bridges[bridge][1])))
        except:
            arcpy.AddError("ERROR! Problem z przypisaniem współrzednych dla bridge {}".format(bridge))

    return branches_copy, weirs, culverts, bridges

def getLocation(nwkBranches, branch, chainage):
    if not branch in nwkBranches:
        arcpy.AddWarning("WARNING. Branch {} zdefiniowany w structure nie odnaleziony w networku.".format(branch))
        return None

    for i in range(1, len(nwkBranches[branch][3])):
        prevPtObj = nwkBranches[branch][3][i - 1]
        nextPtObj = nwkBranches[branch][3][i]

        try:
            if i == 1 and float(prevPtObj[2]) > chainage:
                arcpy.AddMessage(i)
                arcpy.AddWarning("WARNING. Brak kilometrazu {} w branchu {} w nwk (--)".format(chainage, branch))
                return None
        except IndexError:
            arcpy.AddError("ERROR! prevPtObj {} {}".format(prevPtObj, nwkBranches[branch]))

        if float(prevPtObj[2]) <= chainage and float(nextPtObj[2]) >= chainage:
            scale = (chainage - float(prevPtObj[2])) / (float(nextPtObj[2]) - float(prevPtObj[2]))
            ptX = float(prevPtObj[0]) + scale * (float(nextPtObj[0]) - float(prevPtObj[0]))
            ptY = float(prevPtObj[1]) + scale * (float(nextPtObj[1]) - float(prevPtObj[1]))
            return (ptX, ptY)

    arcpy.AddWarning("WARNING. Brak kilometrazu {} w branchu {} w nwk (++)".format(branch, chainage))
    return None

def createOutputFC(weir, culvert, bridge):
    arcpy.AddMessage("INFO. Tworzenie warstw SHP {} {} {}". format(os.path.basename(weir), os.path.basename(culvert), os.path.basename(bridge)))
    arcpy.management.CreateFeatureclass(os.path.dirname(weir),os.path.basename(weir), 'POINT',
                                        spatial_reference = 'ETRS_1989_Poland_CS92')
    arcpy.management.AddField(weir,"WEIR_ID", 'TEXT',field_length=100)
    arcpy.management.AddField(weir,"BRANCH", 'TEXT',field_length=100)
    arcpy.management.AddField(weir,"CHAINAGE", 'FLOAT')
    arcpy.management.AddField(weir, "MODEL", 'TEXT', field_length=254)

    arcpy.management.CreateFeatureclass(os.path.dirname(culvert), os.path.basename(culvert), 'POINT',
                                        spatial_reference='ETRS_1989_Poland_CS92')
    arcpy.management.AddField(culvert, "CULVERT_ID", 'TEXT', field_length=50)
    arcpy.management.AddField(culvert, "BRANCH", 'TEXT', field_length=100)
    arcpy.management.AddField(culvert, "CHAINAGE", 'FLOAT')
    arcpy.management.AddField(culvert, "RZED1", 'FLOAT')
    arcpy.management.AddField(culvert, "RZED2", 'FLOAT')
    arcpy.management.AddField(culvert, "DL_CULV", 'FLOAT')
    arcpy.management.AddField(culvert, "MANING", 'FLOAT')
    arcpy.management.AddField(culvert, "TYP_CULV", 'FLOAT')
    arcpy.management.AddField(culvert, "SZER", 'FLOAT')
    arcpy.management.AddField(culvert, "WYS", 'FLOAT')
    arcpy.management.AddField(culvert, "SREDNICA", 'FLOAT')
    arcpy.management.AddField(culvert, "KSZTALT", 'TEXT', field_length=30)
    arcpy.management.AddField(culvert, "MODEL", 'TEXT', field_length=254)

    arcpy.management.CreateFeatureclass(os.path.dirname(bridge), os.path.basename(bridge), 'POINT',
                                        spatial_reference='ETRS_1989_Poland_CS92')
    arcpy.management.AddField(bridge, "BRIDGE_ID", 'TEXT', field_length=100)
    arcpy.management.AddField(bridge, "BRANCH", 'TEXT', field_length=100)
    arcpy.management.AddField(bridge, "CHAINAGE", 'FLOAT')
    arcpy.management.AddField(bridge, "TYP_BRIDGE", 'FLOAT')
    arcpy.management.AddField(bridge, "WSP_STRT_I", 'TEXT', field_length=60)
    arcpy.management.AddField(bridge, "MODEL", 'TEXT', field_length=254)

def exportNwkStructuresToShp(networkFile):
    branches, weirs, culverts, bridges = getNetworkData(networkFile)
    output_weir_shp = os.path.join(os.path.dirname(networkFile), os.path.basename(networkFile).split('.')[0] + '_WEIR.shp')
    output_culvert_shp = os.path.join(os.path.dirname(networkFile), os.path.basename(networkFile).split('.')[0] + '_CULVERT.shp')
    output_bridge_shp = os.path.join(os.path.dirname(networkFile), os.path.basename(networkFile).split('.')[0] + '_BRIDGE.shp')

    createOutputFC(output_weir_shp, output_culvert_shp, output_bridge_shp)

    arcpy.AddMessage("INFO. Zapisywanie obiektów WEIR do warstwy SHP {}".format(os.path.basename(output_weir_shp)))

    with arcpy.da.InsertCursor(output_weir_shp, ["SHAPE@", "WEIR_ID", "BRANCH", "CHAINAGE", "MODEL"]) as weirCur:
        for weir in weirs:
            pkt = weirs[weir][-1]
            geom = arcpy.PointGeometry(arcpy.Point(pkt[0], pkt[1]))
            row = [geom, weir, weirs[weir][0], weirs[weir][1], os.path.dirname(networkFile)]

            try:
                weirCur.insertRow(row)
            except:
                arcpy.AddError(
                    "ERROR! Problem z załadowaniem obiektu weir {} do warstwy SHP {}".format(weir, output_weir_shp))
                arcpy.AddError("ERROR!  weir - {}".format(row[1]))
                continue
        del weirCur


    arcpy.AddMessage("INFO. Zapisywanie obiektów CULVERT do warstwy SHP {}".format(os.path.basename(output_culvert_shp)))


    with arcpy.da.InsertCursor(output_culvert_shp, ["SHAPE@", "CULVERT_ID", "BRANCH", "CHAINAGE", "RZED1", "RZED2", "DL_CULV", "MANING", "TYP_CULV", "SZER", "WYS", "SREDNICA", "KSZTALT", "MODEL"]) as culvertCur:
        for culvert in culverts:
            pkt = culverts[culvert][-1]
            geom = arcpy.PointGeometry(arcpy.Point(pkt[0], pkt[1]))
            row = [geom, culvert, culverts[culvert][0], culverts[culvert][1],
                              float(culverts[culvert][2]),
                              float(culverts[culvert][3]),
                              float(culverts[culvert][4]),
                              float(culverts[culvert][5]),
                              float(culverts[culvert][6]),
                              float(culverts[culvert][7]),
                              float(culverts[culvert][8]),
                              float(culverts[culvert][9]),
                            culverts[culvert][10],
                            os.path.dirname(networkFile)]
            try:
                culvertCur.insertRow(row)
            except:
                arcpy.AddError("ERROR! Problem z załadowaniem obiektu culvert {} do warstwy SHP {}".format(culvert,
                                                                                                           output_culvert_shp))
                arcpy.AddError("ERROR!  culvert - {}".format(row[1]))
                continue
        del culvertCur


    arcpy.AddMessage("INFO. Zapisywanie obiektów BRIDGE do warstwy SHP {}".format(os.path.basename(output_bridge_shp)))

    with arcpy.da.InsertCursor(output_bridge_shp, ["SHAPE@", "BRIDGE_ID", "BRANCH", "CHAINAGE", "TYP_BRIDGE", "WSP_STRT_I", "MODEL"]) as bridgeCur:
        for bridge in bridges:
            pkt = bridges[bridge][-1]
            geom = arcpy.PointGeometry(arcpy.Point(pkt[0], pkt[1]))
            # print(bridges[bridge], bridge)
            row = [geom, bridge, bridges[bridge][0], float(bridges[bridge][1]), float(bridges[bridge][2]), bridges[bridge][3], os.path.dirname(networkFile)]

            try:
                bridgeCur.insertRow(row)
            except:
                arcpy.AddError(
                    "ERROR! Problem z załadowaniem obiektu bridge {} do warstwy SHP {}".format(bridge,
                                                                                               output_bridge_shp))
                arcpy.AddError("ERROR!  bridge - {}".format(row[1]))
                continue
        del bridgeCur

    return

def searchForNwk(inFolder):
    if os.path.isdir(inFolder):
        for root, dirs, files in os.walk(inFolder, topdown=False):
            #iteracja po plikach
            #print(u"Przeszukuję folder:"+"\n"+root)
            for name in files:
                if name.endswith('.nwk11'):
                    #znajdywanie plikow zawierających okreslone rozszerzenie
                    exportNwkStructuresToShp(os.path.join(root, name))

if __name__ == "__main__":
    # in_path = arcpy.GetParameterAsText(0)
    in_path = r'C:\robo\Przeglad_LOKAL_ROBO\MODELE\S01_ROPA_2019v1\01_MIKE11'
    #sprawdzamy czy wszystko jest
    if (not checkPrerequisites()):
        arcpy.AddError("ERROR. Brak wymaganych skladnikow.")
    else:
        if os.path.isdir(in_path):
            searchForNwk(in_path)

        elif os.path.isfile(in_path):
            exportNwkStructuresToShp(in_path)
