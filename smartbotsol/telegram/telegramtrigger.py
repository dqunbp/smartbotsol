# -*- coding: utf-8 -*-

import telegram as tm
import os
import logging as log
from smartbotsol.telegram.utils.helpers import send_action
from telegram.chataction import ChatAction
from smartbotsol.telegram.utils.helpers import transform_keyboard_to_inline
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from smartbotsol import BaseTrigger

TYPING, UPLOAD_PHOTO = (ChatAction.TYPING, ChatAction.UPLOAD_PHOTO)

class TelegramTrigger(BaseTrigger):
    
    def __init__(self):
        self.user = None
        self.bot = None
        self.update = None

    def __str__(self):
        return str((self.user, self.bot, self.update))

    def get_chat_id(self):
        return self.update.message.chat_id if self.update else None

    def get_txt(self):
        return self.update.message.text if self.update else None

    def get_name(self):
        user = self.update.message.from_user
        return user.first_name if user.first_name else user.username

    def get_phone(self):
        user = self.update.message
        return user.contact.phone_number if user.contact else None

    def get_location(self):
        return self.update.message.location if self.update.message.location else None

    def get_venue(self):
        return self.update.message.venue if self.update.message.venue else None


    @send_action(TYPING)
    def send_msg(self, txt):
        return self.bot.sendMessage(chat_id=self.chat_id,
                             text=txt,
                             disable_web_page_preview=True,
                             parse_mode=tm.ParseMode.MARKDOWN)

    @send_action(TYPING)
    def send_keys(self, txt, keyboard, inline = False):
        reply_markup = tm.ReplyKeyboardMarkup(keyboard=keyboard,
                                              resize_keyboard=True,
                                              one_time_keyboard=True)
        if inline:
            inline_keyboard = transform_keyboard_to_inline(keyboard)
            log.debug(keyboard)
            reply_markup = InlineKeyboardMarkup(inline_keyboard)

        return self.bot.sendMessage(chat_id=self.chat_id,
                             text=txt,
                             disable_web_page_preview=True,
                             parse_mode=tm.ParseMode.MARKDOWN,
                             reply_markup=reply_markup)

    @send_action(UPLOAD_PHOTO)
    def send_photo(self, src):
        return self.bot.sendPhoto(chat_id=self.chat_id, photo=src)

    # will call 'get_chat_id' when accessing like obj.chat_id
    chat_id = property(get_chat_id)
    txt = property(get_txt)
    name = property(get_name)
    phone = property(get_phone)
    venue = property(get_venue)
    location = property(get_location)
