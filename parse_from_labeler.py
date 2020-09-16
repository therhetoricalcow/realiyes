import os
import shutil
import cv2
import Augmentor
import re
from datetime import datetime
import numpy as np


##Function for Alphanumerically ordering file list
def sorted_nicely(l):
    """ Sorts the given iterable in the way that is expected.

    Required arguments:
    l -- The iterable to be sorted.

    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


now = datetime.now()
path_name = '/home/avaneesh/Desktop/Data_Set_'+now.strftime("%d_%m_%Y_%H_%M_%S")

os.mkdir(path_name)
os.mkdir(path_name + '/images')
os.mkdir(path_name + '/masks')

path_to_gui_img = '/home/avaneesh/Desktop/Images'
filelist = os.listdir(path_to_gui_img)
##Looking through Each of the folders in the test gui folder
img_num = 0
for infile in sorted_nicely(filelist):
    ## Left folder loop
    path_left_folder_labeled = path_to_gui_img + '/' + str(infile) + '/left/Labeled_Segments'
    path_left_folder = path_to_gui_img + '/' + str(infile) + '/left'
    left_file_list = os.listdir(path_left_folder_labeled) ##List of Labeled Images in Left Folder
    left_file_list = (sorted_nicely(left_file_list)) ## Labeled Images SOrted
    for left_labeled in left_file_list:
        shutil.copyfile(path_left_folder_labeled + '/' + str(left_labeled),path_name + '/masks/' + str(img_num) + '.png')
        shutil.copyfile(path_left_folder + '/' + str(left_labeled),path_name + '/images/' + str(img_num) + '.png')
        img_num = img_num + 1

    ## Right folder loop
    path_right_folder_labeled = path_to_gui_img + '/' + str(infile) + '/right/Labeled_Segments'
    path_right_folder = path_to_gui_img + '/' + str(infile) + '/right'
    right_file_list = os.listdir(path_right_folder_labeled) ##List of Labeled Images in Right Folder
    right_file_list = (sorted_nicely(right_file_list)) ## Labeled Images SOrted

    for right_labeled in right_file_list:
        shutil.copyfile(path_right_folder_labeled + '/' + str(right_labeled),path_name + '/masks/' + str(img_num) + '.png')
        shutil.copyfile(path_right_folder + '/' + str(right_labeled),path_name + '/images/' + str(img_num) + '.png')
        img_num = img_num + 1





