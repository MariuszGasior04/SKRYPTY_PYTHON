import os
import sys
import re




try:
    import arcpy
    arcpy.env.overwriteOutput = True
except:
    #komunikaty przy braku arcpy
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
    #wynik sprawdzenia
    result = True

    #sprawdzenie wersji Pythona
    if sys.version_info.major != 3:
        result = False
        arcpy.AddWarning("Wymagany jest Python 3")
    
    return result

def getNetwork(nwkFile):
    '''
    Funkcja wczytuje geometrie sieci z pliku nwk zwracajac slowniki dla punktow i branchy
    '''
    network = {'pts':{},'branches':{},'projection':""}
    insidePointSection = False
    insideBranchSection = False
    curBranch = ""
    try:
        with open(nwkFile,"r") as f:
            for line in f.readlines():
                if 'PROJCS' in line:
                    res = re.search('PROJCS\["([^"]+)"',line)
                    if res:
                        network["projection"] = res.group(1)
                #poszukiwanie punktowe
                if '[POINTS]' in line:
                    insidePointSection = True
                    continue
                if 'EndSect' in line and "POINTS" in line:
                    insidePointSection = False
                    continue
                if insidePointSection and "point" in line:
                    res = re.search('point ?= ?([0-9]+), ?([0-9.]+), ?([0-9.]+), ?[0-9], ?([0-9.]+),',line)
                    if res:
                        network['pts'][res.group(1)] = (float(res.group(2)),float(res.group(3)),float(res.group(4)))#[nr_punktu] = (x,y,chainage)
                    continue
                if "[branch]" in line:
                    insideBranchSection = True
                    continue
                if 'EndSect' in line and 'branch' in line:
                    insideBranchSection=False
                    continue
                if insideBranchSection and 'definitions' in line:
                    res = re.search('definitions ?= ?\'([^\']+)\'',line)
                    if res:
                        curBranch = res.group(1)
                    continue
                if insideBranchSection and "points" in line:
                    network['branches'][curBranch] = [x.strip() for x in re.split(', ?',line.replace('points = ',''))]

    except:
        arcpy.AddError("Blad przy odczycie z pliku {}".format(nwkFile))
    return network

def RemoveNonAscii(s):
    #return re.sub(r'[^\x00-\x7f]',r' ',s)
    return s

def getBoundaries(bndFile):
    '''
    Funkcja wczytuje warunki brzegowe z pliku bnd11
    '''
    arcpy.AddMessage("Analiza pliku {}".format(bndFile))
    bnd = []
    try:
        with open(bndFile,'r') as f:
            for line in f.readlines():
                if "DescType = " in line:
                    res = re.search("DescType ?= ?([0-9]), ?([0-9]), ?'([^']+)', ?([0-9.]+), ?([0-9.]*), ?'[^']*', ?'([^']*)'",line)
                    if res:
                        #typ warunku
                        typ = ""
                        if res.group(1) == "0":
                            typ = "Open"
                        elif res.group(1) == "1":
                            typ = "Point Source"
                        elif res.group(1) == "2":
                            typ = "Distributed Source"
                        elif res.group(1) == "3":
                            typ = "Global"
                        elif res.group(1) == "4":
                            typ = "Structures"
                        elif res.group(1) == "5":
                            typ = "Closed"
                        else:
                            typ = "Unrecognized boundary description"
                        typ2 =  "Unrecognized boundary type"
                        if res.group(2) == "0":
                            if typ == "Open":
                                typ2 = "Bottom Level"
                            elif typ == "Point Source":
                                typ2 = "Inflow"
                            elif typ == "Distributed Source":
                                typ2 = "Evaporation"
                            elif typ == "Closed":
                                typ2 = ""
                        elif res.group(2) == "1":
                            if typ == "Open":
                                typ2 = "Inflow"
                            elif typ == "Point Source":
                                typ2 = "Sediment Transport"
                            elif typ == "Distributed Source":
                                typ2 = "Heat Balance"
                            elif typ == "Closed":
                                typ2 = ""
                        elif res.group(2) == "2":
                            if typ == "Open":
                                typ2 = "Q-h"
                            elif typ == "Distributed Source":
                                typ2 = "Inflow"
                            elif typ == "Closed":
                                typ2 = ""
                        elif res.group(2) == "3":
                            if typ == "Open":
                                typ2 = "Sediment Supply"
                            elif typ == "Distributed Source":
                                typ2 = "Rainfall"
                            elif typ == "Closed":
                                typ2 = ""
                        elif res.group(2) == "4":
                            if typ == "Open":
                                typ2 = "Sediment Transport"
                            elif typ == "Distributed Source":
                                typ2 = "Resistance Factor"
                            elif typ == "Closed":
                                typ2 = ""
                        elif res.group(2) == "5":
                            if typ == "Open":
                                typ2 = "Water Level"
                            elif typ == "Distributed Source":
                                typ2 = "Wind Field"
                            elif typ == "Closed":
                                typ2 = ""
                        else:
                            typ = "Unrecognized boundary type"
                        branch = res.group(3)
                        chStart = float(res.group(4))
                        try:
                            chEnd = float(res.group(5))
                        except:
                            chEnd = 0
                        if typ == "Distributed Source":
                            chStart,chEnd = min(chStart,chEnd), max(chStart,chEnd)
                        label = RemoveNonAscii(res.group(6))
                        bnd.append((branch,chStart,chEnd,typ,typ2,label))
    except:
        arcpy.AddError("Blad otwarcia pliku bnd11")
    return bnd


