import time
import threading
import numpy as np
import timeit
class LiveDisplay:
    def __init__(self,name,gui,petalx,petaly,filename):
        self.name = name
        self.petalx = petalx
        self.petaly = petaly
        self.numPoints = petalx.shape[0]
        self.GUI = gui
        self.filename = filename
        self.getPoints = self.GUI.getBoxRows(self.petalx, self.petaly)

    def run(self):
        print("Starting " + self.name)
        self.tracer()
    def marker(self,i):
        start = time.time()
        self.GUI.drawBox(self.getPoints[0][i], self.getPoints[1][i],intended_color=(0,0,255))
        self.GUI.display()
        return time.time() - start
    def tracer(self):
        i = 0
        start = time.time()
        dataArr = np.array([None])
        while(i < self.numPoints):
            time.sleep(0.035)
            self.GUI.drawBox(self.getPoints[0][i], self.getPoints[1][i],intended_color=(0, 0, 255))
            self.GUI.drawBox(self.getPoints[0][i-1], self.getPoints[1][i-1],intended_color=(255, 255, 255))
            dot_time = time.time() - start
            dot_time = np.array([dot_time])
            if(dataArr.any() == None):
                dataArr = np.array([[dot_time],[self.getPoints[0][i]],[self.getPoints[1][i]]])
            else:
                dataArr = np.hstack((dataArr,np.array([[dot_time],[self.getPoints[0][i]],[self.getPoints[1][i]]])))
            i = i + 1

            self.GUI.display()

        np.savetxt(self.filename,np.transpose(dataArr),delimiter = ",")


