# Copyright:   (c) twilk @Arcadis
# ArcGIS Version:   10
# Python Version:   2.7
# --------------------------------
import os
import sys
import arcpy
import traceback

# type of coordinates
CT_NONE = 0
CT_CENTER = 1
CT_ENDS = 2

# radius type
RT_RESISTANCE_RADIUS = 0
RT_HYDRAULIC_RADIUS_EFFECTIVE_AREA = 1
RT_HYDRAULIC_RADIUS_TOTAL_AREA = 2

EOCS = "*******************************"

# markers
MK_NONE = 0
MK_1 = 1
MK_2 = 2
MK_3 = 4
MK_4 = 8
MK_5 = 16
MK_6 = 32
MK_7 = 64

# buffer size for reading
CS_BUFFER_SIZE = 256


# helper types (not necesarrily used in CCrossSection though)
class tMarkerDef:
    def __init__(self):
        self.branch = ""
        self.chainage = 0
        self.id = ""
        self.begin = 0.0  # marker 1
        self.end = 0.0  # marker 3
        self.bottom = 0.0  # marker 2
        self.results = {}
        self.first = False
        self.last = False
        self.geom_begin = 0.0  # poczatek geometrii
        self.geom_end = 0.0  # koniec geometrii

    def __repr__(self):
        return "{0}<{5}> - {1} ({2}, {3}, {4})\n{6}\n".format(self.branch, self.chainage, self.begin, self.bottom,
                                                              self.end, self.id, repr(self.results))


class tXsID:
    def __init__(self, branch, chainage, id):
        self.branch = branch
        self.chainage = chainage
        self.id = id

    def __repr__(self):
        return "{0} - {1} - {2}\n".format(self.branch, self.chainage, self.id)


# one xsection point
class tCsPoint:
    def __init__(self, fX, fZ, fResistance, nMarkers):
        self.fX = fX;
        self.fZ = fZ;
        self.fResistance = fResistance;
        self.nMarkers = nMarkers;


# CCrossSection definition
class CCrossSection:
    def __init__(self):
        self.m_sTopoId = "";
        self.m_sRiverName = "";
        self.m_fChainage = 0.0;
        self.m_sSectionId = ""
        self.m_nCoordinatesType = CT_NONE;
        self.m_sCoordinates = "";
        self.m_bFlowDirection = 0;
        self.m_fFlowDirection = 0.0;
        self.m_fDatum = 0.0;
        self.m_bClosedSection = 0;
        self.m_nRadiusType = RT_RESISTANCE_RADIUS;
        self.m_bDivide = 0;
        self.m_fDivideLevel = 0.0;
        self.m_bAngle = 0;
        self.m_fAngle = 0.0;
        self.m_sResistanceNumbers = "   2  1     1.000     1.000     1.000    1.000    1.000"
        self.m_bInterpolated = 0;
        self.m_vProfile = [];

    def SaveFile(self, file):
        file.write(self.m_sTopoId)
        file.write("\n")
        file.write(self.m_sRiverName)
        file.write("\n")
        file.write("               ")
        file.write(str(self.m_fChainage))
        file.write("\n")
        file.write("COORDINATES")
        file.write("\n")
        file.write("    ")
        file.write(str(self.m_nCoordinatesType))
        file.write("    ")
        file.write(str(self.m_sCoordinates))
        file.write("\n")
        file.write("FLOW DIRECTION")
        file.write("\n")
        file.write("    ")
        file.write(str(self.m_bFlowDirection))
        if self.m_bFlowDirection == 1:
            file.write("   ")
            file.write(str(self.m_fFlowDirection))
        file.write("\n")
        file.write("DATUM")
        file.write("\n")
        file.write("      ")
        file.write(str(self.m_fDatum))
        file.write("\n")
        file.write("RADIUS TYPE")
        file.write("\n")
        file.write("    ")
        file.write(str(self.m_nRadiusType))
        file.write("\n")
        file.write("DIVIDE X-Section")
        file.write("\n")
        file.write(str(self.m_bDivide))
        if self.m_bDivide:
            file.write("   ")
            file.write(str(self.m_fDivideLevel))
        file.write("\n")
        file.write("SECTION ID")
        file.write("\n")
        file.write("    ")
        file.write(self.m_sSectionId)
        file.write("\n")
        file.write("INTERPOLATED")
        file.write("\n")
        file.write("    ")
        file.write(str(self.m_bInterpolated))
        file.write("\n")
        file.write("ANGLE")
        file.write("\n")
        file.write("    ")
        file.write(str(self.m_fAngle))
        file.write("   ")
        file.write(str(self.m_bAngle))
        file.write("\n")
        file.write("RESISTANCE NUMBERS")
        file.write("\n")
        file.write(self.m_sResistanceNumbers)
        file.write("\n")
        file.write("PROFILE")
        file.write("        ")
        file.write(str(len(self.m_vProfile)))
        file.write("\n")
        for it in self.m_vProfile:
            file.write("    ")
            file.write("%.3f" % (it.fX))
            file.write("   ")
            file.write("%.3f" % (it.fZ))
            file.write("     ")
            file.write("%.4f" % (it.fResistance))
            file.write("     <#")
            file.write(str(it.nMarkers))
            file.write(">")
            file.write("\n")

        file.write(EOCS)
        file.write("\n")

    def GetMarker(self, nMarker):
        for it in self.m_vProfile:
            if it.nMarkers == nMarker:
                return it
        return tCsPoint(0, 0, 0, MK_NONE)

    def MoveX(self, dX):
        for i, it in enumerate(self.m_vProfile):
            self.m_vProfile[i].fX = it.fX + dX


