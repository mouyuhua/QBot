# -*- coding = utf-8 -*-
import os
import requests
import json
from base64 import b64encode
from Crypto.Cipher import AES


class Encrypt:

    def __init__(self, text):
        self.data = {
            'encSecKey': '01ec48cb405730aa77f993a988cc1f5bc1938511d75f49eddc581f2fe2aaf18988853200564b2d4b1312cf6e0bb344425addce5a4c81b38b89a5973900946bd100b0f1865d22d2a8e5dd8be208eb5d6eb2f71309a165daeffe95355e1e44edd65bdf28088fe4f5e835a7d9f7569fc2530f9d17c00b51cfafbe421eb462247ea3'
        }

        self.text = text
        self.key = '0CoJUm6Qyw8W8jud'

    def get_form_data(self):
        """生成表单参数"""

        # 随机秘钥参数，可以用固定值
        i = "4JknCzx6uEXUwxpU"

        # 两次加密
        first_encrypt = self.AES_encpyt(self.text, self.key)
        self.data['params'] = self.AES_encpyt(first_encrypt, i)

        return self.data

    def AES_encpyt(self, text, key):
        """AES加密"""

        # AES加密明文必须为16的整数倍
        padding = 16 - len(text.encode()) % 16
        text += padding * chr(padding)

        aes = AES.new(key.encode(), AES.MODE_CBC, b'0102030405060708')
        enctext = aes.encrypt(text.encode())

        return b64encode(enctext).decode('utf-8')