def GetLocation(nwkData, branch, chainage):
    if not branch in nwkData['branches'].keys():
        arcpy.AddWarning("{} [z pliku bnd] brak w nwk.".format(branch))
        return None
    for i in range(1,len(nwkData['branches'][branch])):
        prevCh = nwkData['branches'][branch][i-1]
        nextCh = nwkData['branches'][branch][i]
        prevPtObj = nwkData['pts'][prevCh]
        nextPtObj = nwkData['pts'][nextCh]
        
        if i == 1 and prevPtObj[2] > chainage:
            arcpy.AddMessage(i)
            arcpy.AddWarning("Brak kilometrazu {} w branchu {} w nwk (--)".format(chainage,branch))
            return None
        #arcpy.AddMessage("{} <= {} < {}".format(prevPtObj[2],chainage,nextPtObj[2]))
        #arcpy.AddMessage("{} - {}".format(prevPtObj[2] <= chainage,nextPtObj[2] >= chainage))
        if prevPtObj[2] <= chainage and nextPtObj[2] >= chainage:
            scale = (chainage - prevPtObj[2])/(nextPtObj[2] - prevPtObj[2])
            ptX = prevPtObj[0] + scale* (nextPtObj[0] - prevPtObj[0])
            ptY = prevPtObj[1] + scale* (nextPtObj[1] - prevPtObj[1])
            return (ptX,ptY)
    arcpy.AddWarning("Brak kilometrazu {} w branchu {} w nwk (++)".format(branch,chainage))
    return None

def GetLineLocation(nwkData,branch,chStart,chEnd):
    pts = []
    if not branch in nwkData['branches'].keys():
        arcpy.AddWarning("{} [z pliku bnd] brak w nwk.".format(branch))
        return None
    for i in range(1,len(nwkData['branches'][branch])):
        prevCh = nwkData['branches'][branch][i-1]
        nextCh = nwkData['branches'][branch][i]
        prevPtObj = nwkData['pts'][prevCh]
        nextPtObj = nwkData['pts'][nextCh]

        if prevPtObj[2] <= chStart and nextPtObj[2] >= chStart:
            scale = (chStart - prevPtObj[2])/(nextPtObj[2] - prevPtObj[2])
            ptX = prevPtObj[0] + scale* (nextPtObj[0] - prevPtObj[0])
            ptY = prevPtObj[1] + scale* (nextPtObj[1] - prevPtObj[1])
            pts.append((ptX,ptY))
        if prevPtObj[2] <= chEnd and nextPtObj[2] >= chEnd:
            scale = (chEnd - prevPtObj[2])/(nextPtObj[2] - prevPtObj[2])
            ptX = prevPtObj[0] + scale* (nextPtObj[0] - prevPtObj[0])
            ptY = prevPtObj[1] + scale* (nextPtObj[1] - prevPtObj[1])
            pts.append((ptX,ptY))
            return pts
        if nextPtObj[2] >= chStart and nextPtObj[2] <= chEnd:
            pts.append((nextPtObj[0],nextPtObj[1]))
    return pts



def CreateOutputFC(pt, ln, projection):
    arcpy.management.CreateFeatureclass(os.path.dirname(pt),os.path.basename(pt), 'POINT', spatial_reference = projection)
    arcpy.management.AddField(pt,"branch", 'TEXT',field_length=50)
    arcpy.management.AddField(pt,"chainage", 'FLOAT')
    arcpy.management.AddField(pt,"t1", 'TEXT',field_length=20)
    arcpy.management.AddField(pt,"t2", 'TEXT',field_length=20)
    arcpy.management.AddField(pt,"bndId", 'TEXT',field_length=60)

    arcpy.management.CreateFeatureclass(os.path.dirname(ln),os.path.basename(ln), 'POLYLINE', spatial_reference = projection)
    arcpy.management.AddField(ln,"branch", 'TEXT',field_length=50)
    arcpy.management.AddField(ln,"chStart", 'FLOAT')
    arcpy.management.AddField(ln,"chEnd", 'FLOAT')
    arcpy.management.AddField(ln,"t1", 'TEXT',field_length=20)
    arcpy.management.AddField(ln,"t2", 'TEXT',field_length=20)
    arcpy.management.AddField(ln,"bndId", 'TEXT',field_length=60)

