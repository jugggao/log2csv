1. 取 `gateway.log` 里面含有 `orderNumber` 的记录；

2. 解析出对应记录里面的 `time`，`ip`，`orderNumber`，`sessionId`，`resultUrl`，`openId`；

3. 取 `mvip.knowbox.cn.access.log` 里面每条记录的 `timestamp`，`clientip`，`request`，`referer`，`mobile`，`classNumber`，`token`，`umid`，`&ADTAG`，`&type`，`&tagValue`，`channel`（这个里面不是每条记录都有这些字段的，如果没有就空着）；

4. 取第三步中 clientip 在第二步中存在 ip 的记录（第三步的 clientip 等于第二步的 ip）；

5. 在第四步的结果中将第二步的 ip 和时间放在对应的记录中；

6. 以 Excel 的形式提供第五步的结果。

补充：

- 时间范围从 6 月 1 日到 6 月 5 日；

- ADTAG，&type，&tagValue，channel 这四个如果全部为空，就不用出现在列表里，如果不全为空，还需要。

```
{"@timestamp":"2019-05-25T14:57:07+08:00","clientip":"36.161.44.67","status":"200","log":"log","remote_user":"-","request":"GET /static/image/favicon.ico HTTP/1.1","http_user_agent":"Mozilla/5.0 (Linux; Android 7.0; m3 note Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044704 Mobile Safari/537.36 MMWEBID/2747 MicroMessenger/7.0.4.1420(0x2700043B) Process/tools NetType/WIFI Language/zh_CN","size":1150,"responsetime":0.000,"upstreamhost":"-","upstreamtime":"-","upstreamstatus":"-","http_host":"mvip.knowbox.cn","url":"/static/image/favicon.ico","domain":"mvip.knowbox.cn","xff":"-","referer":"https://mvip.knowbox.cn/details?classNumber=218067690337280&ADTAG=218067690337280&type=14&tagValue=10006432&channel=i_hrmx","trace":"-"}

{"@timestamp":"2019-05-25T15:55:08+08:00","clientip":"223.85.151.68","status":"200","log":"log","remote_user":"-","request":"GET /user/center/imageCode.do?mobile=13990518027&source=h5 HTTP/1.1","http_user_agent":"Mozilla/5.0 (Linux; Android 7.1.2; vivo X9L Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044681 Mobile Safari/537.36 MMWEBID/2558 MicroMessenger/7.0.4.1420(0x2700043B) Process/tools NetType/WIFI Language/zh_CN","size":2092,"responsetime":0.014,"upstreamhost":"10.9.144.53:9091","upstreamtime":"0.014","upstreamstatus":"200","http_host":"mvip.knowbox.cn","url":"//user/center/imageCode","domain":"mvip.knowbox.cn","xff":"-","referer":"https://mvip.knowbox.cn/BindVerify?mobile=13990518027&code=061jqfNV0S4oX02FG2MV0tBhNV0jqfN5&type=getimgcode","trace":"-"}

{"@timestamp":"2019-05-25T14:21:54+08:00","clientip":"117.166.85.120","status":"200","log":"log","remote_user":"-","request":"GET /static/WEB_IM/js/lib/lodash.min.js HTTP/1.1","http_user_agent":"Mozilla/5.0 (Linux; Android 8.1.0; V1809A Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 AppOS/android AppFrom/knowBox AppVersion/4077 AppOS/android AppFrom/knowBox AppVersion/4077","size":24249,"responsetime":0.000,"upstreamhost":"-","upstreamtime":"-","upstreamstatus":"-","http_host":"mvip.knowbox.cn","url":"/static/WEB_IM/js/lib/lodash.min.js","domain":"mvip.knowbox.cn","xff":"-","referer":"https://mvip.knowbox.cn/details?classNumber=220103016275456&activityId=3185&token=61d98dc4-f867-42fb-bdc3-e62a496010d4&version=4077&source=androidNewParent","trace":"-"}

{"@timestamp":"2019-05-25T16:13:15+08:00","clientip":"140.243.132.162","status":"200","log":"log","remote_user":"-","request":"GET /static/WEB_IM/js/common/show_one_msg.js HTTP/1.1","http_user_agent":"Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11s Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 AppOS/android AppFrom/knowBox AppVersion/4077 AppOS/android AppFrom/knowBox AppVersion/4077","size":4012,"responsetime":0.000,"upstreamhost":"-","upstreamtime":"-","upstreamstatus":"-","http_host":"mvip.knowbox.cn","url":"/static/WEB_IM/js/common/show_one_msg.js","domain":"mvip.knowbox.cn","xff":"-","referer":"https://mvip.knowbox.cn/details?classNumber=209559660716032&token=0865ca17-6ae3-4c68-9e20-21c09c7c5b3f&token=0865ca17-6ae3-4c68-9e20-21c09c7c5b3f&umid=a5de17abb3dae2061306a46c69311&source=androidNewParent&appVersion=4.0.77&version=4077&productId=6&payment=NewPayment&pageChannel=3.7.7","trace":"-"}
```

