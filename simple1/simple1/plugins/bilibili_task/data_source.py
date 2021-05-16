import httpx
import time

user_cookie = """
    _uuid=DB7E6232-C25D-C4A7-FC2B-FD1D1A18B93789065infoc; 
    buvid3=F4CF579B-B138-4942-9F83-2FB8580FC3B8155819infoc; 
    rpdid=|(RYuR)mRmm0J'ulmu~)RllY; 
    PVID=1; 
    CURRENT_FNVAL=80; 
    blackside_state=1; 
    CURRENT_QUALITY=80; 
    fingerprint3=0a9fc5e5aece4ab6e51c584e3d2b496c; 
    fingerprint_s=ec114b0d509c8e8ebf9ae9e54e31cb72; 
    buvid_fp=F4CF579B-B138-4942-9F83-2FB8580FC3B8155819infoc; 
    buvid_fp_plain=F4CF579B-B138-4942-9F83-2FB8580FC3B8155819infoc; 
    fingerprint=7a3c6f7454787b48923916b6a75961da;
    sid=7o7by0jx"""

headers = {
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57',
    'cookie': user_cookie
}


def longin_url():
    """
    登录
    """
    url = 'http://passport.bilibili.com/qrcode/getLoginUrl'
    response = httpx.get(url)
    if response.json()['code'] == 0:
        pass_url = response.json()['data']['url']
        oauthkey = response.json()['data']['oauthKey']
        return (pass_url, oauthkey)


def get_longin_cookie(oauthkey):
    passport_url = 'http://passport.bilibili.com/qrcode/getLoginInfo'
    params = {
        'oauthKey': oauthkey
    }
    while True:
        response = httpx.post(passport_url, params=params)
        if response.json()['data'] in [-1, -2, -4, -5]:
            time.sleep(0.5)
        else:
            global user_cookie
            user_cookie = response.cookies
            break


def search(keyword):
    """
    搜索
    """
    params = {
        'keyword': keyword,
    }
    result = {}
    search_url = 'http://api.bilibili.com/x/web-interface/search/all/v2'
    response = httpx.get(url=search_url, params=params).json()
    if response['code'] == 0:
        result['page'] = response['data'][0]['page']
    return response


def geturl(bvid: str):
    """
    获取链接
    """
    params = {
        'bvid': bvid,
        # 'cid': cid,
        # 'qn': qn,
        # 'fnval': fnval,
    }
    cid = []
    # with httpx.stream('get', 'http://api.bilibili.com/x/player/playurl', params=params) as r:
    #     with open('bilibli.mp4', 'wb') as f:
    #         for data in r.iter_bytes():
    #             f.write(data)
    response = httpx.get('http://api.bilibili.com/x/player/pagelist', params=params).json()
    for data in response['data']:
        cid.append(data['cid'])
    for i in cid:

    return cid

def download():
    """
    下载
    """


# url, key = longin_url()
# print(url)
# get_longin_cookie(key)
# keyword = str(input('输入搜索关键字'))
# print(search(keyword))
print(geturl('BV1Tb411N7VA'))
