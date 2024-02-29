#!/usr/env python3
# -*- coding: UTF-8 -*-
import os
import shutil
import time
import zipfile

from pydub import AudioSegment


# 给音频加水印
def add_watermark(source, watermark, i, save_audio):
    audio_ext = source.split('.')[-1]
    # 读取源音频
    source_audio = AudioSegment.from_file(source)
    # 读取水印音频
    watermark_audio = AudioSegment.from_file(watermark)
    # 将水印音频混合到源音频中
    mix_audio = source_audio.overlay(watermark_audio, position=i * 1000)
    # 保存混合后的音频
    mix_audio.export(save_audio, format=audio_ext)


# 获取音频的时长
def get_audio_duration(audio_source):
    source_audio = AudioSegment.from_file(audio_source)
    return len(source_audio) / 1000


# 给音频多次添加水印
def add_watermark_many_times(source, watermark, save_audio, num):
    duration = get_audio_duration(source)
    if duration == 0 or duration == None or duration == "" or duration < 4:
        # 时长为 0 的音频不添加水印,直接复制文件
        print(f'{source}时长为 0 的音频不添加水印,直接复制文件: {save_audio}')
        shutil.copyfile(source, save_audio)
        return
    if num > duration:
        num = int(duration / 2)

    # 每隔 15 秒添加一次水印
    for i in range(int(duration / num)):
        position = i * num
        if position > 0:
            source = save_audio
        add_watermark(source, watermark, position, save_audio)


# wav转mp3
def wav_to_mp3(source):
    save_audio = os.path.splitext(source)[0] + '.mp3'
    print(save_audio)
    try:
        # 读取源音频
        source_audio = AudioSegment.from_file(source)
        # 保存混合后的音频
        source_audio.export(save_audio, format="mp3")
    except:
        save_audio = None
    return save_audio


# 根据音乐文件名生成 zip 文件
def musics_to_zip(musics, zip_path):
    if len(musics) == 0:
        return None

    # 只获取文件名,不包含扩展名
    basename = os.path.basename(musics[0])
    base_name, ext = os.path.splitext(basename)
    zip_file_path = os.path.join(zip_path, base_name + '.zip')
    zip_file = zipfile.ZipFile(zip_file_path, 'w')
    for music in musics:
        zip_file.write(music, os.path.basename(music))

    zip_file.close()
    return zip_file_path


# 遍历目录下的所有文件的wav文件
def get_dirname_files(dir_path, format=".wav"):
    wav_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(format):
                wav_files.append(os.path.join(root, file))
    return wav_files

def dir_wav_to_mp3():
    dirname = r'J:\火花音乐\Spark Music-20231103\data'
    new_dirname = r'J:\火花音乐\Spark Music-20231103\data_new'
    if os.path.exists(new_dirname) == False:
        os.makedirs(new_dirname)

    music_files = get_dirname_files(dirname)
    for music in music_files:
        mp3 = wav_to_mp3(music)
        #检测是否转换成功
        if os.path.exists(mp3) == True:
            print(music + " conver to " + mp3 + " 成功")
        #检测mp3文件能否播放
        try:
            AudioSegment.from_file(mp3)
        except:
            print(mp3 + " 不能播放")
            continue

        #转成 mp3 之后删除 wav 文件
        if os.path.exists(music) == True:
            print(music + " 删除")
            os.remove(music)

def main():
    start_time = time.time()
    watermark = "watermark.mp3"
    dirname = r'J:\火花音乐\Spark Music-20231103\3'
    new_dirname = r'J:\火花音乐\Spark Music-20231103\data'

    if os.path.exists(new_dirname) == False:
        os.makedirs(new_dirname)

    music_files = get_dirname_files(dirname)
    for music in music_files:
        dir = music.split("\\")[-2]
        musicList = []
        musicList.append(music)

        mp3 = wav_to_mp3(music)
        #检测是否转换成功
        if os.path.exists(mp3) == True:
            print(music + " conver to " + mp3 + " 成功")
        else:
            print(music + " conver to " + mp3 + " 失败")
            continue

        musicList.append(mp3)

        save_path = new_dirname + "\\" + dir
        print(save_path)
        if os.path.exists(save_path) == False:
            os.makedirs(save_path)

        zip_path = musics_to_zip(musicList, save_path)
        if os.path.exists(zip_path) == True:
            print(zip_path + " 打包成功")
        else:
            print(zip_path + " 打包失败")
            continue

        save_audio = os.path.join(save_path, os.path.basename(mp3))
        add_watermark_many_times(mp3, watermark, save_audio, 15)
        if os.path.exists(save_audio) == True:
            #删除原文件
            os.remove(music)
            #删除转换后的文件
            os.remove(mp3)
            print(save_audio + " 添加水印成功")
        else:
            print(save_audio + " 添加水印失败")
            continue

    end_time = time.time()
    print("耗时: " + str(end_time - start_time) + " 秒")

if __name__ == '__main__':
    main()