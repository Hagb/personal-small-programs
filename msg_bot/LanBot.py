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
from msg_bot import Msg_bot, Msg_sender
import traceback
from lanunion import LanMsgs_getter, LanMsg
from typing import List


class LanBot(Msg_bot):
    """蓝盟的报修单通知 bot 的`Msg_bot`子类."""
    def __init__(self, senders: List[Msg_sender], lanGetter: LanMsgs_getter):
        super().__init__()
        self.senders = senders  # 发送器列表
        # self.msgs 中和相应发送器相同下标的元素也是一个列表，其中是已经收到并正确发送了的报修单.
        self.msgs: List[List[LanMsg]] = [[] for i in senders]
        self.lanGetter = lanGetter  # 蓝盟报修单列表接收器
        self.first = True  # 是否第一次运行`run()`方法

    def run(self):
        """抓取一次报修单并处理"""
        if self.first:  # 第一次除了接收报修单列表，其余的事情都不做
            tmpMsgs = self.lanGetter.getMsgs()
            self.msgs = [tmpMsgs[:] for i in self.msgs]
            del tmpMsgs
            self.first = False
        else:
            try:
                latestMsgs = self.lanGetter.getMsgs()  # 最新的报修单列表
            except Exception:
                traceback.print_exc()
                return False
            returnValue = True
            for senderNo in range(len(self.senders)):
                msgs = self.msgs[senderNo]
                stop = False  # 对于每个发送器，发送时一旦出现错误/异常，本次该发送器的后续发送就中止
                # 发送上一次的列表中有有但最新的列表中无的报修单，它们被删除了或被分配了
                deletedMsgs = [msg for msg in msgs if msg not in latestMsgs]
                for msg in deletedMsgs:
                    if not stop:
                        try:
                            details = msg.getDetails()
                            if details:
                                text = '被分配给 {repairer} :\n'\
                                    '{sheetId} ({sheetNo})'.format(
                                        **msg.data,
                                        repairer=details['分配给'])
                            else:
                                text = '被删除:\n'\
                                    '{sheetId} ({sheetNo})'.format(
                                        **msg.data)
                            print('del or repaired:', text, sep='\n')
                            res = self.senders[senderNo].sendMsg(text)
                            if res:
                                msgs.remove(msg)
                            else:
                                raise ('Send error')
                        except Exception:
                            traceback.print_exc()
                            stop = True
                    else:
                        break
                addedMsgs = [a for a in latestMsgs if a not in msgs]
                # 发送列表中新增的单子
                for msg in addedMsgs:
                    if not stop:
                        try:
                            text = msg.getStr()
                            print('send:', text, sep='\n')
                            res = self.senders[senderNo].sendMsg(text)
                            if res:
                                msgs.append(msg)
                            else:
                                raise ('Send error')
                        except Exception:
                            traceback.print_exc()
                            stop = True
                    else:
                        break
                returnValue = returnValue and not stop
            return returnValue
