#!/usr/bin/env python
# Dmitry Chastuhin
# Twitter: https://twitter.com/_chipik
import datetime

from getcontact import get_number_info, send_captcha_bot, get_vars, set_new_aes_key, set_new_token, set_new_exp, set_new_device_id, get_env_data
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from numbuster import get_number_info_NumBuster
from prettytable import from_db_cursor
from auto import get_session, get_capcha, get_fio_by_vin, get_sessinon_and_captcha_easto, get_vin
from email2pwd import get_password
import get_telegram
import argparse
import logging
import sqlite3
import string
import random
import sys
import re
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

help_desc = '''
This is telegram bot that allows you to easily get info about phone numbers using reversed API of `GetContact` android app
--- chipik
'''

format_text = "Please use this phone format: +XXXXXXXXXXX (Ex: +79876543210)"

message_size_limit = 4096

parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-t', '--token', help='Telegram bot token')
# parser.add_argument('-p', '--pwd', default=''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(10)), help='admin password for bot management')
parser.add_argument('-v', '--debug', action='store_true', help='Show debug info')
args = parser.parse_args()

bot_token = '' # Write yor own bot token here 
sqlite_file = 'bot_db.sqlite'
admin_id = 11111111  # bot owner id here
whitelist_status = 1 # Whitelist status. 1 - enabled, 0 - disabled
getcontact_status = 1 # Getcontact status. 1 - enabled, 0 - disabled
numbuster_status = 0 # Numbuster status. 1 - enabled, 0 - disabled
tg_status = 1 # Telegram info status. 1 - enabled, 0 - disabled
demoreqests_nbr = 2 # Number of requests in demo mode
remain_count = len(get_env_data())*10 # Number of remain requests
REQUEST_KWARGS={}

vin_db = {}
def init_logger(logname, level):
    # generic log conf
    logger = logging.getLogger(logname)
    logger.setLevel(level)
    console_format = logging.Formatter("[%(levelname)-5s] %(message)s")
    # console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(console_format)
    logger.addHandler(ch)
    return logger


if args.debug:
    logger = init_logger("ya_perezvonu", logging.DEBUG)
else:
    logger = init_logger("ya_perezvonu", logging.INFO)


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        logger.info(e)
    return None


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="This Bot allows you to get information about phone number.\n"
                                                          "Feel free to use it while it works :)\n"
                                                          "Contacts: u can send message to the author via /say command\n"
                                                          "I am not guilty if you quarrel with your partner after this (lol)")


def help(bot, update):
    # help_msg = "Just type the phone number and you will get an answer.\n" \
    #            "You can control me by sending these commands:\n" \
    #            "/help - this message\n" \
    #            "/remain -  number of requests remaining (300 requests a day)\n" \
    #            "/captcha - enter captcha\n" \
    #            "/vin <vin_number> - get car owner name by VIN number\n" \
    #            "/plate <A111AA777> - get car owner name by plate number\n" \
    #            "/pwd <lalala@gmail.com> - get password by email address\n" \
    #            "/invite - request invite\n"\
    #            "/batya - about\n" \
    #            "Have fun!"
    help_msg = "Just type the phone number and you will get an answer.\n" \
               "You can control me by sending these commands:\n" \
               "/help - this message\n" \
               "/remain -  number of requests remaining (300 requests a day)\n" \
               "/captcha - enter captcha\n" \
               "/invite - request invite\n"\
               "/batya - about\n" \
               "/tg - get info by telegram username\n" \
               "Have fun!"
    bot.send_message(chat_id=update.message.chat_id, text=help_msg)


def get_phone_info(bot, chat_id, user, phone_number):
    to_client = ""
    if '+' not in phone_number:
        phone_number = "+{}".format(phone_number)
    if re.match(r"\+(\d)+", phone_number): #best regex ever here
        rez = get_number_info(phone_number)
    else:
        rez = (400,)
    if rez[0] == 200:
        to_client = prepare_msg(rez[1][0]["displayName"], rez[1][0]["tags"], 0)
        log_reamins(rez[1][1])
    elif rez[0] == 400:
        to_client = "Wrong phone number!\n{}".format(format_text)
    elif rez[0] == 404:
        to_client = "Nothing found :("
    elif rez[0] == 403:
        if rez[1][0] == '403004':
            to_client = "Captcha happend! Type */captcha code_from_picture*"
            capthca_img = rez[1][1]
            bot.send_photo(chat_id=chat_id, photo=open(capthca_img, 'rb'))
        elif rez[1][0] == '403020':
            to_client = "We will begin to show results soon for this country"
        else:
            to_client = "Something wrong"
    else:
        to_client = "Something wrong"

    # log_request("{}".format(user.name), phone_number, to_client)
    logger.info("Result:{}".format(to_client.encode('utf-8').strip()))
    return to_client


