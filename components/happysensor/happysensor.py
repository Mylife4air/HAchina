"""
文件名：happysensor.py
文件位置：HomeAssistant配置目录/custom_components/sensor/happysensor.py
"""
import asyncio
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import logging
from homeassistant.helpers.entity import Entity
# 引入这两个库，用于配置文件格式校验
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
_LOGGER = logging.getLogger(__name__)
DOMAIN = 'happysensor'
URL="http://api.jisuapi.com/xiaohua/text?pagenum=1&pagesize=1&sort=rand&appkey="
# 配置文件的样式
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required('appkey'):cv.string,
            }),
    },
    extra=vol.ALLOW_EXTRA)

def setup_platform(hass, config, add_devices, discovery_info=None):   #加载组件
    _LOGGER.info("setup platform sensor.hachina...")
    add_devices([HAChinaPriceSensor(hass,config)])


class HAChinaPriceSensor(Entity):
    def __init__(self,hass,config):          #初始化笑话传感器实体
        self._object_id = 'happysensor'
        self._state = "请稍等一下"
        self._hass = hass
        self._apk = config['appkey']
        self._url = URL+self._apk

    @property
    def name(self):                       #用于呈现笑话传感器名字
        return self._object_id
    @property
    def state(self):                   #用于呈现笑话传感器状态
        return self._state

    @asyncio.coroutine
    def async_update(self):               #异步更新笑话传感器状态
        import json
        session = async_get_clientsession(self._hass)
        resp = yield from session.get(self._url)
        result = yield from resp.text()
        data=json.loads(result, strict=False)['result']['list'][0]['content']
        self._state=data
