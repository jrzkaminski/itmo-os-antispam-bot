import os
import re
import threading
import logging
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from telegram import Update
from telegram.ext import (
    Updater,
    MessageHandler,
    Filters,
    CallbackContext,
    Dispatcher,
)
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class SpamDetector:
    """
    A class responsible for detecting spam messages using a machine learning model.
    """

    def __init__(self, model_name: str):
        """
        Initialize the SpamDetector with the specified model.
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name, num_labels=1
        ).to(self.device).eval()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.homoglyphs = self._create_homoglyphs_mapping()

    @staticmethod
    def _create_homoglyphs_mapping() -> dict:
        """
        Create a mapping of Latin letters to their visually similar Cyrillic equivalents.
        """
        return {
            'A': 'А', 'a': 'а',
            'B': 'В', 'E': 'Е',
            'e': 'е', 'K': 'К',
            'M': 'М', 'H': 'Н',
            'O': 'О', 'o': 'о',
            'P': 'Р', 'C': 'С',
            'c': 'с', 'T': 'Т',
            'X': 'Х', 'y': 'у',
            'Y': 'У', 'p': 'р',
            'b': 'ь', 'I': 'І',
            'i': 'і', 'S': 'Ѕ',
            's': 'ѕ', 'd': 'ԁ',
            'D': 'Ԁ', 'f': 'ғ',
            'F': 'Ғ', 'g': 'ɡ',
            'G': 'Ԍ', 'l': 'ⅼ',
            'L': 'Ꮮ', 'n': 'ո',
            'N': 'Ν',
        }

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize the input text for spam detection.
        """
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        # Remove non-alphanumeric characters (excluding spaces)
        text = re.sub(r'[^А-Яа-яA-Za-z0-9 ]+', ' ', text)
        # Replace Latin letters with Cyrillic equivalents
        text = ''.join([self.homoglyphs.get(char, char) for char in text])
        # Convert to lowercase and strip whitespace
        text = text.lower().strip()
        return text

    def classify_message(self, message: str) -> bool:
        """
        Classify the message as spam or not spam.

        Returns:
            bool: True if the message is spam, False otherwise.
        """
        try:
            message = self.clean_text(message)
            encoding = self.tokenizer(
                message,
                padding='max_length',
                truncation=True,
                max_length=128,
                return_tensors='pt'
            )
            input_ids = encoding['input_ids'].to(self.device)
            attention_mask = encoding['attention_mask'].to(self.device)

            with torch.no_grad():
                outputs = self.model(input_ids, attention_mask=attention_mask).logits
                pred = torch.sigmoid(outputs).cpu().numpy()[0][0]

            is_spam = pred >= 0.5
            logger.debug(f"Message classified as {'spam' if is_spam else 'not spam'} with score {pred:.4f}")
            return is_spam
        except Exception as e:
            logger.error(f"Error in classify_message: {e}")
            return False  # Default to not spam if there's an error


class TelegramSpamBot:
    """
    A Telegram bot that detects and removes spam messages from new users.
    """

    def __init__(self, token: str, model_name: str):
        """
        Initialize the TelegramSpamBot.

        Args:
            token (str): The bot's API token.
            model_name (str): The name of the spam detection model.
        """
        self.updater = Updater(token, use_context=True)
        self.dispatcher: Dispatcher = self.updater.dispatcher
        self.spam_detector = SpamDetector(model_name)
        self.new_members = {}
        self.cleanup_interval = 600  # Time in seconds to track new users

        self._setup_handlers()

    def _setup_handlers(self):
        """
        Set up the message handlers for the bot.
        """
        new_member_handler = MessageHandler(
            Filters.status_update.new_chat_members, self.track_new_members
        )
        first_message_handler = MessageHandler(
            Filters.text & Filters.chat_type.groups, self.check_first_message
        )

        self.dispatcher.add_handler(new_member_handler)
        self.dispatcher.add_handler(first_message_handler)

    def start(self):
        """
        Start the bot.
        """
        logger.info("Starting the bot...")
        self.updater.start_polling()
        self.updater.idle()

    def track_new_members(self, update: Update, context: CallbackContext):
        """
        Track new members who join the chat.
        """
        try:
            for member in update.message.new_chat_members:
                user_id = member.id
                self.new_members[user_id] = True  # Mark user as new
                logger.info(f"New member joined: {member.full_name} (ID: {user_id})")
                # Set a timer to remove them after cleanup_interval
                timer = threading.Timer(
                    self.cleanup_interval,
                    self.remove_user_from_new_members,
                    args=(user_id,)
                )
                timer.start()
        except Exception as e:
            logger.error(f"Error in track_new_members: {e}")

    def remove_user_from_new_members(self, user_id: int):
        """
        Remove a user from the new_members tracking dictionary.
        """
        try:
            self.new_members.pop(user_id, None)
            logger.debug(f"User {user_id} removed from new_members tracking.")
        except Exception as e:
            logger.error(f"Error in remove_user_from_new_members: {e}")

    def check_first_message(self, update: Update, context: CallbackContext):
        """
        Check the first message sent by new members for spam.
        """
        try:
            user_id = update.message.from_user.id
            chat_id = update.message.chat_id
            message = update.message.text

            if self.new_members.get(user_id):
                is_spam = self.spam_detector.classify_message(message)
                if is_spam:
                    # Delete the message and ban the user
                    context.bot.delete_message(
                        chat_id=chat_id,
                        message_id=update.message.message_id
                    )
                    context.bot.kick_chat_member(chat_id=chat_id, user_id=user_id)
                    logger.warning(f"Banned user {user_id} for spam.")
                else:
                    logger.info(f"User {user_id} passed spam check.")

                # Remove the user from tracking after their first message
                self.remove_user_from_new_members(user_id)
        except Exception as e:
            logger.error(f"Error in check_first_message: {e}")

        # Additional methods can be added here for extended functionality


if __name__ == '__main__':
    # Retrieve the bot token from the environment variable
    BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    MODEL_NAME = 'RUSpam/spamNS_v1'

    if not BOT_TOKEN:
        logger.critical("Bot token not found. Please set the TELEGRAM_BOT_TOKEN environment variable.")
        exit(1)

    try:
        bot = TelegramSpamBot(token=BOT_TOKEN, model_name=MODEL_NAME)
        bot.start()
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")