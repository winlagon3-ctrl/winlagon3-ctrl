import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters

HF_TOKEN = "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" 
BOT_TOKEN = "8988974276:AAE5M0Lhg6e4ZNlFxF7Lyi9KuvEuwBRP6sU"  

def generate(prompt):
    url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    r = requests.post(url,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": prompt}
    )
    return r.content

async def start(update: Update, context):
    await update.message.reply_text("Привет! Напиши промпт на английском, и я сгенерирую изображение.")

async def handle(update: Update, context):
    prompt = update.message.text
    await update.message.reply_text("Генерирую, подожди...")
    
    try:
        img = generate(prompt)
        await update.message.reply_photo(img)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
