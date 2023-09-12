# !/usr/bin/env python
# -*- coding: utf-8 -*-

# skrypt do wsadowego przeszukiwania, wypakowywania i kopiowania plikow w folderach

import shutil
import zipfile
import os


def find_copy(in_folder, out_folder, phrase):

    for root, dirs, files in os.walk(in_folder, topdown=False):
        #iteracja po plikach
        print(u"Przeszukuję folder:"+"\n"+root)
        for name in files:
          ###print(os.path.join(root, name))
        #znajdywanie plikow zawierających okreslona fraze i kopiowanie ich do nowej loklaizacji
          if phrase in name:
            shutil.copy2(os.path.join(root, name),out_folder)

def search(in_folder,file_ext):

    for root, dirs, files in os.walk(in_folder, topdown=False):
        #iteracja po plikach
        #print(u"Przeszukuję folder:"+"\n"+root)
        for name in files:
            #znajdywanie plikow zawierających okreslone rozszerzenie
            if name.endswith(file_ext[0]) or name.endswith(file_ext[1]):
                print(os.path.join(root, name) +'#'+name)
                file = os.path.join(root, name)


def search_and_extract(in_folder, phrase, out_folder):
    for root, dirs, files in os.walk(in_folder):
        for file in files:
            if file.endswith('.zip'):
                zip_path = os.path.join(root, file)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    for member in zip_ref.namelist():
                        if phrase in member:
                            # extracted_path = os.path.join(out_folder, file.replace('.zip', ''), member)
                            # os.makedirs(os.path.dirname(extracted_path), exist_ok=True)
                            # zip_ref.extract(member, extracted_path)
                            os.makedirs(os.path.dirname(out_folder), exist_ok=True)
                            zip_ref.extract(member, out_folder)
                            print("Wypakowano plik {0} z pliku {1}".format(member, file))


def search_and_rename(in_folder, in_sign, out_sign):
    '''
    funkcja zamienia nazwy plików w folderze według zadanych znaków
    '''
    for root, dirs, files in os.walk(in_folder):
        for file in files:
            new_file = os.path.splitext(file)[0].replace(in_sign,out_sign)+os.path.splitext(file)[1]
            print([file, new_file])
            os.rename(os.path.join(root,file), os.path.join(root,new_file))

if __name__ == '__main__':
  in_folder = r'C:\robo\_warstwy_tymczasowe\bdot\14'
  out_folder = r'P:\02_Pracownicy\Kubiak\aPMZP\Dane\BDOT_aktualny\Pokrycie_Mazowieckie'
  fraza = "_OT_PT"
#   search_and_extract(in_folder, fraza, out_folder)
  search_and_rename(out_folder,'.','_')
