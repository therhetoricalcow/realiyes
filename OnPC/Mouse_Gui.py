import Mouse_Sim
import numpy as np
import cv2
import time
import os

class Mouse_Gui:
    def __init__(self,w,h):

        self.boxArray = np.zeros([int(h/10),int(w/10)],dtype=np.uint8)
        w = int(w)
        h = int(h)
        self.side_width = int(w/8)
        self.side_height = int(h/5)
        self.width = int(w)
        self.height = int(h)
        self.background = np.zeros([self.height,self.width,3],dtype=np.uint8)
        self.background.fill(0)
        self.mouse = Mouse_Sim.Mouse_Sim()
        self.startDataTaking = False
        self.stopDataTaking = False
        self.pointx = int(w/2)
        self.pointy = int(h/2)
        self.startCalibPoint = False
        self.stopCalibPoint = False
        for i in range(0, w+1 - self.side_width, self.side_width):
            for j in range(0, h+1 - self.side_height, self.side_height):
                cv2.rectangle(self.background, (int(i + 1),int(j + 1)), (int(i+(-1 + self.side_width)), int(j+(-1 + self.side_height))), (255,255,255), (-1))

    def startData(self):
        self.startDataTaking = True

    def stopData(self):
        self.stopDataTaking = True


    def getDataFlags(self):
        return (self.startDataTaking,self.stopDataTaking)

    def getScreenDim(self):
        return self.width,self.height

    def drawBox(self,pointx,pointy,intended_color):
        cv2.rectangle(self.background,(pointx,pointy),(pointx + self.width/10,pointy + self.height/5),intended_color,-1)


    def display(self,background):
        cv2.imshow('Window',background)
        cv2.namedWindow('Window', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.waitKey(500)

    def boxRecord(self,folder_path):
        #block_num = (self.width*self.height)/(self.side_length*self.side_length)
        a = 1
#        newBackground = np.copy(self.background)
        for i in range(int(self.side_width/2), self.width+1, self.side_width):
            for j in range(int(self.side_height/2), self.height+1 , self.side_height):
                newBackground = np.copy(self.background)
                dataArr = np.array([[i],[j]])

                cv2.putText(newBackground, str(a) + ":Press Q to start taking data", (20,20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)  ## Text has been put
                while(self.startDataTaking == False): ## Waiting to Start taking data

                    self.display(newBackground)
                    pass

                newBackground = np.copy(self.background)
                cv2.circle(newBackground, (i, j), 10, (0, 0, 255), -1)
                cv2.putText(newBackground, str(a) + ":Press Q to Stop Taking Data", (20,20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)  ## Text has been put
                while(self.stopDataTaking == False): ## While Taking Data
                    self.display(newBackground)
                    pass
                self.startDataTaking = False
                self.stopDataTaking = False

                np.savetxt(folder_path + '/' + str(a) + '.csv', np.transpose(dataArr), delimiter=",")
                a = a + 1

    def centerBox(self):
        newBackground = np.copy(self.background)
        cv2.putText(newBackground,"Press Q to Calibrate", (20, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)  ## Text has been put
        while(self.startCalibPoint == False):
            self.display(newBackground)

        newBackground = np.copy(self.background)
        cv2.circle(newBackground,(int(self.width/2),int(self.height/2)),30,(0,0,255),-1)
        cv2.putText(newBackground,"Press Q to Stop Calibrating", (20, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)  ## Text has been put
        while(self.stopCalibPoint == False):
            self.display(newBackground)
        self.startCalibPoint = False
        self.stopCalibPoint = False

    def calibBox(self):
        points = np.array([[120,120],[120,120+240+240],[120,1200-120],[120+720,120],[120+720,120+480],[120+720,1200-120],[1920-120,120],[1920-120,120+240+240],[1920-120,1200-120]])

        for i in range(points.shape[0]):

                newBackground = np.copy(self.background)
                cv2.putText(newBackground,  ":Press Q to Calibrate", (20,20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)  ## Text has been put
                while(self.startDataTaking == False): ## Waiting to Start taking data

                    self.display(newBackground)
                    pass

                newBackground = np.copy(self.background)
                cv2.circle(newBackground, (points[i][0], points[i][1]), 30, (0, 0, 255), -1)
                cv2.putText(newBackground,  ":Press Q to Stop Calibrating", (20,20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)  ## Text has been put
                while(self.stopDataTaking == False): ## While Taking Data
                    self.display(newBackground)
                    pass
                self.startDataTaking = False
                self.stopDataTaking = False

    def mousePoints(self,dirpath):
        while(True):
            newBackground = np.copy(self.background)
            cv2.putText(newBackground, ":Press Q to start taking data", (20, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            while(self.startDataTaking==False):
                self.display(newBackground)
            pointArray = None
            while(self.stopDataTaking==False):
                x,y  = self.mouse.getPointer()
                newBackground = np.copy(self.background)
                cv2.circle(newBackground, (int(x), int(y)), 30, (0, 0, 255), -1)
                if(pointArray is None):
                    pointArray = np.array([[x,y]])
                else:
                    pointArray = np.vstack((pointArray,np.array([[x,y]])))
                self.display(newBackground)
            j = 1
            csvPath = dirpath + str(j) + '.csv'
            while(os.path.exists(csvPath)):
                j = j + 1
                csvPath = dirpath + str(j) + '.csv'

            self.startDataTaking = False
            self.stopDataTaking = False
            np.savetxt(csvPath,pointArray,delimiter=",")

    def realtimebox(self):
        while(True):
            try:
                if(self.pointx < 0):
                    self.pointx = 0
                if(self.pointx > 1920):
                    self.pointx = 1920
                if(self.pointy < 0):
                    self.pointy = 0
                if(self.pointy > 1080):
                    self.pointy = 1080
                newBackground = np.copy(self.background)
                cv2.circle(newBackground, (self.pointx, self.pointy), 30, (0, 0, 255), -1)
                self.display(newBackground)
            except:
                pass


    def REALBOX(self):
        while(True):
            x,y  = self.mouse.getPointer()

            newBackground = np.copy(self.background)
            cv2.circle(newBackground, (int(x + np.random.randn()*30), int(y + 30*np.random.randn())), 30, (0, 0, 255), -1)
            self.display(newBackground)





