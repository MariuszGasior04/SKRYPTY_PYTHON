import arcpy
import os

arcpy.env.overwriteOutput = True

def nwk2shp(nwk_file):
    '''
    Funkcja do odczytywania geometrii branchy z pliku NWK MIKE11 i zapisywania ich do geometrii w pliku shp
    input: scieżka do pliku *.nwk11
    output: sciezka wynikowego pliku *.shp
    '''
    pointsFull = {}
    pointsCoord = {}
    branches = {}
    # w tej sekcji następuje zaczytanie branczy i współrzędnych punktów budujących branche do słowników branches, pointsCoord i pointsFull
    if nwk_file.endswith('.nwk11'):
        pointBool = False
        branchBool = False
        with open(nwk_file, 'r') as f:
            arcpy.AddMessage("Odczytywanie struktury pliku {}.".format(nwk_file))
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
                        pointsFull[sl[2]] = (sl[3], sl[4], sl[6], sl[5], sl[7])
                        # [NR punktu] = (wspolrzedna X, wspolrzedna Y)
                        pointsCoord[sl[2]] = (sl[3], sl[4])
                    except IndexError as e:
                        print(sl)
                        raise e
                if '[branch]' in line:
                    branchBool = True
                if 'EndSect  // branch' in line:
                    branchBool = False
                if branchBool:
                    if 'definitions' in line:
                        rsline = line.rstrip('\n').lstrip().replace(',', '')
                        sl = rsline.split(" ")
                        bTemp = sl[2]
                        branches[sl[2]] = [sl[3], sl[4], sl[5]]
                    if 'points' in line:
                        rsline = line.rstrip('\n').lstrip().replace(',', '')
                        sl = rsline.split(" ")
                        branches[bTemp].append(sl[2:])
                    if '[linkchannel]' in line:
                        branches[bTemp].append('link chanel')

        arcpy.AddMessage("Konwertowanie struktury networka {}.".format(os.path.basename(nwk_file)))

        # w tej sekcji następuje zastąpienie punktów w słowniku branches współrzędnymi tych punktów
        for branch in branches:
            for point in pointsCoord:
                try:
                    i = branches[branch][3].index(point)
                    branches[branch][3][i] = pointsCoord[point]
                except ValueError:
                    continue
                except IndexError:
                    continue

    # w tej sekcji następuje utworzenie pustej warstwy shp, dodanie jej atrybutów BRANCH, TOPOID, KM_POCZ_M, KM_KON_M, TYP_BRANCH

        output_shp = os.path.basename(nwk_file).split('.')[0]+'.shp'
        output_dir = os.path.dirname(nwk_file)
        arcpy.AddMessage("Zapis wynikowego pliku {} w lokalizacji {}".format(output_shp, output_dir))
        arcpy.management.CreateFeatureclass(output_dir, output_shp, geometry_type = 'POLYLINE', spatial_reference = 'ETRS_1989_Poland_CS92')
        arcpy.AddField_management(os.path.join(output_dir, output_shp),'BRANCH','TEXT',field_length=200)
        arcpy.AddField_management(os.path.join(output_dir, output_shp), 'TOPOID', 'TEXT', field_length=50)
        arcpy.AddField_management(os.path.join(output_dir, output_shp), 'KM_POCZ_M', 'DOUBLE')
        arcpy.AddField_management(os.path.join(output_dir, output_shp), 'KM_KON_M', 'DOUBLE')
        arcpy.AddField_management(os.path.join(output_dir, output_shp), 'TYP_BRANCH', 'TEXT', field_length=50)
        arcpy.AddField_management(os.path.join(output_dir, output_shp), 'MODEL', 'TEXT', field_length=254)

    # w tej sekcji następuje uzupełnienie warstwy shp danymi ze słownika branches
        arcpy.AddMessage("Zapisywanie poszczególnych branchy nwtworka do pliku {} w lokalizacji {}".format(output_shp, output_dir))
        for branch in branches:
            wsp = []
            for node in branches[branch][3]:
                # print(node, node[0])
                wsp.append(arcpy.Point(float(node[0]), float(node[1])))
            array = arcpy.Array(wsp)
            polyline = arcpy.Polyline(array)

        # dodawanie kolejnego brancha do warstwy shp
            cursor = arcpy.da.InsertCursor(os.path.join(output_dir, output_shp), ['SHAPE@', 'BRANCH', 'TOPOID', 'KM_POCZ_M', 'KM_KON_M', 'TYP_BRANCH','MODEL'])
            try:
                if len(branches[branch]) == 4:
                    cursor.insertRow([polyline, branch.replace("'",''), branches[branch][0].replace("'",''), float(branches[branch][1]), float(branches[branch][2]), 'rzeka/floodplain',output_dir])
                elif len(branches[branch]) == 5:
                    cursor.insertRow([polyline, branch.replace("'",''), branches[branch][0].replace("'",''), float(branches[branch][1]), float(branches[branch][2]), branches[branch][4],output_dir])
            except ValueError as e:
                arcpy.AddMessage("W branchu {} znalazł się znak specialny lub SPACJA. Zmień nazwę branchu w pliku nwk".format(branch))

        arcpy.AddMessage("W lokalizacji - {} - przekonwertowano network {} na warstwe przestrzenną {}".format(output_dir, os.path.basename(nwk_file),output_shp))
    else:
        arcpy.AddMessage(
            "Wskazana ścieżka do pliku - {} - nie wskazuje na plik network *.nwk.".format(nwk_file))
    return

def searchForNwk(in_folder):
    '''
    Funkcja do przeszukiwania folderu i jego podfolderów w celu sprawdzenia wystepowania plików *.nwk11 i zamiany ich na format *.shp
    '''
    if os.path.isdir(in_folder):
        arcpy.AddMessage("Przeszukiwanie - {} - w celu zamiany plików *.nwk11 na *.shp".format(in_folder))
        for root, dirs, files in os.walk(in_folder, topdown=False):
            #iteracja po plikach
            #print(u"Przeszukuję folder:"+"\n"+root)
            for name in files:
                #znajdywanie plikow zawierających okreslone rozszerzenie
                if name.endswith('.nwk11'):
                    nwk2shp(os.path.join(root, name))

    else:
        arcpy.AddMessage("Wskazana scieżka nie istnieje lub nie jest lokalizacją folderu")

if __name__ == "__main__":
    in_path = arcpy.GetParameterAsText(0)

    if os.path.isdir(in_path):
        searchForNwk(in_path)

    if os.path.isfile(in_path):
        nwk2shp(in_path)