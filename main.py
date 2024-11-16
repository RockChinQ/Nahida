from pkg.plugin.events import *  # 导入事件类
from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext

import requests
import random

from mirai import Image
import logging
import traceback


# 注册插件
@register(name="Nahida", description="Hello Nahida", version="0.1", author="RockChinQ")
class NahidaPlugin(BasePlugin):

    images_urls: list[str] = []
    # 插件加载时触发
    # plugin_host (pkg.plugin.host.PluginHost) 提供了与主程序交互的一些方法，详细请查看其源码
    def __init__(self, plugin_host: APIHost):
        json_resp = requests.get(
            url="https://api.github.com/repos/RockChinQ/NahidaImages/contents/images",
        )
        obj_json = json_resp.json()

        for item in obj_json:
            self.images_urls.append(item["download_url"])

        
    @handler(PersonMessageReceived)
    @handler(GroupMessageReceived)
    async def _(self, ctx: EventContext):
        try:
            text = str(ctx.event.message_chain).strip()
            if text == "nahida" or text == "nhd":
                ctx.prevent_default()
                ctx.prevent_postorder()
                # 发送图片
                image_url = random.choice(self.images_urls)
                
                await ctx.reply([Image(url=image_url)])

                self.ap.logger.info("Nahida!")
        except Exception as e:
            self.ap.logger.error(traceback.format_exc())

    # 插件卸载时触发
    def __del__(self):
        pass
