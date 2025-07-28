from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
import os
import time

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("STRING_SESSION")

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

@client.on(events.NewMessage(pattern=r'\.دز (\d+) (\d+)', func=lambda e: e.is_reply))
async def auto_post(event):
    try:
        delay = int(event.pattern_match.group(2))
        count = int(event.pattern_match.group(1))
        reply_msg = await event.get_reply_message()

        await event.reply(f"✅ بدأ النشر التلقائي لـ {count} رسائل بفاصل {delay} ثانية")
        
        for _ in range(count):
            await client.send_message(
                event.chat_id,
                reply_msg,
                reply_to=event.message.reply_to_msg_id
            )
            time.sleep(delay)

    except Exception as e:
        await event.reply(f"❌ خطأ: {str(e)}")

client.start()
client.run_until_disconnected()