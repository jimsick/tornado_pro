# coding:utf-8

from SDK.CCPRestSDK import REST
import ConfigParser

accountSid = '8aaf07086010a0eb016031a9ef8c0ea1';
# 说明：主账号，登陆云通讯网站后，可在控制台首页中看到开发者主账号ACCOUNT SID。

accountToken = '6478ac987eec4ed6abdc4c2afa3cefb3';
# 说明：主账号Token，登陆云通讯网站后，可在控制台首页中看到开发者主账号AUTH TOKEN。

appId = '8aaf07086010a0eb016031a9efe10ea8';
# 请使用管理控制台中已创建应用的APPID。

serverIP = 'app.cloopen.com';
# 说明：请求地址，生产环境配置成app.cloopen.com。

serverPort = '8883';
# 说明：请求端口 ，生产环境为8883.

softVersion = '2013-12-26';  # 说明：REST API版本号保持不变。


def sendTemplateSMS(to, datas, tempId):
    # 初始化REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    for k, v in result.iteritems():
        if k == 'templateSMS':
            for k, s in v.iteritems():
                print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)


