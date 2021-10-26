import numpy as np

class Polar:
    def __init__(self,k,screen_w,screen_h,numpoints,reverse,num_times):
        self.pointNums = numpoints
        if(k%2==0):
            print('Petals = ' + str(2*k))
            self.range = np.pi*2
        else:
            print('Petals = ' + str(k))
            self.range = np.pi
        self.petals = k
        self.width = screen_w
        self.height = screen_h
        self.theta = np.linspace(0,np.pi*2,self.pointNums)
        if (reverse == True):
            self.theta = self.theta*-1
        self.num_times = num_times
        self.theta = np.tile(self.theta,(num_times))
    def normpetalCartesian(self):
        x = 0.5*self.width*np.cos(self.petals*self.theta)*np.cos(self.theta)
        y = 0.5*self.height*np.cos(self.petals*self.theta)*np.sin(self.theta)
        return x,y
    def diagpetalCartesian(self):
        x = 0.5*self.width*np.cos(self.theta)*np.sin(self.theta)*np.cos(self.theta) * 2 * np.sqrt(1.65)
        y = 0.5*self.height*np.cos(self.theta)*np.sin(self.theta)*np.sin(self.theta) * 2 * np.sqrt(1.65)
        return x,y

