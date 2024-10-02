from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost
from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类

import requests

from mirai import Image
import logging
import traceback


# 注册插件
@register(name="GetWeather", description="Hello WeatherPlugin", version="0.1", author="max")
class WeatherPlugin(BasePlugin):

    # API URL for weather
    weather_api_url = "http://www.maxtral.fun/APIphp/ExactlyweatherGet.php?address={address}"

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    @handler(PersonNormalMessageReceived)
    @handler(GroupNormalMessageReceived)
    async def _(self, event: EventContext):
        try:
            text = event.event.text_message
            
            # 修改检测规则
            if text.startswith("getweather ") or text.startswith("天气 "):
                # 提取地名
                location = text.split(" ", 1)[1]  # 获取地名
                event.prevent_default()
                event.prevent_postorder()

                # 调用天气API
                response = requests.get(self.weather_api_url.format(address=location))
                if response.ok:  # 使用 response.ok 来检查请求是否成功
                    event.add_return("reply", [Image(url=response.url)])  # 假设 API 返回的图片 URL
                else:
                    event.add_return("reply", ["天气获取失败，请稍后再试。"])
                logging.info(f"Weather request for location: {location}")
        except Exception as e:
            logging.error(traceback.format_exc())

    # 插件卸载时触发
    def __del__(self):
        pass
