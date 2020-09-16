import cv2
import imgaug as ia
import os
import random

image_list =  os.listdir('/home/avaneesh/Desktop/Data_Set_15_09_2020_12_08_03/images')
mask_list = os.listdir('/home/avaneesh/Desktop/Data_Set_15_09_2020_12_08_03/masks')


##augfunc1 is data augmenting with additive gaussian noise (per channel), Add, Jpeg compression and Median Blur
def augfunc1(images,agn_scale,add_value,jpeg_compression, mblur_k):

##augfunc2 is data augmenting with additive gaussian noise (per channel)
def augfunc2(images,agn_scale):

##augfunc3 is data augmenting with Add
def augfunc3(images,add_value):

##augfunc4 is data augmenting with jpeg compression
def augfunc4(images,jpeg_compression):

##augfunc5 is data augmenting with median blur
def augfunc5(images,mblur_k):

##augfunc6 is data augmenting with Gaussian Blur, Multiply Hue&Saturation, Jpeg Compression, Salt&Pepper
def augfunc6(images,gblur_k,mhs_value,jpeg_compression,sp_value):

##augfunc7 is data augmenting with Gaussian Blur
def augfunc7(images, gblur_k):

##augfunc8 is data augmenting with Multiply Hue&Saturation
def augfunc8(images, mhs_value):

##augfunc9 is data augmenting with Salt&Pepper
def augfunc9(images, sp_value):

