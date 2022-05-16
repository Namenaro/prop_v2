from utils.point import Point

import random
import numpy as np
import matplotlib.pyplot as plt
import math

def sense(picture, point):
    xlen=28
    ylen=28
    if point.x >= 0 and point.y >= 0 and point.x < xlen and point.y < ylen:
        val = picture[point.y, point.x]
        if  val >=10:
            return 1
        else:
            return 0

    return 0


def get_coords_for_radius(centerx, centery, radius):
    #|x|+|y|=radius ->  |y|=radius-|x|
    # x>0  -> y1 = radius-|x|
    X=[]
    Y=[]
    if radius == 0:
        return [centerx], [centery]

    for modx in range(0,radius+1):
        mody = radius - modx
        # x>0
        if modx!=0 and mody!=0:
            X.append(modx+centerx)
            Y.append(mody+centery)

            X.append(-modx + centerx)
            Y.append(mody + centery)

            X.append(modx + centerx)
            Y.append(-mody + centery)

            X.append(-modx + centerx)
            Y.append(-mody + centery)

        if modx==0 and mody!=0:
            X.append(modx+centerx)
            Y.append(mody+centery)

            X.append(modx + centerx)
            Y.append(-mody + centery)

        if modx!=0 and mody==0:
            X.append(modx+centerx)
            Y.append(mody+centery)

            X.append(-modx + centerx)
            Y.append(mody + centery)


    return X,Y

def get_coords_less_or_eq_raduis(centerx, centery, radius):
    XB = []
    YB = []
    for r in range(0, radius+1):
        X, Y = get_coords_for_radius(centerx, centery, r)
        XB = XB + X
        YB = YB + Y
    return XB, YB

def select_random_coord_on_pic(pic):
    maxX = pic.shape[1]
    maxY = pic.shape[0]
    x = random.randint(0, maxX - 1)
    y = random.randint(0, maxY - 1)
    return x,y

def get_random_point():
    x= random.randint(0, 27)
    y = random.randint(0, 27)
    return Point(x,y)


class CoordSelector:
    def __init__(self, image,keys=None):
        self.image = image
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.resultx = []
        self.resulty = []
        self.keys = keys
        if keys is not None:
            self.XY_info_dicts = []


    def onclick(self, event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))
        x = math.ceil(event.xdata)
        y = math.ceil(event.ydata)

        plt.scatter(x, y, s=100, c='red', marker='o', alpha=0.4)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


        self.resultx.append(x)
        self.resulty.append(y)
        if self.keys is not None:
            info_dict = {}
            for key in self.keys:
                info_dict[key] = input(key + "=")
            self.XY_info_dicts.append(info_dict)



    def create_device(self):
        plt.imshow(self.image, cmap='gray_r')
        plt.show()
        if self.keys is None:
            print("xs=" + str(self.resultx))
            print("ys=" + str(self.resulty))
            return self.resultx, self.resulty
        return self.resultx, self.resulty, self.XY_info_dicts

def select_points_on_pic_handly(pic, keys=None):
    devcr = CoordSelector(pic, keys)
    return devcr.create_device()

def get_point_handly(pic):
    X,Y = select_points_on_pic_handly(pic, keys=None)
    return Point(X[0],Y[0])

