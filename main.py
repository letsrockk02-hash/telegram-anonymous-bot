from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7406500942

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.chat_id
    text = update.message.text

    msg = f"📩 New Anonymous Message\nUserID:{uid}\n\n{text}"

    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
    await update.message.reply_text("✅ Message sent anonymously.")

async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        try:
            original = update.message.reply_to_message.text
            uid = int(original.split("UserID:")[1].split("\n")[0])

            await context.bot.send_message(
                chat_id=uid,
                text=f"📨 Admin Reply:\n{update.message.text}"
            )
        except:
            await update.message.reply_text("❌ Reply failed.")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.User(ADMIN_ID), user_message))
app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_ID), admin_reply))

app.run_polling()
