from tkinter import *
from tkinter import messagebox

import PDF_SIZE_COUNTER

root = Tk()
root.title("Zliczanie długości wydruków map PDF")

folder_pdf = StringVar()
copies_no = StringVar()

L1 = Label(root, text="Wklej sciezke do folderu z arkuszami PDF").grid(row=0, column=0)
E1 = Entry(root, textvariable=folder_pdf, width=200, borderwidth=3).grid(row=0, column=1)
L2 = Label(root, text="Podaj liczbe kopii").grid(row=1, column=0)
E2 = Entry(root, textvariable=copies_no, width=5, borderwidth=3).grid(row=1, column=1)


def submit():
    folder = folder_pdf.get()
    copies_count = copies_no.get()

    PDF_SIZE_COUNTER.pdfsizecounter(folder, copies_count)
    info = 'W lokalizacji "{0}" utworzono plik "spis_rysunkow.csv" w którym wyliczono wydruki dla {1} kopii'.format(folder, copies_count)
    messagebox.showinfo("Info", info)

B1 = Button(root, text="Oblicz", command=submit).grid(row=3, column=1)

root.mainloop()
