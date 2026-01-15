import discord
import asyncio
from collections import deque
import yt_dlp

TOKEN = ""

client = discord.Client()

# ===== CONFIG =====
FFMPEG_PATH = r"bin\ffmpeg.exe"
FFMPEG_OPTIONS = {"executable": FFMPEG_PATH, "options": "-vn"}
YDL_OPTIONS = {"format": "bestaudio/best", "quiet": True, "no_warnings": True, "noplaylist": True}

music_queues = {}
current_song = {}

def get_queue(guild_id):
    if guild_id not in music_queues:
        music_queues[guild_id] = deque()
    return music_queues[guild_id]


def play_next(vc, guild_id, channel):
    queue = get_queue(guild_id)
    if queue:
        url, title = queue.popleft()
        current_song[guild_id] = title

        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)

        def after_playing(error):
            play_next(vc, guild_id, channel)

        vc.play(source, after=after_playing)

        asyncio.run_coroutine_threadsafe(channel.send(f"▶ Started playing **{title}**"), client.loop)
    else:
        current_song[guild_id] = None
        asyncio.run_coroutine_threadsafe(channel.send("⏹ Queue ended."), client.loop)




@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()
    guild_id = message.guild.id
    vc = message.guild.voice_client

    # ===== PLAY =====
    if content.startswith("!play "):
        if not message.author.voice:
            await message.channel.send("❌ You are not in a voice channel.")
            return

        url = message.content.split(" ", 1)[1]

        if not vc:
            vc = await message.author.voice.channel.connect(reconnect=False)
            await message.channel.send(f"Joined **{message.author.voice.channel.name}**")

        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info["url"]
            title = info.get("title", "Unknown")

        queue = get_queue(guild_id)

        if vc.is_playing():
            queue.append((audio_url, title))
            await message.channel.send(f"➕ Added to queue: **{title}**")
        else:
            source = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
            vc.play(source, after=lambda e: play_next(vc, guild_id, message.channel))
            current_song[guild_id] = title
            await message.channel.send(f"▶️ Started playing **{title}**")

    # ===== STOP =====
    elif content == "!stop":
        if vc and (vc.is_playing() or vc.is_paused()):
            vc.stop()
        get_queue(guild_id).clear()
        await message.channel.send("⏹ Stopped and cleared the queue.")

    # ===== SKIP =====
    elif content == "!skip":
        if vc and vc.is_playing():
            vc.stop()
        else:
            await message.channel.send("❌ Nothing is playing.")


    # ===== QUEUE =====
    elif content == "!queue":
        queue = get_queue(guild_id)
        if not queue:
            await message.channel.send("📭 Queue is empty.")
        else:
            msg = "\n".join(f"{i+1}. {title}" for i, (_, title) in enumerate(queue))
            await message.channel.send(f"📜 **Queue:**\n{msg}")

    # ===== LEAVE =====
    elif content == "!leave":
        if vc:
            if vc.is_playing():
                vc.stop()
            get_queue(guild_id).clear()
            await vc.disconnect(force=True)
            await message.channel.send("👋 Left voice channel.")
        else:
            await message.channel.send("❌ I'm not in a voice channel.")



    elif content == "!help":
        help_text = (
            "🎵 **Music Bot Commands** 🎵\n"
            "!play <url> - Plays a song from YouTube or adds it to the queue if already playing.\n"
            "!skip - Skips the currently playing song.\n"
            "!stop - Stops playback and clears the queue.\n"
            "!queue - Shows the current queue of songs.\n"
            "!leave - Leaves the voice channel.\n"
            "!help - Shows this help message."
        )

        await message.channel.send(help_text)


client.run(TOKEN)
