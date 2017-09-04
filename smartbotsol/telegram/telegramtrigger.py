

import telegram as tm
import os
import logging as log
# from smartbotsol.telegram.utils.helpers import send_action
from telegram.chataction import ChatAction
from smartbotsol.telegram.utils.helpers import transform_keyboard_to_inline
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from smartbotsol import BaseTrigger

import types
import copy
from telegram.ext import Job
from functools import wraps

TYPING, UPLOAD_PHOTO = (ChatAction.TYPING, ChatAction.UPLOAD_PHOTO)

class JobTimeout(object):
    def __init__(self, timeout, latency):
        self.timeout = timeout
        self.latency = latency
        if timeout < 0:
            self.timeout = abs(timeout)
            log.error('TIMEOUT MUST BE A POSITIVE!')
        if latency:
            if timeout < latency:
                self.latency = 0
                log.error('TIMEOUT MUST BE A BIGGER THAN LATENCY YOU PASSED {} < {}!'.format(timeout, latency))
            if latency < 0:
                log.error('LATENCY MUST BE POSITIVE!')
            self.latency = self.timeout - abs(latency)

class job_decorator(object):
    def __init__(self, trigger):
        self.trigger = trigger
    def __call__(self, fn, *args, **kwargs):
        def telegram_job(bot, job):
            self.trigger.bot = bot
            log.debug('CALL DECORATED {}'.format(fn.__name__))
            log.debug('ARGS {}'.format([args, kwargs]))
            return fn(*args, **kwargs)
        return telegram_job

class allowjob(object):
    def __init__(self, action):
        self.action = action

    def __call__(self, func):
        action = self.action
        @wraps(func)
        def decorator(self, *args, **kwargs):
            if hasattr(self, 'job'):
                log.debug('FOND TIMEOUT ATTR LET\'S PUT FUNC {} TO JOB_QUEUE'.format(func.__name__))
                if self.job.latency != None:
                    send_action_job = job_decorator(self)(self.bot.send_chat_action, chat_id=self.chat_id, action=action)
                    self.job_queue.put(Job(send_action_job, self.job.latency, repeat=False))
                telegram_job = job_decorator(self)(func, self, *args, **kwargs)
                self.job_queue.put(Job(telegram_job, self.job.timeout, repeat=False))
            else:
                return func(self, *args, **kwargs)
                log.debug('FOND TIMEOUT ARGS LET\'S PUT TO JOIN QUEUE FUNC: {}'.format(func.__name__))
        return decorator

class TelegramTrigger(BaseTrigger):
    
    def __init__(self):
        self.user = None
        self.bot = None
        self.update = None
        self.job_queue = None

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

    def send_action(self, action):
        return self.bot.send_chat_action(chat_id=self.chat_id, action=action)


    # @send_action(TYPING)
    @allowjob(TYPING)
    def send_msg(self, txt):
        return self.bot.sendMessage(chat_id=self.chat_id,
                             text=txt,
                             disable_web_page_preview=True,
                             parse_mode=tm.ParseMode.MARKDOWN)

    @allowjob(TYPING)
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

    @allowjob(UPLOAD_PHOTO)
    def send_photo(self, src):
        return self.bot.sendPhoto(chat_id=self.chat_id, photo=src)

    # @classmethod
    def putjob(self, timeout, latency=1.5, **kwargs):
        # create copy of trigger if timeout passed
        if timeout is None:
            log.error('TIMEOUST IS NONE SKIP..')
        else:
            # new_trigger = self.__class__()
            # new_trigger.update = self.update
            # new_trigger.bot = self.bot
            # new_trigger.job_queue = self.job_queue
            # new_trigger.job = JobTimeout(timeout, latency)
            # self = new_trigger
            self.job = JobTimeout(timeout, latency)
        return self
        

        # def put_job(self, timeout, action=None):
        #     def job_wrap(bot, job):
        #             self.trigger.bot = bot
        #             return self.trigger
        #         # job_wrap = lambda bot, job: setattr(trigger, 'bot', bot)
        #         trigger.job_queue.put(
        #             Job(job_wrap, limit, repeat=False)
        #         )
        #         return 
        # def job(self, timeout, pre_job=None, repeat=False, next_t=0.0):
        #     self.update.job_queue.put()

    # will call 'get_chat_id' when accessing like obj.chat_id
    chat_id = property(get_chat_id)
    txt = property(get_txt)
    name = property(get_name)
    phone = property(get_phone)
    venue = property(get_venue)
    location = property(get_location)

