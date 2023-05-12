import os.path
import pickle

from sklearn.metrics.pairwise import cosine_similarity
from seetaface.api import *
import numpy as np
import torch

init_mask = FACE_DETECT | FACERECOGNITION | LANDMARKER5
seetaFace = SeetaFace(init_mask)


def face_detect_id(_face, _feature_path='test.pkl'):
    """
    功能：根据输入面部的图像返回学号和置信概率
    :param _face: cv2格式的人脸图像
    :param _feature_path: 保存的特征路径
    :return: id，置信概率
    """
    with open(_feature_path, 'rb') as f:
        feature = seetaFace.ExtractCroppedFace(_face)
        feature = np.array(feature)
        feature_dic = pickle.load(f)
        sim_set = {}
        similarity = []
        for usr_id in feature_dic:
            contrast_feature = feature_dic[usr_id]
            sim = cosine_similarity(feature.reshape(1, -1), contrast_feature.reshape(1, -1))
            sim_set[usr_id] = sim
            similarity.append(sim)

        ans = max(sim_set.items(), key=lambda x: x[1])
        
        return ans[0], ans[1]


def add_id(_id, _face, _feature_path="test.pkl"):
    """
    功能：添加用户的面部特征
    :param _id: 用户编号
    :param _face: 用户的面部图像
    :param _feature_path: 保存的特征文件路径，如face_dic.pkl
    :return: state：{
        'update':更新用户
        'add'：添加用户
        'create'：创建新表
    }
    """
    if os.path.isfile(_feature_path):
        with open(_feature_path, 'rb') as f:
            _feature_dic = pickle.load(f)
        _state = 'update' if _id in _feature_dic else 'add'
    else:
        _feature_dic = {}
        _state = 'create'
    _feature_tmp = seetaFace.ExtractCroppedFace(_face)
    _feature_tmp = np.array(_feature_tmp)
    _feature_dic[_id] = _feature_tmp
    save_dic(_feature_dic, _feature_path)
    return _state


def del_id(_id, _feature_path):
    """
    :param _id: 用户编号
    :param _feature_path: 保存的特征文件路径，如face_dic.pkl
    :return: state：{
        'del':删除用户
        'no_usr'：没有该用户
        'no_file'：没有数据库
    }
    """
    if os.path.isfile(_feature_path):
        with open(_feature_path, 'rb') as f:
            _feature_dic = pickle.load(f)
        if _id in _feature_dic:
            del _feature_dic[_id]
            save_dic(_feature_dic, _feature_path)
            _state = 'del'
        else:
            _state = 'no_usr'
    else:
        _state = 'no_file'
    return _state


def save_dic(_dic, _feature_path):
    with open(_feature_path, "wb") as tf:
        pickle.dump(_dic, tf)


if __name__ == "__main__":
    # print(add_id("B18231008", cv2.imread("../1009.png")))
    del_id("B18231008", "test.pkl")
    