#!/usr/bin/env python
# -*- coding: utf-8 -*-

# skrypt do zczytywania pliku cross section z MIKE11 (format TXT) do formatu dwoch plikow TXT o uporzadkowanej formie, ktore mozna wyeksportowac do tabeli

import os

file_input =\
    r"C:\Users\mgasior\Documents\Przedluzanie\Jeziorsko\S10_Warta.txt"

file_output = os.path.join(os.path.dirname(file_input),
                           os.path.basename(file_input).split('.')[0] + '_przetworzone_RD.txt')
file_output_lp = os.path.join(os.path.dirname(file_input),
                              os.path.basename(file_input).split('.')[0] + '_przetworzone_LP.txt')
file_output_hl = os.path.join(os.path.dirname(file_input),
                              os.path.basename(file_input).split('.')[0] + '_przetworzone_HL.txt')

counter = 0
counter_lp = None
counter_hl = 0
profile_counter = 0
cs_con = False
f = open(file_output, "w")
f_lp = open(file_output_lp, "w")
f_hl = open(file_output_hl, "w")

f.write(
    "RIVER" + '@' + "TOPO_ID" + '@' + "CHAINAGE" + '@' + "COORDINATES" + '@' + "COORD_X1" + '@' + "COORD_Y1" + '@' + "COORD_X2" + '@' + "COORD_Y2" + '@' + "FLOW_DIR" + '@' + "PROTECTION_DATA" + '@' + "DATUM" + '@' + "CLOSED_SECTION" + '@' + "RADIUS_TYPE" + '@' + "DIVIDE_X_SECTION"
    + '@' + "SECTION_ID" + '@' + "INTERPOLATED" + '@' + "ANGLE" + '@' + "RESIST_NO" + '@' + "PROFILE" + '@' + "XS_DL" + '@' + "XS_Z" + '@' + "XS_N" + '@' + "XS_MARKER" + '@' + "XS_UNK1" + '@' + "XS_UNK2" + '@' + "XS_UNK3" + "\n")

f_lp.write("RIVER" + '@' + "TOPO_ID" + '@' + "CHAINAGE" + '@' + "LEVEL_PARAMS" + "\n")

f_hl.write("RIVER" + '@' + "TOPO_ID" + '@' + "CHAINAGE" + '@' + "H_LEVEL" + '@' + "COUNT_LEVELS" + "\n")

file_txt = open(file_input, "r")
for line in file_txt:
    if line.rstrip('\n') == '*******************************':
        profile_counter += 1

print ('Liczba profili w pliku ' + str(profile_counter))
file_txt.close()

