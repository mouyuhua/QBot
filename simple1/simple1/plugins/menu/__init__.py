# # import nonebot
# from nonebot import get_driver
#
# from .config import Config
#
# global_config = get_driver().config
# config = Config(**global_config.dict())
#
# # Export something for other plugin
# # export = nonebot.export()
# # export.foo = "bar"
#
# # @export.xxx
# # def some_function():
# #     pass

#/--* v0.0.1 *--/

from nonebot import plugin
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from .data_source import get_function_list, function_content

QBotMenu = plugin.on_command('菜单', rule=to_me(), priority=22)

@QBotMenu.handle()
async def QBotMenuDone(bot:Bot, event:Event, state:T_State):
    # await QBotMenu.finish('功能正在加急制作中，请耐心等待一些时间')
    function_dis = get_function_list()
    await QBotMenu.finish(function_dis)
