import requests
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters

HF_TOKEN = "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"
BOT_TOKEN = "8988974276:AAE5M0Lhg6e4ZNlFxF7Lyi9KuvEuwBRP6sU"

def generate(prompt):
    url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    for i in range(5):  # 5 попыток
        r = requests.post(url, headers=headers, json={"inputs": prompt})
        
        if r.headers.get("Content-Type", "").startswith("image"):
            return r.content
        
        # Модель грузится — ждём
        print(f"Попытка {i+1}: {r.text}")
        time.sleep(10)
    
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
app.run_polling()
