from PIL import Image  # read image
import numpy as np  # convert image to matrix
import os
import datetime

CANT_COLORES = 8
PATH = '../files/wn0.png'


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
    print arreglos_por_color
    return arreglos_por_color




if __name__ == '__main__':
    # Crea directorio con nombre unico
    dir_path = "../files/prueba_" + str(datetime.datetime.now()).split(".")[0].replace(" ", "_")
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # Leer Imagen
    im = Image.open(PATH)
    # Largo y ancho de la imagen
    w, h = im.size
    # Segmenta imagen en colores limitados; arreglo
    imagen_arr = trunca_imagen(im)
    # Crea matriz a partir de arreglo
    matriz_im = np.mat(imagen_arr).reshape(h, w)
    # Guarda la nueva imagen
    im = Image.fromarray(np.array(matriz_im, dtype='uint8'))
    save_path = dir_path + "/imagen_segmentada.png"
    im.save(save_path)
    # Genera las matrices por color
    arreglos_por_color = genera_arreglos_por_color(imagen_arr)

