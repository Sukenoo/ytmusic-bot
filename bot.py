import telebot
import yt_dlp
import os

TOKEN = "8474736227:AAEo7Ry1vp2J49lBir__Um3vJKSHpD68D0Y"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎶 Send me a YouTube link or song name, and I’ll send it as an MP3 file!")

@bot.message_handler(func=lambda message: True)
def download_music(message):
    query = message.text.strip()
    bot.reply_to(message, "⏳ Downloading your song... please wait!")

    cache_dir = os.path.join(os.getcwd(), 'cache')
    os.makedirs(cache_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'default_search': 'ytsearch1',
        'nocheckcertificate': True,
        'cachedir': cache_dir,
        'cookiefile': 'cookies.txt',  # cookies fix
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        'extractor_args': {
            'youtube': {'player_client': ['android']},
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            title = info.get('title', 'Unknown Title')
            uploader = info.get('uploader', 'Unknown Artist')
            filename = f"{title}.mp3"

        caption = "🎧 Uploaded by @Sukenoo_yt_music_bot"

        with open(filename, 'rb') as audio:
            bot.send_audio(
                message.chat.id,
                audio,
                title=title,
                performer=uploader,
                caption=caption
            )

        os.remove(filename)
        print(f"✅ Sent: {title}")

    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")
        print(f"Error: {e}")

print("🤖 Bot is running...")
bot.polling()
