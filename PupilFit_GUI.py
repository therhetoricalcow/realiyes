import tkinter as tk
import numpy as np
import cv2
from PIL import Image,ImageTk
class GUI:
    def __init__(self,img,root):
        self.root = root
        b, g, r = cv2.split(img)
        merged = cv2.merge((r, g, b))
        im = Image.fromarray(merged)
        imgtk = ImageTk.PhotoImage(image=im)
        tk.Label(self.root,image=imgtk).grid(row=1,column=1)
        slider1 = tk.Scale(self.root,from_=0, to=200,orient=tk.HORIZONTAL)
        slider1.grid(row=0,column=2)






## Test ERE ##

img = cv2.imread("/home/avaneesh/PycharmProjects/realiyes/test.png")
root = tk.Tk()
test = GUI(img,root)
root.mainloop()