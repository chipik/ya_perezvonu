## What is it?

This script allows to get information about phone number via *GetContact* and *NumBuster* APIs.
Information about API was received by reverse engineering `app.source.getcontact` and `com.numbuster.android` Android applications

## How to use 

1. Install `GetContact` app on rooted device
2. Log In
3. Get `AES_KEY` and `token`

```
adb shell
cat /data/data/app.source.getcontact/shared_prefs/GetContactSettingsPref.xml | grep FINAL_KEY
cat /data/data/app.source.getcontact/shared_prefs/GetContactSettingsPref.xml | grep TOKEN
```
4. Use script `getcontact.py`

```
➜ python getcontact.py -h
usage: getcontact.py [-h] [-p PHONENUMBER] [-t TOKEN] [-d DEVICEID]
                     [-c COUNTRYCODE] [-a] [-D DECRYPT] [-E ENCRYPT]
                     [-P PROXY] [-v]

This script allows to get information about phone number from GetContact servers.
Information about API was received by revers engineering Android app "app.source.getcontact"
--- chipik

optional arguments:
  -h, --help            show this help message and exit
  -p PHONENUMBER, --phoneNumber PHONENUMBER
                        Phone number (example: +xx9217XXX514)
  -t TOKEN, --token TOKEN
                        Token for request (Ex:: AxPA568b72d9c908520b95407e6e95b5482c7995fd98b1e794a2e516a3d1)
  -d DEVICEID, --deviceID DEVICEID
                        DeviceID (default: 27b6dc0c3cb18681)
  -c COUNTRYCODE, --countryCode COUNTRYCODE
                        Country code (default: US)
  -a, --all             Print all possible info
  -D DECRYPT, --decrypt DECRYPT
                        Decrypt data
  -E ENCRYPT, --encrypt ENCRYPT
                        Encrypt data
  -P PROXY, --proxy PROXY
                        Use proxy (ex: 127.0.0.1:8080)
  -v, --debug           Show debug info
```



* Get basic information


```
➜ python getcontact.py -p +xx9217XXX514
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

* Get full information

```
➜  getcontact python getcontact.py -p +xx9217XXX514 -a
We found:
displayName: Мария Стадник
countryCode: RU
tags
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
phoneNumber: +xx9217XXX514
tagCount: 61
Left 122 requests
```

## How does it work?

* check sources (if you able to read shitty python code :) )
* check details in the [reverse engineering](rev/README.md) part

