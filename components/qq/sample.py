import os


def onQQMessage(bot, contact, member, content):
    path = os.path.expanduser('~') + '/.homeassistant'
    path += '/msg.txt'
    if contact.qq == 'xxxxxx':
        with open(path, 'w') as fs:
            fs.write(content)
            fs.close()
            bot.SendTo(contact, '已经弄好了')
    elif content == '-stop':
        bot.SendTo(contact, 'QQ机器人已关闭')
        bot.Stop()