def get_phone_info_nb(bot, chat_id, user, phone_number):
    to_client = ""
    if '+' in phone_number:
        phone_number = phone_number.replace('+', '')
    if re.match(r"(\d)+", phone_number): #best regex ever here
        rez = get_number_info_NumBuster(phone_number)
    else:
        rez = (400,)
    if rez[0] == 200:
        to_client = rez[1]
    elif rez[0] == 400:
        to_client = "Wrong phone number!\n{}".format(format_text)
    elif rez[0] == 428:
        to_client = "Too many request"
    else:
        to_client = "Something wrong"
    logger.info("Result:{}".format(to_client))
    return to_client

def get_info_from_tg(phone_number):
    tg_info = get_telegram.TelegramInfo()
    result = tg_info.get_info_by_phone(phone_number)
    if result:
        result_msg = f"Nickname: @{result['nik']}\n" \
                     f"Phone: +{result['phone']}\n" \
                     f"id: {result['id']}"
    else:
        result_msg = "Nothing found :("
    logger.info("Result from tg:{}".format(result_msg))
    return result_msg

def check_demorequest(id):
    if get_demoreqests_for_user(id) <= demoreqests_nbr+1:
        return True
    elif check_demotime(id):
        return True
    elif check_admin(id):
        return True
    elif check_whitelist(id):
        return True
    else:
        return False


def get_info(bot, update):
    global vin_db
    # log_request("{}:{}".format(update.message.from_user.name,update.message.from_user.id), update.message.text, "")
    logger.info("{}({}) is searching for {}".format(update.message.from_user.name, update.message.from_user.id,
                                                    update.message.text))
    if not check_demorequest(update.message.from_user.id):
        reply(bot, update, 'You had only {}. You have run out of demo requests. Please wait 24 hours. Or request an invite for unlimeted requesrs (friends only).'.format(demoreqests_nbr))
    if not check_user(username=update.message.from_user.name, id=update.message.from_user.id):
        if whitelist_status == 1:
            reply(bot, update, 'This is invite only bot now! He-he-he.\nYou can request invite and I will add you (or not :) ).\nJust type:\n/invite <!!Your message here!!>\nFor example:\n/invite i\'m from Vasya')
        else:
            reply(bot, update, 'Nothing found :(')
        log_request("{}:{}".format(update.message.from_user.name, update.message.from_user.id), update.message.text, "")
        return 0
    if update.message.from_user.name in vin_db.keys() and vin_db[update.message.from_user.name]['captcha1'] == 'NEED' :
        vin_db[update.message.from_user.name]['captcha1'] = update.message.text
        rez = get_vin(vin_db[update.message.from_user.name]['sess1'], vin_db[update.message.from_user.name]['plate'], vin_db[update.message.from_user.name]['captcha1'])
        logger.info("VIN: {}".format(rez))
        if rez:
            text = 'Vin: '+rez
        else:
            text = 'Nothing found :(. Looks like that car is new and don\'t have a diagnostic card'
        reply(bot, update, text)
        if rez:
            get_fio_by_vin_bot(bot, update, [rez])
        log_request("{}:{}".format(update.message.from_user.name, update.message.from_user.id), update.message.text, "")
        return 0
    if update.message.from_user.name in vin_db.keys() and vin_db[update.message.from_user.name]['captcha2'] == 'NEED' :
        vin_db[update.message.from_user.name]['captcha2'] = update.message.text
        rez = get_fio_by_vin(vin_db[update.message.from_user.name]['vin'], vin_db[update.message.from_user.name]['captcha2'], vin_db[update.message.from_user.name]['sess2'])
        if rez['name']:
            text = 'Owner: '+rez['name']+' ('+rez['bof']+')'
        else:
            text = 'Nothing found :(. Looks like it\'s that car not bought on credit or wrong VIN number'
        reply(bot, update, text)
        vin_db.pop(update.message.from_user.name)
        log_request("{}:{}".format(update.message.from_user.name, update.message.from_user.id), update.message.text, "")
        return 0
    # get via getcontact
    if get_reamins() > remain_count and getcontact_status:
        reply(bot, update, "*GetContact*\n\n"+get_phone_info(bot, update.message.chat_id, update.message.from_user,
                                                             update.message.text))
    # get via numbuster
    if numbuster_status:
        reply(bot, update, "*NumBuster*\n\n"+get_phone_info_nb(bot, update.message.chat_id, update.message.from_user,
                                                           update.message.text))
    if (not getcontact_status and not numbuster_status) or (not numbuster_status and get_reamins() <= remain_count) :
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, but we have no more external sources :(",
                         parse_mode="Markdown")
    # get via telegram leak
    if tg_status:
        reply(bot, update, "Telegram\n\n" + get_info_from_tg(update.message.text), parse_mode='')
        # reply(bot, update, result_msg, parse_mode='')

    log_request("{}:{}".format(update.message.from_user.name, update.message.from_user.id), update.message.text, "")


