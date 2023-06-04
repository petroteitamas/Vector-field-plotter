import math
import numpy as np
from heatmap_calculator import *

class vector_field():
    def __init__(self, canvas, height, width, vecffunc, zoom = 1, dt = 0.001, iter = 100):
        self.height = height
        self.width = width
        self.canvas = canvas
        self.arrows = np.array([])
        self.canvas.pack()
        self.vecffunc = vecffunc
        self.zoom = zoom
        self.dt = dt
        self.iter = int(iter)
        self.center()
        self.raster()
        pass

    def center(self):
        x0_x, y0_x = self.c2t(-self.width/2, 0)
        x1_x, y1_x = self.c2t(self.width/2, 0)
        line_x = self.canvas.create_line(x0_x, y0_x, x1_x, y1_x, fill="#444", width=1)

        x0_y, y0_y = self.c2t(0, self.height/2)
        x1_y, y1_y = self.c2t(0, -self.height/2)
        line_y = self.canvas.create_line(x0_y, y0_y, x1_y, y1_y, fill="#444", width=1)
        
        self.canvas.pack()
        return line_x, line_y
    

    def raster(self):
        x0_x, y0_x = self.c2t(-self.width/2, self.zoom)
        x1_x, y1_x = self.c2t(self.width/2, self.zoom)
        line_x = self.canvas.create_line(x0_x, y0_x, x1_x, y1_x, fill="#555", width=1)

        x0_y, y0_y = self.c2t(self.zoom, self.height/2)
        x1_y, y1_y = self.c2t(self.zoom, -self.height/2)
        line_y = self.canvas.create_line(x0_y, y0_y, x1_y, y1_y, fill="#555", width=1)
        
        x0_x, y0_x = self.c2t(-self.width/2, -self.zoom)
        x1_x, y1_x = self.c2t(self.width/2, -self.zoom)
        line_x = self.canvas.create_line(x0_x, y0_x, x1_x, y1_x, fill="#555", width=1)

        x0_y, y0_y = self.c2t(-self.zoom, self.height/2)
        x1_y, y1_y = self.c2t(-self.zoom, -self.height/2)
        line_y = self.canvas.create_line(x0_y, y0_y, x1_y, y1_y, fill="#555", width=1)
        

        self.canvas.pack()
        return line_x, line_y





    def c2t(self, x, y):
        x, y = int(x+self.width/2),int(self.height/2-y) 
        return x, y
    
    def ic2t(self, X, Y, scale_x = 1, scale_y = 1):
        # scale 1: one pixel is one unit
        x, y = (X-self.width/2)/scale_x, (-Y+self.height/2)/scale_y
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
            color = heatmap(1 - (len - mini)/(maxi - mini))
            self.draw_arrow(x, y, dx, dy, color)


    def bind_btn1(self, event):
        x, y = self.ic2t(event.x, event.y, scale_x = self.zoom, scale_y = self.zoom)
        #print("x0: ", x, "y0: ", y)
        self.diffeqsolver(x, y)
        self.show_diff_sol()

    def bind_btn2(self, event):
        self.canvas.delete("all")
        self.center()
        self.raster()
        self.draw_vector_field()



    def bind_wheel(self, event):
        print(event)


    def diffeqsolver(self, x0, y0):
        self.diffplot = np.array([[x0, y0]])

        x = x0
        y = y0

        for i in range(1, self.iter):
            xp, yp = self.vecffunc(x, y)
            if(xp > 1e10 or yp > 1e10):
                break
            #print("xp", xp, "yp", yp)
            x = x + xp * self.dt
            y = y + yp * self.dt
            
            dist = math.sqrt((abs(self.diffplot[-1][0] - x)) ** 2 + (abs(self.diffplot[-1][1] - y)) ** 2)
            if (dist * self.zoom > 4):
                self.diffplot = np.vstack([self.diffplot, [x, y]])
                #print("Added", i, dist * self.zoom)
                print("Calculating: ", int(i*100/self.iter), "%")
            
            stop_conds = [dist * self.zoom > 5000,
                          x * self.zoom > max(self.width, self.height) * 2]
            if any(stop_conds):
                print("END")
                break
            

    def show_diff_sol(self):
        print("Shape", self.diffplot.shape[0])

        for i in range(1, self.diffplot.shape[0]):
            x0, y0 = self.c2t(self.diffplot[i-1][0] * self.zoom, self.diffplot[i-1][1]* self.zoom)
            x1, y1 = self.c2t(self.diffplot[i][0] * self.zoom, self.diffplot[i][1]* self.zoom)
            color = "white"
            #color = heatmap((i/self.diffplot.shape[0])/2+0.25)
            #print(x0, y0, x1, y1)
            line = self.canvas.create_line(x0, y0, x1, y1, fill=color, width=2)
        