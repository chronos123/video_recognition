import os

if os.path.isdir("voicedatabase_part"):
    os.system("rd /s /q voicedatabase_part")
os.system("python seg_audio.py")
os.system("python add_audio.py")
os.system("python test_predict.py")


