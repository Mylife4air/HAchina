from qqbot import _bot as bot
from homeassistant.helpers.entity import Entity
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
import threading
import os

DOMAIN = 'qq'
# 配置文件的样式
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required('qq'): cv.string,
            }),
    },
    extra=vol.ALLOW_EXTRA)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Demo sensors."""
    o = DemoSensor()
    add_devices([o])
    print(config['qq'])
    thread1 = QQ(config['qq'])
    thread1.start()


class DemoSensor(Entity):
    """Representation of a Demo sensor."""
    def __init__(self):
        """Initialize the sensor."""
        self._state = '未知'
        self._name = DOMAIN
        self._mutex = threading.Lock()

    @property
    def should_poll(self):
        """No polling needed for a demo sensor."""
        return True

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        path = os.path.expanduser('~') + '/.homeassistant'
        path += '/msg.txt'
        with open(path, 'r') as fs:
            ms = fs.read()
        print(ms)
        self._state = ms


class QQ(threading.Thread):
        def __init__(self, qq):
            threading.Thread.__init__(self)
            self.thread_stop = False
            self.qq = qq

        def run(self):  # Overwrite run() method, put what you want the thread do here
            bot.Login(['-u', str(self.qq)])
            bot.Run()
                
        def stop(self):
            self.thread_stop = True 
