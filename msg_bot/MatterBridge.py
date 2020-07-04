from msg_bot import Msg_sender, Msgs_getter, Msg, NoneType
from typing import Union, List, Callable
import requests
import json


class MatterBridgeMsg(Msg):
    def __init__(self, mbDict: dict,
                 way2str: Union[Callable, str] = '{username}: {text}',
                 keys: Union[NoneType, List[str]] = None):
        self.mbDict = mbDict
        self.way2str = way2str
        self.keys = keys

    def getDict(self) -> dict:
        return self.mbDict

    def setDict(self, mbDict: dict):
        self.mbDict = mbDict

    def getStr(self) -> str:
        if isinstance(self.way2str, str):
            return self.way2str.format(**self.mbDict)
        else:
            return self.way2str(self.mbDict)


class MatterBridgeMsg_sender(Msg_sender):
    def __init__(self, url: str, gateway: str, nickname: str = 'nickname'):
        self.url = url
        self.gateway = gateway
        self.nickname = nickname

    def sendMsg(self, msg: Union[str, Msg],
                nickname: Union[str, NoneType] = None):
        if nickname is None:
            nickname = self.nickname
        text = msg if isinstance(msg, Union[str]) else msg.getStr()
        requests.post(self.url, data=json.dumps({"gateway": self.gateway,
                                                 "text": text,
                                                 "username": nickname}),
                      headers={'Content-Type': 'application/json'})
        return True


class MatterBridgeMsgs_getter(Msgs_getter):
    def __init__(self, url: str,
                 way2str: Union[Callable, str] = '{username}: {text}',
                 keys: Union[NoneType, List[str]] = None):
        self.url = url
        self.way2str = way2str
        self.keys = keys

    def getMsgs(self) -> List[MatterBridgeMsg]:
        resp = requests.get(self.url)
        resp.encoding = resp.apparent_encoding
        mbJson = json.loads(resp.text)
        return [MatterBridgeMsg(i) for i in mbJson]