def get_remain(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Remain {} requests".format(get_reamins()),
                     parse_mode="Markdown")


def get_stat(limit):
    conn = create_connection(sqlite_file)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    select_stat = "select id, user_name, requested_phone from (select id, user_name, requested_phone from logs order by id DESC limit ?) order by id DESC;"
    c.execute(select_stat, (limit,))
    table = from_db_cursor(c)
    conn.close()
    return table


def get_top(field, limit):
    conn = create_connection(sqlite_file)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    select_rem = "SELECT {}, count({}) from logs group by {} ORDER BY count({}) DESC LIMIT {};".format(field, field, field, field, limit)  # SQLi for bughunters here :)
    c.execute(select_rem)
    table = from_db_cursor(c)
    conn.close()
    return table

def ban_user(username, id):
    conn = create_connection(sqlite_file)
    try:
        c = conn.cursor()
        insert_ban = "INSERT INTO banlist (user_name, user_id, time) VALUES (?, ?, ?)"
        c.execute(insert_ban, (username, id, get_current_timestamp(),))
        conn.commit()
        conn.close()
    except:
        conn.rollback()
        conn.close()
        raise RuntimeError("Uh oh, an error occurred ...{}")

def whitelist_user(username, id):
    conn = create_connection(sqlite_file)
    try:
        c = conn.cursor()
        insert_whitelist = "INSERT INTO whitelist (user_name, user_id, time) VALUES (?, ?, ?)"
        c.execute(insert_whitelist, (username, id, get_current_timestamp(),))
        conn.commit()
        conn.close()
    except:
        conn.rollback()
        conn.close()
        raise RuntimeError("Uh oh, an error occurred ...{}")
    if check_in_invites(id):
        invitelist_rem_user(id)


def whitelist_rem_user(id):
    conn = create_connection(sqlite_file)
    try:
        c = conn.cursor()
        c.execute("DELETE FROM whitelist WHERE user_id=?", (id,))
        conn.commit()
        conn.close()
    except:
        conn.rollback()
        conn.close()
        raise RuntimeError("Uh oh, an error occurred ...{}")

def banlist_rem_user(id):
    conn = create_connection(sqlite_file)
    try:
        c = conn.cursor()
        c.execute("DELETE FROM banlist WHERE user_id=?", (id,))
        conn.commit()
        conn.close()
    except:
        conn.rollback()
        conn.close()
        raise RuntimeError("Uh oh, an error occurred ...{}")

def invitelist_rem_user(id):
    conn = create_connection(sqlite_file)
    try:
        c = conn.cursor()
        c.execute("DELETE FROM invitelist WHERE user_id=?", (id,))
        conn.commit()
        conn.close()
    except:
        conn.rollback()
        conn.close()
        raise RuntimeError("Uh oh, an error occurred ...{}")

def check_ban(id):
    conn = create_connection(sqlite_file)
    c = conn.cursor()
    c.execute("SELECT * FROM banlist WHERE user_id=?", (id,))
    row = c.fetchone()
    conn.close()
    if row:
        return True
    else:
        return False

def get_banlist(limit):
    conn = create_connection(sqlite_file)
    c = conn.cursor()
    select_stat = "select * from banlist order by id DESC limit ?;"
    c.execute(select_stat, (limit,))
    table = from_db_cursor(c)
    conn.close()
    return table.get_string()

def get_whitelist(limit):
    conn = create_connection(sqlite_file)
    c = conn.cursor()
    select_stat = "select * from whitelist order by id DESC limit ?;"
    c.execute(select_stat, (limit,))
    table = from_db_cursor(c)
    conn.close()
    return table.get_string()