class SearchMusic:

    def __init__(self, song_name):
        self.url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        self.headers = {
            'authority': 'music.163.com',
            'method': 'POST',
            'path': '/weapi/song/enhance/player/url/v1?csrf_token=',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '434',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': '__root_domain_v=.163.com; _qddaz=QD.28yaab.3jymc6.kf0ihnaf; _ntes_nnid=e7c5f90265b4d5a5bcb511efebf7a890,1600596980395; _ntes_nuid=e7c5f90265b4d5a5bcb511efebf7a890; _iuqxldmzr_=32; WM_TID=OlHvFOuIVclAQFQUAEJvJZyLuh3MwtGb; NMTID=00ODCot1Uq8CvcXIUIMmKBlPfRiyfoAAAF3NHwibw; WM_NI=%2BWiHzgkFWg%2BON3YYI0rQzlpsOW8x4BPGt%2FWRNpkD3r2Utv8U1gx6RZgvmmJQ0IpSBgdk1GvY9uIQW6BfIN7lVoHo8z1BIoa%2FdLUgKwpx6twUKJtgDlexKOu7LqWGuYApZzg%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb9c844a3b1aba3b24489eb8eb6d15b929a9baaaa5cace70087b64e8ab18299d02af0fea7c3b92ae989a7a9f96da99a9988aa458eed97bacc3cb28fb68df3798d89f899b74a9499bcd0d65a8eb0a5a5b27af28bbc97bb5ff3b9b8d7d152a5aaa38ec95bf497c0b4c16da8b5ffa8f553fbab87b2d63e82ba87afb66896b18890bb72f39e8790e425a8949b88ca7db4a8fa95f65f8996bc88c768a7a885b0f83d90af99a8f85383b0969be637e2a3; hb_MA-9F44-2FC2BD04228F_source=www.baidu.com; JSESSIONID-WYYY=bERBG86BVbD29X%5C35acjg8ndIoGYPEZvQ8fc0t7WUnMu3KTujvG1zqfSMIG%2By4%2FZRz9hC%2FwBN0Mf%2B%2B1RJBK2TeR96X7l%2BmS%2FHhuuqBwl7yxwe4jQ%5ChzFoFgKylb3ZdOnw6%2FqsqaUYUrJ12EVVy0m66JVlQez0T5ijmgZuOsk0KcMnUe4%3A1611553513123; WEVNSM=1.0.0; WNMCID=kctjbv.1611551714155.01.0',
            'origin': 'https://music.163.com',
            'pragma': 'no-cache',
            'referer': 'https://music.163.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
        self.text = str({
            "hlpretag": '<span class="s-fc7">',
            "hlposttag": "</span>",
            "s": song_name,
            "type": "1",
            "offset": "0",
            "total": "true",
            "limit": "30",
            "csrf_token": ""
        })

    def search(self):
        """搜索音乐，返回音乐列表"""

        data = Encrypt(self.text).get_form_data()
        try:
            res = requests.post(self.url, headers=self.headers, data=data).json()
        except:
            return 'ERROR'

        songlist = []
        songs = res['result']['songs']

        for i in songs:
            # id、歌名、歌手、封面
            item = {
                'song_id': i['id'],
                'song_name': i['name'],
                'singer': i['ar'][0]['name'],
                'song_pic_url': i['al']['picUrl']
            }
            songlist.append(item)

        return songlist


class NeteaseCloudMusic:

    def __init__(self, song_id):

        self.url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='

        self.headers = {'authority': 'music.163.com',
                        'method': 'POST',
                        'path': '/weapi/song/enhance/player/url/v1?csrf_token=',
                        'scheme': 'https',
                        'accept': '*/*',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'zh-CN,zh;q=0.9',
                        'cache-control': 'no-cache',
                        'content-length': '434',
                        'content-type': 'application/x-www-form-urlencoded',
                        'cookie': '__root_domain_v=.163.com; _qddaz=QD.28yaab.3jymc6.kf0ihnaf; _ntes_nnid=e7c5f90265b4d5a5bcb511efebf7a890,1600596980395; _ntes_nuid=e7c5f90265b4d5a5bcb511efebf7a890; _iuqxldmzr_=32; WM_TID=OlHvFOuIVclAQFQUAEJvJZyLuh3MwtGb; NMTID=00ODCot1Uq8CvcXIUIMmKBlPfRiyfoAAAF3NHwibw; WM_NI=%2BWiHzgkFWg%2BON3YYI0rQzlpsOW8x4BPGt%2FWRNpkD3r2Utv8U1gx6RZgvmmJQ0IpSBgdk1GvY9uIQW6BfIN7lVoHo8z1BIoa%2FdLUgKwpx6twUKJtgDlexKOu7LqWGuYApZzg%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb9c844a3b1aba3b24489eb8eb6d15b929a9baaaa5cace70087b64e8ab18299d02af0fea7c3b92ae989a7a9f96da99a9988aa458eed97bacc3cb28fb68df3798d89f899b74a9499bcd0d65a8eb0a5a5b27af28bbc97bb5ff3b9b8d7d152a5aaa38ec95bf497c0b4c16da8b5ffa8f553fbab87b2d63e82ba87afb66896b18890bb72f39e8790e425a8949b88ca7db4a8fa95f65f8996bc88c768a7a885b0f83d90af99a8f85383b0969be637e2a3; hb_MA-9F44-2FC2BD04228F_source=www.baidu.com; JSESSIONID-WYYY=bERBG86BVbD29X%5C35acjg8ndIoGYPEZvQ8fc0t7WUnMu3KTujvG1zqfSMIG%2By4%2FZRz9hC%2FwBN0Mf%2B%2B1RJBK2TeR96X7l%2BmS%2FHhuuqBwl7yxwe4jQ%5ChzFoFgKylb3ZdOnw6%2FqsqaUYUrJ12EVVy0m66JVlQez0T5ijmgZuOsk0KcMnUe4%3A1611553513123; WEVNSM=1.0.0; WNMCID=kctjbv.1611551714155.01.0',
                        'origin': 'https://music.163.com',
                        'pragma': 'no-cache',
                        'referer': 'https://music.163.com/',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

        self.text = str({"ids": f"[{str(song_id)}]",
                         "level": "standard",
                         "encodeType": "aac",
                         "csrf_token": ""})

    def music(self, song_name, singer):
        """获取音乐的url"""

        data = Encrypt(self.text).get_form_data()
        try:
            res = requests.post(self.url, headers=self.headers, data=data).json()
        except:
            return 'ERROR'

        song_url = res['data'][0]['url']
        if song_url == None:
            return 'v'
        # self.save(self.download(song_url))
        # self.download(song_url, song_name)

    # def download(self, url, song_name):
        """下载音乐"""

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
        res = requests.get(song_url, headers=headers)
        content = res.content

        # 当前文件目录
        path = os.path.dirname(__file__)
        path = os.path.abspath(path)
        # 检查'data'目录是否存在，不存在则创建目录
        if not os.path.exists(path + '\\data'):
            os.mkdir(path + '\\data')
        # 音乐保存路径
        music_path = path + '\\data' + f'\\{song_name}-{singer}.m4a'
        # 保存
        if not os.path.exists(music_path):
            with open(music_path, 'wb') as f:
                f.write(content)
            return music_path, True
        else:
            return music_path, True


# search_song_name = '让风告诉你'
# songs = SearchMusic(search_song_name).search()
# for i in songs:
#     if 'song_name' in i:
#         print(i['song_name'])
# index = int(input())
# url = NeteaseCloudMusic(songs[index]['song_id']).music()
# NeteaseCloudMusic(songs[index]['song_id']).download(url, songs[index]['song_name'])
