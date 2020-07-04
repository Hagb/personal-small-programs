#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
__author__ = "Hagb (郭俊余)"
__copyright__ = f"Copyright 2020, {__author__}"
__credits__ = ["CQU Lanunion"]
__license__ = "GNU AGPL v3"
__version__ = "2.0"
__maintainer__ = __author__
__email__ = "hagb_green@qq.com"
__status__ = "Development"
from msg_bot import Msg_sender, Msg
from typing import Union
import time
import requests
import json


class MiraiSession():
    def __init__(self,
                 miraiAuthKey: str,
                 miraiUrl: str = 'http://127.0.0.1:8080/',
                 qqID: int = 0):
        self.miraiUrl = miraiUrl
        self.miraiAuthKey = miraiAuthKey
        self.qqID = qqID

    def login(self) -> str:
        miraiPost = requests.post(self.miraiUrl + 'auth',
                                  data=json.dumps(
                                      {'authKey': self.miraiAuthKey}),
                                  headers={'Content-Type': 'application/json'})
        miraiPost.encoding = miraiPost.apparent_encoding
        miraiJson = json.loads(miraiPost.text)
        if miraiJson['code'] == 0:
            self.sessionKey = miraiJson['session']
            return miraiJson['session']
        else:
            self.sessionKey = ''
            return ''

    def verify(self, qqID: int = 0) -> bool:
        if qqID == 0:
            assert self.qqID != 0
            qqID = self.qqID
        assert self.sessionKey != ''
        miraiPost = requests.post(self.miraiUrl + 'verify',
                                  data=json.dumps({
                                      'sessionKey': self.sessionKey,
                                      'qq': self.qqID
                                  }),
                                  headers={'Content-Type': 'application/json'})
        miraiPost.encoding = miraiPost.apparent_encoding
        miraiJson = json.loads(miraiPost.text)
        if miraiJson['code'] == 0:
            return True
        else:
            print(miraiJson)
            return False

    def release(self, qqID: int = 0) -> bool:
        if qqID == 0:
            assert self.qqID != 0
            qqID = self.qqID
        assert self.sessionKey != ''
        miraiPost = requests.post(self.miraiUrl + 'release',
                                  data=json.dumps({
                                      'sessionKey': self.sessionKey,
                                      'qq': self.qqID
                                  }),
                                  headers={'Content-Type': 'application/json'})
        miraiPost.encoding = miraiPost.apparent_encoding
        miraiJson = json.loads(miraiPost.text)
        if miraiJson['code'] == 0:
            self.sessionKey = ''
            return True
        else:
            print(miraiJson)
            return False


class MiraiGroupMsg_sender(Msg_sender):
    def __init__(self, group: int, session: MiraiSession, delay: int = 10):
        super().__init__()
        self.session = session
        self.group = group
        self.delay = delay

    @staticmethod
    def sendGroupMsg(group: int, msg: str, session: MiraiSession):
        miraiPost = requests.post(session.miraiUrl + '/sendGroupMessage',
                                  data=json.dumps({
                                      "sessionKey":
                                      session.sessionKey,
                                      "target":
                                      group,
                                      "messageChain": [{
                                          'type': 'Plain',
                                          'text': msg
                                      }]
                                  }),
                                  headers={'Content-Type': 'application/json'})
        miraiPost.encoding = miraiPost.apparent_encoding
        miraiJson = json.loads(miraiPost.text)
        if miraiJson['code'] == 0:
            return True
        else:
            print(miraiJson)
            return False

    def sendMsg(self, msg: Union[str, Msg]) -> bool:
        text = msg if isinstance(msg, str) else msg.getStr()
        result = MiraiGroupMsg_sender.sendGroupMsg(self.group, text,
                                                   self.session)
        time.sleep(self.delay)
        return result
