#!/usr/bin/env python


import logging as logger
from telegram.ext import Handler, Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from smartbotsol.telegram.utils.helpers import extract_chat_and_user
from smartbotsol.telegram import TelegramTrigger

from telegram import Update
from smartbotsol import DictCache

class FsmTelegramHandler(Handler):

    def __init__(self, state_machine, users_cache=DictCache(), trigger=TelegramTrigger()):
        self.users_cache = users_cache
        self.state_machine = state_machine
        self.trigger = trigger

    def set_users_cache(self, store):
        pass

    def check_update(self, update):
        if not isinstance(update, Update):
            return False
        return True

    def handle_update(self, update, dispatcher):

        chat, usr = extract_chat_and_user(update)
        key = (chat.id, usr.id) if chat else (None, usr.id)
        user = self.users_cache.get(key)

        #wraper for telegram methods
        trigger = self.trigger
        trigger.bot = dispatcher.bot
        trigger.user = user
        trigger.update = update
        trigger.job_queue = dispatcher.job_queue
        
        self.state_machine.fire(trigger)
