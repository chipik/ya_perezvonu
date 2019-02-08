<!-- MarkdownTOC -->

- Target
- Input
- Output
    - Search phone number
    - Comments
- Tokens
- Other

<!-- /MarkdownTOC -->


## Target

Numbuster Android app (https://play.google.com/store/apps/details?id=com.numbuster.android)

## Input

* phone number:
I used shared phone number **+15153290434**  from [https://www.receivesms.org](https://www.receivesms.org) 

## Output

As you will see below app doesn't use any cryptothings. For API request we have to have only token.

### Search phone number

```request
GET /api/v4/search/74952521125?access_token=oig19z3dcyswwowws0880c84gsoww0gkko11gwg8w0so8ow4k&locale=en HTTP/1.1
Host: api.numbuster.com
Connection: close
Accept-Encoding: gzip, deflate
User-Agent: okhttp/3.9.1
```


```resp
HTTP/1.1 200 OK
Server: nginx
Content-Type: application/json
Connection: close
X-Powered-By: PHP/7.0.24-1+ubuntu14.04.1+deb.sury.org+1
Cache-Control: no-cache, private
Date: Fri, 08 Feb 2019 16:24:09 GMT
Strict-Transport-Security: max-age=31536000;
Content-Security-Policy-Report-Only: default-src https:; script-src https: 'unsafe-eval' 'unsafe-inline'; style-src https: 'unsafe-inline'; img-src https: data:; font-src https: data:; report-uri /csp-report
Content-Length: 380

{"id":572960531,"firstName":"\u0421\u0430\u043d\u043b\u0430\u0439\u0442","lastName":"","profile":{"id":null,"firstName":null,"lastName":null,"phones":null,"avatar":null,"branding":null},"avatar":null,"branding":null,"rating":{"likes":0,"dislikes":1},"commentsCount":12,"region":"Russia","carrier":"\u041e\u041e\u041e \u0022\u0413\u0410\u0420\u0421 \u0422\u0415\u041b\u0415\u041a\u041e\u041c - \u0443\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0442\u0435\u043b\u0435\u043a\u043e\u043c\u043c\u0443\u043d\u0438\u043a\u0430\u0446\u0438\u044f\u043c\u0438\u0022","tags":[{"id":2,"count":1,"type":"PERSON","emoji":"\ud83d\ude07","name":"good","tagged_by_me":false},{"id":18,"count":6,"type":"COMPANY","emoji":"\ud83d\udc8e","name":"useful","tagged_by_me":false},{"id":19,"count":1,"type":"COMPANY","emoji":"\ud83c\udfd4","name":"reliable","tagged_by_me":false},{"id":20,"count":13,"type":"COMPANY","emoji":"\ud83c\udf9f","name":"cheap","tagged_by_me":false},{"id":21,"count":3,"type":"COMPANY","emoji":"\ud83c\udfe2","name":"known\\solid","tagged_by_me":false},{"id":23,"count":4,"type":"COMPANY","emoji":"\ud83d\udc38","name":"useless","tagged_by_me":false},{"id":24,"count":4,"type":"COMPANY","emoji":"\ud83e\udd2c","name":"aggressive","tagged_by_me":false},{"id":25,"count":5,"type":"COMPANY","emoji":"\u26a0","name":"spam","tagged_by_me":false},{"id":26,"count":2,"type":"COMPANY","emoji":"\ud83d\udca8","name":"unreliable","tagged_by_me":false},{"id":27,"count":1,"type":"COMPANY","emoji":"\ud83d\udcb0","name":"expensive","tagged_by_me":false},{"id":28,"count":3,"type":"COMPANY","emoji":"\ud83e\udd2f","name":"enrage","tagged_by_me":false},{"id":29,"count":3,"type":"COMPANY","emoji":"\u26d4","name":"fraudsters","tagged_by_me":false},{"id":49,"count":1,"type":"PERSON","emoji":"\ud83d\udca9","name":"nasty","tagged_by_me":false}],"contacts":[{"firstName":"\u0421\u0430\u043d\u043b\u0430\u0439\u0442","lastName":"","count":3},{"firstName":"\u0421\u043f\u0430\u043c","lastName":"","count":3},{"firstName":"+74952521125","lastName":"","count":2},{"firstName":"\u0416\u0435\u0440\u0442\u0432\u044b","lastName":"\u043c\u0430\u0440\u043a\u0435\u0442\u0438\u043d\u0433\u0430. \u0420\u0430\u0437\u0432\u043e\u0434!","count":1},{"firstName":"\u0420\u0430\u0437\u0432\u043e\u0434!","lastName":"\u0412\u043f\u0430\u0440\u0438\u0432\u0430\u044e\u0442 \u0442\u0443\u0444\u0442\u0443","count":1},{"firstName":"\u041d\u0435","lastName":"\u0417\u043d\u0430\u044e","count":1},{"firstName":"\u0425\u0435\u044098","lastName":"","count":1},{"firstName":"\u0421\u0430\u043d\u043b\u0430\u0439\u0442","lastName":"?","count":1},{"firstName":"\u0422\u0432","lastName":"2","count":1},{"firstName":"\u041f\u0440\u043e\u043e","lastName":"","count":1},{"firstName":"\u041c\u043e\u0441\u043a\u0432\u0430","lastName":"","count":1},{"firstName":"Sunlight","lastName":"\u043c\u0430\u0433\u0430\u0437\u0438\u043d","count":1}],"phoneType":"COMPANY","phones":["74952521125"],"bans":300}
```

### Comments

```req
GET /api/old4a27f7a4025447ee5560a49bc5bcde34/comments?phone[]=74952521125&access_token=oig19z3dcyswwowws0880c84gsoww0gkko11gwg8w0so8ow4k HTTP/1.1
Host: api.numbuster.com
Connection: close
Accept-Encoding: gzip, deflate
User-Agent: okhttp/3.9.1
```


```resp
HTTP/1.1 200 OK
Server: nginx
Content-Type: application/json
Connection: close
Cache-Control: no-cache
Date: Fri, 08 Feb 2019 17:48:24 GMT
Strict-Transport-Security: max-age=31536000;
Content-Security-Policy-Report-Only: default-src https:; script-src https: 'unsafe-eval' 'unsafe-inline'; style-src https: 'unsafe-inline'; img-src https: data:; font-src https: data:; report-uri /csp-report
Content-Length: 9390

{"comments":{"my":[],"contacts":[],"other":[{"id":462023,"text":"\u0441\u043f\u0430\u043c","toNumber":"74952521125","createdAt":"2018-12-31T15:36:29+0300","updatedAt":"2018-12-31T15:36:29+0300","isVisible":true,"rating":0,"author":{"profile":{"id":834948,"firstName":"Crash Craft","lastName":"","avatar":null,"branding":null,"phones":[{"number":"79039770427","rating":{"likes":0,"dislikes":1,"level":10},"isBanned":false}],"updatedAt":"2018-06-23T09:47:18+0300"},"averageProfile":{"id":291229031,"firstName":"\u041c\u0430\u043a\u0441\u0438\u043c\u043a\u0430","lastName":"","avatar":null,"branding":null,"phones":[{"number":"79039770427"}]},"branding":null,"rating":{"likes":0,"dislikes":1,"level":10},"isAutoBanned":false,"isBanned":false}},{"id":461989,"text":"\u043c\u0443\u0441\u043e\u0440\u043d\u0430\u044f \u0440\u0435\u043a\u043b\u0430\u043c\u0430 \u0437\u043e\u043b\u043e\u0442\u0438\u0448\u043a\u0430","toNumber":"74952521125","createdAt":"2018-12-31T13:46:38+0300","updatedAt":"2018-12-31T13:46:38+0300","isVisible":true,"rating":0,"author":{"profile":{"id":2265971,"firstName":"\u0421\u0435\u0440\u0433\u0435\u0439","lastName":"","avatar":null,"branding":null,"phones":[{"number":"79158919543","rating":{"likes":0,"dislikes":0,"level":0},"isBanned":false}],"updatedAt":"2018-12-16T13:51:05+0300"},"averageProfile":null,"branding":null,"rating":{"likes":0,"dislikes":0,"level":0},"isAutoBanned":false,"isBanned":false}},{"id":461968,"text":"\u044f \u0443\u0436\u0435 \u043e\u0431\u0440\u0430\u0434\u043e\u0432\u0430\u043b\u0441\u044f, \u0447\u0442\u043e \u043a\u043e\u043b\u043b\u0435\u043a\u0442\u043e\u0440\u0430 \u0437\u0432\u043e\u043d\u044f\u0442, \u0430 \u0442\u0443\u0442 \u043d\u0430 \u0442\u0435 \u043a\u0430\u043a\u043e\u0439 \u0442\u043e \u0433\u0440\u0443\u0437\u0438\u043d","toNumber":"74952521125","createdAt":"2018-12-31T12:00:48+0300","updatedAt":"2018-12-31T12:00:48+0300","isVisible":true,"rating":0,"author":{"profile":{"id":831840,"firstName":"+7 912 863-07-33","lastName":"","avatar":null,"branding":null,"phones":[{"number":"79128630733","rating":{"likes":0,"dislikes":0,"level":0},"isBanned":false}],"updatedAt":"2018-07-08T11:29:02+0300"},"averageProfile":null,"branding":null,"rating":{"likes":0,"dislikes":0,"level":0},"isAutoBanned":false,"isBanned":false}},{"id":461748,"text":"\u0421\u0430\u043d\u043b\u0430\u0439\u0442","toNumber":"74952521125","createdAt":"2018-12-30T21:59:32+0300","updatedAt":"2018-12-30T21:59:32+0300","isVisible":true,"rating":0,"author":{"profile":{"id":1099088,"firstName":"+7 903 315-80-38","lastName":"","avatar":null,"branding":null,"phones":[{"number":"79033158038","rating":{"likes":0,"dislikes":0,"level":0},"isBanned":false}],"updatedAt":"2018-07-13T17:10:58+0300"},"averageProfile":null,"branding":null,"rating":{"likes":0,"dislikes":0,"level":0},"isAutoBanned":false,"isBanned":false}},{"id":461459,"text":"\u0437\u0432\u043e\u043d\u0438\u043b \u041c\u0435\u043b\u0430\u0434\u0437\u0435, \u0441\u043a\u0430\u0437\u0430\u043b \u0022 \u043a\u0430\u043a \u0442\u044b \u043a\u0440\u0430\u0441\u0438\u0438\u0438\u0438\u0432\u0430 \u0441\u0435\u0433\u043e\u043e\u043e\u043e\u0434\u043d\u044f\u0022:)))), \u043f\u0440\u0435\u0434\u043b\u0430\u0433\u0430\u043b \u0437\u043e\u043b\u043e\u0442\u0430 \u043a\u0443\u043f\u0438\u0442\u044c \u0432 \u0441\u0430\u043d\u043b\u0430\u0439\u0442\u0435:))))","toNumber":"74952521125","createdAt":"2018-12-30T13:26:49+0300","updatedAt":"2018-12-30T13:26:49+0300","isVisible":true,"rating":0,"author":{"profile":{"id":1289006,"firstName":"\u041c\u0443\u0440\u043a\u0430","lastName":"\u041c","avatar":{"bucket":"numbusters-avatar","name":"upload-5ba0ee017327c8.44635170.jpg","link":"https:\/\/numbusters-avatar.s3.amazonaws.com\/upload-5ba0ee017327c8.44635170.jpg","eTag":"cbfc0d96bb4c6aacc0a751d832be37ed","size":13591},"branding":null,"phones":[{"number":"79104885940","rating":{"likes":0,"dislikes":0,"level":0},"isBanned":false}],"updatedAt":"2018-09-18T15:22:57+0300"},"averageProfile":{"id":307594028,"firstName":"\u041c\u0430\u0440\u0438\u044f","lastName":"","avatar":null,"branding":null,"phones":[{"number":"79104885940"}]},"branding":null,"rating":{"likes":0,"dislikes":0,"level":0},"isAutoBanned":false,"isBanned":false}},{"id":461380,"text":"\u0421\u043f\u0430\u043c \u043e\u0442 \u0441\u0430\u043d \u0440\u0430\u0439\u0437\u0430.","toNumber":"74952521125","createdAt":"2018-12-30T10:45:17+0300","updatedAt":"2018-12-30T10:45:17+0300","isVisible":true,"rating":0,"author":{"profile":{"id":2233894,"firstName":"","lastName":"","avatar":null,"branding":null,"phones":[{"number":"79034582277","rating":{"likes":0,"dislikes":0,"level":0},"isBanned":false}],"updatedAt":"2018-11-02T12:09:15+0300"},"averageProfile":{"id":41471074,"firstName":"\u0421\u0435\u0440\u0433\u0435\u0439","lastName":"\u0414\u0438\u0440\u0435\u043a\u0442\u043e\u0440 \u041d\u0438\u0441\u0441\u0430\u043d","avatar":null,"branding":null,"phones":[{"number":"79034582277"}]},"branding":null,"rating":{"likes":0,"dislikes":0,"level":0},"isAutoBanned":false,"isBanned":false}},{"id":461323,"text":"\u0433\u043e\u043b\u043e\u0441\u043e\u043c \u041a\u043e\u043d\u0441\u0442\u0430\u043d\u0442\u0438\u043d\u0430 \u041c\u0435\u043b\u0430\u0434\u0437\u0435 \u043f\u043e\u0437\u0434\u0440\u0430\u0432\u043b\u044f\u044e\u0442 \u0441 \u041d\u0413 \u0438 \u0440\u0435\u043a\u043b\u0430\u043c\u0438\u0440\u0443\u044e\u0442 \u0437\u043e\u043b\u043e\u0442\u043e \u0441\u0430\u043d\u0440\u0430\u0439\u0441","toNumber":"74952521125","createdAt":"2018-12-30T09:02:19+0300","updatedAt":"2018-12-30T09:02:19+0300","isVisible":true,"rating":0,"author":{"profile":{"id":1381694,"firstName":"VIVA","lastName":"","avatar":{"bucket":"numbusters-avatar","name":"upload-5b80d12e7ae396.69501423.jpg","link":"https:\/\/numbusters-avatar.s3.amazonaws.com\/upload-5b80d12e7ae396.69501423.jpg","eTag":"9ec9a8cd5660421ef495144932cb6fb9","size":30368},"branding":null,"phones":[{"number":"79086395237","rating":{"likes":1,"dislikes":0,"level":0},"isBanned":false}],"updatedAt":"2018-12-30T09:12:56+0300"},"averageProfile":null,"branding":null,"rating":{"likes":1,"dislikes":0,"level":0},"isAutoBanned":false,"isBanned":false}},{"id":460853,"text":"\u0422\u0440\u0438\u043a\u043b\u044f\u0442\u044b\u0439 \u0441\u0430\u043d\u043b\u0430\u0439\u0442","toNumber":"74952521125","createdAt":"2018-12-29T15:22:45+0300","updatedAt":"2018-12-29T15:22:45+0300","isVisible":true,"rating":0,"author":{"profile":{"id":2198500,"firstName":"\u041d\u0435\u0442 \u0438\u043c\u0435\u043d\u0438","lastName":"","avatar":null,"branding":null,"phones":[{"number":"79054939569","rating":{"likes":0,"dislikes":0,"level":0},"isBanned":false}],"updatedAt":"2018-10-21T10:39:27+0300"},"averageProfile":{"id":307616073,"firstName":"\u0420\u043e\u043c\u0430\u043d","lastName":"\u0420\u0443\u0441\u0441\u043a\u0438\u0439 \u0421\u0442\u0430\u043d\u0434\u0430\u0440\u0442","avatar":null,"branding":null,"phones":[{"number":"79054939569"}]},"branding":null,"rating":{"likes":0,"dislikes":0,"level":0},"isAutoBanned":false,"isBanned":false}},{"id":459708,"text":"\u0441\u043f\u0430\u043c","toNumber":"74952521125","createdAt":"2018-12-28T12:13:39+0300","updatedAt":"2018-12-28T12:13:39+0300","isVisible":true,"rating":0,"author":{"profile":{"id":505492,"firstName":"\u041a\u043e\u0447\u0435\u0442\u043a\u043e\u0432\u0430 \u0412\u043b\u0430\u0434\u0438\u043c\u0438\u0440\u043e\u0432\u043d\u0430 \u041c\u0430\u0440\u0438\u043d\u0430","lastName":"","avatar":null,"branding":null,"phones":[{"number":"79266287862","rating":{"likes":0,"dislikes":0,"level":0},"isBanned":false}],"updatedAt":"2018-07-16T21:21:20+0300"},"averageProfile":{"id":200767335,"firstName":"\u041a\u043e\u0447\u0435\u0442\u043a\u043e\u0432\u0430","lastName":"","avatar":null,"branding":null,"phones":[{"number":"79266287862"}]},"branding":null,"rating":{"likes":0,"dislikes":0,"level":0},"isAutoBanned":false,"isBanned":false}},{"id":459686,"text":"\u0421\u0430\u043d\u043b\u0430\u0439\u0442","toNumber":"74952521125","createdAt":"2018-12-28T11:58:04+0300","updatedAt":"2018-12-28T11:58:04+0300","isVisible":true,"rating":0,"author":{"profile":{"id":2194917,"firstName":"\u041d\u0435\u0442 \u0438\u043c\u0435\u043d\u0438","lastName":"","avatar":null,"branding":null,"phones":[{"number":"79876969630","rating":{"likes":0,"dislikes":0,"level":0},"isBanned":false}],"updatedAt":"2018-10-19T22:41:47+0300"},"averageProfile":null,"branding":null,"rating":{"likes":0,"dislikes":0,"level":0},"isAutoBanned":false,"isBanned":false}},{"id":459544,"text":"\u0421\u0430\u043d\u043b\u0430\u0439\u0442","toNumber":"74952521125","createdAt":"2018-12-28T08:56:49+0300","updatedAt":"2018-12-28T08:56:49+0300","isVisible":true,"rating":0,"author":{"profile":{"id":231822,"firstName":"\u0410\u0434\u0432\u043e\u043a\u0430\u0442 \u0410\u043d\u044f","lastName":"","avatar":null,"branding":null,"phones":[{"number":"79171237212","rating":{"likes":0,"dislikes":0,"level":0},"isBanned":false}],"updatedAt":"2018-07-11T12:15:26+0300"},"averageProfile":{"id":149370010,"firstName":"\u0410\u043d\u043d\u0430","lastName":"\u0413\u0435\u043e\u0440\u0433\u0438\u0435\u0432\u043d\u0430 \u0427\u0438\u0441\u0442\u044f\u043a\u043e\u0432\u0430, \u042e\u0440\u0438\u0441\u0442","avatar":null,"branding":null,"phones":[{"number":"79171237212"}]},"branding":null,"rating":{"likes":0,"dislikes":0,"level":0},"isAutoBanned":false,"isBanned":false}}]}}
```


## Tokens

We can get them after registration. 

Tokens look like that:

```
oig19z3dcyswwowws0880c84gsoww0gkko11gwg8w0so8ow4k
4cgbi0yecb40cw4so8g088kk8wkss0488wc184sg4ww4k8gk4o
```

## Other

Interesting thing that server will return you info about random phone number if you send incorrect http headers


