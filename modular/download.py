################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

import asyncio
import os
import subprocess
import time
from datetime import timedelta
from time import time

import wget
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.file_id import *
from pyrogram.raw.functions.messages import *
from pyrogram.types import *
from youtubesearchpython import VideosSearch

from Mix import Emojik, YoutubeDownload, cgr, get_cgr, ky, progress

__modles__ = "Download"
__help__ = get_cgr("help_download")


def get_video_dimensions(file_path):
    width, height = 0, 0
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height",
        "-of",
        "csv=p=0:s=x",
        file_path,
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        dimensions = result.stdout.decode().split("x")
        if len(dimensions) == 2:
            width, height = map(int, dimensions)
    return width, height


def clear_directory(directory):
    command = ["rm", "-rf", directory]
    subprocess.run(command)


async def download_tiktok_video(context: Client, chat_id: int, tiktok_link: str):
    try:
        output_filename = "media/downloaded_video.%(ext)s"

        command = ["yt-dlp", "-o", output_filename, tiktok_link]
        subprocess.check_call(command)

        width, height = get_video_dimensions("media/downloaded_video.mp4")

        with open("media/downloaded_video.mp4", "rb") as video_file:
            await context.send_video(
                chat_id=chat_id,
                video=video_file,
                width=width,
                height=height,
                timeout=120,
            )

        clear_directory("media")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        await context.send_message(chat_id=chat_id, text="Tautan rusak.")


@ky.ubot("dtik", sudo=True)
async def download_tiktok_command(context: Client, message: Message):
    em = Emojik()
    em.initialize()
    tiktok_link = message.command[1] if len(message.command) > 1 else None
    if tiktok_link:
        pros = await message.reply(cgr("proses").format(em.proses))
        await asyncio.sleep(2)
        await download_tiktok_video(context, message.chat.id, tiktok_link)
        await pros.delete()


@ky.ubot("vtube", sudo=True)
async def _(c, m):
    em = Emojik()
    em.initialize()
    if len(m.command) < 2:
        return await m.reply(cgr("down_1").format(em.gagal, m.command))
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        search = VideosSearch(m.text.split(None, 1)[1], limit=1).result()["result"][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await pros.reply_text(cgr("err").format(em.gagal, error))
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=True)
    except Exception as error:
        return await pros.reply_text(cgr("err").format(em.gagal, error))
    thumbnail = wget.download(thumb)
    await c.send_video(
        m.chat.id,
        video=file_name,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        supports_streaming=True,
        caption=data_ytp.format(
            "VIDEO",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            c.me.mention,
        ),
        progress=progress,
        progress_args=(
            pros,
            time(),
            cgr("proses").format(em.proses),
            f"{search['id']}.mp4",
        ),
        reply_to_message_id=m.id,
    )
    await pros.delete()
    await m.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)


@ky.ubot("stube", sudo=True)
async def _(c, m):
    em = Emojik()
    em.initialize()
    if len(m.command) < 2:
        return await m.reply(cgr("down_1").format(em.gagal, m.command))
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        search = VideosSearch(m.text.split(None, 1)[1], limit=1).result()["result"][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await pros.edit(cgr("err").format(em.gagal, error))
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=False)
    except Exception as error:
        return await pros.edit(cgr("err").format(em.gagal, error))
    thumbnail = wget.download(thumb)
    await c.send_audio(
        m.chat.id,
        audio=file_name,
        thumb=thumbnail,
        file_name=title,
        performer=channel,
        duration=duration,
        caption=data_ytp.format(
            "AUDIO",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            c.me.mention,
        ),
        progress=progress,
        progress_args=(
            pros,
            time(),
            cgr("proses").format(em.proses),
            f"{search['id']}.mp3",
        ),
        reply_to_message_id=m.id,
    )
    await pros.delete()
    await m.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)
