import edge_tts
import asyncio
import io
from pydub import AudioSegment

class TTSDurationHelper:
    def __init__(self):
        self.voice_map = {
            '中文': 'zh-CN-XiaoxiaoNeural',
            '英语': 'en-US-JennyNeural',
            '越南语': 'vi-VN-HoaiMyNeural',
            '泰语': 'th-TH-PremwadeeNeural',
        }
    async def get_duration(self, text, language='中文', speed=1.0):
        voice=self.voice_map.get(language, self.voice_map['中文'])
        if speed == 1.0:
            rate = "+0%"
        elif speed > 1.0:
            rate = f"+{int((speed - 1) * 100)}%"
        else:
            rate = f"-{int((1 - speed) * 100)}%"

        print(f"正在预测: {text} (语言: {language}, 语速: {speed}x)")
        communicate=edge_tts.Communicate(text,voice,rate=rate)
        audio_data=b''
        async for chunk in communicate.stream():
            if chunk["type"]=="audio":
                audio_data+=chunk["data"]

        audio=AudioSegment.from_file(io.BytesIO(audio_data),format="mp3")
        duration_seconds = len(audio) / 1000

        return duration_seconds

async def main():
    helper=TTSDurationHelper()
    duration=await helper.get_duration("好好学习天天向上","中文")
    print(f"中文台词需要: {duration:.2f}秒\n")

if __name__ == "__main__":
        asyncio.run(main())