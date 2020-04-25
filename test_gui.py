import tkinter as Tk
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
from ellipse_fitter import

import cv2



class Application(Frame):
    def __init__(self,master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        panelA = None
        panelB = None
        self.create_button()

    def create_button(self):
        btn = Button(root, text="Select an image", command=self.create_panels)
        btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
    def create_panels(self):
        global panelA,panelB
        path = filedialog.askopenfilename()
        if len(path)>0:
            image = cv2.imread(path)
            shifted_ellipse = pupilAreafitRR(image)
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