def FieldExist(featureclass, fieldname):
    fieldList = arcpy.ListFields(featureclass, fieldname)

    fieldCount = len(fieldList)

    if (fieldCount == 1):
        return True
    else:
        return False


def extent2Polygon(ext):
    XMAX = ext.XMax
    XMIN = ext.XMin
    YMAX = ext.YMax
    YMIN = ext.YMin
    pnt1 = arcpy.Point(XMIN, YMIN)
    pnt2 = arcpy.Point(XMIN, YMAX)
    pnt3 = arcpy.Point(XMAX, YMAX)
    pnt4 = arcpy.Point(XMAX, YMIN)
    array = arcpy.Array()
    array.add(pnt1)
    array.add(pnt2)
    array.add(pnt3)
    array.add(pnt4)
    array.add(pnt1)
    return arcpy.Polygon(array)


def getRasterValue(raster, point):
    try:
        result = arcpy.GetCellValue_management(raster, str(point.X) + ' ' + str(point.Y))
        r = result.getOutput(0)
        return float(r.replace(",", "."))
    except:
        # print "getRasterValue: Value error: {0}".format(r)
        return None


def locateMeasures(routes, points, fldRid, fldRKod, fldRzedna, tolerancja):
    outTbl = "in_memory/rtPts"
    pts = []

    arcpy.LocateFeaturesAlongRoutes_lr(points, routes, fldRid, tolerancja, outTbl)
    with arcpy.da.SearchCursor(outTbl, ["MEAS", fldRKod, fldRzedna], sql_clause=('', 'ORDER BY "MEAS"')) as cur:
        for row in cur:
            pts.append((row[0], row[2], kod2Manning(row[1])))
    arcpy.Delete_management(outTbl)
    pts.sort()
    return pts


