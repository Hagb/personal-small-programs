from rss_get import RSSMsgs_getter, RSSMsg
from msg_bot import Msg_bot, Msg_sender
from typing import List
import traceback


class RSSBot(Msg_bot):
    def __init__(self,
                 senders: List[Msg_sender],
                 rssGetter: RSSMsgs_getter,
                 timeCheck: bool = True,
                 timeNewer: bool = True):
        self.senders = senders
        self.msgs: List[List[RSSMsg]] = [[] for i in senders]
        self.rssGetter = rssGetter
        self.first = True
        self.timeCheck = timeCheck
        self.timeNewer = timeNewer

    def run(self):
        if self.first:
            tmpMsgs = self.rssGetter.getMsgs()
            self.msgs = [tmpMsgs[:] for i in self.msgs]
            latestTime = max([i.getRss()['published_parsed'] for i in tmpMsgs])
            self.latestTime = [latestTime for i in self.msgs]
            del tmpMsgs
            self.first = False
        else:
            try:
                latestMsgs = self.rssGetter.getMsgs()
            except Exception:
                traceback.print_exc()
                return False
            returnValue = True
            for senderNo in range(len(self.senders)):
                msgs = self.msgs[senderNo]
                stop = False
                newMsgs = [a for a in latestMsgs if a not in msgs]
                if self.timeCheck:
                    if self.timeNewer:
                        newMsgs = [
                            a for a in newMsgs if a.getRss()
                            ['published_parsed'] > self.latestTime[senderNo]
                        ]
                    else:
                        newMsgs = [
                            a for a in newMsgs if a.getRss()
                            ['published_parsed'] >= self.latestTime[senderNo]
                        ]
                for msg in newMsgs:
                    if not stop:
                        try:
                            text = msg.getStr()
                            print('send:', text, sep='\n')
                            res = self.senders[senderNo].sendMsg(text)
                            if res:
                                msgs.append(msg)
                                self.latestTime[senderNo] = max(
                                    self.latestTime[senderNo],
                                    msg.getRss()['published_parsed'])
                            else:
                                raise ('Send error')
                        except Exception:
                            traceback.print_exc()
                            stop = True
                    else:
                        break
                returnValue = returnValue and not stop
            return returnValue
