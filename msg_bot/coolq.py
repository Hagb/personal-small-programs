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


class CqGroupMsg_sender(Msg_sender):
    """通过 CoolQ HTTP API 发送 QQ 群消息的`Msg_sender`子类"""
    @staticmethod
    def sendGroupMsg(group: int, msg: str,
                     cqUrl_group:
                     str = 'http://127.0.0.1:5700/send_group_msg') -> bool:
        """发送群消息"""
        coolqPost = requests.post(cqUrl_group, data=json.dumps(
            {"group_id": group, "message": msg, "auto_escape": True}),
            headers={'Content-Type': 'application/json'})
        coolqPost.encoding = coolqPost.apparent_encoding
        coolqJson = json.loads(coolqPost.text)
        if coolqJson['status'] == 'failed':
            return False
        else:
            return True

    def __init__(self,
                 cqUrl_group: str = 'http://127.0.0.1:5700/send_group_msg',
                 group: int = 0, delay: int = 10):
        super().__init__()
        self.cqUrl_group = cqUrl_group
        self.group = group
        self.delay = delay

    def sendMsg(self, msg: Union[str, Msg]) -> bool:
        text = msg if isinstance(msg, str) else msg.getStr()
        result = CqGroupMsg_sender.sendGroupMsg(
            self.group, text, self.cqUrl_group)
        time.sleep(self.delay)
        return result
