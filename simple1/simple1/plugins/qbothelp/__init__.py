# /** v0.0.1 **/

from nonebot import plugin
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from ..menu.data_source import *

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


QBotHelp = plugin.on_command('help', rule=to_me(), priority=21)


@QBotHelp.handle()
async def QBotHelpDone(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state['name'] = args


@QBotHelp.got('name', 'What can i do for you?')
async def QBotHelpGot(bot: Bot, event: Event, state: T_State):
    content = function_content(state['name'], 'describe')
    await QBotHelp.finish(content)
