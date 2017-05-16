__author__ = 'JP'
from random import randint  # enteros aleatorios
import scipy

if __name__ == '__main__':
    # X_MAX = 1215
    # Y_MAX = 1600
    X_MAX = 120
    PASO_X = 3
    Y_MAX = 160

#   Settings iniciales:
#   G90=coordenadas absolutas
#   G17=eje XY
#   f22000=feed rate (?)
#   S0 = tiempo de descanso del motor desactivado
    print "G90G17\n" \
          "f22000\n" \
          "S0"

#   Mover cursor al punto inicial
    print "G00 X-3.00 Y-3.00 Z3.00"

#   Prueba para escribir una linea en incrementos aleatorios
#   X = 0; Y en [0,1600], incrementos en [1,40]; Z en [-5,5]

    X = range(0, X_MAX+1, PASO_X)
    Y = []
    y = 0
    while y <= Y_MAX:
        Y.append(y)
        y += randint(1, 10)
    # print Y

#   Crea g-code coord x,y --> baja --> sube --> x,y
#   Formato: Gnn Xnn Ynn Znn;  G00 max speed, G01 feed speed
    for x in X:
        for y in Y:
            # Mover el cursor al punto x,y
            print "G00 X%d Y%d" % (x, y)
            # Pintar
            print "G00 Z-5"
            # Subir
            print "G00 Z5"

