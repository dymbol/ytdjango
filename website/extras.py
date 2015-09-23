#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import youtube_dl
import os
from django.conf import settings
from website.models import *

downloaded_files = list()

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('YTDJANGO: Done downloading, now converting ...')
        downloaded_files.append(d['filename'])


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    #'verbose': True,
}

def download_yt_mp3(YT_url_object,url, user):

    print ("YTDJANGO: START prztwarzania {}".format(url))

    YT_url_object.status = 2
    YT_url_object.save()

    return_info = dict()
    return_info['info'] = "none"
    return_info['error'] = "none"

    #zmziana na string gdyz user pochodzi z request i nie jest stringiem
    user = str(user)
    #aktualny katalog
    master_dir = os.getcwd()

    #zmiana katalogu na katalog zapisu mp3
    path = settings.MAIN_MP3_DIR+"/"+user
    if not os.path.exists(path):
        print("YTDJANGO: No user dir '{}'").format(path)
        print("YTDJANGO: Creating path '{}'").format(path)
        os.mkdir(path)

    os.chdir(path)
    print("YTDJANGO: Using output dir {}").format(path)

    #ściąganie mp3
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        #zmiana statusu na zakończony
        YT_url_object.status = 3
        YT_url_object.save()

        #powrót do katalogu macierzystego
        os.chdir(master_dir)
        return_info['info'] = downloaded_files

    except Exception as error:
        #zmiana statusu na zakończony BLEDEM
        YT_url_object.status = 4
        YT_url_object.save()
        print error.args[0]
        return_info['error'] = ":".join(error.args[0].split(":")[2:])

    return return_info


