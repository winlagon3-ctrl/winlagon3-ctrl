import time
import os
import io
from huggingface_hub import InferenceClient
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters

HF_TOKEN = os.environ.get("HF_TOKEN")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

client = InferenceClient(api_key=HF_TOKEN)

def generate(prompt):
    try:
        image = client.text_to_image(
            prompt,
            model="black-forest-labs/FLUX.1-schnell"
        )
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        return buf
    except Exception as e:
        print(f"Ошибка генерации: {e}")
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
