import librosa
import numpy as np
from scipy import signal
import pickle

from audio_rec import label_dict


FS = 44100
FrameLen = 2048
sos = signal.butter(10, 80, 'hp', fs=FS, output='sos')

audio_file, sample_rate = librosa.load("./voicedatabase/B18231008_2023437452.mp3", sr=FS, res_type='scipy')
filtersig = signal.sosfilt(sos, audio_file)  # highpass filter
X, _ = librosa.effects.trim(filtersig, top_db=40, frame_length=FrameLen)  # Head and tail mute removal
leni = np.array(len(X)/sample_rate)
sample_rate = np.array(sample_rate)
mfcc = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=32, n_fft=FrameLen, hop_length=FrameLen)
length = mfcc.shape[1]
if length > 1024:
    mfcc = mfcc[:, :1024]
elif length < 1024:
    mfcc = np.pad(mfcc, (0, 1024 - length))
with open('clf.pickle', 'rb') as f:
    clf = pickle.load(f)
label = clf.predict(mfcc)[0]
_id = label_dict[label]

print(_id)

