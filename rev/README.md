<!-- MarkdownTOC -->

- Main\(\)
    - Traffic
    - Encryption
        - AES key calculation
    - Signature
    - Init token and AES key
    - Tools

<!-- /MarkdownTOC -->


# Main()

Here you will find some details about reverse engineering of `app.source.getcontact` Android application 


## Traffic

Didn't notice any working SSL pinning mechanism. Just install Burp's certificate in an Android Device.

You will find traffic example in [requests.md](requests.md) 
Ok, obviously data in POST requests is:

1. encrypted 
`{"data":"it1BCQGnv+A3i6FmRigzviBGSJqF58K42YBCMtDP53fvMH/bJO4XZnXlDEC3AZWYSGGBpZgRv21LcNvgaP94gA64L4BbqgE7dzHW0vXK5Ql8vBrtqZiWEfZ+aXHDWydQok/mYnMTfYNDxySkGGUez2qwL4mLIR7yelOlQQ9sup0="}`

2. signed   
`X-Req-Signature` header

Let's decompile the application.

![decompiled](img/decompiled.png) 

It seems that the obfuscator worked here :/
Let's drill it.


## Encryption

`ᔮ` class is responsible for encryption:

```java
    public final String ˋ(String str) {
        int i = 2 % 2;
        String str2 = "";
        try {
            Key secretKeySpec = new SecretKeySpec(aj.ˋ(this.ʻ), ᔮ.ˊ(172, 3, 58400).intern());
            Cipher instance = Cipher.getInstance(ᔮ.ˊ(172, 3, 58400).intern());
            instance.init(1, secretKeySpec);
            str2 = fyn.ˎ(instance.doFinal(str.getBytes()));
        } catch (Throwable e) {
            e.printStackTrace();
        } catch (Throwable e2) {
            e2.printStackTrace();
        } catch (Throwable e22) {
            e22.printStackTrace();
        } catch (Throwable e222) {
            e222.printStackTrace();
        } catch (Throwable e2222) {
            e2222.printStackTrace();
        }
        i = ˏॱ + 45;
        ॱˊ = i % 128;
        if (i % 2 != 0) {
        }
        return str2;
    }
```


