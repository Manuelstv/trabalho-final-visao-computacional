# -*- coding: utf-8 -*-
"""yolo_file_manipulation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FvkyprgkqJhSbVs1vpmnetukVZL2vrSl
"""

import os
import pandas as pd
from fileinput import input as fileinput
import glob
import shutil
from sklearn.model_selection import train_test_split

DIR_PATH = '/media/bycrop/byCrop_Dataset/SUN3601024x512/pano1024x512/indoor'

dir = os.listdir(DIR_PATH)

#only select files with both .txt and .JPG formats
images = [x for x in os.listdir(DIR_PATH) if x[-3:] == "jpg"]
#images = [x.replace("JPG", "txt") for x in os.listdir(DIR_PATH) if x[-3:] == "JPG"]

def intersection(list_1, list_2):
    list_3 = [value for value in list_1 if value in list_2]
    return list_3

#annotation_list = intersection(images, annotations) 
#images = [x.replace("txt", "JPG") for x in annotations]
print(images)

print("Número de imagens: {}".format(len(images)))

images.sort()
#annotations.sort()

# Split the dataset into train-valid-test splits 
#train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size = 0.2, random_state = 1)
#val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size = 0.5, random_state = 1)

train_images = images[0:2000]
val_images = images[2000:2500]
test_images = images[2000:2500]


#Utility function to move images 
def move_files_to_folder(list_of_files, destination_folder):
    for file in list_of_files:
        try:
            shutil.copy(f"{DIR_PATH}/{file}", f"{destination_folder}")
        except:
            print(file)
            assert False

# Move the splits into their folders
move_files_to_folder(train_images, '/media/bycrop/byCrop_Dataset/SUN3601024x512/pano1024x512/train/indoor')
move_files_to_folder(val_images, '/media/bycrop/byCrop_Dataset/SUN3601024x512/pano1024x512/val/indoor')
move_files_to_folder(test_images, '/media/bycrop/byCrop_Dataset/SUN3601024x512/pano1024x512/test/indoor')
#move_files_to_folder(train_annotations, '/media/bycrop/byCrop_Dataset/SUN3601024x512/pano1024x512/train')
#move_files_to_folder(val_annotations, '/media/bycrop/byCrop_Dataset/SUN3601024x512/pano1024x512/val')
#move_files_to_folder(test_annotations, '/media/bycrop/byCrop_Dataset/SUN3601024x512/pano1024x512/test')
