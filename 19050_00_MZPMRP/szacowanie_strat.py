#!/usr/bin/env python
#-*- coding: utf-8 -*-

#skrypt do okreslania rzedowosci rzek zgodnie z metodyką Strahlera w bazie MPHP

import arcpy

arcpy.env.overwriteOutput = True

"""parametry programu"""

#geobaza robocza
workspace = arcpy.env.workspace = r"R:\OIIS_KR5\_PROJEKTY 2020\20029-00_Mapy_Budowle_cz2\07.GIS\4_Opracowanie_baz_danych\_Warstwy_opracowywane\MRP_E1_robo.gdb"

luz_dol = {'1': 193.51, '2': 338.64, '3': 580.53, '4': 919.18}
gest_dol = {'1': 248.8, '2': 435.4, '3': 745.5, '4': 1181.8}
przem_dol = {'1': 295.97, '2': 591.93, '3': 887.90, '4': 1183.87}
dolnoslaskie = {'1': {'Zwr': gest_dol, 'Gst': gest_dol, 'Luz': luz_dol}, '2': przem_dol, '6': 0.31, '7': 0.08}

luz_mp = {'1': 143.93, '2': 251.88, '3': 431.80, '4': 683.69}
gest_mp = {'1': 185.06, '2': 323.85, '3': 555.17, '4': 879.03}
przem_mp = {'1': 370.12, '2': 740.24, '3': 1110.36, '4': 1480.48}
malopolskie = {'1': {'Zwr': gest_mp, 'Gst': gest_mp, 'Luz': luz_mp}, '2': przem_mp, '6': 0.4, '7': 0.08}

luz_slk = {'1': 208.07, '2': 364.13, '3': 624.22, '4': 988.35}
gest_slk = {'1': 267.52, '2': 468.17, '3': 802.57, '4': 1270.74}
przem_slk = {'1': 334.34, '2': 668.69, '3': 1003.03, '4': 1337.37}
slaskie = {'1': {'Zwr': gest_slk, 'Gst': gest_slk, 'Luz': luz_slk}, '2': przem_slk, '6': 0.33, '7': 0.1}

luz_sw = {'1': 72.38, '2': 126.67, '3': 217.15, '4': 343.82}
gest_sw = {'1': 93.06, '2': 162.86, '3': 279.19, '4': 442.05}
przem_sw = {'1': 295.16, '2': 590.33, '3': 885.49, '4': 1180.66}
swietokrzyskie = {'1': {'Zwr': gest_sw, 'Gst': gest_sw, 'Luz': luz_sw}, '2': przem_sw, '6': 0.37, '7': 0.07}

luz_pod = {'1': 82.97, '2': 145.20, '3': 248.91, '4': 394.11}
gest_pod = {'1': 106.68, '2': 186.68, '3': 320.03, '4': 506.71}
przem_pod = {'1': 353.01, '2': 706.02, '3': 1059.03, '4': 1412.04}
podkrpackie = {'1': {'Zwr': gest_pod, 'Gst': gest_pod, 'Luz': luz_pod}, '2': przem_pod, '6': 0.26, '7': 0.06}

luz_lodz = {'1': 110.22, '2': 192.88, '3': 330.66, '4': 523.54}
gest_lodz = {'1': 141.71, '2': 247.99, '3': 425.13, '4': 673.12}
przem_lodz = {'1': 452.44, '2': 904.88, '3': 1357.32, '4': 1809.76}
lodzkie = {'1': {'Zwr': gest_lodz, 'Gst': gest_lodz, 'Luz': luz_lodz}, '2': przem_lodz, '6': 0.32, '7': 0.1}

luz_lub = {'1': 60.88, '2': 106.54, '3': 182.64, '4': 289.18}
gest_lub = {'1': 78.27, '2': 136.98, '3': 234.82, '4': 371.81}
przem_lub = {'1': 329.85, '2': 659.71, '3': 989.56, '4': 1319.41}
lubelskie = {'1': {'Zwr': gest_lub, 'Gst': gest_lub, 'Luz': luz_lub}, '2': przem_lub, '6': 0.33, '7': 0.09}

luz_opo = {'1': 105.5, '2': 184.63, '3': 316.5, '4': 501.13}
gest_opo = {'1': 135.64, '2': 237.38, '3': 406.93, '4': 644.31}
przem_opo = {'1': 249.02, '2': 498.03, '3': 747.05, '4': 996.06}
opolskie = {'1': {'Zwr': gest_opo, 'Gst': gest_opo, 'Luz': luz_opo}, '2': przem_opo, '6': 0.34, '7': 0.1}

luz_kp = {'1': 118.02, '2': 206.54, '3': 354.07, '4': 560.61}
gest_kp = {'1': 151.74, '2': 265.55, '3': 455.23, '4': 720.78}
przem_kp = {'1': 270.23, '2': 540.47, '3': 810.7, '4': 1080.94}
kujawsko_pom = {'1': {'Zwr': gest_kp, 'Gst': gest_kp, 'Luz': luz_kp}, '2': przem_kp, '6': 0.3, '7': 0.09}

luz_maz = {'1': 191.63, '2': 335.36, '3': 574.90, '4': 910.27}
gest_maz = {'1': 246.39, '2': 431.18, '3': 739.16, '4': 1170.34}
przem_maz = {'1': 514.69, '2': 1029.38, '3': 1544.07, '4': 2058.75}
mazowieckie = {'1': {'Zwr': gest_maz, 'Gst': gest_maz, 'Luz': luz_maz}, '2': przem_maz, '6': 0.37, '7': 0.08}

