'''
avatar for class Analyze
'''
import os
import httpx
import asyncio
from io import BytesIO
from dotenv import load_dotenv


class Avatar:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('HEYGEN_API_KEY')
        self.url_generate = 'https://api.heygen.com/v2/video/generate'
        self.url_status = 'https://api.heygen.com/v2/video/status'
        self.headers = {
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }

    async def create_video(self, text: str) -> BytesIO:
        '''Генерируем видео по тексту и возвращаем BytesIO для Telegram'''
        # шаг 1: generate
        async with httpx.AsyncClient() as client:
            payload = {
                'video_inputs': [
                    {
                        'character': {
                            'type': 'avatar', 
                             'avatar_id': 'dd300185b5e7441585ef8c23b7fa5f3d', 
                             'avatar_style': 'normal'
                             },
                        'voice': {
                            'type': 'text', 
                            'input_text': text, 
                            'voice_id': '084760b4922a44599575c770070ec2d7'},
                        'background': {
                            'type': 'color', 
                            'value': '#FFFFFF'}
                    }
                ],
                'dimension': {
                    'width': 1280, 
                    'height': 720
                    }
            }
            resp = await client.post(self.url_generate, headers=self.headers, json=payload)
            data = resp.json()
            video_id = data.get('data', {}).get('video_id')

        # шаг 2: опрашиваем статус
        async with httpx.AsyncClient() as client:
            while True:
                r = await client.get(f'{self.url_status}/{video_id}', headers=self.headers)
                d = r.json()
                status = d.get('data', {}).get('status')
                if status == 'completed':
                    video_url = d['data']['video_url']
                    break
                elif status == 'failed':
                    raise Exception('Video generation failed')
                await asyncio.sleep(5)

        # шаг 3: скачиваем видео в BytesIO
        async with httpx.AsyncClient() as client:
            r = await client.get(video_url)
            video_file = BytesIO(r.content)
            video_file.name = f'video_{video_id}.mp4'

        return video_file

