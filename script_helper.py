import asyncio
from tts_duration_helper import TTSDurationHelper


class ScriptHelper:
    # 国家 -> 语言
    country_to_language = {
        '泰国': '泰语',
        '越南': '越南语',
        '菲律宾': '英语',
        '印尼': '印尼语',
        '新加坡': '中文',
        '马来西亚': '马来语',
        '美国': '英语',
        '英国': '英语',
        '日本': '日语',
        '韩国': '韩语',
    }

    def __init__(self):
        self.tts_helper = TTSDurationHelper()

    async def check_duration_match(self, text, country, target_seconds):

        language = self.country_to_language.get(country, '中文')
        print(f"国家: {country} -> 使用语言: {language}")

        actual_seconds = await self.tts_helper.get_duration(text, language)
        #判断实际时长和分镜时长是否匹配
        if actual_seconds <= target_seconds:
            print(f"匹配！台词需要 {actual_seconds:.2f}秒，分镜有 {target_seconds}秒")
            return {
                'match': True,
                'actual': actual_seconds,
                'target': target_seconds,
                'suggestion': None
            }
        else:
            needed_speed = actual_seconds / target_seconds
            print(f"不匹配！台词需要 {actual_seconds:.2f}秒，分镜只有 {target_seconds}秒")
            print(f"建议将语速调整为 {needed_speed:.2f}倍")

            return {
                'match': False,
                'actual': actual_seconds,
                'target': target_seconds,
                'suggestion': f'建议语速: {needed_speed:.2f}x',
                'suggested_speed': needed_speed
            }



async def main():
    helper = ScriptHelper()
    test_cases = [
        {"text": "这款音箱颜值超高", "country": "中国", "target": 3},
        {"text": "This speaker is amazing", "country": "美国", "target": 2},
    ]

    for case in test_cases:
        print(f"\n--- 测试: {case['text']} ---")
        result = await helper.check_duration_match(
            case['text'],
            case['country'],
            case['target']
        )
        print(f"结果: {result}")


if __name__ == "__main__":
    asyncio.run(main())