def ProcessLine(river, topo, chain, xsID, selLayer, selRough, line_geometry, outFile, fldKm, fldRKod, fldRzedna,
                rtPrzekroje, tolerancja, strefyN):
    ptList = []
    maxZ = 0.0
    minZ = 9000.0

    arcpy.AddMessage("Rzutowanie punktow...")
    geod = locateMeasures(rtPrzekroje, "lyrPomiary", fldKm, fldRKod, fldRzedna, tolerancja)
    gminX = 10000
    gmaxX = -10000
    gminZ = 9000
    gminZs = 0

    # znalezienie min max X oraz minZ i X przy minZ
    for gpt in geod:
        if gpt[0] < gminX:
            gminX = gpt[0]
        if gpt[0] > gmaxX:
            gmaxX = gpt[0]
        if gpt[1] < gminZ:
            gminZ = gpt[1]
            gminZs = gpt[0]

    # arcpy.AddMessage(str(geod))
    # arcpy.AddMessage("Geodezja: minX = {0}, maxX = {1}, gminZ = {2}, gminZs = {3}".format(gminX,gmaxX,gminZ,gminZs))

    arcpy.AddMessage("Przygotowanie ograniczonych rastrow...")
    # clp_raster = os.path.join(arcpy.env.scratchGDB,arcpy.CreateScratchName("clip", "", "RasterDataset", arcpy.env.scratchGDB))
    clp_raster = arcpy.env.scratchFolder + "\\clp_raster.tif"
    if arcpy.Exists(clp_raster):
        arcpy.Delete_management(clp_raster)
    if arcpy.Exists("clp_layer"):
        arcpy.Delete_management("clp_layer")

    arcpy.Clip_management(selLayer, str(line_geometry.extent), clp_raster,
                          maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    arcpy.MakeRasterLayer_management(clp_raster, "clp_layer")
    # arcpy.StackProfile_3d(line_geometry,clp_raster,out_table)

    clp_RoughShp = "in_memory\\clp_RoughShp"
    if arcpy.Exists(clp_RoughShp):
        arcpy.Delete_management(clp_RoughShp)
    clp_RoughR = arcpy.env.scratchFolder + "\\clp_RoughR.tif"
    if arcpy.Exists(clp_RoughR):
        arcpy.Delete_management(clp_RoughR)
    if arcpy.Exists("lyrRoughR"):
        arcpy.Delete_management("lyrRoughR")

    arcpy.Clip_analysis(selRough, extent2Polygon(line_geometry.extent), clp_RoughShp)
    arcpy.PolygonToRaster_conversion(clp_RoughShp, "n_aMZP", clp_RoughR, "CELL_CENTER", cellsize=1.0)
    arcpy.MakeRasterLayer_management(clp_RoughR, "lyrRoughR")

    pos = 0
    delta = max(1, line_geometry.length / 5000)
    # print "Delta: {0}".format(delta)

    tot = int(line_geometry.length / delta)
    cnt = 0
    arcpy.AddMessage("Probkowanie rzednych i szorstkosci...")
    arcpy.SetProgressor("step", "Probkowanie rzednych i szorstkosci...", 0, tot, 1)

    while pos <= line_geometry.length:
        pt = line_geometry.positionAlongLine(pos).centroid
        val = getRasterValue("clp_layer", pt)
        n = getRasterValue("lyrRoughR", pt)
        if val:
            if not n:
                n = 0.03333333333333
            if val < minZ:
                minZ = val
            if val > maxZ:
                maxZ = val
            if pos and val and n:
                ptList.append((pos, val, n))
        pos += delta
        arcpy.SetProgressorPosition()
        cnt += 1
        # print "{0}/{1}".format(cnt,tot)
    arcpy.ResetProgressor()
    arcpy.AddMessage("Generalizacja przekroju NMT...")
    try:
        import rdp
        ptList = rdp.rdp(ptList, epsilon=0.05)
    except ImportError:
        arcpy.AddWarning(
            "Brak modulu rdp - generalizacja przekroju nie zostanie przeprowadzona.\n\nPrzykladowa komenda do instalacji modulu: \n\tC:\\Python27\\ArcGIS10.5\\Scripts\\easy_install rdp")

    cs = CCrossSection()

    cs.m_sRiverName = river
    cs.m_sTopoId = topo
    cs.m_fChainage = chain
    cs.m_sSectionId = xsID
    cs.m_nCoordinatesType = CT_ENDS
    cs.m_sCoordinates = "{0:.3f}  {1:.3f} {2:.3f}  {3:.3f}".format(line_geometry.firstPoint.X,
                                                                   line_geometry.firstPoint.Y,
                                                                   line_geometry.lastPoint.X, line_geometry.lastPoint.Y)

    # najpierw poczatek
    sum = 0
    sumN = 0
    for pt in ptList:
        if pt[0] >= gminX:
            break
        cs.m_vProfile.append(tCsPoint(pt[0], pt[1], pt[2], MK_NONE))
        sum += 1
        sumN += pt[2]
    if sum > 0:
        leftN = sumN / sum
    else:
        leftN = 0.0333333333333
    # srodek z geodezji
    bFirst = True

    prevX = 0.0
    sumlen = 0
    sumNlen = 0
    for pt in geod:
        if bFirst:
            bFirst = False
            cs.m_vProfile.append(tCsPoint(pt[0], pt[1], pt[2], MK_4))
            prevX = pt[0]
        else:
            if pt[0] == gminZs and pt[1] == gminZ:
                cs.m_vProfile.append(tCsPoint(pt[0], pt[1], pt[2], MK_2))
            else:
                cs.m_vProfile.append(tCsPoint(pt[0], pt[1], pt[2], MK_NONE))
            sumlen += pt[0] - prevX
            sumNlen += (pt[0] - prevX) * pt[2]
    if sumlen > 0:
        middleN = sumNlen / sumlen
    else:
        middleN = leftN
    cs.m_vProfile[len(cs.m_vProfile) - 1].nMarkers = MK_5
    # druga czesc przekroju
    sum = 0
    sumN = 0
    if len(geod) > 0:
        for pt in ptList:
            if pt[0] > gmaxX:
                cs.m_vProfile.append(tCsPoint(pt[0], pt[1], pt[2], MK_NONE))
                sum += 1
                sumN += pt[2]
    if sum > 0:
        rightN = sumN / sum
    else:
        rightN = leftN
    cs.m_vProfile[0].nMarkers = MK_1
    cs.m_vProfile[len(cs.m_vProfile) - 1].nMarkers = MK_3

    if strefyN:
        cs.m_sResistanceNumbers = "   1  1     1.000     {0:.3f}     {1:.3f}    {2:.3f}    1.000".format(leftN, middleN,
                                                                                                         rightN)

    arcpy.AddMessage("Dopisywanie przekroju do pliku...")
    with open(outFile, 'a') as f:
        cs.SaveFile(f)

    arcpy.Delete_management("clp_layer")
    arcpy.Delete_management(clp_raster)
    arcpy.Delete_management("lyrRoughR")
    arcpy.Delete_management(clp_RoughR)
    arcpy.Delete_management(clp_RoughShp)


def kod2Manning(kod):
    kody = {'K01': 0.035, "K02": 0.032, 'K03': 0.035, 'K04': 0.038, 'K05': 0.040, 'K06': 0.020, 'K07': 0.050,
            'K09': 0.070, 'K10': 0.100, 'T01': 0.025, 'T03': 0.120, 'T04': 0.080, 'T06': 0.120, 'T07': 0.045,
            'T08': 0.090, 'T09': 0.200, 'T10': 0.035, 'T11': 0.200, 'T12': 0.050, 'T14': 0.020, 'T15': 0.090,
            'T16': 0.100, 'T17': 0.300}
    if kod in kody:
        return kody[kod]
    else:
        return 0.033333333333


def generateXSs(lPrzekroje, fldKm, fldRivername, fldTopo, fldXsId, rNMT, lRoughness, fldN, lPomiary, fldRzedna, fldRKod,
                outFile, tolerancja, strefyN):
    """TODO: Add documentation about this function here"""
    # wyzerowanie pliku jesli istnial
    with open(outFile, 'w') as f:
        pass

    # sprawdzenie, czy w argumentach sa nazwy pol, czy wartosci
    bRivername = FieldExist(lPrzekroje, fldRivername)
    bTopo = FieldExist(lPrzekroje, fldTopo)
    bXsId = FieldExist(lPrzekroje, fldXsId)

    intermediate = []

    # wyselekcjonuj
    lsPrzekroje = "in_memory/lsPrzekroje"
    intermediate.append(lsPrzekroje)
    arcpy.Select_analysis(lPrzekroje, lsPrzekroje)
    lsPomiary = "in_memory/lsPomiary"
    intermediate.append(lsPomiary)
    arcpy.Select_analysis(lPomiary, lsPomiary)

    # przygotowanie route
    arcpy.AddMessage("Przygotowanie routes...")
    arcpy.AddField_management(lsPrzekroje, "rtStart", "FLOAT", 10, 3)
    arcpy.AddField_management(lsPrzekroje, "rtEnd", "FLOAT", 10, 3)
    arcpy.CalculateField_management(lsPrzekroje, "rtStart", "0.0", "PYTHON")
    arcpy.CalculateField_management(lsPrzekroje, "rtEnd", "!shape.length!", "PYTHON")
    rtPrzekroje = "in_memory/rtPrzekroje"
    intermediate.append(rtPrzekroje)
    arcpy.CreateRoutes_lr(lsPrzekroje, fldKm, rtPrzekroje, "TWO_FIELDS", "rtStart", "rtEnd")

    intermediate.append("lyrPomiary")
    arcpy.MakeFeatureLayer_management(lsPomiary, "lyrPomiary")

    # lista pol ze zmiennymi indeksami
    indeksy = {'r': -1, 't': -1, 'x': -1}
    i = 3
    fields = ["OID@", "SHAPE@", fldKm]

    if bRivername:
        indeksy['r'] = i
        i += 1
        fields.append(fldRivername)
    if bTopo:
        indeksy['t'] = i
        i += 1
        fields.append(fldTopo)
    if bXsId:
        indeksy['x'] = i
        i += 1
        fields.append(fldXsId)
    with arcpy.da.SearchCursor(lsPrzekroje, fields) as cur:
        for row in cur:
            oid = row[0]
            przekroj = row[1]
            chain = int(round(row[2]))
            river = row[indeksy['r']] if bRivername else fldRivername
            topo = row[indeksy['t']] if bTopo else fldTopo
            xsID = row[indeksy['x']] if bXsId else "km_{0:d}".format(chain)
            arcpy.AddMessage(">>> Przekroj {0}".format(oid))
            arcpy.SelectLayerByLocation_management('lyrPomiary', 'WITHIN_A_DISTANCE', przekroj,
                                                   "{0} Meters".format(tolerancja), "NEW_SELECTION")
            result = arcpy.GetCount_management('lyrPomiary')
            arcpy.AddMessage(
                "- znaleziono {0} punktow pomiarowych w odległości {1} metrow".format(result[0], tolerancja))
            try:
                ProcessLine(river, topo, chain, xsID, rNMT, lRoughness, przekroj, outFile, fldKm, fldRKod, fldRzedna,
                            rtPrzekroje, tolerancja, strefyN)
            except:
                arcpy.AddWarning("Przekroje w km {} na rzece {} wygenerowal blad.".format(chain, river))
                # Get the traceback object
                #
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]

                # Concatenate information together concerning the error into a message string
                #
                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"

                # Return python error messages for use in script tool or Python Window
                #
                arcpy.AddWarning(pymsg)
                arcpy.AddError(msgs)

                # Print Python error messages for use in Python / Python Window
                #
                print(pymsg)
                print(msgs)


