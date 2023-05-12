from flask import Flask, Response, make_response, jsonify, request
import cv2
import datetime
import face_recognition
from flask_cors import CORS
import base64
import numpy as np
import time
from PIL import Image
import subprocess
from extract_face import recognise
import base64
import os
from face_recongnize_test import face_detect_id, face_detect_id_with_feature
from seetaface.api import *
import librosa
from scipy import signal
import pickle
from audio_rec import label_dict
from pydub import AudioSegment
from VoiceprintRecognition_Pytorch.mvector.predict import MVectorPredictor


# os.system("source ~/.bash_profile")
app = Flask(__name__)
CORS(app, supports_credentials=True)


predictor = MVectorPredictor(
    configs ='./VoiceprintRecognition_Pytorch/configs/ecapa_tdnn.yml',
    model_path ='./VoiceprintRecognition_Pytorch/VoiceprintRecognition_Pytorch-zhvoice-MelSpectrogram/models/ecapa_tdnn_MelSpectrogram/best_model/',
    use_gpu = True
    )


rec_image = None
init_mask = FACE_TRACK | FACE_DETECT | FACERECOGNITION | LANDMARKER5

seetaFace = SeetaFace(init_mask)
FS = 44100
FrameLen = 2048
camera = cv2.VideoCapture(0)
sos = signal.butter(10, 80, 'hp', fs=FS, output='sos')


@app.route('/video_feed0')
def video_feed0():
    return Response(gen_frames0(),mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_frames0():
    while 1:
        flag, frame = camera.read()
        frame = cv2.flip(frame, flipCode=1)
        if flag:
            detect_result = seetaFace.Track(frame)
            for i in range(detect_result.size):
                face = detect_result.data[i].pos
                points = seetaFace.mark5(frame, face)
                feature = seetaFace.Extract(frame, points)
                face_id, p, thresh = face_detect_id_with_feature(feature)
                height, width, _ = frame.shape
                cv2.rectangle(frame, (face.x, face.y), (face.x + face.width, face.y + face.height),(255, 0, 0), 2)
                if thresh > 0.18:
                    cv2.putText(frame,"id:%s %.2f %.2f"%(face_id, p, thresh),(face.x, face.y), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0,0,255))
                else:
                    cv2.putText(frame,"id:%s %.2f %.2f"%("no", p, thresh),(face.x, face.y), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0,0,255))
                PID = detect_result.data[i].PID  #同一张人脸没有离开视频则其PID 一般不会改变
                
            #把获取到的图像格式转换(编码)成流数据，赋值到内存缓存中;
            #主要用于图像数据格式的压缩，方便网络传输
            ret1, buffer = cv2.imencode('.jpg', frame)
            #将缓存里的流数据转成字节流
            frame_by = buffer.tobytes()
            #指定字节流类型image/jpeg
            yield  (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_by + b'\r\n')


@app.route("/face_recognition", methods=["POST"])
def face_rec():
    global rec_image
    if request.method != "POST":
        return "Call form get"
    if len(request.get_data()) != 0:
        image_b = str(request.get_data())
        head1, encode= image_b.split(',',1)
        img_b64decode = base64.b64decode(encode)
        img_array = np.frombuffer(img_b64decode,np.uint8)
        image = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
        cv2.imwrite("img.png", image)
        value_dict, rec_image = recognise(image)
        classes = []
        probs = []
        for key, value in value_dict.items():
            classes.append(value[4])
            probs.append(f"{float(value[5]): .4f}")
        
        time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ret, buffer = cv2.imencode('.jpg', rec_image)
        image_data = base64.b64encode(buffer)
        value_list = {
            "class": ", ".join(classes),
            "prob": ", ".join(probs),
            "time": time1,
            "image": str(image_data).strip("b'"),
        }
        response = make_response(value_list)
            # "image": image_data
        return response


@app.route("/audio_recognition", methods=["POST"])
def audio_rec():
    global clf
    if request.method == "POST":
        file = request.files['file']
        content = file.read()
        with open("audio.wav", "wb") as aud:
            aud.write(content)
        try:
            # _id, p = predictor.contrast_standard(content)
            ans_s = predictor.recognize_sum(content)

        # # AudioSegment.from_wav("audio.wav").export("audio.mp3", format="mp3")
        # os.system("del audio.mp3")
        # os.system("D:/ffmpeg-master-latest-win64-gpl-shared/ffmpeg-master-latest-win64-gpl-shared/bin/ffmpeg -i audio.wav -acodec libmp3lame audio.mp3")
        # audio_file, sample_rate = librosa.load("audio.mp3", sr=FS, res_type='scipy')
        # filtersig = signal.sosfilt(sos, audio_file)  # highpass filter
        # X, _ = librosa.effects.trim(filtersig, top_db=40, frame_length=FrameLen)  # Head and tail mute removal
        # leni = np.array(len(X)/sample_rate)
        # sample_rate = np.array(sample_rate)
        # mfcc = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=32, n_fft=FrameLen, hop_length=FrameLen)
        # length = len(mfcc.flatten())
        # if length > 1024:
        #     mfcc = mfcc.flatten()[:1024]
        # elif length < 1024:
        #     mfcc = np.pad(mfcc.flatten(), (1024 - length, 0))
        # mfcc = mfcc.reshape(-1, 1)
        # mfcc = np.repeat(mfcc, 32, axis=1)
        # mfcc = np.transpose(mfcc, (1, 0))
        # label = clf.predict(mfcc)[0]
        # _id = label_dict[label]
            time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            value_dicts = {}
            for i, ans in enumerate(ans_s):
                _id, p = ans
                value_dict = {
                    "class": _id,
                    "time": time1,
                    "prob": f"{float(p): .2f}",
                }
                value_dicts[i] = value_dict
            return jsonify(value_dicts)
        except:
            _id = "当前音频过短"
            p = "None"
            time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            value_dict = {
                "class": _id,
                "time": time1,
                "prob": p,
            }
            return jsonify(value_dict)
    else:
        return "Call from get", 404
    
    
@app.route("/rec_image/<name>")
def get_image():
    if rec_image is None:
        return "no image", 404
    else:
        ret, buffer = cv2.imencode('.jpg', rec_image)
        image_data = buffer.tobytes()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/jpg' #返回的内容类型必须修改
        return response


if __name__=='__main__':
    app.run(host='127.0.0.1', port="5004")
