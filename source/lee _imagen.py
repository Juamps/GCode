from PIL import Image  # read image
import numpy as np  # convert image to matrix
import os
import datetime

CANT_COLORES = 8
PATH = '../files/wn0.png'
X_INIT = -3
X_MAX = 120
PASO_X = 3
Y_INIT = -3
Y_MAX = 160
PASO_Y = 3
Z_MAX = 5
PRES_Z_RECARGA = -8
PRES_Z_PINTA = -5
MODO_PINTURA = 0  # 0 Puntual; 1 Semi diagonal post; 2 Semi diagonal pre
RECARGA = 10
X_RECARGA_DER = -10
X_RECARGA_IZQ = X_MAX + 10


def genera_rangos(n):
    a = range(256)
    k, m = divmod(len(a), n)
    return list(a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in xrange(n))


def trunca_imagen(imagen):
    # Convertir a escala de grises
    im = imagen.convert('L')
    # Genera rangos de color
    rangos = genera_rangos(CANT_COLORES)
    # Crear arreglo a partir de imagen
    arreglo_im = list(im.getdata())
    # Segmentar imagen incluyendo blancos y negros absolutos
    for index, pix in enumerate(arreglo_im):
        for ind, rango in enumerate(rangos):
            if pix in rango:
                if ind == 0:
                    arreglo_im[index] = 1
                elif ind == CANT_COLORES - 1:
                    arreglo_im[index] = 255
                else:
                    arreglo_im[index] = (max(rango) + min(rango)) / 2
    # print arreglo_im

    return arreglo_im


def genera_arreglos_por_color(arr_img):
    # Selecciona valores unicos de la lista
    vals_unicos = sorted(list(set(arr_img)))
    # Crea diccionario para almacenar las matrices separadas
    arreglos_por_color = {}
    for elem in vals_unicos:
        arreglos_por_color[elem] = [0]*len(arr_img)
    # Agrega el elemento que corresponda a cada valor en el indice adecuado
    for ind, color in enumerate(arr_img):
        arreglos_por_color[color][ind] = color
    return arreglos_por_color


def gesto_pintura(ind_x, ind_y, gesto, direc, arch):
    if gesto == 1:
        #  pinta semi diagonal post
        inst = "G00 X" + str(ind_x*PASO_X) + " Y" + str(ind_y*PASO_Y) + " Z" + str(Z_MAX) + "\n"
        arch.write(inst)
        arch.write("G00 Z" + str(PRES_Z_PINTA) + "\n")
    elif gesto == 2:
        # pinta semi diagonal pre
        inst = "G00 X" + str(ind_x*PASO_X) + " Y" + str(ind_y*PASO_Y) + " Z" + str(PRES_Z_PINTA) + "\n"
        arch.write(inst)
        arch.write("G00 Z" + str(Z_MAX) + "\n")
    else:
        #  pinta puntual
        if direc == "ver":
            inst = "G00 X" + str(ind_x*PASO_X) + " Y" + str(ind_y*PASO_Y) + "\n"
            arch.write(inst)
            arch.write("G00 Z" + str(PRES_Z_PINTA) + "\n")
            arch.write("G00 Z" + str(Z_MAX) + "\n")
        else:
            inst = "G00 X" + str(ind_x*PASO_X) + " Y" + str(ind_y*PASO_Y) + "\n"
            arch.write(inst)
            arch.write("G00 Z" + str(PRES_Z_PINTA) + "\n")
            arch.write("G00 Z" + str(Z_MAX) + "\n")


def recarga(ind_x, arch):
    if ind_x + 1 > w/2:
        arch.write("G00 X" + str(X_RECARGA_DER) + "\n")
    else:
        arch.write("G00 X" + str(X_RECARGA_IZQ) + "\n")

    arch.write("G00 Z" + str(PRES_Z_RECARGA) + "\n")
    arch.write("G00 Z" + str(Z_MAX) + "\n")

def pintado(mat, direc, path_archivo):
    # direc = 0: pinta horizontal
    # direc = 1: pinta vertical

    with open(path_archivo, "w+") as a:
        #   Settings iniciales:
        #   G90=coordenadas absolutas
        #   G17=eje XY
        #   f22000=feed rate (?)
        #   S0 = tiempo de descanso del motor desactivado
        a.write("G90G17\n"
                "f22000\n"
                "S0\n")
        #   Mover cursor al punto inicial
        a.write("G00 X" + str(X_INIT) + " Y" + str(Y_INIT) + " Z" + str(Z_MAX) + "\n")
        cont = 0
        if direc == 0:  # pinta vertical
            mat = mat.tolist()
            print mat
            print "\n\n"
            for ind_y, renglon in enumerate(mat):
                print ind_y, renglon
                for ind_x, val in enumerate(renglon):
                    if val > 0:
                        # print ind_x + 1
                        gesto_pintura(ind_x, ind_y, MODO_PINTURA, "ver", a)
                        cont += 1
                        if cont == RECARGA:
                            recarga(ind_x, a)
                            cont = 0
        else:  # pinta horizontal
            mat = mat.transpose()
            mat = mat.tolist()
            print mat
            print "\n\n"
            for ind_x, columna in enumerate(mat):
                print ind_x, columna
                for ind_y, val in enumerate(columna):
                    if val > 0:
                        # print ind_x + 1
                        gesto_pintura(ind_x, ind_y, MODO_PINTURA, "hor", a)
                        cont += 1
                        if cont == RECARGA:
                            recarga(ind_x, a)
                            cont = 0


def genera_gcode(dict_colores):
    rec_izq = "G00 " + str(X_RECARGA_IZQ)
    rec_der = "G00 " + str(X_RECARGA_DER)
    for cont_col, elem in enumerate(dict_colores):
        nom_archivo = str(elem) + ".txt"
        path_archivo = dir_path + "/" + nom_archivo
        print path_archivo
        # Crea matriz a partir de arreglo
        matriz_im = np.mat(dict_colores[elem]).reshape(w, h)
        # exit()
        pintado(matriz_im, divmod(cont_col, 2)[1], path_archivo)


if __name__ == '__main__':
    # Crea directorio con nombre unico
    dir_path = "../files/prueba_" + str(datetime.datetime.now()).split(".")[0].replace(" ", "_")
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # Leer Imagen
    im = Image.open(PATH)
    # Largo y ancho de la imagen
    w, h = im.size
    w, h = h, w
    # Segmenta imagen en colores limitados; arreglo
    imagen_arr = trunca_imagen(im)
    # Crea matriz a partir de arreglo
    matriz_im = np.mat(imagen_arr).reshape(w, h)
    # Guarda la nueva imagen
    im = Image.fromarray(np.array(matriz_im, dtype='uint8'))
    save_path = dir_path + "/imagen_segmentada.png"
    im.save(save_path)
    # Genera los arreglos por color
    arreglos_por_color = genera_arreglos_por_color(imagen_arr)
    # Genera archivos de texto de gcode
    genera_gcode(arreglos_por_color)
