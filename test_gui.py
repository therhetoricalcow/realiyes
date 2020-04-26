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
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.panelA = None
        self.panelB = None
        self.currImageObj = None  ##PupilFit Object
        self.directory = None  ##Loaded Directory
        self.fileiter = 0  ##File Number in Directory
        self.sortedfilelist = None  ##Sorted File LIst
        self.labeled_folder = None
        self.shifted_ellipse = None
        self.create_button()
        self.create_sliders()

    def create_button(self):
        btn0 = Button(root, text="Next Image", command=self.next_image)
        btn0.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

        btn1 = Button(root, text="Prev Image", command=self.prev_image)
        btn1.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

        btn2 = Button(root, text="Save Image/Ellipse", command=self.save_outputs)
        btn2.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

        btn3 = Button(root, text="Erode = False", command=self.setEroder)
        btn3.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

        btn4 = Button(root, text="Open Directory", command=self.open_folder)
        btn4.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

    def next_image(self):
        ##If Next Image Button is Pressed, go to the next image in the sorted directory
        try:
            self.fileiter += 1
            path2currimage = str(self.directory) + '/' + str(self.sortedfilelist[self.fileiter])
            self.load_InitialImage(path2currimage)
        except:
            print("There is No Next Image")

    def prev_image(self):
        ##If Prev Image Button is Pressed, go to the previous image in the sorted directory
        try:
            self.fileiter -= 1
            path2currimage = str(self.directory) + '/' + str(self.sortedfilelist[self.fileiter])
            self.load_InitialImage(path2currimage)
        except:
            print("There is No Prev Image")

    def save_outputs(self):

        black = self.currImageObj.getImageSegment(self.shifted_ellipse,self.image)
        path = self.labeled_folder + '/' + str(self.sortedfilelist[self.fileiter])
        cv2.imwrite(path,black)

    def setEroder(self):
        ##Helper Function to Change Erode Bool if button is pressed
        try:
            if self.currImageObj.getErode() == False:
                self.currImageObj.setErode(True)
            else:
                self.currImageObj.setErode(False)

            path2image = str(self.directory) + '/' + str(self.sortedfilelist[self.fileiter])
            self.create_panels(path2image)
        except:
            print("Make Sure You Load a Pupil Object First!")

    def open_folder(self):
        ##If Open Folder Button Is Pressed, then it will ask to select a folder and it iterates from there
        self.directory = filedialog.askdirectory()


        filelist = os.listdir(self.directory)
        self.sortedfilelist = sorted(filelist, key=lambda f: int(re.sub('\D', '', f)))
        path2currimage = str(self.directory) + '/' + str(self.sortedfilelist[0])
        self.labeled_folder = str(self.directory) + '/Labeled_Segments'  ##Labeled_Segments
        os.mkdir(self.labeled_folder)  ##Make Labeled Directory in Folder
        self.load_InitialImage(path2currimage)

    def create_sliders(self):
        # Sliders for adjusting CV Params
        self.ltcSlider = Scale(root, from_=1, to=30, orient=VERTICAL, command=self.recalibrate,
                               label="ltc")  # , text="lowThresholdCanny"
        self.ltcSlider.pack(side=LEFT)

        self.htcSlider = Scale(root, from_=1, to=30, orient=VERTICAL, command=self.recalibrate,
                               label="htc")  # text="highThresholdCanny",
        self.htcSlider.pack(side=LEFT)

        self.dpl1Slider = Scale(root, from_=5, to=50, orient=VERTICAL, command=self.recalibrate,
                                label="dpl1")  # , text="darkestPixelL1"
        self.dpl1Slider.pack(side=LEFT)

        self.dpl2Slider = Scale(root, from_=5, to=50, orient=VERTICAL, command=self.recalibrate,
                                label="dpl2")  # , text="darkestPixelL2"
        self.dpl2Slider.pack(side=LEFT)

        self.thicknessSlider = Scale(root, from_=1, to=20, orient=VERTICAL, command=self.recalibrate,
                                     label="t")  # , text="thickness"
        self.thicknessSlider.pack(side=LEFT)

        self.spacingSlider = Scale(root, from_=2, to=20, orient=VERTICAL, command=self.recalibrate,
                                     label="spacing")  # , text="Spacing"
        self.spacingSlider.pack(side=LEFT)

        self.psxSlider = Scale(root, from_=0, to=80, orient=VERTICAL, command=self.recalibrate,
                                   label="psx")  # , text="Spacing"
        self.psxSlider.pack(side=LEFT)

        self.psySlider = Scale(root, from_=0, to=80, orient=VERTICAL, command=self.recalibrate,
                               label="psy")  # , text="Spacing"
        self.psySlider.pack(side=LEFT)

    def recalibrate(self, *args):

        self.currImageObj.setLtc(self.ltcSlider.get())
        self.currImageObj.setHtc(self.htcSlider.get())
        self.currImageObj.setDpl1(self.dpl1Slider.get())
        self.currImageObj.setDpl2(self.dpl2Slider.get())
        self.currImageObj.setThickness(self.thicknessSlider.get())
        self.currImageObj.setSpacing(self.spacingSlider.get())
        self.currImageObj.setPsx(self.psxSlider.get())
        self.currImageObj.setPsx(self.psySlider.get())
        path2image = str(self.directory) + '/' + str(self.sortedfilelist[self.fileiter])
        self.create_panels(path2image)

    def setSliders(self):
        self.ltcSlider.set(self.currImageObj.getLtc())
        self.htcSlider.set(self.currImageObj.getHtc())
        self.dpl1Slider.set(self.currImageObj.getDpl1())
        self.dpl2Slider.set(self.currImageObj.getDpl2())
        self.psxSlider.set(self.currImageObj.getPsx())
        self.psySlider.set(self.currImageObj.getPsy())
        self.thicknessSlider.set(self.currImageObj.getThickness())
        self.spacingSlider.set(self.currImageObj.getSpacing())

    def load_InitialImage(self, path2image):
        if len(self.directory) > 0:

            self.image = cv2.imread(path2image)
            image_name=str(self.sortedfilelist[self.fileiter])
            self.currImageObj = PupilFit(image_name)
            self.setSliders()
            self.shifted_ellipse = self.currImageObj.pupilAreafitRR(self.image)
            drawn = self.currImageObj.getDrawnImage(self.shifted_ellipse, self.image)

            image = Image.fromarray(self.image)
            drawn = Image.fromarray(drawn)

            image = ImageTk.PhotoImage(image)
            drawn = ImageTk.PhotoImage(drawn)

            if self.panelA is None or self.panelB is None:
                self.panelA = Label(image=image)
                self.panelA.image = image
                self.panelA.pack(side="left", padx=10, pady=10)

                self.panelB = Label(image=drawn)
                self.panelB.image = drawn
                self.panelB.pack(side="right", padx=10, pady=10)

            else:
                self.panelA.configure(image=image)
                self.panelB.configure(image=drawn)
                self.panelA.image = image
                self.panelB.image = drawn

    def create_panels(self, path2image):
        if len(self.directory) > 0:
            self.image = cv2.imread(path2image)
            shifted_ellipse = self.currImageObj.pupilAreafitRR(self.image)
            drawn = self.currImageObj.getDrawnImage(shifted_ellipse, self.image)

            image = Image.fromarray(self.image)
            drawn = Image.fromarray(drawn)

            image = ImageTk.PhotoImage(image)
            drawn = ImageTk.PhotoImage(drawn)

            if self.panelA is None or self.panelB is None:
                self.panelA = Label(image=image)
                self.panelA.image = image
                self.panelA.pack(side="left", padx=10, pady=10)

                self.panelB = Label(image=drawn)
                self.panelB.image = drawn
                self.panelB.pack(side="right", padx=10, pady=10)

            else:
                self.panelA.configure(image=image)
                self.panelB.configure(image=drawn)
                self.panelA.image = image
                self.panelB.image = drawn


root = Tk()
app = Application(master=root)
app.mainloop()