luz_wlk = {'1': 154.8876, '2': 271.0533, '3': 464.6628, '4': 735.7161}
gest_wlk = {'1': 199.1412, '2': 348.4971, '3': 597.4236, '4': 945.9207}
przem_wlk = {'1': 431.55, '2': 863.1, '3': 1294.65, '4': 1726.2}
wielkopolskie = {'1': {'Zwr': gest_wlk, 'Gst': gest_wlk, 'Luz': luz_wlk}, '2': przem_wlk, '6': 0.3, '7': 0.09}

luz_pom = {'1': 166.45, '2': 291.29, '3': 499.35, '4': 790.63}
gest_pom = {'1': 214.01, '2': 374.51, '3': 642.02, '4': 1016.53}
przem_pom = {'1': 379.13, '2': 758.25, '3': 1137.38, '4': 1516.51}
pomorskie = {'1': {'Zwr': gest_pom, 'Gst': gest_pom, 'Luz': luz_pom}, '2': przem_pom, '6': 0.26, '7': 0.08}

luz_lb = {'1': 111.15, '2': 194.51, '3': 333.44, '4': 527.94}
gest_lb = {'1': 142.9, '2': 250.08, '3': 428.71, '4': 678.78}
przem_lb = {'1': 432.71, '2': 865.42, '3': 1298.13, '4': 1730.84}
lubuskie = {'1': {'Zwr': gest_lb, 'Gst': gest_lb, 'Luz': luz_lb}, '2': przem_lb, '6': 0.31, '7': 0.08}

luz_zpom = {'1': 156.74, '2': 274.29, '3': 470.22, '4': 744.51}
gest_zpom = {'1': 201.52, '2': 352.66, '3': 604.56, '4': 957.22}
przem_zpom = {'1': 164.6, '2': 329.19, '3': 493.79, '4': 658.38}
zachodniopomorskie = {'1': {'Zwr': gest_zpom, 'Gst': gest_zpom, 'Luz': luz_zpom}, '2': przem_zpom, '6': 0.27, '7': 0.08}

luz_podl = {'1': 67.1, '2': 117.42, '3': 201.3, '4': 318.72}
gest_podl = {'1': 86.27, '2': 150.97, '3': 258.81, '4': 409.78}
przem_podl = {'1': 289.18, '2': 578.37, '3': 867.55, '4': 1156.74}
podlaskie = {'1': {'Zwr': gest_podl, 'Gst': gest_podl, 'Luz': luz_podl}, '2': przem_podl, '6': 0.18, '7': 0.1}

luz_wm = {'1': 78.85, '2': 137.99, '3': 236.55, '4': 374.54}
gest_wm = {'1': 101.38, '2': 177.41, '3': 304.14, '4': 481.55}
przem_wm = {'1': 299.69, '2': 599.37, '3': 899.06, '4': 1198.74}
warminskomazurskie = {'1': {'Zwr': gest_wm, 'Gst': gest_wm, 'Luz': luz_wm}, '2': przem_wm, '6': 0.24, '7': 0.1}

straty = {u'dolnośląskie': dolnoslaskie,
          u'małopolskie': malopolskie,
          u'śląskie': slaskie,
          u'świętokrzyskie': swietokrzyskie,
          u'podkarpackie': podkrpackie,
          u'łódzkie': lodzkie,
          u'opolskie': opolskie,
          u'lubelskie': lubelskie,
          u'kujawsko-pomorskie': kujawsko_pom,
          u'mazowieckie': mazowieckie,
          u'wielkopolskie': wielkopolskie,
          u'pomorskie': pomorskie,
          u'lubuskie': lubuskie,
          u'zachodniopomorskie': zachodniopomorskie,
          u'podlaskie': podlaskie,
          u'warmińsko-mazurskie': warminskomazurskie
          }

walk = arcpy.da.Walk(workspace, datatype="FeatureClass", type="Polygon")

for dirpath, dirnames, filenames in walk:
    for filename in filenames:
        if 'Goczalkowice' in filename:
            #NAZWA to nazwa wojewodztwa
            with arcpy.da.UpdateCursor(filename, ['GLEBOKOSC', 'CHARAKT', 'NAZWA', 'ID_KLAS', 'STRATY', 'STRATY_2', 'SHAPE_Area'])as cur:
                for row in cur:
                    if row[3] == '1':
                        row[4] = straty[unicode(row[2])][row[3]][row[1]][row[0]]
                    elif row[3] == '2':
                        row[4] = straty[unicode(row[2])][row[3]][row[0]]
                    elif row[3] == '3' and row[0] == '1':
                        row[4] = 35.85
                        row[1] = 'ND'
                    elif row[3] == '3' and row[0] != '1':
                        row[4] = 71.7
                        row[1] = 'ND'
                    elif row[3] == '4':
                        row[4] = 0.04
                        row[1] = 'ND'
                    elif row[3] == '5':
                        row[4] = 8
                        row[1] = 'ND'
                    elif row[3] == '6':
                        row[4] = straty[row[2]][row[3]]
                        row[1] = 'ND'
                    elif row[3] == '7':
                        row[4] = straty[row[2]][row[3]]
                        row[1] = 'ND'
                    else:
                        row[4] = -7777
                        row[1] = 'ND'

                    if row[3] in ['1', '2', '3', '4', '5', '6', '7']:
                        row[5] = round(row[4]*round(row[6], 4), 0)
                    else:
                        row[5] = -7777

                    cur.updateRow(row)
            del cur
        print("koniec " + filename)
