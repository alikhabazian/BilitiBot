import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
from dotenv import load_dotenv
from Task import Task
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

BOT_TOKEN=bot_token = os.getenv("BOT_TOKEN")
# Access the password variable
mongodb_password = os.getenv("MONGODB_PASSWORD")

# Use the password in your connection string or wherever needed
uri = f"mongodb+srv://khabaziana:{mongodb_password}@cluster0.l4miazp.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


# Define conversation states
ENTER_RECEIVERS = 0
ENTER_TASK = 1

async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('''
    Hi I'm Biliti bot.
I can help you to find a bus ticket from alibaba and snapp.
I will notify you when I find a ticket for you.
It is free for now but It requires resources so I encourage you /donate to me for keep this bot alive.
add your task with /add_task command.
and if you are not familiar with this bot you can use /help command to connect to admin.
    ''')

async def donate(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('''
You can donate to me by sending ether or USDC (ERC20) to this address:
0x1FbdFC3C41c65C8d2E578f0c0fFa52D0eDbcBA3F
or sending Rial to this card number:
6219-8619-2231-3464
and send me a message with your transaction id to khabaziana@gmail.com for get premium account if bot become paid.
    ''')


# Store user input
async def start_help(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('''
Please enter your question admin will answer you soon in this bot.
You can use /cancel command to cancel this conversation.
    ''')
    return 0

async def enter_help(update: Update, context: CallbackContext) -> int:
    await update.message.forward(chat_id='684630739')
    await context.bot.send_message('684630739', text=str(update.effective_user.id))
    await update.message.reply_text("Your message has been sent to the admins, they will contact you soon.")
    return ConversationHandler.END

async def start_answer(update: Update, context: CallbackContext) -> int:
    if update.effective_user.id=='684630739':
        await update.message.reply_text("Please enter userid")
        return 0
    else:
        await update.message.reply_text("You are not admin")
        return ConversationHandler.END

async def enter_answer(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Please enter your answer")
    return ConversationHandler.END

# Define a function to start the conversation
async def start_insert(update: Update, context: CallbackContext) -> int:
    context.user_data['index'] = 3
    context.user_data['user_input'] = {}
    # context.user_data['receiver'] = []

    context.user_data['user_input']['creator'] = str(update.effective_user.id)
    context.user_data['user_input']['receivers'] = [str(update.effective_user.id)]
    context.user_data['user_input']['how_often'] = [str('daily')]

    
    await update.message.reply_text('''
Please enter the task information in the requested format.
You can use /cancel command to cancel this conversation.
    ''')
    await update.message.reply_text(f"Pleaee enter the {Task.get_task_fields()[context.user_data['index']]['message']}")
    return ENTER_TASK

async def enter_field(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    print(context.user_data['index'])

    context.user_data['user_input'][Task.get_task_fields()[context.user_data['index']]['field_name']] = text
    context.user_data['index'] += 1  # Increment the index
    if context.user_data['index'] < len(Task.get_task_fields()) and Task.get_task_fields()[context.user_data['index']]['required']:
        await update.message.reply_text(f"Pleaee enter the {Task.get_task_fields()[context.user_data['index']]['message']}")
    else:
        task=Task(**context.user_data['user_input'])
        print(task)
        try:
            db = client.Biliti
            collection = db.Tasks
            document = task.__dict__
            collection.insert_one(document)
            await update.message.reply_text(
                f"Inserting task finished")
        except Exception as e:
            await update.message.reply_text("Your task has problem feel free to ask /help ")

        return ConversationHandler.END




    # # Check if the user has finished entering all fields
    # if context.user_data['index'] >= len(Task.get_task_fields())-1:
    #     context.user_data['user_input'].append(text)
    #     # Read the existing content of manually.py
    #
    #     with open("manually.py", "r") as f:
    #         content = f.read()
    #
    #     # Find the position in content to insert the new task
    #     insertion_point = content.find("Tasks=[")
    #
    #     if insertion_point != -1:
    #         # Combine the user input into a single line and add it to manually.py at the correct position
    #         # task_line = f"Task({', '.join(user_input)}),"
    #         task_line="Task("
    #         count=0
    #         for item in Task.get_task_fields():
    #             print(count,task_line)
    #             if item is not "receivers":
    #                 task_line+=f"{item} = '{context.user_data['user_input'][count]}',"
    #
    #                 count+=1
    #             else:
    #                 task_line+=f"{item} = {context.user_data['receiver']},"
    #         task_line+='),\n'
    #         print(task_line)
    #         updated_content = content[:insertion_point + len("Tasks=[\n")] +task_line + content[insertion_point + len("Tasks=[\n") + 1 :]
    #         with open("manually.py", "w") as f:
    #             f.write(updated_content)
    #
    #     await update.message.reply_text("Task added to manually.py.")
    #     return ConversationHandler.END
    #
    # # Ask for the next field
    # else:
    #     context.user_data['user_input'].append(text)
    #     context.user_data['index'] += 1  # Increment the index
    #     remaining_fields = Task.get_task_fields()[context.user_data['index']]
    #        # Check if it's time to ask for receivers
    #     if Task.get_task_fields()[context.user_data['index']] == "receivers":
    #         context.user_data['receiver'].append(text)
    #         await update.message.reply_text("Please enter the receiver's username.")
    #         return ENTER_RECEIVERS
    #     await update.message.reply_text(f"Please enter the {remaining_fields}.")
    #     return ENTER_TASK

async def enter_reciver(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if text=='Done':
        context.user_data['index'] += 1  # Increment the index
        return ENTER_TASK
    else:
        await update.message.reply_text("Please enter the next receiver's username or send Done.")
        context.user_data['receiver'] .append(text)
    return ENTER_RECEIVERS


async def cancel(update: Update, context: CallbackContext) -> int:

    await update.message.reply_text("Task creation canceled.")
    return ConversationHandler.END

if __name__ == "__main__":
    # Initialize the Telegram Bot API with your token
    application = ApplicationBuilder().token(BOT_TOKEN).build()



    # Create a conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add_task", start_insert)],
        states={
            ENTER_TASK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_field)
                ],
            ENTER_RECEIVERS:[
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_reciver),

                ],
            },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    help = ConversationHandler(
        entry_points=[CommandHandler("help", start_help)],
        states={
            0: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_help)
            ],

        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    answering = ConversationHandler(
        entry_points=[CommandHandler("answer", start_answer)],
        states={
            0: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_answer)
            ],

        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    donate=CommandHandler("donate", donate)

    start_handler=CommandHandler("start", start)


    # Register the conversation handler
    application.add_handler(conv_handler)
    application.add_handler(help)
    application.add_handler(answering)
    application.add_handler(donate)
    application.add_handler(start_handler)


    # Start the bot
    application.run_polling()
