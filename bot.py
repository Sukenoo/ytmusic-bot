import telebot
import yt_dlp
import os

# Replace this with your bot token
TOKEN = "8474736227:AAEo7Ry1vp2J49lBir__Um3vJKSHpD68D0Y"
bot = telebot.TeleBot(TOKEN)

# /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎶 Send me a YouTube link or song name, and I’ll send it as an MP3 file!")

# Handle all text messages
@bot.message_handler(func=lambda message: True)
def download_music(message):
    query = message.text.strip()

    bot.reply_to(message, "⏳ Downloading your song... please wait!")

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'default_search': 'ytsearch1',  # allows just song names
        'nocheckcertificate': True,
        'cachedir': os.path.join(os.getcwd(), 'cache'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',  # faster download
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

        # Optional: choose static or dynamic caption
        # 1️⃣ Static bot name version (recommended)
        caption = "🎧 Uploaded by @Sukenoo_yt_music_bot"

        # 2️⃣ Dynamic user version (uncomment below if you prefer)
        # user = message.from_user.username or message.from_user.first_name
        # caption = f"🎧 Requested by @{user}" if message.from_user.username else f"🎧 Requested by {user}"

        with open(filename, 'rb') as audio:
            bot.send_audio(
                message.chat.id,
                audio,
                title=title,
                performer=uploader,
                caption=caption
            )

        os.remove(filename)  # cleanup
        print(f"✅ Sent: {title}")

    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")
        print(f"Error: {e}")

print("🤖 Bot is running...")
bot.polling()
