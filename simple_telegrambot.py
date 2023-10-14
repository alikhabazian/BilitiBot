import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN=bot_token = os.getenv("BOT_TOKEN")

async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
"""Hello, I'm the Biliti bot. Please send your details to I will reserve ticket for you.
things you need to send me:
orgin_city : the city you want to start your trip from in persian
destination_city : the city you want to go in persian
date : the date you want to go
start_time : the start time of that date you want me search for you
end_time : the end time of that date you want me search for you"""
    )

async def forward_message(update: Update, context: CallbackContext) -> int:
    await update.message.forward(chat_id='684630739')
    await context.bot.send_message('684630739',text=str(update.effective_user.id))
    await update.message.reply_text("I have forwarded your message to the admins, they will contact you soon.")



if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    commandHandler=CommandHandler("start", start)

    messageHandler=MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message)

    # Register the conversation handler
    application.add_handler(commandHandler)
    application.add_handler(messageHandler)



    # Start the bot
    application.run_polling()