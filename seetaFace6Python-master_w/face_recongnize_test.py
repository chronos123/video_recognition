# -*- coding: utf-8 -*-
# @Time    : 2023/4/23 22:11
# @Author  : wth
# @FileName: face_recongnize_test.py
# @Software: PyCharm
import os.path
import pickle
import time

from sklearn.metrics.pairwise import cosine_similarity

from create_id_label import id_list
from seetaface.api import *

init_mask = FACE_DETECT | FACERECOGNITION | LANDMARKER5
seetaFace = SeetaFace(init_mask)


'''
输入：cv2格式的人脸图像， 对比的人脸图像数量
输出：学号，置信度
'''


def face_detect_id(_image, feature_path='test.pkl'):
    with open(feature_path, 'rb') as f:
        feature = seetaFace.ExtractCroppedFace(_image)
        feature = np.array(feature)
        feature_dic = pickle.load(f)
        sim_set = {}
        
        for usr_id in id_list:
            contrast_feature = feature_dic[usr_id]
            sim = cosine_similarity(feature.reshape(1, -1), contrast_feature.reshape(1, -1))
            sim_set[usr_id] = sim

        ans = max(sim_set.items(), key=lambda x: x[1])
        return ans[0], ans[1]


def face_detect_id_with_feature(_feature, _feature_path='test.pkl'):
    """
    功能：根据输入面部的图像返回学号和置信概率
    :param _face: cv2格式的人脸图像
    :param _feature_path: 保存的特征路径
    :return: id，置信概率
    """
    with open(_feature_path, 'rb') as f:
        feature = np.array(_feature)
        feature_dic = pickle.load(f)
        sim_set = {}
        sim_feature = []
        for usr_id in feature_dic:
            contrast_feature = feature_dic[usr_id]
            sim = cosine_similarity(feature.reshape(1, -1), contrast_feature.reshape(1, -1))
            sim_set[usr_id] = sim
            sim_feature.append(sim)

        ans = max(sim_set.items(), key=lambda x: x[1])
        mean_feature = np.mean(np.array(sim_feature))
        max_mean = ans[1] - mean_feature
        # print(max_mean)
        return ans[0], ans[1], max_mean


if __name__ == '__main__':
    test_path = 'Test'
    img_name_set = os.listdir(test_path)
    ACC = 0
    NUM = 0
    Test_ID = 'B19376210'
    for img_name in img_name_set:
        image = cv2.imread(os.path.join(test_path, img_name))
        T1 = time.time()
        face_id, p = face_detect_id(image)
        print('i: %d Predict_ID: ' % NUM + face_id)
        print('Test time:%s ms' % ((time.time() - T1) * 1000))
        if face_id == Test_ID:
            ACC += 1
        NUM += 1
    acc = (ACC / NUM) * 100
    print('acc:%.1f' % acc)
