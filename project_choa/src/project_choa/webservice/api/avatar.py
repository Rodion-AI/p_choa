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
        """
        Генерируем видео по тексту и возвращаем BytesIO для Telegram
        """
        # Шаг 1: generate
        async with httpx.AsyncClient() as client:
            payload = {
                'video_inputs': [
                    {
                        'character': {
                            'type': 'talking_photo', 
                            'talking_photo_id': 'a6f8435e374a46fb99904b0a7a0e0a46'
                        },
                        'voice': {
                            'type': 'text',
                            'input_text': text,
                            'voice_id': '1156e00bc07f47cd94facef758b51f25'
                        },
                        'background': {
                            'type': 'color',
                            'value': '#FFFFFF'
                        }
                    }
                ],
                'dimension': {
                    'width': 720,
                    'height': 1280
                }
            }

            resp = await client.post(self.url_generate, headers=self.headers, json=payload)
            if resp.status_code != 200:
                raise Exception(f"HeyGen API error {resp.status_code}: {resp.text}")

            try:
                data = resp.json()
            except Exception:
                raise Exception(f"Invalid JSON response: {resp.text}")

            video_id = data.get('data', {}).get('video_id')
            if not video_id:
                raise Exception(f"Video ID not found in response: {data}")

        # Шаг 2: опрашиваем статус
        max_attempts = 30  # до 20 минут (120*10 секунд)
        sleep_seconds = 60

        async with httpx.AsyncClient() as client:
            for attempt in range(max_attempts):
                r = await client.get(f'{self.url_status}/{video_id}', headers=self.headers)
                
                if r.status_code == 404:
                    print(f"[{attempt+1}] Video ID не найден, пробуем снова...")
                elif r.status_code != 200:
                    print(f"[{attempt+1}] Ошибка API: {r.status_code}, {r.text}")
                else:
                    try:
                        d = r.json()
                        status = d.get('data', {}).get('status')
                        if status == 'completed':
                            video_url = d['data']['video_url']
                            print(f"Видео готово! URL: {video_url}")
                            break
                        elif status == 'failed':
                            raise Exception('Video generation failed')
                        else:
                            print(f"[{attempt+1}] Статус видео: {status}")
                    except Exception as e:
                        print(f"[{attempt+1}] Ошибка при разборе JSON: {e}")

                await asyncio.sleep(sleep_seconds)
            else:
                raise Exception("Video was not generated in time")

        # Шаг 3: скачиваем видео в BytesIO
        async with httpx.AsyncClient() as client:
            r = await client.get(video_url)
            video_file = BytesIO(r.content)
            video_file.name = f'video_{video_id}.mp4'

        return video_file


