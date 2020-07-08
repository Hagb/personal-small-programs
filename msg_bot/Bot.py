import LanBot
import RSSBot
import time
import Mirai
import realGroups

KEY = 'keyofhagb'

miraiSession = Mirai.MiraiSession(KEY, qqID=realGroups.qqID)
miraiSessionTest = Mirai.MiraiSession(KEY, qqID=realGroups.qqID_test)

testcq = [Mirai.MiraiGroupMsg_sender(realGroups.testG, miraiSession)
          ] + [Mirai.MiraiGroupMsg_sender(realGroups.testG, miraiSessionTest)]

jwccqs = [
    Mirai.MiraiGroupMsg_sender(group, miraiSession) for group in
    [realGroups.mathGradeG, realGroups.lanWaterG, realGroups.otherCampusG]
]

youthcqs = [
    Mirai.MiraiGroupMsg_sender(group, miraiSession) for group in
    [realGroups.mathOtherG, realGroups.otherCampusG, realGroups.testG]
]

mathcqs = [Mirai.MiraiGroupMsg_sender(realGroups.mathGradeG, miraiSession)]
lancqs = [
    Mirai.MiraiGroupMsg_sender(realGroups.lanNotifyG, miraiSession),
    Mirai.MiraiGroupMsg_sender(realGroups.lanTestG, miraiSession)
]
netcqs = [
    Mirai.MiraiGroupMsg_sender(group, miraiSession)
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


def run():
    global n
    miraiSession.login()
    miraiSessionTest.login()
    miraiSession.verify()
    miraiSessionTest.verify()
    if not n:
        rssRun()
    if not n % 2:
        for i in testcq:
            i.sendMsg(time.asctime())
    n = (n + 1) % 6
    lanbot.run()
    miraiSession.release()
    miraiSessionTest.release()


while True:
    run()
    time.sleep(5 * 60)
