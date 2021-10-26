import numpy as np
import re
import cv2
import os
from pynput import keyboard

chooseBool = False

def on_press(key):
    global i
    if key == keyboard.Key.esc:
            return False
    try:
        k = key.char
    except:
        k = key.name
    print('Key pressed: ' + k)
    if(k == 'q'):
        chooseBool = True


def sorted_nicely(l):
    """ Sorts the given iterable in the way that is expected.

    Required arguments:
    l -- The iterable to be sorted.

    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)
listener = keyboard.Listener(on_press=on_press)
listener.start()
raw_data = '/home/avaneesh/Desktop/Recording/raw/'
denoised_data = '/home/avaneesh/Desktop/Recording/denoised/'
background = np.zeros([224,224,3],dtype=np.uint8)
raw_files = os.listdir(raw_data)
for infile in sorted_nicely(raw_files):
    if(str(infile).endswith('.csv')):
        raw_arr = np.genfromtxt(raw_data + str(infile),delimiter=',')
        raw_arr = raw_arr[~np.isnan(raw_arr).any(axis=1)]
        denoised_arr = np.array([None])
        for i in range(0,raw_arr.shape[0]):
            arr = raw_arr[i,:]
            ellipse1 = ((arr[0],arr[1]),(arr[2],arr[3]),arr[4])
            ellipse2 = ((arr[5],arr[6]),(arr[7],arr[8]),arr[9])
            ellipse1_img = np.copy(background)
            ellipse2_img = np.copy(background)
            ellipse1_img = cv2.ellipse(ellipse1_img,ellipse1,(0,255,0),-1)
            ellipse2_img = cv2.ellipse(ellipse2_img,ellipse2,(0,255,0),-1)
            cv2.imshow("ellipse1",ellipse1_img)
            cv2.imshow("ellipse2",ellipse2_img)
            cv2.waitKey(0)
            if(chooseBool == True):
                print(True)
                if(denoised_arr.any() == None):
                     denoised_arr = raw_arr[i,:]
                else:
                     denoised_arr = np.vstack((denoised_arr,raw_arr[i,:]))

            chooseBool = False


