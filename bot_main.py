import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
from dotenv import load_dotenv
from Task import Task


load_dotenv()

BOT_TOKEN=bot_token = os.getenv("BOT_TOKEN")
# Define conversation states
ENTER_RECEIVERS = 0
ENTER_TASK = 1

# Store user input


# Define a function to start the conversation
async def start(update: Update, context: CallbackContext) -> int:
    context.user_data['index'] = 0
    context.user_data['user_input'] = []
    context.user_data['receiver'] = []
    
    await update.message.reply_text("Please enter the task information in the format you provided earlier.")
    return ENTER_TASK

async def enter_field(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    print(context.user_data['index'])

    # Check if the user has finished entering all fields
    if context.user_data['index'] >= len(Task.get_task_fields())-1:
        context.user_data['user_input'].append(text)
        # Read the existing content of manually.py
        
        with open("manually.py", "r") as f:
            content = f.read()

        # Find the position in content to insert the new task
        insertion_point = content.find("Tasks=[")

        if insertion_point != -1:
            # Combine the user input into a single line and add it to manually.py at the correct position
            # task_line = f"Task({', '.join(user_input)}),"
            task_line="Task("
            count=0
            for item in Task.get_task_fields():
                print(count,task_line)
                if item is not "receivers":
                    task_line+=f"{item} = '{context.user_data['user_input'][count]}',"
                    
                    count+=1
                else:
                    task_line+=f"{item} = {context.user_data['receiver']},"
            task_line+='),\n'
            print(task_line)
            updated_content = content[:insertion_point + len("Tasks=[\n")] +task_line + content[insertion_point + len("Tasks=[\n") + 1 :]
            with open("manually.py", "w") as f:
                f.write(updated_content)

        await update.message.reply_text("Task added to manually.py.")
        return ConversationHandler.END

    # Ask for the next field
    else:
        context.user_data['user_input'].append(text)
        context.user_data['index'] += 1  # Increment the index
        remaining_fields = Task.get_task_fields()[context.user_data['index']]
           # Check if it's time to ask for receivers
        if Task.get_task_fields()[context.user_data['index']] == "receivers":
            context.user_data['receiver'].append(text)
            await update.message.reply_text("Please enter the receiver's username.")
            return ENTER_RECEIVERS
        await update.message.reply_text(f"Please enter the {remaining_fields}.")
        return ENTER_TASK

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
        entry_points=[CommandHandler("add_task", start)],
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

    # Register the conversation handler
    application.add_handler(conv_handler)

    # Start the bot
    application.run_polling()
