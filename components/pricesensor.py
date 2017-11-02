"""
文件名：pricesensor.py
文件位置：HomeAssistant配置目录/custom_components/sensor/pricesensor.py

"""
import logging
from homeassistant.helpers.entity import Entity
_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):

    _LOGGER.info("setup platform sensor.hachina...")
    add_devices([HAChinaWeatherSensor()])

class HAChinaWeatherSensor(Entity):
    def __init__(self):

        self._object_id = 'pricesensor'
        self._state = 0
        self._unit_of_measurement='￥'
    @property
    def name(self):
        return self._object_id
    @property
    def state(self):
        return self._state
    def update(self):
        import requests
        import re
        
        r = requests.get(
            'https://p.3.cn/prices/mgets?callback=jQuery5614231&type=1&area=1_72_2799_0&pdtk=mYRfHvynjZowefXscI7IeQSCZxlXRmwWV1jTlcCA44vgU8icXTSBSO2FPFke$
        str1 = re.findall("\"p\":\".*\"", r.text)[0]
        str1 = re.findall('[1-9]\d*\.\d*|0\.\d*[1-9]\d*', str1)
        self._state = float(str1[0])
    
