from VoiceprintRecognition_Pytorch.mvector.predict import MVectorPredictor


predictor = MVectorPredictor(
    configs ='./VoiceprintRecognition_Pytorch/configs/ecapa_tdnn.yml',
    model_path ='./VoiceprintRecognition_Pytorch/VoiceprintRecognition_Pytorch-zhvoice-MelSpectrogram/models/ecapa_tdnn_MelSpectrogram/best_model/',
    use_gpu = True
    )

# ret = predictor.add_audio(r"VoiceprintRecognition_Pytorch\mvector\voicedatabase_wav\B18231008_2023437452.wav")
ret = predictor.create_audios("voicedatabase_part")
print(ret)
