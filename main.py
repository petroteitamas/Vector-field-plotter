import tkinter as tk
import math
from math import sqrt, sin, cos, tan
import numpy as np
import sys
from heatmap_calculator import *
from vector_field import vector_field


## -------------------------------------------
# Left-click to draw the path with the initial mouse position x, y.
# Right-click to delete the path(s)

# Set the variables
W, H  = 1700, 800 # Window size
zoom = 300 # Zoom level
dxy = 20 # vector filed plot distance delta
dt = 0.001 # simulation time delta
iter = 1e5 # simulation max iteration
animation = True # Animation

# Define a function which uses 
def vectorfield(x, y):
    xp = -4 * y + 2 * x * y - 8
    yp = 4 * y**2 - x**2
    return xp, yp
## -------------------------------------------

# Only modify if you know what you are doing
def main():
    top = tk.Tk()
    top.title("Vector field plot")
    C = tk.Canvas(top, bg="black", height=H, width=W)
    vf = vector_field(C, H, W, vectorfield, zoom = zoom, dt = dt, iter = iter, dxy = dxy, animation=animation)
    top.bind('<Button-1>', vf.bind_btn1)
    top.bind('<Button-3>', vf.bind_btn2)
    top.bind("<MouseWheel>", vf.bind_wheel)
    top.mainloop()

if __name__ == "__main__":
    main()

