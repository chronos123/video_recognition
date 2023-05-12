import subprocess 
import os
from tqdm import tqdm


base_dir = "voicedatabase"
target_dir = "voicedatabase_wav"

os.makedirs(target_dir, exist_ok=True)
for name in tqdm(os.listdir(base_dir)):
    file_path = os.path.join(base_dir, name)
    new_file_path = file_path.replace(base_dir, target_dir)
    new_file_path = new_file_path.replace("mp3", "wav")
    subprocess.run(f"D:/ffmpeg-master-latest-win64-gpl-shared/ffmpeg-master-latest-win64-gpl-shared/bin/ffmpeg -i {file_path} {new_file_path}")
    