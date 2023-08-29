from telegram import Update,ReplyKeyboardMarkup,constants
from telegram.ext import filters, MessageHandler,ApplicationBuilder, ContextTypes, CommandHandler,ConversationHandler
import asyncio
import os
from dotenv import load_dotenv
import pickle


load_dotenv()

BOT_TOKEN=bot_token = os.getenv("BOT_TOKEN")

#TODO
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    menue_handler = ConversationHandler(
        entry_points=[
        CommandHandler('start', start),
        #MessageHandler(filters.TEXT & (~filters.COMMAND), unknown_command)
        ],
        fallbacks=[MessageHandler('BACK_TO_MAIN_MENU', send_main_menu)],
        states={
         HOME:[
                CommandHandler('start', start),
                MessageHandler(filters.Regex(labbels[HOME][0]),ready_to_add_channel),
                MessageHandler(filters.Regex(labbels[HOME][1]),list_channel),
         ],
         INSERTING_CHANNEL:[
                CommandHandler('start', start),
                MessageHandler(filters.TEXT,add_channel),
         ],
         SELECTING_CHANNEL:[
                CommandHandler('start', start),
                MessageHandler(filters.TEXT,collect_channel),
         ],
         SENDING_IMAGE:[
                CommandHandler('start', start),
                MessageHandler(filters.Document.ALL,income_file),
         ]
        }
    )
    application.add_handler(menue_handler)
    # print(dotenv_values(os.path.join(dir_path, ".env"))['PORT'])
    # application.run_webhook(
    # listen='0.0.0.0',
    # port = dotenv_values(os.path.join(dir_path, ".env"))['PORT'],
    # secret_token=secrets.token_urlsafe(16),
    # key='private.key',
    # cert='cert.pem',
    # webhook_url='https://{}:{}'.format(dotenv_values(os.path.join(dir_path, ".env"))['DOMAIN'], dotenv_values(os.path.join(dir_path, ".env"))['PORT'])
    # )
    application.run_polling()