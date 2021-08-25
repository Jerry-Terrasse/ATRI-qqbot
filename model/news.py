import asyncio
from aiohttp import ClientSession
import aiohttp
import aiofiles

from engine import atri

news = atri.news

class News:
    enable = news['enable']
    cmd = news['command']
    path = news['path']
    BASE = "http://api.soyiji.com/news_jpg"
    headers = {'Referer': 'safe.soyiji.com'}

    @classmethod
    async def get_url(cls):
        async with aiohttp.ClientSession() as client:
            response = await client.get(cls.BASE)
            response.raise_for_status()
            data = await response.json()
            return data['url']

    @classmethod
    async def get_img(cls):
        url = await cls.get_url()
        async with aiohttp.ClientSession() as client:
            response = await client.get(url,headers=cls.headers)
            response.raise_for_status()
            # print('###', response)
            data = await response.read()
            with open(cls.path, 'wb') as f:
                f.write(data)
            return cls.path

    @classmethod
    async def get_news(cls):
        try:
            img = await cls.get_img() # img_path
            return (True, img)
        except Exception as e:
            return (False, str(e))
