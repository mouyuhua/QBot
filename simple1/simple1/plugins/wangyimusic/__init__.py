# -*- coding = utf-8 -*-
# -*- v 0.0.1 -*-
import os
from nonebot import plugin
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import utils
from .data_source import SearchMusic, NeteaseCloudMusic

music_listen = plugin.on_command('music', rule=to_me(), priority=7)


@music_listen.handle()
async def deal_event(bot: Bot, event: Event, state: T_State):
    """
    说明
    """
    cmd_words = ['song_name', 'index']
    cmd_flag = ['song_name_flag', 'index_flag']
    state['song_name_flag'] = False
    state['index_flag'] = False
    des = event.get_event_description()
    des = des.split(' ')[3].split('@')
    args = str(event.get_message()).strip()
    if len(des) == 1:
        state['type'] = 'friend'
        state['user_id'] = int(des[0])
        # await music_listen.finish('该命令不支持私聊，请通过群聊进行')
    else:
        des = des[1].split(':')[1].replace(']', '')
        state['type'] = 'group'
        state['group_id'] = int(des)
    if args:
        args = args.split('#')
        args.remove('')
        for i in range(len(args)):
            state[cmd_words[i]] = args[i]
            state[cmd_flag[i]] = True


@music_listen.got('song_name', prompt='请输入搜索歌曲的相关内容')
async def send_song_information(bot: Bot, state: T_State):
    """
    说明
    """
    song_list_information = lambda index, song_name, singer: f'''{index}:{song_name}--{singer}\n'''
    state['song_list'] = SearchMusic(state['song_name']).search()
    i = 0
    list_put = ''
    if state['song_list'] == 'ERROR':
        await music_listen.finish('哎呀，内容被外星人拿走了，再重新试试吧')
    for song in state['song_list']:
        list_put += song_list_information(i, song['song_name'], song['singer'])
        i += 1
    if not state['index_flag']:
        await music_listen.send(list_put)


@music_listen.got('index', prompt='请发送对应歌曲的序号来获取对应歌曲链接')
async def send_song(bot: Bot, event: Event, state: T_State):
    """
    说明
    """
    a = state['index'].split('-')
    song_id = state['song_list'][int(a[0])]['song_id']
    singer = state['song_list'][int(a[0])]['singer']
    if len(a) == 1:
        share = f'[CQ:music,type=163,id={song_id}]'
        if state['type'] == 'group':
            await bot.send_msg(group_id=state['group_id'], message=share)
        else:
            await bot.send_msg(user_id=state['user_id'], message=share)
        await music_listen.finish()
    else:
        if state['type'] == 'friend':
            await music_listen.finish(f'{a[1]}指令暂不支持私聊，请通过群聊进行')
        else:
            if a[1] != 'f':
                await music_listen.finish(f'命令符{a[1]}有误，请重新输入，如需帮助请使用命令/help music')
            else:
                folder = 'music'
                song_name = state['song_list'][int(a[0])]['song_name']
                file_name = f'{song_name}-{singer}.m4a'
                # await music_listen.send(music_path)
                file_information = await bot.get_group_root_files(group_id=state['group_id'])
                folder_id = folder_in_group(file_information['folders'], folder)
                if folder_id == None:
                    await music_listen.send(f'群文件中不存在”{folder}“文件夹，请尽快创建该文件来保证文件秩序')
                    if file_in_group(file_information['files'], file_name):
                        await music_listen.finish('该歌曲已经在群文件了，快去找找吧')
                # await music_listen.send(str(flag))
                else:
                    group_files = await bot.get_group_files_by_folder(group_id=state['group_id'], folder_id=folder_id)
                    # await music_listen.send(str(group_files))
                    if file_in_group(group_files['files'], file_name):
                        await music_listen.finish('该歌曲已经在群文件的music文件夹下了，快去找找吧')
                await music_listen.send('歌曲下载中，请稍等...')
                music_path = NeteaseCloudMusic(song_id).music(song_name, singer)[0]
                # await music_listen.send(music_path)
                if music_path == 'ERROR':
                    await music_listen.finish('歌曲好像被外星人抢走了＞︿＜')
                elif music_path == 'v':
                    await music_listen.finish('这首歌需要VIP呢，麻烦自己去客户端下载吧，啾咪~')
                elif music_path[1]:
                    await bot.upload_group_file(group_id=state['group_id'], file=f'{music_path}',name=file_name, folder=folder_id)
                    await music_listen.finish(f'文件“{file_name}“上传中，请稍后在群文件中查看')


def folder_in_group(group_folders, folder):
    if group_folders == None:
        return None
    for i in group_folders:
        if i['folder_name'] == folder:
            return i['folder_id']
        else:
            return None


def file_in_group(group_files, file_name):
    if group_files == None:
        return False
    for i in group_files:
        if i['file_name'] == file_name:
            return True
        else:
            return False
