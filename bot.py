from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
import random
import datetime
import pytz
import os

# Function to generate period number
def generate_period_number() -> str:
    # Get current time in Indian timezone
    tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(tz)
    
    # Calculate period number
    start_time = datetime.datetime(current_time.year, current_time.month, current_time.day, 9, 0, 0, tzinfo=tz)
    diff = current_time - start_time
    minutes_passed = diff.total_seconds() / 60
    period_number = int(minutes_passed) + 1  # Period numbers start from 001
    
    if period_number > 439:
        period_number = 439
    
    return f"{period_number:03d}"

# Command handler for /start command
def start(update: Update, context: CallbackContext) -> None:
    # Check if the user is a member of any of the channels
    if update.message.chat.type == "private":
        user_id = update.message.from_user.id
        for channel_username in CHANNEL_USERNAMES:
            channel_member = context.bot.get_chat_member(channel_username, user_id)
            if channel_member.status == "left":
                update.message.reply_text(
                    f"To use this bot, please join {channel_username} first." +
                    "\n\nOnce you have joined the channel, please restart the bot."
                )
                return
    # If the user is a member of any channel or the message is not sent from private chat
    keyboard = [[InlineKeyboardButton("Get Prediction", callback_data='predict')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome! You are now eligible to use the prediction bot. Click the button below to get a prediction.", reply_markup=reply_markup)

# Callback handler for /predict command
def predict(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    options = ['red', 'green', 'big', 'small']
    selected_option = random.choice(options)
    period_number = generate_period_number()
    prediction_message = f"Period {period_number}: {selected_option.upper()}"
    query.message.reply_text(prediction_message)

def main() -> None:
    # Bot token
    TOKEN = os.environ.get("TOKEN")
    # Channel usernames
    CHANNEL_USERNAMES = ["@boss_igcc_store", "@boss_ig_cc_chats"]

    # Create the Updater and pass it the bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("predict", predict))
    dispatcher.add_handler(CallbackQueryHandler(predict, pattern='^predict$'))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == "__main__":
    main()
