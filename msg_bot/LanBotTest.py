import coolq
import LanBot
import time
username = '20xxxxxx'
password = '********'

lb = LanBot.LanBot(
    [coolq.CqGroupMsg_sender(group=1234567)],
    LanBot.LanMsgs_getter(username=username, password=password))

while True:
    lb.run()
    time.sleep(10*60)
