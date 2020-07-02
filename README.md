<!-- MarkdownTOC -->

- What is it?
    - How to use ?
    - All the options of getcontact.py script
- Telegram bot
    - How to use bot
    - Limitation
    - How to install Telegram bot
- How does it work?

<!-- /MarkdownTOC -->


## What is it?

This script allows to get information about phone number via *GetContact* and *NumBuster* APIs.
Information about API was received by reverse engineering `app.source.getcontact` and `com.numbuster.android` Android applications

### How to use ?

1. Install `GetContact` app on rooted device
2. Login into `GetContact` application
3. Get `AES_KEY` and `token`

```
#Connect to the rooted Android device
adb shell
#Let's get AES_KEY key
cat /data/data/app.source.getcontact/shared_prefs/GetContactSettingsPref.xml | grep FINAL_KEY
#And token value
cat /data/data/app.source.getcontact/shared_prefs/GetContactSettingsPref.xml | grep TOKEN
```
4. Clone this repo `git clone https://github.com/chipik/ya_perezvonu.git`
5. Install dependencies `pip3 install -r requirements.txt --user`
6. Run script `getcontact.py -t <token_value> -k <AES_KEY_value> -p <any_phone_number>`
7. *(Options)* You also can specify <token_value> and <AES_KEY_value> inside `getcontact.py`


### All the options of getcontact.py script

```
➜ python3 getcontact.py

usage: getcontact.py [-h] [-p PHONENUMBER] [-t TOKEN] [-k KEY] [-d DEVICEID]
                     [-e EXP] [-c COUNTRYCODE] [-a] [-D DECRYPT] [-E ENCRYPT]
                     [-P PROXY] [-T] [-v]

This script allows to get information about phone number from GetContact servers.
Information about API was received by reverse engineering "app.source.getcontact" Android application
--- chipik

optional arguments:
  -h, --help            show this help message and exit
  -p PHONENUMBER, --phoneNumber PHONENUMBER
                        Phone number (example: +79217XXX514)
  -t TOKEN, --token TOKEN
                        Token for request (Ex:: AxPA568b72d9c908520b95407e6e95b5482c7995fd98b1e794a2e516a3d1)
  -k KEY, --key KEY     AES key (Ex:: 0d3badabbf2bf06b1e343dc1ca0ae711d324efe3309e013d8603a6418072a417)
  -d DEVICEID, --deviceID DEVICEID
                        DeviceID (Ex.: 27b6dc0c3cb35485)
  -e EXP, --exp EXP     PRIVATE_KEY value
  -c COUNTRYCODE, --countryCode COUNTRYCODE
                        Country code (default: US)
  -a, --all             Print all possible info
  -D DECRYPT, --decrypt DECRYPT
                        Decrypt data
  -E ENCRYPT, --encrypt ENCRYPT
                        Encrypt data
  -P PROXY, --proxy PROXY
                        Use proxy (ex: 127.0.0.1:8080)
  -T, --newuser         get new token from server
  -v, --debug           Show debug info
```



* Get basic information


```
➜ python3 getcontact.py -p +xx9217XXX514
Mariya Stadnik
Mariya Stadnik
Masha Stadnik
Masha Trener
Mariya Stadnik Fud Park
Masha Kassir
Mariya Fitnesfemili
Stadnik Masha
Masha Kassa
Masha Kassir 🌳 Food Park
Mariya Stadnik Kasir Ginza
Masha Kassa Gastro Stadnik
Mariya Olimp Na Optikov
Mariya Stadnik Evroplan
Mariya Trener Olimpik
Mariya Bol'shoj Orekh
Mariya Fitnes Bar/2
Masha Stadnik Siab
Masha Trener Olimp
Masha Siab Lichnyj
Masha Stadnik Zal
Hs Mariya Stadnik
Mariya Kassir Fp
Si Stadnik Masha
Fitnes Bar Masha
Masha 💪 Stadnik
Mary Big Ass
Masha New Bar
Mariya Trener🏋🏼‍♀️
Mashul'ka Stadnik
Mashka Fitonyashka
Masha Nachal'nik
Mashulya Stadnik
Mariya Fudpark
Mashulya Kasir)
Stadnik Mariya
Mariya Tinder
Masha Kachalka
Masha Standik
Stadnik Manya
Mari Kassir
Masha Solyara
Masha Careva
Masha Artur
Masha Vanek
Masha Olimp
Moya Sestra
M Stadnik
Mariya Fit
Masha Boss
Maks Zal
Mariya Ff
Mahych 👸🏽
Masha Bar
Masha St
Marina...
Stadnik💃🏽
Masha💪🏻❤️
Stadnik
Manyasha
Zyobra
Mariya
```

## Telegram bot

Also there is [Telegram bot](https://t.me/ya_perezvonu_bot) that allows you get info about phone numbers using reversed API of `GetContact` android app, `Numbuster` and [Telegram data leak](https://xss.is/threads/38129/)

### How to use bot

Just sent interested phone number to this bot [@ya_perezvonu_bot](https://t.me/ya_perezvonu_bot)

![bot](bot.png) 

Also bot get phone number by telegram nickname using [Telegram data leak](https://xss.is/threads/38129/):


```
~user
/tg @vova_ivanov

                                            ~я перезвоню
                                            Nickname: @vova_ivanov
                                            Phone: +79165507327
                                            id: 155170541
```
    

Now bot understand these commands:
```
/help - this message
/remain -  number of requests remaining (300 requests a day)
/captcha - enter captcha
/invite - request invite
/batya - about
/tg - get info by telegram username
```
### Limitation 

**!!IMPORTANT NOTE!!!**

**I have no my own database with phone numbers!  That means that scripts or Telegram bot CAN\'T find phone number by the person name or surname!**

Because bot uses reversed `GetContact` API that means we have phone request limit. Now it's **200 request for one GetContact user**

**!!!You can add as many as you want/can users in `getcontact.py`!!!**

See instruction above.

Bot [@ya_perezvonu_bot](https://t.me/ya_perezvonu_bot) also has a request limits for all users. Now it's **2 request a day**.
You can request invitation that will allow you to do more requests. For that you have to send command to [@ya_perezvonu_bot](https://t.me/ya_perezvonu_bot):

`/invite <here you can write a message why you need more request>`

But will be honest you have almost no chance to get approve on your invitation request. 
Do not waste your time, just install your own instants of Telegram bot. You will find instruction how to do that below.

### How to install Telegram bot

1. Configure `getcontact.py` (see instructions above)
2. Create new Telegram bot (official documentation is [here](https://core.telegram.org/bots#6-botfather))
3. Specify `bot_token` variable in  `ya_perezvonu.py`
4. Specify `admin_id` in `ya_perezvonu.py`. This is Telegram user identifier that will allow you to control the bot
5. Run `python3 ya_perezvonu.py`
6. *(Option)* You can run bot on your VPS as a service. 
```
# change <username> in ya_perezvonu_bot.service on your own user (Ex:. root)
# then copy ya_perezvonu_bot.service to directory /etc/systemd/system/
cp ya_perezvonu_bot.service /etc/systemd/system/
# start new service
systemctl start ya_perezvonu_bot
``` 
7. Now you can use your own `ya_perezvonu` bot instance


## How does it work?

* check sources (if you able to read shitty python code :) )
* check details in the [reverse engineering](rev/README.md) part

