from create_id_label import id_list
from seetaface.api import *
import pandas as pd
import pickle

init_mask = FACE_DETECT | FACERECOGNITION | LANDMARKER5
seetaFace = SeetaFace(init_mask)


def get_feature(_face):
    feature = seetaFace.ExtractCroppedFace(_face)
    return feature


def save_dic(_dic, path):
    with open(path, "wb") as tf:
        pickle.dump(_dic, tf)
        
def add_id_feature(_id, _feature, _feature_path="test.pkl"):
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
    _feature_dic[_id] = _feature
    save_dic(_feature_dic, _feature_path)
    return _state


if __name__ == '__main__':
    feature_path = 'dataset'
    pd_file = pd.DataFrame(data=None)
    feature_dic = {}
    for usr_id in id_list:
        for i in range(0, 200):
            _img_name = usr_id + '_' + str(i) + '.jpg'
            tmp_path = os.path.join(feature_path, _img_name)
            if os.path.isfile(tmp_path):
                _image = cv2.imread(tmp_path)
                feature_tmp = seetaFace.ExtractCroppedFace(_image)
                feature_tmp = np.array(feature_tmp)
                feature_dic[usr_id] = feature_tmp
                break
    save_dic(feature_dic)
    print('done')