file_txt = open(file_input, "r")
for line in file_txt:
    if line.rstrip('\n') != '*******************************':
        counter += 1
    else:
        counter = 0
        profile_counter -= 1
        cs_con = False
        print (u'Pozostało ' + str(profile_counter))

    if line.rstrip('\n') == 'LEVEL PARAMS':
        counter_lp = counter

    try:
        if counter - counter_lp == 1:
            level_params = line.rstrip('\n')
            f_lp.write(str(river) + '@' + str(topo_id) + '@' + str(chainage) + '@' + level_params + '\n')
            counter_lp = None
            counter = -1
    except:
        pass

    if counter_hl < 0:
        h_level = line.rstrip('\n')
        f_hl.write(str(river) + '@' + str(topo_id) + '@' + str(chainage) + '@' + h_level + '@' + count_levels + '\n')
        counter_hl += 1
        counter = counter_hl
    try:
        if line.rstrip('\n').split()[0] == 'H-LEVELS':
            count_levels = line.rstrip('\n').split()[1]
            counter_hl = -float(line.rstrip('\n').split()[1])
            counter = -float(line.rstrip('\n').split()[1])
    except:
        pass

    if counter == 1:
        topo_id = line.rstrip('\n')
    if counter == 2:
        river = line.rstrip('\n')
    if counter == 3:
        chainage = float(line.rstrip('\n').split()[0])
    if counter == 5:
        coordinates = line.rstrip('\n')

        if len(line.rstrip('\n').split()) > 1:
            coordX1 = line.rstrip('\n').split()[1]
            coordY1 = line.rstrip('\n').split()[2]
            coordX2 = line.rstrip('\n').split()[3]
            coordY2 = line.rstrip('\n').split()[4]
        else:
            coordX1 = 0
            coordY1 = 0
            coordX2 = 0
            coordY2 = 0

    if counter == 7:
        flow_dir = float(line.rstrip('\n').split()[0])
    if counter == 9:
        protection_data = float(line.rstrip('\n').split()[0])
    if counter == 11:
        datum = float(line.rstrip('\n').split()[0])

    if line.rstrip('\n') == 'CLOSED SECTION':
        cs_con = True

    if cs_con is True:
        if counter == 13:
            closed_section = line.rstrip('\n')
        if counter == 15:
            radius_type = float(line.rstrip('\n').split()[0])
        if counter == 17:
            divide_xsection = float(line.rstrip('\n').split()[0])
        if counter == 19:
            section_id = line.rstrip('\n')
        if counter == 21:
            interpolated = line.rstrip('\n').split()[0]
        if counter == 23:
            angle = line.rstrip('\n')
        if counter == 25:
            resist_no = line.rstrip('\n')
        if counter == 26:
            print chainage
            profile = float(line.rstrip('\n').split()[1])

        # tutaj zaczyna się dodawanie do tabeli punktow z pliku txt na profilu
        if counter > 26 and line.rstrip('\n') != 'LEVEL PARAMS':
            xs_dl = float(line.rstrip('\n').split()[0])
            xs_z = float(line.rstrip('\n').split()[1])
            xs_n = float(line.rstrip('\n').split()[2])
            xs_mark = line.rstrip('\n').split()[3]
            xs_unk1 = float(line.rstrip('\n').split()[4])
            xs_unk2 = float(line.rstrip('\n').split()[5])
            xs_unk3 = float(line.rstrip('\n').split()[6])

            # row = (river, topo_id, chainage,  coordinates, flow_dir, protection_data, datum, radius_type, divide_xsection, section_id, interpolated, angle, resist_no, profile, xs_dl, xs_z, xs_n, xs_mark, xs_unk1, xs_unk2, xs_unk3)
            f.write(str(river) + '@' + str(topo_id) + '@' + str(chainage) + '@' + str(coordinates) + '@' + str(
                coordX1) + '@' + str(coordY1) + '@' + str(coordX2) + '@' + str(coordY2) + '@' + str(
                flow_dir) + '@' + str(protection_data) + '@' + str(datum) + '@' + str(closed_section) + '@' + str(
                radius_type) + '@' + str(divide_xsection)
                    + '@' + str(section_id) + '@' + str(interpolated) + '@' + str(angle) + '@' + str(
                resist_no) + '@' + str(profile) + '@' + str(xs_dl) + '@' + str(xs_z) + '@' + str(xs_n) + '@' + str(
                xs_mark) + '@' + str(xs_unk1) + '@' + str(xs_unk2) + '@' + str(xs_unk3) + "\n")
    else:
        closed_section = 'NIE DOTYCZY'

        if counter == 13:
            radius_type = float(line.rstrip('\n').split()[0])
        if counter == 15:
            divide_xsection = float(line.rstrip('\n').split()[0])
        if counter == 17:
            section_id = line.rstrip('\n')
        if counter == 19:
            interpolated = line.rstrip('\n').split()[0]
        if counter == 21:
            angle = line.rstrip('\n')
        if counter == 23:
            resist_no = line.rstrip('\n')
        if counter == 24:
            print chainage
            profile = float(line.rstrip('\n').split()[1])

        if counter > 24 and line.rstrip('\n') != 'LEVEL PARAMS':
            xs_dl = float(line.rstrip('\n').split()[0])
            xs_z = float(line.rstrip('\n').split()[1])
            xs_n = float(line.rstrip('\n').split()[2])
            xs_mark = line.rstrip('\n').split()[3]
            xs_unk1 = float(line.rstrip('\n').split()[4])
            xs_unk2 = float(line.rstrip('\n').split()[5])
            xs_unk3 = float(line.rstrip('\n').split()[6])

            # row = (river, topo_id, chainage,  coordinates, flow_dir, protection_data, datum, radius_type, divide_xsection, section_id, interpolated, angle, resist_no, profile, xs_dl, xs_z, xs_n, xs_mark, xs_unk1, xs_unk2, xs_unk3)
            f.write(str(river) + '@' + str(topo_id) + '@' + str(chainage) + '@' + str(coordinates) + '@' + str(
                coordX1) + '@' + str(coordY1) + '@' + str(coordX2) + '@' + str(coordY2) + '@' + str(
                flow_dir) + '@' + str(protection_data) + '@' + str(datum) + '@' + str(closed_section) + '@' + str(
                radius_type) + '@' + str(divide_xsection)
                    + '@' + str(section_id) + '@' + str(interpolated) + '@' + str(angle) + '@' + str(
                resist_no) + '@' + str(profile) + '@' + str(xs_dl) + '@' + str(xs_z) + '@' + str(xs_n) + '@' + str(
                xs_mark) + '@' + str(xs_unk1) + '@' + str(xs_unk2) + '@' + str(xs_unk3) + "\n")

file_txt.close()
f_lp.close()
f_hl.close()
f.close()
