# THIS IS A VERY OUTDATED CODE FOR OLD TELEGRAM API

import os
import re

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

load_dotenv()

# Retrieve the bot token from the environment variable
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

spam_keywords = [
    r"\bДоход\b",
    r"\bЗаработок\b",
    r"\bПишите в личные сообщения\b",
    r"\bУдалённый формат\b",
    r"\bUSD\b",
    r"\bдлр\b",
]

# Dictionary to keep track of new members
new_members = {}


def track_new_members(update: Update, context: CallbackContext):
    for member in update.message.new_chat_members:
        user_id = member.id
        new_members[user_id] = True


def check_first_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    message = update.message.text

    # Proceed only if the user is in new_members
    if new_members.get(user_id):
        # Check if the message contains any spam keywords
        for pattern in spam_keywords:
            if re.search(pattern, message, re.IGNORECASE):
                # Delete the message
                context.bot.delete_message(
                    chat_id=chat_id, message_id=update.message.message_id
                )
                # Ban the user
                context.bot.kick_chat_member(chat_id=chat_id, user_id=user_id)
                # Remove the user from new_members
                del new_members[user_id]
                return
        # If not spam, remove the user from new_members after their first message
        del new_members[user_id]


new_member_handler = MessageHandler(
    Filters.status_update.new_chat_members, track_new_members
)
dispatcher.add_handler(new_member_handler)


first_message_handler = MessageHandler(
    Filters.text & Filters.chat_type.groups, check_first_message
)
dispatcher.add_handler(first_message_handler)


updater.start_polling()
updater.idle()
