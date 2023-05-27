import tkinter as tk
import math
import numpy as np
import sys
from heatmap_calculator import *
from vector_field import vector_field

#np.set_printoptions(threshold=sys.maxsize)


# Define a function which uses 
def vectormezo(x, y):
    xp = 2*x*y - x + y
    yp = 5*x**4+y**3+2*x-3*y

    return xp, yp


def main():
    #H, W = 1000,2560
    H, W = 1000,1920 #for Full HD
    top = tk.Tk()
    top.title("Vector field plot")
    C = tk.Canvas(top, bg="black", height=H, width=W)
    vf = vector_field(C, H, W, vectormezo)
    vf.raster()
    #vf.draw_arrow(150, 150, 1,4 ,5)
    dxy = 20
    zoom = 800
    vf.calculate_vector_field(int(-W/2), int(W/2), dxy, int(-H/2), int(H/2), dxy, zoom)
    vf.draw_vector_field()
    top.mainloop()

if __name__ == "__main__":
    main()

