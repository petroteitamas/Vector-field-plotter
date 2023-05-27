import math
import numpy as np
from heatmap_calculator import *

class vector_field():
    def __init__(self, canvas, height, width, vecffunc):
        self.height = height
        self.width = width
        self.canvas = canvas
        self.arrows = np.array([])
        self.canvas.pack()
        self.vecffunc = vecffunc
        pass

    def raster(self):
        x0_x, y0_x = self.c2t(-self.width/2, 0)
        x1_x, y1_x = self.c2t(self.width/2, 0)
        line_x = self.canvas.create_line(x0_x, y0_x, x1_x, y1_x, fill="green", width=1)

        x0_y, y0_y = self.c2t(0, self.height/2)
        x1_y, y1_y = self.c2t(0, -self.height/2)
        line_y = self.canvas.create_line(x0_y, y0_y, x1_y, y1_y, fill="green", width=1)
        print(self.canvas)
        
        self.canvas.pack()
        return line_x, line_y


    def c2t(self, x, y):
        x, y = int(x+self.width/2),int(self.height/2-y) 
        return x, y

    def draw_arrow(self, x, y, x_dir, y_dir, color, zoom = 8):
        # Main line
        #scale = math.sqrt(x_dir**2 + y_dir**2)
        scale = 1
        direction = math.atan2(y_dir,x_dir)
        #print(direction * 180 / math.pi)
        x0_m, y0_m = self.c2t(x - zoom*scale*math.cos(direction), y - zoom*scale*math.sin(direction))
        x1_m, y1_m = self.c2t(x + zoom*scale*math.cos(direction), y + zoom*scale*math.sin(direction))

        zoom = 4
        arr1_x, arr1_y = self.c2t(x - zoom*scale*math.cos(direction+math.pi/4), y - zoom*scale*math.sin(direction+math.pi/4))
        arr2_x, arr2_y = self.c2t(x - zoom*scale*math.cos(direction-math.pi/4), y - zoom*scale*math.sin(direction-math.pi/4))

        width = 2
        #color = "white"
        line = self.canvas.create_line(x0_m, y0_m, x1_m, y1_m, fill=color, width=width)
        line = self.canvas.create_line(x1_m, y1_m, arr1_x, arr1_y, fill=color, width=width)
        line = self.canvas.create_line(x1_m, y1_m, arr2_x, arr2_y, fill=color, width=width)
        return line
    
    def calculate_vector_field(self, x_min, x_max, x_step, y_min, y_max, y_step, zoom):
        i = 0
        for x in range(x_min, x_max, x_step):
            for y in range(y_min, y_max, y_step):
                dx, dy = self.vecffunc(x/zoom, y/zoom)
                dxy_len = math.sqrt(dx**2 + dy**2)
                if i == 0:
                    self.arrows = np.array([x, y, dx, dy, dxy_len])
                else:
                    self.arrows = np.vstack([self.arrows, [x, y, dx, dy, dxy_len]])
                i = i + 1

                
    def draw_vector_field(self):
        maxi = self.arrows.min(axis = 0)[4]
        mini = self.arrows.max(axis = 0)[4]
        for i in range(0, self.arrows.shape[0]):
            row = self.arrows[i]
            x = row[0]
            y = row[1]
            dx = row[2]
            dy = row[3]
            len = row[4]
            #print(row)
            color = heatmap((len - mini)/(maxi - mini))
            self.draw_arrow(x, y, dx, dy, color)

