"""
支持博联RMmini3智能遥控器组件
"""
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
import broadlink
import os
import time

from homeassistant.helpers.entity import Entity


REQUIREMENTS = ['broadlink==0.6']
DOMAIN = 'RMmini3'
type = 0x2737
path = os.path.expanduser('~')+'/.homeassistant/learn'
# 配置文件的样式
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required('mac'): cv.string,
                vol.Required('host'): cv.port,
            }),
    },
    extra=vol.ALLOW_EXTRA)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """装载实体."""
    host = config['host']
    mac = bytearray.fromhex(config['mac'])
    dev = broadlink.gendevice(type, (host, 80), mac)
    o = Rmmin3(hass, dev)
    add_devices([o])


class Rmmin3(Entity):
    """创建RMmini3类."""

    def __init__(self, hass, dev):
        """初始化."""
        self._state = '未知'
        self._hass = hass
        self._dev = dev
        self._name = DOMAIN
        self._unit_of_measurement = '度'
        # 注册学习服务和发送服务
        hass.services.register(DOMAIN, 'send', self.send)   
        hass.services.register(DOMAIN, 'learn', self.learn)
    
    @property
    def should_poll(self):
        """需要更新温度"""
        return True

    @property
    def name(self):
        """返回实体名字"""
        return self._name

    @property
    def state(self):
        """返回实体状态"""
        return self._state

    @property
    def unit_of_measurement(self):
        """返回实体单位符号"""
        return self._unit_of_measurement

    def update(self):
        """更新实体传感器温度"""
        self._dev.auth()
        self._state = self._dev.check_temperature()

    def send(self, data):   
        """发送红外信息"""
        self._dev.auth()
        with open(path, 'r') as fs:
            for line in fs:
                if line[:line.index(':')] == str(data.data['send']):
                    date = line[line.index(':') + 1:line.index('。')]
                    print(date)
                    date = bytearray.fromhex(date)
                    self._dev.send_data(date)
                    break
 
    def learn(self, date):          
        """学习红外信息"""
        self._dev.auth()
        self._dev.enter_learning()
        data = None
        timeout = 30
        while (data is None) and (timeout > 0):
            time.sleep(2)
            timeout -= 2
            data = self._dev.check_data()
        if data:
            learned = ''.join(format(x, '02x') for x in bytearray(data))
            self._message = learned
            with open(path, 'a+') as fs:
                fs.write(str(date.data['learn']))
                fs.write(':')
                fs.write(str(learned))
                fs.write('。')
                fs.write('\n')
                fs.close()
        else:
            print("No data received...")