Let's check the encryption algorithm. 
The easiest way to get algorithm (and other stuff from app) is using [frida](https://www.frida.re/) toolkit
Below you will find `frida` script for that:

```javascript
Java.perform(function x() { 
    console.log("Decrypt strings")
    var instance = Java.use("ᔮ");
    var result = instance.ˊ(172, 93 String.fromCharCode(58400));
    console.log("Result: " + result)
});
```

```
Result: AES
```


OK, we have to find encryption key. And again `frida` helps:

```javascript
Java.perform(function x() { 
    console.log("\nGetting AES key:")
    var instance = Java.use("ᔮ");
    var result = instance.ॱ().ʻ.value;
    console.log("Result: " + result)
});
```

So, know we can try to decrypt data from intercepted traffic:

```python
def decrypt_aes(payload):
    logger.debug("Decrypting...\nDATA:{}".format(payload.encode("hex")))
    cipher = AES.new(AES_key, AES.MODE_ECB)
    rez =  unpad(cipher.decrypt(payload))
    logger.debug("Decrypted result:{}".format(rez))
    return rez
```

```
➜ python getcontact.py -D "it1BCQGnv+A3i6FmRigzviBGSJqF58K42YBCMtDP53fvMH/bJO4XZnXlDEC3AZWYSGGBpZgRv21LcNvgaP94gA64L4BbqgE7dzHW0vXK5Ql8vBrtqZiWEfZ+aXHDWydQok/mYnMTfYNDxySkGGUez2qwL4mLIR7yelOlQQ9sup0="

Decrypted: {countryCode:US,phoneNumber:+79040991328,source:detail,token:AxPu569b72d9c908520b95408e6e95b5482c8995fd98b0e794a2e516a3d1}
```

It works!


### AES key calculation

Right from installation application sends `register` request to the server

```req
POST /v2.1/register HTTP/1.1
X-Req-Timestamp: 1548968515989
User-Agent: Dalvik/2.1.0 (Linux; U; Android 7.1.1; Android SDK built for x86 Build/NYC)
X-Os: android 7.1.1
X-Encrypted: 0
X-Client-Device-Id: 37b6dc0c4cb9a598
X-Lang: en_US
X-App-Version: 4.2.0
X-Req-Signature: yaKSrt7wKp6OTCf6e3cZ82K2Bs4UuWjnWwrwb/8DeZI=
Content-Type: application/json; charset=UTF-8
Content-Length: 390
Host: pbssrv-centralevents.com
Connection: close
Accept-Encoding: gzip, deflate

{"adjustId":"aa8a3ea2e1c10552070e3aeb93d0cfea","adjustParams":{"adid":"aa8a3ea2e1c10552070e3aeb93d0cfea","network":"Organic","trackerName":"Organic","trackerToken":"5nd8yt7"},"androidId":"37b6dc0c4cb9a598","countryCode":"us","deviceName":"Android SDK built for x86","deviceType":"Android","gpsAdid":"273c9507-1d80-4913-b3f0-03e5fde34810","peerKey":"734470887651","timeZone":"Europe/Moscow"}
```

For AES key calculation app uses `serverKey` parameter form registration response:

```resp
HTTP/1.1 201 Created
Date: Thu, 31 Jan 2019 21:01:53 GMT
Content-Type: application/json; charset=UTF-8
Connection: close
Server: nginx
X-Encrypted: 0
Content-Length: 909

{"meta":{"requestId":"172-31-9-53-REQ-5c536241120b7","httpStatusCode":201},"result":{"token":"AxPub4a6575279f0d87735dac89c1fd2908844b651f45e6f21fe61b4a95f","serverKey":"400467965658","cert":true,"isd":false,"localizationKey":"lc-1548160689","isSoftUpdate":false,"isForceUpdate":false,"storeUrl":null,"inviteUrl":"https:\/\/gogtc.co\/invite","updateMessage":null,"ratingOptions":{"callHistoryShow":false,"searchHistoryShow":false,"spamTabShow":false},"isVerified":false,"mTag":0,"chkStatus":false,"sStatus":true,"mTagSkipDuration":5,"social":[{"name":"instagram","title":"Instagram","link":"https:\/\/www.instagram.com\/getcontact\/"},{"name":"facebook","title":"Facebook","link":"https:\/\/www.facebook.com\/getcontactapp\/"},{"name":"twitter","title":"Twitter","link":"https:\/\/twitter.com\/getcontactapp"},{"name":"linkedin","title":"Linkedin","link":"https:\/\/www.linkedin.com\/company\/getcontact\/"}]}}
```


App calculates sha256 hash from `(serverKey ^ 2082716) mod 900719925481`. Result is our AES key.

```python
def calculate_new_aes_key(serverKey):
    print "Calculating new AES key. It can takes time..."
    longInt = int(serverKey)**exp%mod
    new_key =  hashlib.sha256(bytearray(str(longInt), "utf-8")).hexdigest()
    return str(new_key)
```


Let's move to the signature.

## Signature

We have to sign our requests and for that have to send calculated HMAC value in `X-Req-Signature` header:

```
 POST /v2.1/number-detail HTTP/1.1
X-App-Version: 4.2.0
X-Req-Timestamp: 1547742064906
X-Os: android 7.1.1
X-Token: AxPu569b72d9c908520b95408e6e95b5482c8995fd98b0e794a2e516a3d1
X-Encrypted: 1
X-Client-Device-Id: 37b6dc0c3cb9a596
X-Req-Signature: Zh5yxvtGLAEaMJ13M0eUS99dT0TQGE5h8qqIjQtH/zo=
Content-Type: application/json; charset=utf-8
Content-Length: 205
Host: pbssrv-centralevents.com
Connection: close
Accept-Encoding: gzip, deflate

{"data":"it1BCQGnv+A3i6FmRigzviBGSJqF58K42YBCMtDP53fvMH/bJO4XZnXlDEC3AZWYSGGBpZgRv21LcNvgaP94gA64L4BbqgE7dzHW0vXK5Ql8vBrtqZiWEfZ+aXHDWydQok/mYnMTfYNDxySkGGUez2qwL4mLIR7yelOlQQ9sup0="}
 ```


Class responsible for that is `冖`

```java
public final class 冖 implements fms {
    public final fne ˏ(ˋ ˋ) {
        byte[] bArr;
        fmw ˊ = ˋ.ˊ();
        fnc fnc = ˊ.ॱ;
        Object fpj = new fpj();
        fnc.ˎ(fpj);
        String ˊॱ = fpj.ˊॱ();
        eqi.ॱ("Plain Body".concat(String.valueOf(ˊॱ)));
        String str = ᔮ.ॱ().ʼ;  <--- secret key
        ˊॱ = new StringBuilder().append(fmu.ˊ(ˊ.ˋ.ॱ, "X-Req-Timestamp")).append("-").append(ˊॱ).toString().replace("\\/", "/"); <--- string to hash
        eqi.ॱ("String to hash".concat(String.valueOf(ˊॱ)));
        fyo fyo = new fyo(fyp.HMAC_SHA_256, str);
        str = ˊॱ;
        Mac mac = fyo.ॱ;
        ˊॱ = str;
        Charset charset = fyl.ᐝ;
        if (ˊॱ == null) {
            bArr = null;
        } else {
            bArr = ˊॱ.getBytes(charset);
        }
        If ˏ = new If(ˊ).ˏ("X-Req-Signature", fyn.base64(mac.doFinal(bArr)).trim());
        if (ˏ.ˏ != null) {
            return ˋ.ˊ(new fmw(ˏ));
        }
        throw new IllegalStateException("url == null");
    }
}
```


So, because it's `HMAC_SHA_256` we have to know the key.
Below you will find `frida` script for that

```javascript
Java.perform(function x() { 
    console.log("Getting HMAC key...")
    var instance = Java.use("ᔮ");
    var result = instance.ॱ().ʼ.value;
    console.log("Result: " + result)
});
```

So, we've got it:

`HMAC_key = 2Wq7)qkX~cp7)H|n_tc&o+:G_USN3/-uIi~>M+c ;Oq]E{t9)RC_5|lhAA_Qq%_4`


If you noticed data json contains `token`. It's something like user session. You can get your token value using this `frida` script:

```javascript
Java.perform(function x() { 
    console.log("Getting user token...")
    var instance = Java.use("ᒨ");
    var result = instance.ˋ();
    console.log("Result: " + result)
});
```


Finally! Now we can sign our requests:

```python
def create_sign(timestamp, payload):
    logger.debug("Signing...\n{}-{}".format(timestamp, payload))
    message = bytes("{}-{}".format(timestamp, payload))
    secret = bytes(HMAC_key)
    signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
    logger.debug("Result: {}".format(signature))
    return signature
```


That's all folks!
We can encrypt/decrypt data and sign request.


## Init token and AES key

Looks like for during first launch getcontact initialize AES key and user's token.


```request
POST /v2.1/register HTTP/1.1
X-Req-Timestamp: 1548968515989
User-Agent: Dalvik/2.1.0 (Linux; U; Android 7.1.1; Android SDK built for x86 Build/NYC)
X-Os: android 7.1.1
X-Encrypted: 0
X-Client-Device-Id: 37b6dc0c3cb9a595
X-Lang: en_US
X-App-Version: 4.2.0
X-Req-Signature: yaKSrt7wKp6OTCf6e3cZ82K2Bs4UuWjnWwrwb/8DeZI=
Content-Type: application/json; charset=UTF-8
Content-Length: 390
Host: pbssrv-centralevents.com
Connection: close
Accept-Encoding: gzip, deflate

{"adjustId":"aa8a3ea2e1c10552070e3aeb93d0cfea","adjustParams":{"adid":"aa8a3ea2e1c10552070e3aeb93d0cfea","network":"Organic","trackerName":"Organic","trackerToken":"5nd8yt7"},"androidId":"37b6dc0c3cb9a595","countryCode":"us","deviceName":"Android SDK built for x86","deviceType":"Android","gpsAdid":"273c9507-1d80-4913-b3f0-03e5fde34810","peerKey":"734470887651","timeZone":"Europe/Moscow"}
 ```

We can find token in clear text in response:

```response
HTTP/1.1 201 Created
Date: Thu, 31 Jan 2019 21:01:53 GMT
Content-Type: application/json; charset=UTF-8
Connection: close
Server: nginx
X-Encrypted: 0
Content-Length: 909

{"meta":{"requestId":"172-31-9-53-REQ-5c536241120b7","httpStatusCode":201},"result":{"token":"AxPub4a6575279f0d87735dac89c1fd2908844b651f45e6f21fe61b4a95f","serverKey":"400567965658","cert":true,"isd":false,"localizationKey":"lc-1548160689","isSoftUpdate":false,"isForceUpdate":false,"storeUrl":null,"inviteUrl":"https:\/\/gogtc.co\/invite","updateMessage":null,"ratingOptions":{"callHistoryShow":false,"searchHistoryShow":false,"spamTabShow":false},"isVerified":false,"mTag":0,"chkStatus":false,"sStatus":true,"mTagSkipDuration":5,"social":[{"name":"instagram","title":"Instagram","link":"https:\/\/www.instagram.com\/getcontact\/"},{"name":"facebook","title":"Facebook","link":"https:\/\/www.facebook.com\/getcontactapp\/"},{"name":"twitter","title":"Twitter","link":"https:\/\/twitter.com\/getcontactapp"},{"name":"linkedin","title":"Linkedin","link":"https:\/\/www.linkedin.com\/company\/getcontact\/"}]}}
```


looks like AES key is generated using `serverKey` from response in method from `ᔮ` class

```java
    public final void ˊ(String str) {
        Object obj;
        byte[] bArr;
        int i = 2 % 2;
        eqi.ॱ(ᔮ.ˊ(126, 24, 10888).intern());
        float currentTimeMillis = (float) System.currentTimeMillis();
        String obj2 = new BigInteger(str).modPow(ˋ, this.ᐝ).toString();
        Charset charset = fyl.ᐝ;
        if (obj2 == null) {
            obj = null;
        } else {
            obj = 1;
        }
        switch (obj) {
            case null:
                i = ॱˊ + 95;
                ˏॱ = i % 128;
                if (i % 2 == 0) {
                    bArr = null;
                    i = 40 / 0;
                } else {
                    bArr = null;
                }
                i = 2 % 2;
                break;
            default:
                bArr = obj2.getBytes(charset);
                break;
        }
        this.ʻ = fym.ˏ(fyq.ˏ(Constants.SHA256).digest(bArr));
        float currentTimeMillis2 = ((float) System.currentTimeMillis()) - currentTimeMillis;
        eqi.ˊ(ᔮ.ˊ(150, 22, 0).intern(), Float.valueOf(currentTimeMillis2));
        if (Ꭻ.ˎ == null) {
            Ꭻ.ˎ = new Ꭻ(Ꭻ.ˋ);
        }
        Ꭻ.ˎ.ˊ.edit().putString(ᔮ.ˊ(105, 10, 55851).intern(), ˏ.toString()).apply();
        if (Ꭻ.ˎ == null) {
            Ꭻ.ˎ = new Ꭻ(Ꭻ.ˋ);
        }
        try {
            Ꭻ Ꭻ = Ꭻ.ˎ;
            try {
                Ꭻ.ˊ.edit().putString(ᔮ.ˊ(115, 11, 3617).intern(), ˋ.toString()).apply();
                if (Ꭻ.ˎ == null) {
                    Ꭻ.ˎ = new Ꭻ(Ꭻ.ˋ);
                    i = 2 % 2;
                }
                Ꭻ.ˎ.ˊ.edit().putString(ᔮ.ˊ(96, 9, 0).intern(), this.ʻ).apply();
                ˊ = true;
                i = ॱˊ + 17;
                ˏॱ = i % 128;
                switch (i % 2 == 0 ? 51 : 81) {
                    case 51:
                        i = 25 / 0;
                        return;
                    default:
                        return;
                }
            } catch (Exception e) {
                throw e;
            }
        } catch (Exception e2) {
            throw e2;
        }
    }
```



## Tools

Please find [frida script](get_keys_and_token_frida.js) that allows you to get all necessary values from Android Application   



```
➜ frida -U -l get_keys_and_token_frida.js --no-paus -f app.source.getcontact
     ____
    / _  |   Frida 12.2.29 - A world-class dynamic instrumentation toolkit
   | (_| |
    > _  |   Commands:
   /_/ |_|       help      -> Displays the help system
   . . . .       object?   -> Display information about 'object'
   . . . .       exit/quit -> Exit
   . . . .
   . . . .   More info at http://www.frida.re/docs/home/
Spawned `app.source.getcontact`. Resuming main thread!
[Android Emulator 5554::app.source.getcontact]->
Getting AES key:
Result: 0705a53f0b0c1fbe14d68313939c6683f2baa687aff535dd2469291834bff606
Getting HMAC key...
Result: 2Wq7)qkX~cp7)H|n_tc&o+:G_USN3/-uIi~>M+c ;Oq]E{t9)RC_5|lhAA_Qq%_4
Getting user token...
Result: AxPu569b72d9c908520b95408e6e95b5482c8995fd98b0e794a2e516a3d1
```
