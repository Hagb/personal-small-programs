import coolq
import RSSBot
import time


cq = [coolq.CqGroupMsg_sender(group = 1234566)]

rssbot1 = RSSBot.RSSBot(cq
        , RSSBot.RSSMsgs_getter('http://127.0.0.1:1200/cqu/jwc/announcement'))

rssbot2 = RSSBot.RSSBot(cq
        , RSSBot.RSSMsgs_getter('https://www.solidot.org/index.rss'))



while True:
    rssbot1.run()
    rssbot2.run()
    time.sleep(30*60)