def get_invitelist(limit):
    conn = create_connection(sqlite_file)
    c = conn.cursor()
    select_stat = "select * from invitelist order by id DESC limit ?;"
    c.execute(select_stat, (limit,))
    table = from_db_cursor(c)
    conn.close()
    return table.get_string()

def check_whitelist(id):
    conn = create_connection(sqlite_file)
    c = conn.cursor()
    c.execute("SELECT * FROM whitelist WHERE user_id=?", (id,))
    row = c.fetchone()
    conn.close()
    if row:
        return True
    else:
        return False

def check_demotime(id):
    cur_date = datetime.datetime.now()
    last_req_date = get_demoreqests_date_for_user(id)
    if last_req_date:
        delta = cur_date - datetime.datetime.strptime(last_req_date, "%b %d %Y")
        if delta.days >= 1:
            set_demoreqests_for_user(id, 1)
            return True
        else:
            return False
    else:
        return True

def get_demoreqests_for_user(id):
    conn = create_connection(sqlite_file)
    c = conn.cursor()
    c.execute("SELECT count_nmbr FROM demorequests WHERE user_id=?", (id,))
    row = c.fetchone()
    conn.close()
    if row is None:
        return 0
    else:
        return row[0]

def set_demoreqests_for_user(id, nmbr):
    conn = create_connection(sqlite_file)
    c = conn.cursor()
    update_demoreq = "UPDATE demorequests SET count_nmbr=?, date=?  WHERE user_id =?"
    c.execute(update_demoreq, (nmbr, get_current_timestamp(), id,))
    row = c.fetchone()
    conn.close()
    if row is None:
        return 0
    else:
        return row[0]

def get_demoreqests_date_for_user(id):
    conn = create_connection(sqlite_file)
    c = conn.cursor()
    c.execute("SELECT date FROM demorequests WHERE user_id=?", (id,))
    row = c.fetchone()
    conn.close()
    if row is None:
        return 0
    else:
        return row[0]


def check_admin(id):
    if id == admin_id:
        return True
    else:
        return False

def check_user(username = 'None', id='None'):
    if check_admin(id):
        return True
    if check_demorequest(str(id)):
        return True
    if check_ban(str(id)):
        return False
    if not check_whitelist(str(id)):
        return False
    return True

def check_in_invites(id):
    conn = create_connection(sqlite_file)
    c = conn.cursor()
    c.execute("SELECT * FROM invitelist WHERE user_id=?", (id,))
    row = c.fetchone()
    conn.close()
    if row:
        return True
    else:
        return False


def add_in_invitelist(username, id, msg):
    conn = create_connection(sqlite_file)
    try:
        c = conn.cursor()
        insert_whitelist = "INSERT INTO invitelist (user_name, user_id, message, time) VALUES (?, ?, ?, ?)"
        c.execute(insert_whitelist, (username, id, msg, get_current_timestamp(),))
        conn.commit()
        conn.close()
    except:
        conn.rollback()
        conn.close()
        raise RuntimeError("Uh oh, an error occurred ...{}")


