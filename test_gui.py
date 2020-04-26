import tkinter as Tk
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
from PupilFit import PupilFit
import os
import cv2
import pandas


class Application(Frame):
    def __init__(self,master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.directory = None
        self.fileiter = 0
        self.sortedfilelist = None
        self.create_button()
        self.create_sliders()
        

    def create_button(self):
        btn0 = Button(root, text="Next Image", command=self.next_image)
        btn0.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

        btn1 = Button(root,text="Prev Image",command = self.prev_image)
        btn1.pack(side = "bottom",fill="both",expand = "yes",padx = "10",pady="10")

        btn2 = Button(root, text="Save Image/Ellipse", command=self.save_outputs)
        btn2.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

        btn3 = Button(root, text="Erode = False", command=self.setEroder)
        btn3.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

        btn4 = Button(root, text="Open Directory", command=self.open_folder)
        btn4.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

    def next_image(self):
        try:
            self.fileiter +=1
            path2currimage = str(self.directory) + '/' + str(self.sortedfilelist[self.fileiter])
            self.create_panels(path2currimage)
        except:
            print("There is No Next Image")

    def prev_image(self):
        try:
            self.fileiter -=1
            path2currimage = str(self.directory) + '/' + str(self.sortedfilelist[self.fileiter])
            self.create_panels(path2currimage)
        except:
            print("There is No Prev Image")
    def save_outputs(self):

    def setEroder(self):
    def open_folder(self):
        self.directory = filedialog.askdirectory()
        filelist = os.listdir(self.directory)
        self.sortedfilelist = sorted(filelist, key=lambda x: int("".join([i for i in x if i.isdigit()])))
        path2currimage = str(self.directory) + '/' + str(self.sortedfilelist[0])
        self.create_panels(path2currimage)


    def create_sliders(self):
        v0 = Tk.IntVar(0)
        v1 = Tk.IntVar(0)
        v2 = Tk.IntVar(0)
        v3 = Tk.IntVar(0)
        v4 = Tk.IntVar(0)
        v5 = Tk.IntVar(0)
        v6 = Tk.IntVar(0)
        v7 = Tk.IntVar(0)
        v8 = Tk.IntVar(0)
        v9 = Tk.IntVar(0)

        slider0 = Scale(root,text="lowThresholdCanny",variable=v0)
        slider1 = Scale(root,text="highThresholdCanny",variable=v1)
        slider2 = Scale(root,text="size",variable=v2)
        slider3 = Scale(root,text="darkestPixelL1",variable=v3)
        slider4 = Scale(root, text="darkestPixelL2", variable=v4)
        slider5 = Scale(root, text="pupilSearchArea", variable=v5)
        slider6 = Scale(root, text="pupilSearchXMin", variable=v6)
        slider7 = Scale(root, text="pupilSearchYMin", variable=v7)
        slider8 = Scale(root, text="dilation", variable=v8)
        slider9 = Scale(root, text="thickness", variable=v9)

    def create_panels(self,path2image):
        global panelA,panelB
        if len(self.directory)>0:
            image = cv2.imread(path2image)
            im1 = PupilFit('test')
            shifted_ellipse = im1.pupilAreafitRR(image)
            drawn = image.copy()
            cv2.ellipse(drawn,shifted_ellipse,(0, 255, 0),2)

            image = Image.fromarray(image)
            drawn = Image.fromarray(drawn)

            image = ImageTk.PhotoImage(image)
            drawn = ImageTk.PhotoImage(drawn)

            if panelA is None or panelB is None:
                panelA = Label(image=image)
                panelA.image = image
                panelA.pack(side="left", padx=10, pady=10)

                panelB = Label(image=drawn)
                panelB.image = drawn
                panelB.pack(side="right", padx=10, pady=10)

            else:
                panelA.configure(image=image)
                panelB.configure(image=drawn)
                panelA.image = image
                panelB.image = drawn


root = Tk()
app = Application(master = root)
app.mainloop()
