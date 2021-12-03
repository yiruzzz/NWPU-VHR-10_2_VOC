"""
code  by lyf0801 in 2021.03.14
"""
import shutil
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import xml.dom.minidom
import os
import sys
from PIL import Image


# 处理NWPU VHR-10数据集中的txt标注信息转换成 xml文件
# 此处的path应该传入的是NWPU VHR-10数据集文件夹下面的ground truth文件夹的目录
# 即 path = "D:/pytorch_code/NWPUintoVOC/NWPU VHR-10 dataset/ground truth"
def deal(path):
    files = os.listdir(path)  # files获取所有标注txt文件的文件名
    # 此处可以自行设置输出路径  按照VOC数据集的格式，xml文件应该输出在数据集文件下面的Annotations文件夹下面
    outpath = "D:/code/faster-rcnn-pytorch-master/VOCdevkit/VOC2007/Annotations/"
    # 如果输出文件夹不存在，就创建它
    if os.path.exists(outpath) == False:
        os.mkdir(outpath)
    # 遍历所有的txt标注文件，一共650个txt文件
    for file in files:

        filename = os.path.splitext(file)[0]  # 获取ground truth文件夹中标注txt文件的文件名，比如如果文件名为001.txt，那么filename = '001'
        print(filename)
        sufix = os.path.splitext(file)[1]  # 获取标注txt文件的后缀名 判断是否为txt
        if sufix == '.txt':  # 标注txt文件中每一行代表一个目标，(x1,y1)，(x2,y2)，class_number来表示
            xmins = []
            ymins = []
            xmaxs = []
            ymaxs = []
            names = []

            # num,xmins,ymins,xmaxs,ymaxs,names=readtxt(path + '/' + file)    # 调用readtxt文件获取信息，转到readtxt函数
            path_txt = path + '/' + file  # 获取txt标注文件的路径信息
            # 打开txt标注文件
            with open(path_txt, 'r') as f:
                contents = f.read()  # 将txt文件的信息按行读取到contents列表中
                print("contents:")
                print(contents)
                """一个输出例子：
                contents:
                (563,478),(630,573),1
                """
                objects = contents.split('\n')  # 以换行划分每一个目标的标注信息，因为每一个目标的标注信息在txt文件中为一行
                print("objects:")
                print(objects)
                """
                objects:
                ['(563,478),(630,573),1 ', '']
                """
                for i in range(objects.count('')):
                    objects.remove('')  # 将objects中的空格移除
                print("objects:")
                print(objects)
                """
                objects:
                ['(563,478),(630,573),1 ']
                """
                num = len(objects)  # 获取一个标注文件的目标个数，objects中一个元素代表的信息就是一个检测目标
                # print(num)
                # 遍历 objects列表，获取每一个检测目标的五维信息
                for objecto in objects:
                    print("objecto:")
                    print(objecto)
                    xmin = objecto.split(',')[0]  # xmin = '(563'
                    xmin = xmin.split('(')[1]  # xmin = '563' 可能存在空格
                    xmin = xmin.strip()  # strip函数去掉字符串开头结尾的空格符

                    ymin = objecto.split(',')[1]  # ymin = '478)'
                    print("ymin:")
                    print(ymin)
                    ymin = ymin.split(')')[0]  # ymin = '478'  可能存在空格
                    ymin = ymin.strip()  # strip函数去掉字符串开头结尾的空格符

                    xmax = objecto.split(',')[2]  # xmax同理
                    xmax = xmax.split('(')[1]
                    xmax = xmax.strip()

                    ymax = objecto.split(',')[3]  # ymax同理
                    ymax = ymax.split(')')[0]
                    ymax = ymax.strip()

                    name = objecto.split(',')[4]  # 与上 同理
                    name = name.strip()

                    if name == "1 " or name == "1":  # 将数字信息转换成label字符串信息
                        name = 'airplane'
                    elif name == "2 " or name == "2":
                        name = 'ship'
                    elif name == "3 " or name == "3":
                        name = 'storage tank'
                    elif name == "4 " or name == "4":
                        name = 'baseball diamond'
                    elif name == "5 " or name == "5":
                        name = 'tennis court'
                    elif name == "6 " or name == "6":
                        name = 'basketball court'
                    elif name == "7 " or name == "7":
                        name = 'ground track field'
                    elif name == "8 " or name == "8":
                        name = 'harbor'
                    elif name == "9 " or name == "9":
                        name = 'bridge'
                    elif name == "10 " or name == "10":
                        name = 'vehicle'
                    else:
                        print(path)
                    # print(xmin,ymin,xmax,ymax,name)
                    xmins.append(xmin)
                    ymins.append(ymin)
                    xmaxs.append(xmax)
                    ymaxs.append(ymax)
                    names.append(name)
                print("num,xmins,ymins,xmaxs,ymaxs,names")
                print(num, xmins, ymins, xmaxs, ymaxs, names)
                """
                num,xmins,ymins,xmaxs,ymaxs,names
                1 ['563'] ['478'] ['630'] ['573'] ['airplane']
                """
            print("num,xmins,ymins,xmaxs,ymaxs,names")
            print(num, xmins, ymins, xmaxs, ymaxs, names)
            filename_fill = str(int(filename)).zfill(6)  # 将xml的文件名填充为6位数。比如1.xml就改为00001.xml

            filename_jpg = filename_fill + ".jpg"  # 由于xml中存储的文件名为000001.jpg 所以还得对所有的NWPU数据集中的图片进行重命名

            dealpath = outpath + filename_fill + ".xml"

            # 注意，经过重命名转换之后，图片都存放在D:/pytorch_code/NWPUintoVOC/NWPU VHR-10 dataset/JPEGImages/中
            imagepath = "D:/code/faster-rcnn-pytorch-master/VOCdevkit/VOC2007/JPEGImages/" + filename_fill + ".jpg"
            with open(dealpath, 'w') as f:
                img = Image.open(imagepath)  # 根据图片的地址打开图片并获取图片的宽 和 高
                width = img.size[0]
                height = img.size[1]
                # 将图片的宽和高以及其他和VOC数据集向对应的信息
                writexml(dealpath, filename_jpg, num, xmins, ymins, xmaxs, ymaxs, names, height, width)

    #  同时也得给negatiive image set文件夹下面的所有负样本图片生成xml标注
    negative_path = "D:/dataset/OD/NWPU VHR-10 dataset/negative image set/"
    negative_images = os.listdir(negative_path)
    for file in negative_images:
        filename = file.split('.')[0]  # 获取文件名，不包括后缀名
        filename_fill = str(int(filename) + 650).zfill(6)  # 将xml的文件名填充为6位数。同时加上650，比如1.xml就改为00001.xml
        filename_jpg = filename_fill + '.jpg'  # 比如第一个负样本001.jpg的filename_jpg 为000651.jpg
        ## 重命名为6位数
        print(filename_fill)
        ## 生成不含目标的xml文件
        dealpath = outpath + filename_fill + ".xml"
        # 注意，经过重命名转换之后，图片都存放在D:/pytorch_code/NWPUintoVOC/NWPU VHR-10 dataset/JPEGImages/中
        imagepath = "D:/code/faster-rcnn-pytorch-master/VOCdevkit/VOC2007/JPEGImages/" + filename_fill + ".jpg"
        with open(dealpath, 'w') as f:
            img = Image.open(imagepath)
            width = img.size[0]
            height = img.size[1]
            # 将宽高和空的目标标注信息写入xml标注
            writexml(dealpath, filename_jpg, num=0, xmins=[], ymins=[], xmaxs=[], ymaxs=[], names=[], width=width,
                     height=height)

    # with open()