def get_about(bot, update, args):
    rez = ""
    global whitelist_status
    global getcontact_status
    global numbuster_status
    global tg_status
    if len(args):
        if args[0] == "stat" and update.message.from_user.id == admin_id:
            if len(args) > 1:
                limit = args[1]
            else:
                limit = 10
            rez = "Last {} request:\n```\n".format(limit) + get_stat(limit).get_string() + "\n```"
        elif args[0] == "top" and update.message.from_user.id == admin_id:
            if len(args) > 1:
                field = args[1]
                limit = 10
                if len(args) > 2:
                    limit = args[2]
            else:
                field = 'user_name'
                limit = 10
            rez = "TOP {}s:\n```\n".format(field).replace('_','-') + get_top(field, limit).get_string().replace('_','-') + "\n```"
        elif args[0] == "get-vars" and update.message.from_user.id == admin_id:
            vars = get_vars()
            rez = "AES KEY: {}\n" \
                  "token: {}\n" \
                  "DeviceID: {}\n" \
                  "PRIVATE\_KEY: {}".format(vars[0], vars[1], vars[2], vars[3])
        elif args[0] == "set-vars" and update.message.from_user.id == admin_id:
            if '-t' in args:
                set_new_token(args[args.index('-t')+1])
            if '-k' in args:
                set_new_aes_key(args[args.index('-k')+1])
            if '-d' in args:
                set_new_device_id(args[args.index('-d')+1])
            if '-e' in args:
                set_new_exp(args[args.index('-e')+1])
            if '-r' in args:
                remain={"name":get_env_data()[0]['name'],"remain":args[args.index('-r')+1]}
                log_reamins(remain)
            rez = 'New vars have been setup'
        elif args[0] == "ban" and update.message.from_user.id == admin_id:
            if len(args)<=1:
                rez = 'Banned users:\n{}'.format(get_banlist(15))
            else:
                ban_user(args[1].split(":")[0],args[1].split(":")[1])
                rez = 'User {} was banned'.format(args[1])
        elif args[0] == "add" and update.message.from_user.id == admin_id:
            if len(args) <= 1:
                rez = "Add username that will be added to the whitelist"
            else:
                whitelist_user(args[1].split(":")[0],args[1].split(":")[1])
                rez = 'User {} was whitelisted'.format(args[1])
                bot.send_message(chat_id=int(args[1].split(":")[1]),
                                 text='Hey! Your invite was approved. Now you can use bot without any restrictions.')
        elif args[0] == "rem" and update.message.from_user.id == admin_id:
            if len(args) <= 1:
                rez = "Add user_id that will be removed from the whitelist"
            else:
                whitelist_rem_user(args[1])
                rez = 'User {} was removed from the whitelist'.format(args[1])
                bot.send_message(chat_id=int(args[1]),
                                 text='Hey! You was banned. Sorry for that :)')
        elif args[0] == "remban" and update.message.from_user.id == admin_id:
            if len(args) <= 1:
                rez = "Add user_id that will be removed from the banlist"
            else:
                banlist_rem_user(args[1])
                rez = 'User {} was removed from the banlist'.format(args[1])
        elif args[0] == "wlist" and update.message.from_user.id == admin_id:
            if len(args) <= 1:
                whitelist_status = 1
                rez = "Whitelist was enabled"
            else:
                whitelist_status = int(args[1])
                rez = 'Whitelist status set to {}'.format(args[1])
        elif args[0] == "getc" and update.message.from_user.id == admin_id:
            if len(args) <= 1:
                getcontact_status = 1
                rez = "GetContact was enabled"
            else:
                getcontact_status = int(args[1])
                rez = 'GetContact status set to {}'.format(args[1])
        elif args[0] == "numb" and update.message.from_user.id == admin_id:
            if len(args) <= 1:
                numbuster_status = 1
                rez = "NumBuster was enabled"
            else:
                numbuster_status = int(args[1])
                rez = 'NumBuster status set to {}'.format(args[1])
        elif args[0] == "status" and update.message.from_user.id == admin_id:
            rez = "Reamain:\n {}\n" \
                  "Whitelist status: {}\n" \
                  "GetContact status: {}\n"\
                  "NumBuster status: {}\n" \
                  "Demorequests: {}\n" \
                  "Banned:\n{}\n" \
                  "Whitelisted:\n{}\n" \
                  "Invite req:\n".format(get_admin_reamins(),whitelist_status,getcontact_status,numbuster_status,demoreqests_nbr,get_banlist(15),get_whitelist(15))
            rez = rez + get_invitelist(15)
            bot.send_message(chat_id=update.message.chat_id,
                             text=rez)
            return
        elif args[0] == "inv" and update.message.from_user.id == admin_id:
            rez = 'Invite requests:\n' + get_invitelist(20)
            bot.send_message(chat_id=update.message.chat_id,
                             text=rez)
            return
        elif args[0] == "say" and update.message.from_user.id == admin_id:
            if args[1]:
                say_to_user(bot,[args[1]], ' '.join(args[2:]))
            return
        elif args[0] == "sayall" and update.message.from_user.id == admin_id:
            if args[1]:
                say_to_all_users(bot,' '.join(args[2:]))
            return
    else:
        if update.message.from_user.id == admin_id:
            rez = "Hello my master!\nYou can use commands:\n" \
                  "/batya stat 15 - Last 15 request (default 10)\n" \
                  "/batya top user\_name 15 - Top 15 users who asked bot (default: user-name)\n" \
                  "/batya top requested\_phone 15 - Top 15 requested-phone (default: user-name)\n" \
                  "/batya get-vars - Get vars values\n" \
                  "/batya set-vars -t token -k key -d DeviceID -e PRIVATE-KEY -r REMAIN\n" \
                  "/batya ban USERNAME:id - Ban user\n" \
                  "/batya remban id - Unban user\n" \
                  "/batya add USERNAME:id - Add user to whitelist\n" \
                  "/batya rem id - Remove user from whitelist\n" \
                  "/batya wlist 1/0 - Enamble/disable whitelist\n" \
                  "/batya inv - print invite request\n" \
                  "/batya getc 1/0 - Enable/disable GetContact\n" \
                  "/batya numb 1/0 - Enable/disable Numbuster\n" \
                  "/batya status - Print lists (white/black), remains, etc\n" \
                  "/batya say ids text\n" \
                  "/batya sayall text"
        else:
            rez = "Hi {}.\nFeel free to write me a message via /say command".format(update.message.from_user.username)

    bot.send_message(chat_id=update.message.chat_id,
                     text=rez, parse_mode="Markdown")


