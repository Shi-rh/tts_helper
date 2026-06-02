import edge_tts
import asyncio

async def test_tts():
    text = "你好，欢迎使用视频生成工具"
    voice = "zh-CN-XiaoxiaoNeural"
    communicate=edge_tts.Communicate(text,voice)
    print("正在合成语音")
    async for chunk in communicate.stream():
        if chunk["type"]=="audio":
            print(f"收到音频数据，长度: {len(chunk['data'])} 字节")

asyncio.run(test_tts())