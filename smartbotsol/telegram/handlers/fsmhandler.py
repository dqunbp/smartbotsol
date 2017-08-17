#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging as logger
from telegram.ext import Handler, Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from smartbotsol.utils.helpers import extract_chat_and_user
from smartbotsol.telegram import TelegramTrigger

from telegram import Update

class fsmTelegramHandler(Handler):

    def __init__(self, users_store, state_machine, trigger=TelegramTrigger()):
        self.users_store = users_store
        self.state_machine = state_machine
        self.trigger = trigger


    def check_update(self, update):
        if not isinstance(update, Update):
            return False
        return True

    def handle_update(self, update, dispatcher):

        chat, usr = extract_chat_and_user(update)
        key = (chat.id, usr.id) if chat else (None, usr.id)
        user = self.users_store.get(key)

        #wraper for telegram methods
        trigger = self.trigger
        trigger.bot = dispatcher.bot
        trigger.user = user
        trigger.update = update
        
        self.state_machine.fire(trigger)
