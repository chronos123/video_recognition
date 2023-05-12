from pydub import AudioSegment
import os
from tqdm import tqdm


def get_second_part_wav(main_mp3_path, start_time, end_time, part_wav_path):
    """
    音频切片, 获取部分音频, 单位秒, 一次截取出一个文件
    :param main_wav_path: 原音频文件路径
    :param start_time: 截取的开始时间
    :param end_time: 截取的结束时间
    :param part_wav_path: 截取后的音频路径
    :return:
    """
    start_time = start_time * 1000
    end_time = end_time * 1000

    sound = AudioSegment.from_mp3(main_mp3_path)
    word = sound[start_time:end_time]

    word.export(part_wav_path, format="wav")


def get_second_sound_people(database_path: str, save_dir: str):
    """_summary_
    对每个人的长音频截取为5秒的20个短音频
    Args:
        database_path (str): 输入音频文件
        save_dir (str): 输出音频文件夹, 一个文件夹中有一个人截取的32个音频片段
    """
    internal = 2
    for file in tqdm(os.listdir(database_path)):
        start_time = 0
        end_time = internal
        for i in range(round(54/internal)):
            file_name = os.path.join(database_path, file)
            name = file.split("_")[0]
            save_path = os.path.join(save_dir, f"{name}")     
            os.makedirs(save_path, exist_ok=True)
            save_path_a = os.path.join(save_path, f"{start_time}.wav")
            get_second_part_wav(file_name, start_time, end_time, save_path_a)
            start_time += internal
            end_time += internal
        
    return


if __name__ == '__main__':
    wav_path = "voicedatabase"
    part_path = "voicedatabase_part"
    get_second_sound_people(wav_path, part_path)




