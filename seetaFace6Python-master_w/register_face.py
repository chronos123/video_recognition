#_*_coding:utf-8 _*_
"""
人脸追踪demo （用于视频模式下）
以打开本地摄像头为例
"""
import time

from face_recongnize_test import face_detect_id, face_detect_id_with_feature
from save_face_feature import add_id_feature
from seetaface.api import *

registerID = 'lhx'

"""
使用到的函数:
    Track：将测一帧中的人脸位置信息
    Reset: 更换视频源时，需要调用
    SetSingleCalculationThreads: 设置追踪处理的线程数
    SetInterval: #设置检测人脸间隔帧数
    SetMinFaceSize: 设置最小人脸检测大小，默认20
    SetThreshold: 设置人脸检测得分阈值
要加载的功能 :
    FACE_TRACK:人脸跟踪功能
"""
init_mask = FACE_TRACK | FACE_DETECT | FACERECOGNITION | LANDMARKER5

seetaFace = SeetaFace(init_mask)

camera = cv2.VideoCapture(0)

num = 30

if camera.isOpened():
    face_id = input('Please Input Your ID:')
    print('Please look at the Camera...')
    time.sleep(2)
    print('Start collect..')
    time.sleep(2)
    feature_set = []
    select_num = 0
    while 1:
        flag,frame = camera.read()
        if flag:
            detect_result = seetaFace.Track(frame)
            for i in range(detect_result.size):
                face = detect_result.data[i].pos
                points = seetaFace.mark5(frame, face)
                feature = seetaFace.Extract(frame, points)
                feature_set.append(np.array(feature))
                PID = detect_result.data[i].PID  #同一张人脸没有离开视频则其PID 一般不会改变
                cv2.rectangle(frame, (face.x, face.y), (face.x + face.width, face.y + face.height),(255, 0, 0), 2)
                cv2.putText(frame,"save %s..."%(face_id),(face.x,face.y),1,1,(0,0,255))
                select_num += 1
            cv2.imshow("track",frame)
            cv2.waitKey(30)
        time.sleep(0.1)
        if select_num >= num:
            break
    feature_set = np.array(feature_set)
    avg_feature = np.mean(feature_set, axis=0)
    state = add_id_feature(face_id, avg_feature, 'test.pkl')
else:
    print("摄像头打开失败！")