def inline_get_info(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Check phone',
            input_message_content=InputTextMessageContent(get_phone_info(query), parse_mode="Markdown")
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)


def get_captcha(bot, update, args):
    if len(args):
        logger.info("Got captcha from user: {}".format(args[0]))
        if send_captcha_bot(args[0]):
            logger.info("Wrong captcha from user")
            bot.send_message(chat_id=update.message.chat_id, text="Wrong captcha")
        else:
            logger.info("Captcha passed")
            bot.send_message(chat_id=update.message.chat_id, text="Captcha passed. Try to send phone number")
    else:
        logger.info("Empty captcha")
        bot.send_message(chat_id=update.message.chat_id, text="Send captcha from picture. Ex.: /captcha OLoLoH")


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.\nUse /help")


def prepare_msg(name, tags, remain):
    translation_table = dict.fromkeys(map(ord, '_*#'), None)
    name = name.translate(translation_table)
    tags = '\n'.join(tags)
    if len(tags):
        tags = tags.translate(translation_table)
    if remain:
        rez = "{}\n{}\nRemain:{}".format(name, tags, remain)
    else:
        rez = "*We have found:*\n" + name + "\n" + tags
    return rez


def reply(bot, update, text, parse_mode="Markdown"):
    messages_count = int(len(text) / message_size_limit + 1)
    for i in range(messages_count):
        bot.send_message(chat_id=update.message.chat_id, text=text[message_size_limit * i:message_size_limit * (i+1)],
                         parse_mode=parse_mode)


def log_request(user, requested_phone, response):
    log_demorequest(int(user.split(":")[1]))
    conn = create_connection(sqlite_file)
    try:
        c = conn.cursor()
        insert_log = "INSERT INTO logs (user_name, requested_phone, response) VALUES (?, ?, ?)"
        c.execute(insert_log, (user, requested_phone, response,))
        conn.commit()
        conn.close()
    except:
        conn.rollback()
        conn.close()
        raise RuntimeError("Uh oh, an error occurred ...{}")

def log_demorequest(id):
    nmbr = get_demoreqests_for_user(id)
    if nmbr:
        conn = create_connection(sqlite_file)
        try:
            c = conn.cursor()
            update_demoreq = "UPDATE demorequests SET count_nmbr=?, date=?  WHERE user_id =?"
            c.execute(update_demoreq, (nmbr+1, get_current_timestamp(), id,))
            conn.commit()
            conn.close()
        except:
            conn.rollback()
            conn.close()
            raise RuntimeError("Uh oh, an error occurred ...{}")
    else:
        conn = create_connection(sqlite_file)
        try:
            c = conn.cursor()
            insert_demoreq = "INSERT INTO demorequests (user_id, count_nmbr, date) VALUES (?, ?,?)"
            c.execute(insert_demoreq, (id, 1,get_current_timestamp(),))
            conn.commit()
            conn.close()
        except:
            conn.rollback()
            conn.close()
            raise RuntimeError("Uh oh, an error occurred ...{}")

def log_reamins(remain):
    conn = create_connection(sqlite_file)
    try:
        c = conn.cursor()
        update_rem = "UPDATE remain SET count=? WHERE name=?"
        c.execute(update_rem, (remain['remain'],remain['name'],))
        conn.commit()
        conn.close()
    except:
        conn.rollback()
        conn.close()
        raise RuntimeError("Uh oh, an error occurred ...{}")


def get_reamins():
    conn = create_connection(sqlite_file)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    select_rem = "SELECT sum(count) from remain"
    result = c.execute(select_rem).fetchone()['sum(count)']
    conn.close()
    return result

def get_admin_reamins():
    conn = create_connection(sqlite_file)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    select_rem = "SELECT * from remain"
    c.execute(select_rem,)
    table = from_db_cursor(c)
    conn.close()
    return table.get_string()

def get_current_timestamp():
    return datetime.datetime.now().strftime("%b %d %Y")

