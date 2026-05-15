import requests
import time
import asyncio
import os
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters

HF_TOKEN = os.environ.get("HF_TOKEN")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def main():
    bot = telegram.Bot(BOT_TOKEN)
    async with bot:
        await bot.delete_webhook(drop_pending_updates=True)

    def generate(prompt):
        url = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-2-1"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        for i in range(5):
            r = requests.post(url, headers=headers, json={"inputs": prompt})
            print(f"Попытка {i+1}: статус {r.status_code}, ответ: {r.text[:200]}")
            
            if r.headers.get("Content-Type", "").startswith("image"):
                return r.content
            
            time.sleep(15)
        
        return None

    async def start(update: Update, context):
        await update.message.reply_text("Привет! Напиши промпт на английском.")

    async def handle(update: Update, context):
        prompt = update.message.text
        await update.message.reply_text("Генерирую, подожди ~30 сек...")
        img = generate(prompt)
        if img:
            await update.message.reply_photo(img)
        else:
            await update.message.reply_text("Не удалось сгенерировать, попробуй ещё раз.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    await app.run_polling()

asyncio.run(main())
