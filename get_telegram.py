#!/usr/bin/env python
# Dmitry Chastuhin
# Twitter: https://twitter.com/_chipik

import logging
import phonenumbers
import sqlite3
import sys

help_desc = '''
This script allows to get info about telegram messenger user by his phone number or nickname
--- chipik
'''

class TelegramInfo(object):
    def __init__(self):
        self.db_file = 'telegram_40m.db' # telegram leak from this thread https://xss.is/threads/38129/ 
        DEBUG = 0
        if DEBUG:
            self.logger = self.init_logger("TelegramInfo",logging.DEBUG)
        else:
            self.logger = self.init_logger("TelegramInfo", logging.INFO)
        self.logger.info("TelegramInfo started")

    def init_logger(self, logname, level):
        logger = logging.getLogger(logname)
        logger.setLevel(level)
        console_format = logging.Formatter("[%(levelname)-5s] %(message)s")
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(console_format)
        logger.addHandler(ch)
        return logger

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except sqlite3.Error as e:
            self.logger.info(e)
        return None

    def get_info_by_nik(self, nik):
        conn = self.create_connection()
        c = conn.cursor()
        find_info = "select nik, uid, phone from tg where nik == ?;"
        c.execute(find_info, (nik,))
        row = c.fetchone()
        conn.close()
        if row:
            return {'nik':row[0],'id':row[1],'phone':row[2]}
        else:
            return False

    def get_info_by_phone(self, phone):
        conn = self.create_connection()
        c = conn.cursor()
        find_info = "select nik, uid, phone from tg where phone == ?;"
        c.execute(find_info, (self.format_phone(phone),))
        row = c.fetchone()
        conn.close()
        if row:
            return {'nik':row[0],'id':row[1],'phone':row[2]}
        else:
            return False

    def format_phone(self, phone):
        if phone[:1] == '7':
            phone = f'+{phone}'
        elif phone[:1] == '8':
            phone = f'+7{phone[1:]}'
        x = phonenumbers.parse(phone, None)
        return phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.E164).replace('+','')
