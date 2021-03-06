#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function
nonebot.init()
# nonebot.init(apscherduler_autostart=True)
# nonebot.init(apscherduler_config={"apscheduler.timezone":"Asia/Shanghai"})
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

# nonebot.load_from_toml("pyproject.toml")
# nonebot.load_plugin('nonebot_plugin_test')
# nonebot.load_plugin('nonebot_plugin_guess')
nonebot.load_plugin('simple1.plugins.menu')
nonebot.load_plugin('simple1.plugins.Qbotdone')
nonebot.load_plugin('simple1.plugins.weather')
nonebot.load_plugin('simple1.plugins.push_sys')
nonebot.load_plugin('simple1.plugins.qbothelp')
nonebot.load_plugin('simple1.plugins.wangyimusic')
# nonebot.load_plugin('simple1.plugins.test1')

# Modify some config / config depends on loaded configs
# config = driver.config
# do something...


if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
