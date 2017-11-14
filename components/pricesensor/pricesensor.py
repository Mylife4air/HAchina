"""
文件名：pricesensor.py
文件位置：HomeAssistant配置目录/custom_components/sensor/pricesensor.py
"""
import asyncio
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import logging
from homeassistant.helpers.entity import Entity
# 引入这两个库，用于配置文件格式校验
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
_LOGGER = logging.getLogger(__name__)
DOMAIN = 'pricesensor'
URL = "url"
DEFAULT_URL="https://item.taobao.com/item.htm?scm=1007.12493.92624.100200300000005&id=549816031459&pvid=ccf56d0c-3737-4$"
# 配置文件的样式
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(URL,default = DEFAULT_URL):cv.string,
            }),
    },
    extra=vol.ALLOW_EXTRA)

def setup_platform(hass, config, add_devices, discovery_info=None):   #加载实体
    _LOGGER.info("setup platform sensor.hachina...")
    add_devices([HAChinaPriceSensor(hass,config)])


class HAChinaPriceSensor(Entity):
    def __init__(self,hass,config):          #初始化传感器实体
        self._object_id = 'pricesensor'
        self._state = "不支持"
        self._hass = hass
        self._url = config['url']
        self._unit_of_measurement='￥'
    @property
    def unit_of_measurement(self):       #用于呈现传感器符号
        return self._unit_of_measurement
    @property
    def name(self):                       #用于呈现传感器名字
        return self._object_id
    @property
    def state(self):                   #用于呈现传感器状态
        return self._state

    @asyncio.coroutine
    def async_update(self):               #异步更新传感器状态
        import re
        session = async_get_clientsession(self._hass)
        resp = yield from session.get(self._url)
        result = yield from resp.read()
        if self._url[13:16]=='tao':
            data = re.findall('"tb-rmb-num">(.*?)</em>', str(result), re.S)
            self._state = str(re.findall('\d+', str(data))[0])
        elif self._url[15:17] =='tm':
            data = re.findall('"price":"(.*?)","priceCent', str(result), re.S)
            self._state = str(re.findall('\d+', str(data))[0])
