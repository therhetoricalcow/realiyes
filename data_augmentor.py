import imageio
import imgaug as ia
import os
import random
from imgaug import augmenters as iaa
from imgaug.augmentables.segmaps import SegmentationMapsOnImage
import skimage
import numpy as np

##path to dataset
path_to_images = '/home/avaneesh/Desktop/Data_Set_15_09_2020_12_08_03/images'
path_to_masks = '/home/avaneesh/Desktop/Data_Set_15_09_2020_12_08_03/masks'
# list of names
image_name_list = os.listdir(path_to_images)
mask_name_list = os.listdir(path_to_masks)

##augmentation functions used in sequences pipeline
seq1 = iaa.Sequential([
    iaa.AdditiveGaussianNoise(scale=(0, 0.3), per_channel=True),
    iaa.Add((-25, 60)),
    iaa.JpegCompression(compression=(30, 87)),
    iaa.MedianBlur(k=(1, 3)),
    iaa.PiecewiseAffine(scale=(0.01,0.05)),
    iaa.Fliplr(0.5),
    iaa.Flipud(0.5),
    iaa.CoarseDropout((0.0, 0.09), size_percent=(0.02, 0.15))
], random_order=True)

seq2 = iaa.Sequential([
    iaa.GaussianBlur(sigma=(0, 3)),
    iaa.MultiplyHueAndSaturation((0.5, 1.5)),
    iaa.JpegCompression(compression=(45, 87)),
    iaa.PiecewiseAffine(scale=(0.01,0.05)),
    iaa.SaltAndPepper(p=(0.1, 0.15), per_channel=True),
    iaa.Fliplr(0.5),
    iaa.Flipud(0.5),
    iaa.CoarseDropout((0.0, 0.09), size_percent=(0.02, 0.15))
], random_order=True)

##divide the dataset into two batches
first_image_list = []
second_image_list = []
first_segmap_list = []
second_segmap_list = []
j = len(image_name_list)
k = 1
for i in range(len(image_name_list)):
    image = imageio.imread(path_to_images + '/' + image_name_list[i])
    corresp_mask = skimage.img_as_bool(imageio.imread(path_to_masks + '/' + mask_name_list[i]))
    print(i)
    if i < len(image_name_list) / 2:
        image_aug, seg_aug = seq1(image=image, segmentation_maps=SegmentationMapsOnImage(corresp_mask, shape=image.shape))

    else:
        image_aug, seg_aug = seq2(image=image, segmentation_maps=SegmentationMapsOnImage(corresp_mask, shape=image.shape))

    k = k+1
    mask_img = seg_aug.draw(size=None, colors=None)[0]
    mask_img[np.where((mask_img == [230, 25, 75]).all(axis=2))] = [255, 255, 255]
    imageio.imwrite(path_to_images + '/' + str(k + j) + '.png', image_aug)
    imageio.imwrite(path_to_masks + '/' + str(k + j) + '.png', mask_img)
    image = None
    corresp_mask = None
    image_aug = None
    seg_aug = None


