from VoiceprintRecognition_Pytorch.mvector.predict import MVectorPredictor


predictor = MVectorPredictor(
    configs ='./VoiceprintRecognition_Pytorch/configs/ecapa_tdnn.yml',
    model_path ='./VoiceprintRecognition_Pytorch/VoiceprintRecognition_Pytorch-zhvoice-MelSpectrogram/models/ecapa_tdnn_MelSpectrogram/best_model/',
    use_gpu = True
    )

res = predictor.recognize_sum("./voicedatabase_part/B19376210/20.wav", _print=True)

print(res)
