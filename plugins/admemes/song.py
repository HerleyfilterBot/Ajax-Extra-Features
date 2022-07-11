from __future__ import unicode_literals

import os
import requests
import aiohttp
import yt_dlp
import asyncio
import math
import time

import wget
import aiofiles

from pyrogram import filters, Client
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL
import youtube_dl
import requests

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


@Client.on_message(filters.command('song') & ~filters.private & ~filters.channel)
def song(client, message):

    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply("**ѕєαrchíng чσur ѕσng...!**")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        performer = f"[ᗩᒍᗩ᙭]" 
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "**𝙵𝙾𝚄𝙽𝙳 𝙽𝙾𝚃𝙷𝙸𝙽𝙶 𝙿𝙻𝙴𝙰𝚂𝙴 𝙲𝙾𝚁𝚁𝙴𝙲𝚃 𝚃𝙷𝙴 𝚂𝙿𝙴𝙻𝙻𝙸𝙽𝙶 𝙾𝚁 𝚂𝙴𝙰𝚁𝙲𝙷 𝙰𝙽𝚈 𝙾𝚃𝙷𝙴𝚁 𝚂𝙾𝙽𝙶**"
        )
        print(str(e))
        return
    m.edit("**dσwnlσαdíng чσur ѕσng...!**")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        TEXT = title = results[0]["title"][:40]
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=TEXT, parse_mode='md',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit("**🚫 𝙴𝚁𝚁𝙾𝚁 🚫**")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

def get_text(message: Message) -> [None,str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " not in text_to_return:
        return None
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None


@Client.on_message(filters.command(["video", "mp4"]))
def song(client, message):

    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply("**ѕєαrchíng чσur ѕσng...!**")
    ydl_opts = {"format": "bestvideo[ext=mp4]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
        performer = f"[ᗩᒍᗩ᙭]" 
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "**𝙵𝙾𝚄𝙽𝙳 𝙽𝙾𝚃𝙷𝙸𝙽𝙶 𝙿𝙻𝙴𝙰𝚂𝙴 𝙲𝙾𝚁𝚁𝙴𝙲𝚃 𝚃𝙷𝙴 𝚂𝙿𝙴𝙻𝙻𝙸𝙽𝙶 𝙾𝚁 𝚂𝙴𝙰𝚁𝙲𝙷 𝙰𝙽𝚈 𝙾𝚃𝙷𝙴𝚁 𝚂𝙾𝙽𝙶**"
        )
        print(str(e))
        return
    m.edit("**dσwnlσαdíng чσur ѕσng...!**")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            Video_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        TEXT = title = results[0]["title"][:40]
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_video(video_file, caption=TEXT, parse_mode='md',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit("**🚫 𝙴𝚁𝚁𝙾𝚁 🚫**")
        print(e)

    try:
        os.remove(video_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

def get_text(message: Message) -> [None,str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " not in text_to_return:
        return None
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None
