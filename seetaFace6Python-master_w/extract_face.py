from PIL import Image
import os
import face_recognition
import cv2
import numpy as np
import time
from face_recognize_core import face_detect_id
from seetaface.api import *

init_mask = FACE_DETECT
seetaFace = SeetaFace(init_mask)
seetaFace.SetProperty(DetectProperty.PROPERTY_MIN_FACE_SIZE, 80)
seetaFace.SetProperty(DetectProperty.PROPERTY_THRESHOLD, 0.9)


def recognise(image):
    """
    调用api返回识别结果
    dict{'0': 4个位置, 类别, 置信度, 加框图片}
    """
    global init_mask, seetaFace
    detect_result = seetaFace.Detect(image)
    face_locations = {}
    for i in range(detect_result.size):
        face = detect_result.data[i].pos
        top = face.y
        bottom = face.y + face.height
        left = face.x
        right = face.x + face.width
        face_image = image[top:bottom, left:right]
        face_locations[str(i)] = [top, bottom, left, right]
        face_id, p = face_detect_id(face_image)
        face_locations[str(i)].append(face_id)
        face_locations[str(i)].append(p)
        
    for key, info in face_locations.items():
        cv2.rectangle(image, (info[2], info[0]), (info[3], info[1]), (55, 255, 155), 2)
        cv2.putText(image, f'{info[4]} {float(info[5]) * 100: .2f}%', (info[2] - 10, info[0] - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (55, 255, 155), 2)
    
    return face_locations, image
    

def extract_recognise_face(data_path, save_path):
    """
    功能：原图提取人脸，并返回位置字典
    :param _data_path: 图片路径
    :param _save_path: 保存的提取结果的文件夹，保存多张人脸，图片命名为 i.png
    """
    init_mask = FACE_DETECT
    seetaFace = SeetaFace(init_mask)
    image = cv2.imread(data_path)
    seetaFace.SetProperty(DetectProperty.PROPERTY_MIN_FACE_SIZE, 80)
    seetaFace.SetProperty(DetectProperty.PROPERTY_THRESHOLD, 0.9)
    detect_result = seetaFace.Detect(image)
    face_locations = {}
    for i in range(detect_result.size):
        face = detect_result.data[i].pos
        top = face.y
        bottom = face.y + face.height
        left = face.x
        right = face.x + face.width
        face_image = image[top:bottom, left:right]
        face_image_resize = cv2.resize(face_image, (224, 224), interpolation=cv2.INTER_CUBIC)
        save_path_tmp = os.path.join(save_path, f'{i}.jpg')
        cv2.imwrite(save_path_tmp, face_image_resize)
        face_locations[str(i)] = [top, bottom, left, right]

    return face_locations


def face_recognise(test_path, face_locations):
    """
        功能：识别人脸，返回位置信息和id，p
        :param _test_path: 提取出的人脸路径
        :param _face_locations: 输入人脸位置信息
        """
    img_name_set = os.listdir(test_path)
    for img_name in img_name_set:
        if img_name != "result.jpg":
            image = cv2.imread(os.path.join(test_path, img_name))
            face_id, p = face_detect_id(image)
            # 加入 id和p的信息
            key = img_name[0]
            face_locations[key].append(face_id)
            face_locations[key].append(p)

    return face_locations


def paint_bbox(infos, data_path, save_path):
    """
        功能：将识别结果和框标在图上
        :param _infos: 人脸位置，id，p 信息
        :param _data_path: 原图
        :param _save_path: 保存路径文件夹
        """
    image = cv2.imread(data_path)
    for key, info in infos.items():
        cv2.rectangle(image, (info[2], info[0]), (info[3], info[1]), (55, 255, 155), 2)
        cv2.putText(image, f'{info[4]} {info[5]}', (info[2] - 10, info[0] - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (55, 255, 155), 2)

    cv2.imwrite(f'{save_path}/result.jpg', image)


if __name__ == '__main__':
    data_path = 'asserts/3.jpg'
    save_path = 'Result'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # step 1 将图片数据提取人脸
    T1 = time.time()
    face_locations = extract_recognise_face(data_path, save_path)
    time1 = (time.time() - T1) * 1000
    print(f'Extract time:{time1} ms')

    # step 2 人脸识别
    T2 = time.time()
    infos = face_recognise(save_path, face_locations)
    time2 = (time.time() - T2) * 1000
    print(f'Recognise time:{time2} ms')

    # step 3 加框
    paint_bbox(infos, data_path, save_path)



