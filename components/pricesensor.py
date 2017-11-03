"""
文件名：pricesensor.py
文件位置：HomeAssistant配置目录/custom_components/sensor/pricesensor.py

"""
import logging
from homeassistant.helpers.entity import Entity
_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):   #在homeassistant注册实体
    _LOGGER.info("setup platform sensor.hachina...")
    add_devices([HAChinaPriceSensor()])

class HAChinaPriceSensor(Entity):  
    def __init__(self):          #初始化传感器实体
        self._object_id = 'pricesensor'
        self._state = 0
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
    def update(self):               #更新传感器状态
        import requests
        import re        
        “”“获取商品价格”“”
        r = requests.get(
            'https://p.3.cn/prices/mgets?callback=jQuery5614231&type=1&area=1_72_2799_0&pdtk=mYRfHvynjZowefXscI7IeQSCZxlXRmwWV1jTlcCA44vgU8icXTSBSO2FPFke$
        str1 = re.findall("\"p\":\".*\"", r.text)[0]
        str1 = re.findall('[1-9]\d*\.\d*|0\.\d*[1-9]\d*', str1)
        self._state = float(str1[0])
    
