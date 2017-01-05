# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response
 
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage

import json
 
WECHAT_TOKEN = '09231211'
AppID = 'wx693c4716eeb8db16'
AppSecret = '7338069c1463b40d3f81f3b814133668'
 
# 实例化 WechatBasic
wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
)

@csrf_exempt
def exam(request):
    fs = file(r"/opt/dn2134/s.jo")
    jsonBuf = json.load(fs)
    data = jsonBuf["questions"][1]
    return render_to_response('test.html', {"data" : data})

@csrf_exempt
def index(request):
    return HttpResponse("wlabdk")

@csrf_exempt
def weixin_main(request):
    if request.method == 'GET':
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
 
        if not wechat_instance.check_signature(
                signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')
 
        return HttpResponse(
            request.GET.get('echostr', ''), content_type="text/plain")
 
 
    # 解析本次请求的 XML 数据
    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')
 
    # 获取解析好的微信请求信息
    message = wechat_instance.get_message()
 
    # 关注事件以及不匹配时的默认回复
    response = wechat_instance.response_text(
        content = (
            '感谢您的关注！\n目前支持的回复内容：\n复习\n'
                    '考试\n'
            ))
    if isinstance(message, TextMessage):
        # 当前会话内容
        content = message.content.strip()
        if content == '复习':
            reply_text = '<a href="http://www.ziqiangxuetang.com">点击进入【全题复习】</a>'

        elif content == '考试':
            reply_text = '<a href="http://www.lllzone.com/exam/">点击进入【模拟测试】</a>'

        else :
            reply_text = '回复内容无效，请重新输入。'
 
        response = wechat_instance.response_text(content=reply_text)
 
    return HttpResponse(response, content_type="application/xml")
