"""
this code was inspired by https://github.com/WZMIAOMIAO/deep-learning-for-image-processing/blob/master/pytorch_object_detection/faster_rcnn/split_data.py

recode by lyf0801 in 2021.03.14
"""
import os
import random

files_path = "D:/code/faster-rcnn-pytorch-master/VOCdevkit/VOC2007/JPEGImages/"
if not os.path.exists(files_path):
    print("文件夹不存在")
    exit(1)
val_rate = 0.2  # 设置train数据集占80%，测试占20%

files_name = sorted([file.split(".")[0] for file in os.listdir(files_path)])
files_num = len(files_name)
print(files_num)
val_index = random.sample(range(0, files_num), k=int(files_num*val_rate))
train_files = []
val_files = []
for index, file_name in enumerate(files_name):
    if index in val_index:
        val_files.append(os.path.join(files_path, file_name + '.jpg'))
    else:
        train_files.append(os.path.join(files_path, file_name + '.jpg'))

try:
    train_f = open("VOCdevkit/VOC2007/ImageSets/Main/train.txt", "x")
    eval_f = open("VOCdevkit/VOC2007/ImageSets/Main/val.txt", "x")
    train_f.write("\n".join(train_files))
    eval_f.write("\n".join(val_files))
except FileExistsError as e:
    print(e)
    exit(1)

