from Tkinter import *
import lee_imagen

variables = 'Cantidad de grises', \
            'Path de la imagen', \
            'X inicial',\
            'X max', \
            'Paso X',\
            'Y inicial', \
            'Y max', \
            'Paso Y', \
            'Z max', \
            'Presion en recarga (Z)', \
            'Presion en pintado (Z)', \
            'Modo de Pintado \n(0 Puntual; 1 Semi diagonal post; 2 Semi diagonal pre)', \
            'Puntos antes de recarga', \
            'Coord X de recarga derecha', \
            'Coordenada X de recarga izquierda'



lee_imagen.CANT_COLORES = 8
lee_imagen.PATH = '../files/wn0.png'
lee_imagen.X_INIT = -3
lee_imagen.X_MAX = 120
lee_imagen.PASO_X = 3
lee_imagen.Y_INIT = -3
lee_imagen.Y_MAX = 160
lee_imagen.PASO_Y = 3
lee_imagen.Z_MAX = 5
lee_imagen.PRES_Z_RECARGA = -8
lee_imagen.PRES_Z_PINTA = -5
lee_imagen.MODO_PINTURA = 0  # 0 Puntual; 1 Semi diagonal post; 2 Semi diagonal pre
lee_imagen.RECARGA = 10
lee_imagen.X_RECARGA_DER = -10
lee_imagen.X_RECARGA_IZQ = lee_imagen.X_MAX + 10

def fetch(entries):
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        print('%s: "%s"' % (field, text))


def makeform(root, variables):
    entries = []
    for var in variables:
        row = Frame(root)
        lab = Label(row, width=50, text=var, anchor='w', justify='left')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append((var, ent))
    return entries


if __name__ == '__main__':
    root = Tk()
    ents = makeform(root, variables)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))
    b1 = Button(root, text='Show',
          command=(lambda e=ents: fetch(e)))
    b1.pack(side=LEFT, padx=5, pady=5)
    b2 = Button(root, text='Quit', command=root.quit)
    b2.pack(side=LEFT, padx=5, pady=5)
    root.mainloop()