def create_db():
    logger.info("Creating new DB")
    conn = create_connection(sqlite_file)
    c = conn.cursor()
    c.execute("CREATE TABLE {} ("
              "{} {}",
              "{} {}"
              ")".format("remain",
                         "name", "TEXT"
                         "count", "INTEGER",))
    c.execute("INSERT INTO remain (count) VALUES (200)")
    c.execute("CREATE TABLE {} ("
              "{} {} PRIMARY KEY,"
              "{} {} NOT NULL,"
              "{} {} NOT NULL,"
              "{} {}"
              ")".format("logs",
                         "id", "INTEGER",
                         "user_name", "TEXT",
                         "requested_phone", "TEXT",
                         "response", "TEXT"))
    c.execute("CREATE TABLE {} ("
              "{} {} PRIMARY KEY,"
              "{} {} NOT NULL,"
              "{} {} NOT NULL,"
              "{} {} NOT NULL"
              ")".format("banlist",
                         "id", "INTEGER",
                         "user_name", "TEXT",
                         "user_id", "TEXT",
                         "time", "TEXT"))
    c.execute("CREATE TABLE {} ("
              "{} {} PRIMARY KEY,"
              "{} {} NOT NULL,"
              "{} {} NOT NULL,"
              "{} {} NOT NULL"
              ")".format("whitelist",
                         "id", "INTEGER",
                         "user_name", "TEXT",
                         "user_id", "TEXT",
                         "time", "TEXT"))
    c.execute("CREATE TABLE {} ("
              "{} {} PRIMARY KEY,"
              "{} {} NOT NULL,"
              "{} {} NOT NULL,"
              "{} {} NOT NULL,"
              "{} {} NOT NULL"
              ")".format("invitelist",
                         "id", "INTEGER",
                         "user_name", "TEXT",
                         "user_id", "TEXT",
                         "message", "TEXT",
                         "time", "TEXT"))
    c.execute("CREATE TABLE {} ("
              "{} {} PRIMARY KEY,"
              "{} {} NOT NULL,"
              "{} {} NOT NULL,"
              "{} {} NOT NULL,"
              ")".format("demorequests",
                         "id", "INTEGER",
                         "user_id", "TEXT",
                         "count_nmbr", "INTEGER",
                         "time", "TEXT"))
    conn.commit()
    conn.close()


def get_fio_by_vin_bot(bot, update, args):
    if update.message.from_user.name not in vin_db.keys():
        vin_db[update.message.from_user.name]={'captcha1':'','captcha2':'','vin':args[0], 'plate':'','sess2':get_session()}
        text = 'Hi there! Getting info can takes time (up to 5 minutes). Also you have to pass the captcha. Please wait...'
    else:
        vin_db[update.message.from_user.name]['sess2'] = get_session()
        vin_db[update.message.from_user.name]['vin'] = args[0]
        text = 'Now we\'r gonna get owner number by VIN'
    reply(bot, update, text)
    capcha_file = get_capcha(vin_db[update.message.from_user.name]['sess2'])
    bot.send_photo(chat_id=update.message.chat_id, photo=open(capcha_file, 'rb'))
    vin_db[update.message.from_user.name]['captcha2'] = 'NEED'
    os.remove(capcha_file)

def get_fio_by_plate_bot(bot, update, args):
    log_request("{}:{}".format(update.message.from_user.name, update.message.from_user.id), update.message.text, "")
    reply(bot, update, 'Hi there! Getting info can takes time (up to 5 minutes). Also you have to pass the captchas. Please wait...')
    if update.message.from_user.name not in vin_db.keys():
        vin_db[update.message.from_user.name]={'captcha1':'','captcha2':'','vin':'','plate':args[0],'sess1':'','sess2':''}
    captcha_file, sess = get_sessinon_and_captcha_easto()
    vin_db[update.message.from_user.name]['sess1'] = sess
    bot.send_photo(chat_id=update.message.chat_id, photo=open(captcha_file, 'rb'))
    vin_db[update.message.from_user.name]['captcha1'] = 'NEED'
    os.remove(captcha_file)

def get_pwd_bot(bot, update, args):
    logger.info("Getting password for {}".format(args[0]))
    log_request("{}:{}".format(update.message.from_user.name, update.message.from_user.id), update.message.text, "")
    email = args[0]
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email): #best regex ever here
        result = get_password(str(email))
        if not result:
            message = 'Nothing found :('
        else:
            message = "We have found:\n\n" + result
    else:
        message = "Wrong email format"
    reply(bot, update, message, parse_mode='')