# End do_analysis function

def PrepareDummyPts(punkty, szorstkosc, rzedna):
    arcpy.CreateFeatureclass_management(os.path.dirname(punkty), os.path.basename(punkty), "POINT")
    arcpy.AddField_management(punkty, szorstkosc, "TEXT", "", "", 5)
    arcpy.AddField_management(punkty, rzedna, "DOUBLE", 6, 3)


# This test allows the script to be used from the operating
# system command prompt (stand-alone), in a Python IDE,
# as a geoprocessing script tool, or as a module imported in
# another script
if __name__ == '__main__':
    lPrzekroje = arcpy.GetParameterAsText(0)
    fldKm = arcpy.GetParameterAsText(1)
    fldRivername = arcpy.GetParameterAsText(2)
    fldTopo = arcpy.GetParameterAsText(3)
    fldXsId = arcpy.GetParameterAsText(4)
    rNMT = arcpy.GetParameterAsText(5)
    lRoughness = arcpy.GetParameterAsText(6)
    fldN = arcpy.GetParameterAsText(7)
    lPomiary = arcpy.GetParameterAsText(8)
    fldRzedna = arcpy.GetParameterAsText(9)
    fldRKod = arcpy.GetParameterAsText(10)
    outFile = arcpy.GetParameterAsText(11)
    tolerancja = arcpy.GetParameterAsText(12)
    strefyN = (arcpy.GetParameterAsText(13).lower() == "true")

    if lPomiary == "" or lPomiary == "#":
        lPomiary = "in_memory/pomiary"
        if arcpy.Exists(lPomiary):
            arcpy.Delete_management(lPomiary)
        fldRzedna = "rzedna"
        fldRKod = "szorstkosc"
        PrepareDummyPts(lPomiary, fldRKod, fldRzedna)

    generateXSs(lPrzekroje, fldKm, fldRivername, fldTopo, fldXsId, rNMT, lRoughness, fldN, lPomiary, fldRzedna, fldRKod,
                outFile, tolerancja, strefyN)

    if lPomiary == "in_memory/pomiary":
        arcpy.Delete_management(lPomiary)
