from random import randint
import logging
import requests
import argparse
import sys

help_desc = '''
This script allows to get information about phone number from NumBuster servers.
Information about API was received by reverse engineering "com.numbuster.android" Android application 
--- chipik
'''

parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-p', '--phoneNumber', help='Phone number (example: +79217XXX514)')
parser.add_argument('-t', '--token', default='oig19z3dcyswwowws0180c84gsoww0gkko10gwg8w0so8ow4k',
                    help='Token for request (Ex:: oig19z3dcyswwowws0211c84gsoww0gkko10gwg8w0so8ow4k)')
parser.add_argument('-c', '--countryCode', default='us', help='Country code (default: us)')
parser.add_argument('-a', '--all', action='store_true', help='Print all possible info')
parser.add_argument('-P', '--proxy', help='Use proxy (ex: 127.0.0.1:8080)')
# parser.add_argument('-T', '--newuser', action='store_true', help='get new token from server')
parser.add_argument('-v', '--debug', action='store_true', help='Show debug info')
args = parser.parse_args()

proxies = {}
verify = True
if args.proxy:
    verify = False
    proxies = {
        'http': args.proxy,
        'https': args.proxy,
    }

headers = {
    "User-Agent": "okhttp/3.9.1",
}

nm_token = args.token
nm_token = tokens[randint(0, len(tokens)-1)]
phoneNumber = args.phoneNumber
base_url = "https://api.numbuster.com"
base_uri_search_api = "/api/v4/search/"
base_uri_comments_api = "/api/old4a27f7a4025447ee5560a49bc5bcde34/comments"
country_code = args.countryCode
search_params = {"access_token": nm_token, "locale": country_code}
comments_params = {"access_token": nm_token, "phone[]": phoneNumber}




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

def set_random_token():
    logger.info("Setting random token...")
    token = tokens[randint(0, len(tokens)-1)]
    search_params['access_token']=token
    comments_params['access_token']=token

logger = init_logger("GetContact", logging.INFO)


def send_post(url, params):
    set_random_token()
    logger.debug("Sending request: {}\nDATA: {}".format(url, str(search_params)))
    r = requests.get(url, proxies=proxies, params=params, headers=headers, verify=verify)
    if r.status_code == 200:
        result = r.json()
        logger.debug("Response: {}".format(result))
        return (r.status_code, result)
    elif r.status_code == 403:
        logger.debug("Wrong token?Status:{}".format(r.status_code))
        return (r.status_code, [])
    elif r.status_code == 428:
        rez = "Too many request"
        logger.debug("{}. Status:{}".format(rez, r.status_code))
        return (r.status_code, [r])
    else:
        print "Something wrong! Status: {}".format(r.status_code)
    return (r.status_code, [])


def get_comments_NumBuster(phoneNumber):
    comments_params["phone[]"] = phoneNumber
    comments_rez = send_post(base_url + base_uri_comments_api, comments_params)
    comments_to_client = []
    if comments_rez[1]:
        for comment in comments_rez[1]['comments']['other']:
            tmp_phone = ''
            av_str = ''
            for phone in comment['author']['profile']['phones']:
                tmp_phone += phone['number']
            comments_str = "{} by {} {} ({})".format(comment['text'].encode("utf-8").strip(),
                                                     comment['author']['profile']['firstName'].encode("utf-8").strip(),
                                                     comment['author']['profile']['lastName'].encode("utf-8").strip(),
                                                     tmp_phone)
            if comment['author']['averageProfile']:
                tmp_av_phone = ''
                for av_phone in comment['author']['averageProfile']['phones']:
                    tmp_av_phone += av_phone['number']
                av_str = " or {} {} ({})".format(
                    comment['author']['averageProfile']['firstName'].encode("utf-8").strip(),
                    comment['author']['averageProfile']['lastName'].encode("utf-8").strip(), tmp_av_phone)
            comments_to_client.append(comments_str + av_str)
        return '\n'.join(comments_to_client)


def get_contacts_NumBuster(contacts):
    parsed_contacts = []
    for contact in contacts:
        parsed_contacts.append(
            "{} {}".format(contact["firstName"].encode("utf-8").strip(), contact["lastName"].encode("utf-8").strip()))
    return parsed_contacts


def get_number_info_NumBuster(phoneNumber):
    info = send_post(base_url + base_uri_search_api + phoneNumber, search_params)
    if info[1]:
        if info[1]['id']:
            comments = ''
            contacts = ''
            if info[1]['commentsCount'] > 0:
                comments = get_comments_NumBuster(phoneNumber)
            if len(info[1]['contacts']):
                contacts = get_contacts_NumBuster(info[1]['contacts'])
            result = "{} {}\n" \
                     "{}\n" \
                     "{}".format(info[1]["firstName"].encode("utf-8").strip(), info[1]["lastName"].encode("utf-8").strip(),
                                 '\n'.join(contacts), comments)
            print "Result:\n{}".format(result)
            return (info[0], "*We have found:*\n{}".format(result))
        else:
            return (info[0], "Nothing found :(")
    else:
        return (info[0], 'Something Wrong')


if __name__ == '__main__':
    if args.debug:
        logger = init_logger("GetContact", logging.DEBUG)

    if args.phoneNumber:
        get_number_info_NumBuster(args.phoneNumber)