# NWPU数据集中标注的五维信息 (x1,y1) denotes the top-left coordinate of the bounding box,
#  (x2,y2) denotes the right-bottom coordinate of the bounding box
# 所以 xmin = x1  ymin = y1,  xmax = x2, ymax = y2  同时要注意这里的相对坐标是以图片左上角为坐标原点计算的
# VOC数据集对于包围框标注的格式是bounding-box（包含左下角和右上角xy坐标

# 将从txt读取的标注信息写入到xml文件中
def writexml(path, filename, num, xmins, ymins, xmaxs, ymaxs, names, height, width):  # Nwpu-vhr-10 < 1000*600
    node_root = Element('annotation')

    node_folder = SubElement(node_root, 'folder')
    node_folder.text = "VOC2012"

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = "%s" % filename

    node_size = SubElement(node_root, "size")
    node_width = SubElement(node_size, 'width')
    node_width.text = '%s' % width

    node_height = SubElement(node_size, 'height')
    node_height.text = '%s' % height

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '3'
    for i in range(num):
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = '%s' % names[i]
        node_name = SubElement(node_object, 'pose')
        node_name.text = '%s' % "unspecified"
        node_name = SubElement(node_object, 'truncated')
        node_name.text = '%s' % "0"
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'
        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = '%s' % xmins[i]
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = '%s' % ymins[i]
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = '%s' % xmaxs[i]
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = '%s' % ymaxs[i]

    xml = tostring(node_root, pretty_print=True)
    dom = parseString(xml)
    with open(path, 'wb') as f:
        f.write(xml)
    return


# 该代码主要解决的是图片的重命名问题，因为voc的图片是从000001.jpg开始，而且是6位数
def imag_rename(old_path, new_path, start_number=0):
    filelist = os.listdir(old_path)  # 该文件夹下所有的文件（包括文件夹）
    if os.path.exists(new_path) == False:
        os.mkdir(new_path)
    for file in filelist:  # 遍历所有文件
        Olddir = os.path.join(old_path, file)  # 原来的文件路径
        if os.path.isdir(Olddir):  # 如果是文件夹则跳过
            continue
        filename = os.path.splitext(file)[0]  # 文件名
        filetype = os.path.splitext(file)[1]  # 文件扩展名
        if filetype == '.jpg':
            Newdir = os.path.join(new_path, str(int(filename) + start_number).zfill(6) + filetype)
            # 用字符串函数zfill 以0补全所需位数
            shutil.copyfile(Olddir, Newdir)


if __name__ == "__main__":
    # # 由于xml中存储的文件名为000001.jpg 所以还得对所有的NWPU数据集中的图片进行重命名处理
    # 解决positive image set文件夹中的重命名问题，start_number = 0
    old_path = "D:/dataset/OD/NWPU VHR-10 dataset/positive image set/"
    new_path = "D:/code/faster-rcnn-pytorch-master/VOCdevkit/VOC2007/JPEGImages"
    imag_rename(old_path, new_path)
    # 解决negative image set文件夹中的重命名问题，start_number = 650
    old_path = "D:/dataset/OD/NWPU VHR-10 dataset/negative image set/"
    new_path = "D:/code/faster-rcnn-pytorch-master/VOCdevkit/VOC2007/JPEGImages"
    imag_rename(old_path, new_path, start_number=650)

    # path指定的是标注txt文件所在的路径
    path = "D:/dataset/OD/NWPU VHR-10 dataset/ground truth"
    deal(path)

    # VOC 数据集中的负样本是如何标注的，关于NWPU中的负样本图片也没有得到解决？

    # 如何划分NWPU的train集合和 val集合也是一个问题？？？
    # 随机划分吗？