def ExportBndToShp(simFile,ptPath,lnPath):

    arcpy.AddMessage("Analiza pliku {}".format(simFile))
    baseFolder = os.path.dirname(simFile)
    nwkPath = ""
    bndPath = ""
    try:
        with open(simFile,'r') as f:
            txtSim = f.read()
            result = re.search('\[Input\].*nwk = \|([^|]*)\|.*bnd = \|([^|]*)\|',txtSim,re.S)
            if result:
                nwkPath = os.path.join(baseFolder,result.group(1))
                bndPath = os.path.join(baseFolder,result.group(2))
                arcpy.AddMessage("Znalezione pliki:\n nwk: {}\nbnd: {}".format(nwkPath,bndPath))
            else:
                arcpy.AddError("Blad w pliku sim11")
                return
        
    except:
        arcpy.AddError("Mike nie moze otworzyc pliku: {}".format(simFile))
        arcpy.AddError(traceback.format_exc())
        return
    nwk = getNetwork(nwkPath)
    #arcpy.AddMessage(str(nwk))
    bnd = getBoundaries(bndPath)
    #arcpy.AddMessage(str(bnd))

    CreateOutputFC(ptPath,lnPath,nwk['projection'])
    with arcpy.da.InsertCursor(ptPath,["SHAPE@","branch","chainage","t1","t2","bndId"]) as ptCur:
        with arcpy.da.InsertCursor(lnPath,["SHAPE@","branch","chStart","chEnd","t1","t2","bndId"]) as lnCur:
            for b in bnd:
                row = []
                #type
                if b[3] in ('Open', 'Point Source'):
                    loc =  GetLocation(nwk,b[0],b[1])
                    if loc is None:
                        arcpy.AddWarning("Nie znaleziono lokalizacji w nwk: {} {}".format(b[0],b[1]))
                        continue               
                    row.append(arcpy.PointGeometry(arcpy.Point(loc[0],loc[1])))#branch,chainage
                    row.append(b[0])
                    row.append(b[1])
                    row.append(b[3])
                    row.append(b[4])
                    row.append(b[5])
                    ptCur.insertRow(row)
                elif b[3] == "Distributed Source":
                    locList = GetLineLocation(nwk,b[0],b[1],b[2]);
                    if len(locList) < 2:
                        arcpy.AddWarning("Nie znaleziono lokalizacji w nwk: {} {} - {}".format(b[0], b[1], b[2]))
                        continue
                    row.append(arcpy.Polyline(arcpy.Array([arcpy.Point(x[0],x[1]) for x in locList]))) #branch,chainage
                    row.append(b[0])
                    row.append(b[1])
                    row.append(b[2])
                    row.append(b[3])
                    row.append(b[4])
                    row.append(b[5])
                    lnCur.insertRow(row)
    
    #dodanie do aktualnej mapy
    

    aprx = arcpy.mp.ArcGISProject('CURRENT')
    if aprx.activeMap: #jesli jest jakis widok mapowy
        lyrPoint = aprx.activeMap.addDataFromPath(ptPath)
        lyrLine = aprx.activeMap.addDataFromPath(lnPath)
    
    
        
    #arcpy.AddMessage(str(GetLineLocation(nwk,"MYSLA",0.0,150.0)))


if __name__ == "__main__":

    lyrxPoint = os.path.join(os.path.dirname(os.path.abspath(__file__)),"bnd_pt.lyrx")
    lyrxLine = os.path.join(os.path.dirname(os.path.abspath(__file__)),"bnd_ln.lyrx")

    arcpy.SetParameterSymbology(1,lyrxPoint)
    arcpy.SetParameterSymbology(2,lyrxLine)

    sim_path = arcpy.GetParameterAsText(0)
    out_point = arcpy.GetParameterAsText(1)
    out_linie = arcpy.GetParameterAsText(2)


    #sprawdzamy czy wszystko jest
    if (not checkPrerequisites()):
        arcpy.AddError("Brak wymaganych skladnikow.")
    else:
        if os.path.isfile(sim_path):
            ExportBndToShp(sim_path, out_point,out_linie)
        else:
            arcpy.AddError("Brak pliku sim w podanej lokalizacji: {}".format(sim_path))

    
    