import coolq
import LanBot
import RSSBot
import time
import Mirai
import realGroups

miraiSession = Mirai.MiraiSession('keyofhagb', qqID=realGroups.qqID_test)

testcq = [coolq.CqGroupMsg_sender(group=realGroups.testG)
          ] + [Mirai.MiraiGroupMsg_sender(realGroups.testG, miraiSession)]

jwccqs = [
    coolq.CqGroupMsg_sender(group=group) for group in
    [realGroups.mathGradeG, realGroups.lanWaterG, realGroups.otherCampusG]
]

youthcqs = [
    coolq.CqGroupMsg_sender(group=group) for group in
    [realGroups.mathOtherG, realGroups.otherCampusG, realGroups.testG]
]

mathcqs = [coolq.CqGroupMsg_sender(group=realGroups.mathGradeG)]
lancqs = [
    coolq.CqGroupMsg_sender(group=group) for group in [realGroups.lanNotifyG]
] + [Mirai.MiraiGroupMsg_sender(realGroups.lanTestG, miraiSession)]
netcqs = [
    coolq.CqGroupMsg_sender(group=group)
    for group in [realGroups.lanNotifyG, realGroups.lanWaterG]
]

jwcbot = RSSBot.RSSBot(
    jwccqs,
    RSSBot.RSSMsgs_getter('http://jwc.cqu.edu.cn/rss.xml',
                          way2str="教务处公告：\n{title}\n{link}"))

youthbot = RSSBot.RSSBot(
    youthcqs,
    RSSBot.RSSMsgs_getter('http://127.0.0.1:1200/cqu/youth/tzgg',
                          way2str="校团委公告：\n{title}\n{link}"))

mathbot = RSSBot.RSSBot(
    mathcqs,
    RSSBot.RSSMsgs_getter('http://127.0.0.1:1200/cqu/sci/1056',
                          way2str="数统学术活动：\n{title}\n{link}"))

netbot = RSSBot.RSSBot(netcqs,
                       RSSBot.RSSMsgs_getter(
                           'http://127.0.0.1:1200/cqu/net/tzgg',
                           way2str="信息化办公室公告：\n{title}\n{link}"),
                       timeNewer=False)

lanbot = LanBot.LanBot(
    lancqs,
    LanBot.LanMsgs_getter(username=realGroups.lanUser,
                          password=realGroups.lanPass))
n = 0


def rssRun():
    jwcbot.run()
    youthbot.run()
    mathbot.run()
    netbot.run()


while True:
    miraiSession.login()
    miraiSession.verify()
    if not n:
        rssRun()
    if not n % 2:
        for i in testcq:
            i.sendMsg(time.asctime())

#    rssbot2.run()
    n = (n + 1) % 6
    lanbot.run()
    miraiSession.release()
    time.sleep(5 * 60)
