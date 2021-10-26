import cv2
import numpy as np
import tkinter as tk

class Test_GUI:
    def __init__(self,box_dimension):
        self.root = tk.Tk()
        self.dim = box_dimension
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.background = np.zeros([self.screen_height,self.screen_width,3],dtype=np.uint8)
        self.background.fill(255)
        self.boxArray = np.zeros([int(self.screen_height/self.dim),int(self.screen_width/self.dim)],dtype=np.uint8) ##initialize box array to hold what you wish to look at
        self.centerBox = np.array([int(((self.screen_height/self.dim)/2) -1),int(((self.screen_width/self.dim)/2) -1)]) ##middle box

    def getScreenDim(self):
        return self.screen_width,self.screen_height

    def drawBoxTargets(self,pointx,pointy,intended_color):
        cv2.rectangle(self.background,(pointx,pointy),(pointx + self.dim,pointy + self.dim),intended_color,-1)

    def getboxDim(self):
        return self.dim

    def setBoxArrayCartesian(self,x_coord,y_coord):
        box_row = ((y_coord - 0.5*self.dim-self.centerBox[0]*self.dim)/(-self.dim)).astype(int)
        box_col = ((x_coord + 0.5*self.dim+self.centerBox[1]*self.dim) / self.dim).astype(int)
        try:
            self.boxArray[box_row,box_col] = 1
        except:
            print("Out of Bounds")
            pass

    def drawfromBoxArray(self,color):
        non_zero_indices = np.transpose(np.nonzero(self.boxArray))
        for i in range(len(non_zero_indices)):
            boxindex = non_zero_indices[i]
            try:
                pointy = boxindex[0]*self.dim
                pointx = boxindex[1]*self.dim
                self.drawBoxTargets(pointx,pointy,color)
            except:
                print('Out of Canvas Range')
                pass

    def display(self):
        cv2.imshow('Window',self.background)
        # cv2.namedWindow('Window', cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty('Window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.waitKey(1)
