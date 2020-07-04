# msg\_bot

除了 Bot.py，其它 py 文件均为类定义。

注释不多，没啥文档，风格混乱，代码肮脏…… 任何意见或建议，或者任何能够帮到你的，都欢迎提 issue、PR。

## 文件说明

各文件的依赖表现为层次结构

- [msg\_bot.py](msg_bot.py): 抽象基类
    - [lanunion.py](lanunion.py): 获取重大蓝盟报修单的类（已加密，可用系统后台地址作为密码解压 [lanunion.py.zip](lanunion.py.zip) 得到明文）
        - [LanBot.py](LanBot.py): 蓝盟报修单 bot 的封装
    - [Mirai.py](Mirai.py): 通过 Mirai 发送信息的类
    - [coolq.py](coolq.py): 通过非自由的 CoolQ 发送信息的类
    - [rss\_get.py](rss_get.py): 接受 RSS Feed 信息的类
        - [RSSBot.py](RSSBot.py): RSS 发送 bot 的封装
    - [MatterBridge.py](MatterBridge.py): 通过 [MatterBridge](https://github.com/42wim/matterbridge) 收发信息的类

将这些类实例化的是，你可将其视作上述类的使用例子：

- [Bot.py](Bot.py)

其中群号在 [realGroups.py](realGroups.py)，已经隐去。
