from msg_bot import Msg, Msgs_getter, NoneType
from typing import Union, List, Callable
import feedparser


class RSSMsg(Msg):
    def __init__(self, rssDict: dict,
                 way2str: Union[Callable, str] = '{title}',
                 keys: Union[NoneType, List[str]] = None):
        self.keys = keys
        self.rssDict = rssDict if not keys else \
            {i: rssDict[i] for i in rssDict if i in keys}
        self.way2str = way2str

    def getRss(self) -> dict:
        return self.rssDict

    def setRss(self, rssDict: dict):
        self.rssDict = rssDict

    def getStr(self) -> str:
        if isinstance(self.way2str, str):
            return self.way2str.format(**self.rssDict)
        else:
            return self.way2str(self.rssDict)

    def __eq__(self, rhs) -> bool:
        if type(self) == type(rhs):
            if self.rssDict == rhs.rssDict and self.way2str == rhs.way2str \
               and self.keys == rhs.keys:
                return True
        return False


class RSSMsgs_getter(Msgs_getter):
    def __init__(self, url: str, way2str: Union[Callable, str] = '{title}',
                 keys: Union[NoneType, List[str]] = None):
        self.url = url
        self.way2str = way2str
        self.keys = keys

#    class RSSMsgsGetException(Msgs_getter.MsgsGetException):
#        def __init__(self, error: str):
#            Exception.__init__(self, 'RSS bozo_exception: ' + error)

    def getMsgs(self) -> List[RSSMsg]:
        feed: feedparser = feedparser.parse(self.url)
        if feed['bozo']:
            raise(feed['bozo_exception'])
        else:
            return [RSSMsg(rssDict=i, way2str=self.way2str, keys=self.keys)
                    for i in feed['entries'][::-1]]
