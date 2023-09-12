import zal5_formatter_lk201
import zal5_formatter_piekielko
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from functools import partial


def browseFiles(E1, B2):
    filename = filedialog.askopenfilename(initialdir='/',
                                        title="Select a File",
                                        filetypes=(("MS Excell files",
                                                    "*.xls*, *.xlsx*"),
                                                   ("all files",
                                                    "*.*")))
    E1.delete(0, tk.END)
    E1.insert(tk.END, filename)
    B2['state'] = 'normal'

def submit104():
    folder = folder_excell104.get()

    zal5_formatter_piekielko.rewriteDraftXls(os.path.dirname(folder), os.path.basename(folder), zal5_formatter_piekielko.createTemplateXlsx(os.path.dirname(folder)))
    info = 'W lokalizacji "{0}" utworzono wykaz "Wykaz załacznik 5 - przetworzony wykaz GIS.xlsx"'.format(folder)
    messagebox.showinfo("Info", info)

def openLK104():
    root1 = tk.Toplevel(master)
    root1.title("Przeformatowanie wykazu GIS na wykaz docelowy dla LK 104")

    L0=tk.Label(root1, text="Wykaz dla LK104")
    L0.grid(row=0, column=1)
    E1=tk.Entry(root1, textvariable=folder_excell104, width=100, borderwidth=3)
    E1.grid(row=1, column=1)

    B2=tk.Button(root1, text="Formatuj", image=xicon, command=submit104)
    B2['state']='disabled'
    B2.grid(row=4, column=2)

    B1=tk.Button(root1, text="Wyszukaj wykaz", command=partial(browseFiles, E1, B2))
    B1.grid(row=1, column=2)

def submit201():
    folder = folder_excell201.get()
    zal5_formatter_lk201.mergeCells(os.path.dirname(folder), zal5_formatter_lk201.rewriteDraftXls(os.path.dirname(folder), os.path.basename(folder), zal5_formatter_lk201.createTemplateXlsx(os.path.dirname(folder))))
    info = 'W lokalizacji "{0}" utworzono wykaz "Wykaz załacznik 5 - przetworzony wykaz GIS.xlsx"'.format(folder)
    messagebox.showinfo("Info", info)

def openLK201():
    root2 = tk.Toplevel(master)
    root2.title("Przeformatowanie wykazu GIS na wykaz docelowy dla LK 201")

    L0=tk.Label(root2, text="Wykaz dla LK201")
    L0.grid(row=0, column=1)
    E1=tk.Entry(root2, textvariable=folder_excell201, width=100, borderwidth=3)
    E1.grid(row=1, column=1)

    B2=tk.Button(root2, text="Formatuj", image=xicon, command=submit201)
    B2['state']='disabled'
    B2.grid(row=4, column=2)

    B1=tk.Button(root2, text="Wyszukaj wykaz", command=partial(browseFiles, E1, B2))
    B1.grid(row=1, column=2)

def openInfo201():
    rootinfo201=tk.Toplevel(master)
    rootinfo201.title("Info wykaz LK 201")
    Linfo201=tk.Label(rootinfo201, image=imInfo201)
    Linfo201.grid(row=0, column=0)

def openInfo104():
    rootinfo104=tk.Toplevel(master)
    rootinfo104.title("Info wykaz LK 104")
    Linfo104=tk.Label(rootinfo104, image=imInfo104)
    Linfo104.grid(row=0, column=0)

master = tk.Tk()
canvas = tk.Canvas(master, width = 150, height =50)
canvas.grid(columnspan = 3, rowspan=3)

folder_excell104=tk.StringVar()
folder_excell201=tk.StringVar()

# ficon = tk.PhotoImage(file='R:\\OIIS_KR5\\_BRANŻOWE\\_GIS\\SKRYPTY_PYTHON\\ZAL_5\\image\\document.png')
xicon = tk.PhotoImage(file='R:\\OIIS_KR5\\_BRANŻOWE\\_GIS\\SKRYPTY_PYTHON\\ZAL_5\\image\\file.png')
iicon = tk.PhotoImage(file='R:\\OIIS_KR5\\_BRANŻOWE\\_GIS\\SKRYPTY_PYTHON\\ZAL_5\\image\\info.png')
imInfo201 = tk.PhotoImage(file='R:\\OIIS_KR5\\_BRANŻOWE\\_GIS\\SKRYPTY_PYTHON\\ZAL_5\\image\\instrukcja_LK201.png')
imInfo104 = tk.PhotoImage(file='R:\\OIIS_KR5\\_BRANŻOWE\\_GIS\\SKRYPTY_PYTHON\\ZAL_5\\image\\instrukcja_LK104.png')
logo = tk.PhotoImage(file='R:\\OIIS_KR5\\_BRANŻOWE\\_GIS\\SKRYPTY_PYTHON\\ZAL_5\\image\\LOGO_MGGP.png')

master.title("Przeformatowanie wykazu GIS na wykaz docelowy")

#logo
logo_label = tk.Label(image = logo)
logo_label.image = logo
logo_label.grid(row=0)

#Buttons
ButtonLK104 = tk.Button(master, text="Przeformatuj wykaz dla załącznika 5 na LK104", width=50, command=openLK104)
ButtonLK104.grid(row=1, column=1)
ButtonLK104info = tk.Button(master, image = iicon, command=openInfo104)
ButtonLK104info.grid(row=1, column=2)

ButtonLK201 = tk.Button(master, text="Przeformatuj wykaz dla załącznika 5 na LK201", width=50, command=openLK201)
ButtonLK201.grid(row=2, column=1)
ButtonLK201info = tk.Button(master, image = iicon, command=openInfo201)
ButtonLK201info.grid(row=2, column=2, columnspan = 4)

canvas = tk.Canvas(master, width = 150, height =50)
canvas.grid(rowspan=1)

master.mainloop()
