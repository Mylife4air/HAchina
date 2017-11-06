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
        from lxml import etree
        url ='https://item.taobao.com/item.htm?scm=1007.12493.92624.100200300000005&id=549816031459&pvid=ccf56d0c-3737-4863-ab35-206b76d014d3'
        req= requests.get(url)
        tree = etree.HTML(req.text)
        data = tree.xpath('//*[@id="J_StrPrice"]/em[2]/text()')
        self._state = str(data[0])
    
