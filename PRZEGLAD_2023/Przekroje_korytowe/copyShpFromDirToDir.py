import os
import shutil

# arcpy.env.parallelProcessingFactor = "50%"

def isNwk11In(files):
    for file in files:
        nazwa, rozszerzenie = os.path.splitext(file)
        rozszerzenie = rozszerzenie.lower()[1:]  # Usuń kropkę i zamień na małe litery

        if rozszerzenie == 'nwk11':
            return True

    return False

def searcCopyNwkShp(in_folder, out_folder):
    # Sprawdź, czy oba foldery istnieją
    if not os.path.exists(in_folder):
        print(f"Folder źródłowy '{in_folder}' nie istnieje.")
        return

    if not os.path.exists(out_folder):
        print(f"Tworzę folder docelowy '{out_folder}'.")
        os.makedirs(out_folder)

    # Pobierz listę plików w folderze źródłowym
    for root, dirs, files in os.walk(in_folder, topdown=False):
        if isNwk11In(files):
            for plik in files:
                nazwa, rozszerzenie = os.path.splitext(plik)

                if rozszerzenie in ['.cpg', '.dbf','.prj','.shp','.xml','.shx']:
                    in_dir = os.path.join(root, plik)
                    out_dir = os.path.join(out_folder, plik)

                    # Jeśli istnieje już plik o tej samej nazwie w docelowej lokalizacji
                    if os.path.exists(out_dir):
                        index = 1
                        while True:
                            # Modyfikuj nazwę pliku, dodając indeks przed rozszerzeniem
                            nowa_nazwa = f"{nazwa}_{index}{rozszerzenie}"
                            out_dir = os.path.join(out_folder, nowa_nazwa)

                            # Jeśli zmodyfikowana nazwa pliku nie istnieje w docelowej lokalizacji, przerwij pętlę
                            if not os.path.exists(out_dir):
                                break
                            index += 1

                    print(f"Kopiowanie '{plik}' do '{out_folder}'.")
                    shutil.copy(in_dir, out_dir)

def searcCopyShp(in_folder, out_folder,phraze):
    # Sprawdź, czy oba foldery istnieją
    if not os.path.exists(in_folder):
        print(f"Folder źródłowy '{in_folder}' nie istnieje.")
        return

    if not os.path.exists(out_folder):
        print(f"Tworzę folder docelowy '{out_folder}'.")
        os.makedirs(out_folder)

    # Pobierz listę plików w folderze źródłowym
    for root, dirs, files in os.walk(in_folder, topdown=False):
        for plik in files:
            if phraze in plik:
                nazwa, rozszerzenie = os.path.splitext(plik)

                if rozszerzenie in ['.cpg', '.dbf','.prj','.shp','.xml','.shx']:
                    in_dir = os.path.join(root, plik)
                    out_dir = os.path.join(out_folder, plik)

                    # Jeśli istnieje już plik o tej samej nazwie w docelowej lokalizacji
                    if os.path.exists(out_dir):
                        index = 1
                        while True:
                            # Modyfikuj nazwę pliku, dodając indeks przed rozszerzeniem
                            nowa_nazwa = f"{nazwa}_{index}{rozszerzenie}"
                            out_dir = os.path.join(out_folder, nowa_nazwa)

                            # Jeśli zmodyfikowana nazwa pliku nie istnieje w docelowej lokalizacji, przerwij pętlę
                            if not os.path.exists(out_dir):
                                break
                            index += 1

                    print(f"Kopiowanie '{plik}' do '{out_folder}'.")
                    shutil.copy2(in_dir, out_dir)
if __name__ == "__main__":

    folder1 = r'R:\Dane_PGW_WP_3M\10. Modele hydrauliczne\RW SW'
    folder2 = r'C:\robo\Przeglad_LOKAL_ROBO\MODELE\_Structures'
    fraza = '_BRIDGE'

    searcCopyShp(folder1,folder2,fraza)