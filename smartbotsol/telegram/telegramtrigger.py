

import telegram
import os
import logging
from smartbotsol.telegram.utils.helpers import send_action
from telegram.chataction import ChatAction
from smartbotsol.telegram.utils.helpers import transform_keyboard_to_inline
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

from smartbotsol import BaseTrigger

TYPING, UPLOAD_PHOTO = (ChatAction.TYPING, ChatAction.UPLOAD_PHOTO)
log = logging.getLogger(__name__)

class TelegramTrigger(BaseTrigger):
    """Wrap for telegram bot update"""


    def __init__(self):
        self.user = None
        self.bot = None
        self.update = None
        
        self.default_message_kwargs = {
            'parse_mode': telegram.ParseMode.MARKDOWN,
            'disable_web_page_preview': True,
            'disable_notification': True
        }
        self.default_markup_kwargs = {
            'resize_keyboard': True,
            'one_time_keyboard': False,
        }

    def __str__(self):
        return str((self.user, self.bot, self.update))

    def _get_chat_id(self):
        return self.update.message.chat_id if self.update else None

    def _get_text(self):
        return self.update.message.text if self.update else None

    def _get_name(self):
        user = self.update.message.from_user
        return user.first_name if user.first_name else user.username

    def _get_phone(self):
        user = self.update.message
        return user.contact.phone_number if user.contact else None

    def _get_location(self):
        return self.update.message.location if self.update.message.location else None

    def _get_venue(self):
        return self.update.message.venue if self.update.message.venue else None

    def send_venue(self, title, address, location):
        """Sends telegram location"""
        assert isinstance(location, list)
        return self.bot.sendVenue(
            chat_id=self.chat_id,
            latitude=location[0],
            longitude=location[1],
            title=title,
            address=address
        )

    def send_message(self, text, remove_keyboard=False, **kwargs):
        """Sends telegram message"""
        message_kwargs = self.default_message_kwargs.copy()
        message_kwargs.update(**kwargs)
        if remove_keyboard:
            message_kwargs.setdefault(
                'reply_markup',
                ReplyKeyboardRemove()
            )
        return self.bot.sendMessage(
            chat_id=self.chat_id,
            text=text,
            **message_kwargs
        )

    def send_keyboard(self, text, keyboard, inline=False,**kwargs):
        """Sends telegram message with keyboard"""
        message_kwargs = self.default_message_kwargs.copy()
        markup_kwargs = self.default_markup_kwargs.copy()
        message_kwargs.update(
            {k: v for k,v in kwargs.items() if k in self.default_message_kwargs}
        )
        markup_kwargs.update(
            {k: v for k,v in kwargs.items() if k in self.default_markup_kwargs}
        )

        reply_markup = telegram.ReplyKeyboardMarkup(
            keyboard=keyboard,
            **markup_kwargs
        )
        if inline:
            reply_markup = InlineKeyboardMarkup(
                transform_keyboard_to_inline(keyboard),
                **markup_kwargs
            )
        return self.bot.sendMessage(
            chat_id=self.chat_id,
            text=text,
            reply_markup=reply_markup,
            **message_kwargs
        )

    def send_photo(self, src):
        return self.bot.sendPhoto(chat_id=self.chat_id, photo=src)

    chat_id = property(_get_chat_id)
    text = property(_get_text)
    name = property(_get_name)
    phone = property(_get_phone)
    venue = property(_get_venue)
    location = property(_get_location)
