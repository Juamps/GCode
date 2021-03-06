from Tkinter import *
import tkMessageBox
import tkFileDialog
import lee_imagen
from PIL import Image  # read image

variables = 'Path de la imagen', \
            'Cantidad de grises', \
            'Paso (mm)', \
            'Ancho Canvas (X max 1200/700mm)', \
            'Largo Canvas (Y max 2400/1220mm)', \
            'X inicial (coord)',\
            'Y inicial (coord)', \
            'Z max', \
            'Presion en recarga (Z)', \
            'Presion en pintado (Z)', \
            'Modo de Pintado \n  0 Puntual\n  1 Semi diagonal post\n  2 Semi diagonal pre', \
            'Trazos antes de recargar ', \
            'Coordenada X de recarga derecha\n(mm despues de canvas, ej. 5)', \
            'Coordenada X de recarga izquierda\n(mm antes de canvas, ej. -5)'

entries = []

def genera_codigo(entries):
    lee_imagen.PATH = entries[0][1].get()
    lee_imagen.CANT_COLORES = int(entries[1][1].get())
    lee_imagen.PASO_X = float(entries[2][1].get())
    lee_imagen.PASO_Y = float(entries[2][1].get())
    lee_imagen.X_CANVAS = int(entries[3][1].get())
    lee_imagen.Y_CANVAS = int(entries[4][1].get())
    lee_imagen.X_INIT = int(entries[5][1].get())
    lee_imagen.Y_INIT = int(entries[6][1].get())
    lee_imagen.Z_MAX = float(entries[7][1].get())
    lee_imagen.PRES_Z_RECARGA = float(entries[8][1].get())
    lee_imagen.PRES_Z_PINTA = float(entries[9][1].get())
    lee_imagen.MODO_PINTURA = int(entries[10][1].get())  # 0 Puntual; 1 Semi diagonal post; 2 Semi diagonal pre
    lee_imagen.RECARGA = float(entries[11][1].get())
    lee_imagen.X_RECARGA_IZQ = float(entries[13][1].get())

    ## Leer imagen para validar tamanos
    im = Image.open(lee_imagen.PATH)
    # Largo y ancho de la imagen
    w, h = im.size
    ## Invierte ejes para router chico
    w, h = h, w
    print w, h
    ans = True

    ## Calculadas
    lee_imagen.X_MAX = w * lee_imagen.PASO_X
    lee_imagen.Y_MAX = h * lee_imagen.PASO_Y
    lee_imagen.X_RECARGA_DER = lee_imagen.X_MAX + int(entries[12][1].get())

    ancho = w * lee_imagen.PASO_X
    largo = h * lee_imagen.PASO_Y

    if lee_imagen.X_CANVAS < ancho or lee_imagen.Y_CANVAS < largo:
        ##  Styles:
        ##  0 : OK
        ##  1 : OK | Cancel
        ##  2 : Abort | Retry | Ignore
        ##  3 : Yes | No | Cancel
        ##  4 : Yes | No
        ##  5 : Retry | No
        ##  6 : Cancel | Try Again | Continue
        ans = tkMessageBox.askyesno("Warning!", "La imagen excede el tamano del canvas.\n"
                                                "Medida minima de canvas \n"
                                                "X: %smm Y: %smm \n"
                                                "Continuar?" % (ancho, largo))
    if ans:
        lee_imagen.main()


def iniciales(entries):
    entries[0][1].insert(END, lee_imagen.PATH)
    entries[1][1].insert(END, lee_imagen.CANT_COLORES)
    entries[2][1].insert(END, lee_imagen.PASO_X)
    entries[3][1].insert(END, lee_imagen.X_CANVAS)
    entries[4][1].insert(END, lee_imagen.Y_CANVAS)
    entries[5][1].insert(END, lee_imagen.X_INIT)
    entries[6][1].insert(END, lee_imagen.Y_INIT)
    entries[7][1].insert(END, lee_imagen.Z_MAX)
    entries[8][1].insert(END, lee_imagen.PRES_Z_RECARGA)
    entries[9][1].insert(END, lee_imagen.PRES_Z_PINTA)
    entries[10][1].insert(END, lee_imagen.MODO_PINTURA)  # 0 Puntual; 1 Semi diagonal post; 2 Semi diagonal pre
    entries[11][1].insert(END, lee_imagen.RECARGA)
    entries[12][1].insert(END, lee_imagen.X_RECARGA_DER)
    entries[13][1].insert(END, lee_imagen.X_RECARGA_IZQ)


def browse_file():
    fname = tkFileDialog.askopenfilename(filetypes=[("Images1", "*.png"), ("Images2", "*.jpg")])
    # print fname, type(fname)
    entries[0][1].delete(0,'end')
    entries[0][1].insert(END, fname)

def crea_forma(root, variables):
    row = Frame(root)
    lab = Label(row, width=30, text=variables[0], anchor='w', justify='left')
    ent = Entry(row)
    entries.append((variables[0], ent))
    b0 = Button(row, text= '...',
                command=browse_file)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    lab.pack(side=LEFT)
    b0.pack(side=RIGHT)
    ent.pack(side=RIGHT, expand=YES, fill=X)

    for var in variables[1:]:
        row = Frame(root)
        lab = Label(row, width=30, text=var, anchor='w', justify='left')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append((var, ent))
    iniciales(entries)
    return entries


if __name__ == '__main__':
    root = Tk()
    ents = crea_forma(root, variables)
    root.bind('<Return>', (lambda event, e=ents: genera_codigo(e)))
    b2 = Button(root, text='Salir', command=root.quit)
    b2.pack(side=RIGHT, padx=5, pady=20)
    b1 = Button(root, text='Genera g-code',
                command=(lambda e=ents: genera_codigo(e)))
    b1.pack(side=RIGHT, padx=5, pady=20)
    root.mainloop()