def invite_me(bot, update, args):
    invmessage = ' '.join(args)
    logger.info("Invite request from {}. Msg:{}".format(update.message.from_user.name, str(update.message.from_user.id), invmessage))
    if check_in_invites(str(update.message.from_user.id)):
        message = 'You have already requested an invitation. Please wait for approval'
    else:
        add_in_invitelist(update.message.from_user.name, str(update.message.from_user.id), invmessage)
        message = 'Got yor request. Please wait for approval'
    reply(bot, update, message, parse_mode='')
    bot.send_message(chat_id=int(admin_id), text='[ADMIN] Invite request from {}:{} msg: '.format(update.message.from_user.name, str(update.message.from_user.id))+invmessage)

def say_to_admin(bot, update, args):
    message_to_admin = ' '.join(args)
    if not args:
        reply(bot, update, 'Please enter your message to admin like that:\n "/say hello admin!"', parse_mode='')
        return
    logger.info("Message to admin from {}. Msg:{}".format(update.message.from_user.name, str(update.message.from_user.id),
                                                        message_to_admin))
    bot.send_message(chat_id=int(admin_id),
                     text='[ADMIN] Message from {}:{} msg: '.format(update.message.from_user.name, str(
                         update.message.from_user.id)) + message_to_admin)

def say_to_user(bot, user_ids, message):
    logger.info("Message from admin to {}. Msg:{}".format(','.join(user_ids), message))
    for user_id in user_ids:
        bot.send_message(chat_id=int(user_id), text=message.encode('utf-8').decode('unicode_escape') , parse_mode="Markdown")

def say_to_all_users(bot, message):
    conn = create_connection(sqlite_file)
    c = conn.cursor()
    c.execute("SELECT user_id from demorequests;")
    rows = c.fetchall()
    conn.close()
    user_ids = [i[0] for i in rows]
    logger.info("Message from admin to all users. Msg:{}".format(message))
    for user_id in user_ids:
        bot.send_message(chat_id=int(user_id), text=message.encode('utf-8').decode('unicode_escape') , parse_mode="Markdown")


def check_tg_info(bot, update, args):
    if not args:
        reply(bot, update, 'Please enter telegram niсkname you want to check', parse_mode='')
        return
    else:
        nick_req = args[0].replace('@','')
        tg_info = get_telegram.TelegramInfo()
        result = tg_info.get_info_by_nik(nick_req)
        if result:
            result_msg = f"Nickname: @{result['nik']}\n" \
                         f"Phone: +{result['phone']}\n" \
                         f"id: {result['id']}"
        else:
            result_msg = "Nothing found :("
        reply(bot, update, result_msg, parse_mode='')


if not os.path.isfile(sqlite_file):
    create_db()

updater = Updater(bot_token, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
remain_handler = CommandHandler('remain', get_remain)
about_handler = CommandHandler('batya', get_about, pass_args=True)
captcha_handler = CommandHandler('captcha', get_captcha, pass_args=True)
pwd_handler = CommandHandler('pwd', get_pwd_bot, pass_args=True)
invite_handler = CommandHandler('invite', invite_me, pass_args=True)
say_to_admin_handler = CommandHandler('say', say_to_admin, pass_args=True)
tg_info_handler = CommandHandler('tg', check_tg_info, pass_args=True)
phone_handler = MessageHandler(Filters.text, get_info)
unknown_handler = MessageHandler(Filters.command, unknown)
# inline_phone_handler = InlineQueryHandler(inline_get_info)
# vin_handler = CommandHandler('vin', get_fio_by_vin_bot, pass_args=True)
# plate_handler = CommandHandler('plate', get_fio_by_plate_bot, pass_args=True)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(about_handler)
dispatcher.add_handler(remain_handler)
dispatcher.add_handler(captcha_handler)
dispatcher.add_handler(invite_handler)
dispatcher.add_handler(say_to_admin_handler)
dispatcher.add_handler(tg_info_handler)
dispatcher.add_handler(phone_handler)
dispatcher.add_handler(unknown_handler)
# dispatcher.add_handler(pwd_handler)
# dispatcher.add_handler(vin_handler)
# dispatcher.add_handler(plate_handler)
# dispatcher.add_handler(tst_handler)
# dispatcher.add_handler(inline_phone_handler)

logger.info("Starting...\n"
            "We have {} accounts for getcontact\n"
            "Admin is: {}".format(len(get_env_data()),admin_id))

updater.start_polling()
updater.idle()
