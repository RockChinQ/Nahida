from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost

import requests
import random

from mirai import Image
import logging
import traceback


# 注册插件
@register(name="Nahida", description="Hello Nahida", version="0.1", author="RockChinQ")
class NahidaPlugin(Plugin):

    images_urls: list[str] = []
    # 插件加载时触发
    # plugin_host (pkg.plugin.host.PluginHost) 提供了与主程序交互的一些方法，详细请查看其源码
    def __init__(self, plugin_host: PluginHost):
        json_resp = requests.get(
            url="https://api.github.com/repos/RockChinQ/NahidaImages/contents/images",
        )
        obj_json = json_resp.json()

        for item in obj_json:
            self.images_urls.append(item["download_url"])

        
    @on(PersonMessageReceived)
    @on(GroupMessageReceived)
    def _(self, event: EventContext, host: PluginHost, message_chain, **kwargs):
        try:
            text = str(message_chain).strip()
            if text == "nahida" or text == "nhd":
                event.prevent_default()
                event.prevent_postorder()
                # 发送图片
                image_url = random.choice(self.images_urls)
                
                if kwargs["launcher_type"] == "group":
                    host.send_group_message(kwargs["launcher_id"], [Image(url=image_url)])
                else:
                    host.send_person_message(kwargs["launcher_id"], [Image(url=image_url)])

                logging.info("Nahida!")
        except Exception as e:
            logging.error(traceback.format_exc())

    # 插件卸载时触发
    def __del__(self):
        pass
