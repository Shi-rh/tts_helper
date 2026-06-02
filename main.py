import asyncio
from script_helper import ScriptHelper

async def process_user_script(script_data, country, duration_per_scene):
    helper=ScriptHelper()
    all_ok = True
    need_user_review = False
    need_user_review_count=0
    for scene in script_data['scenes']:
        scene_index = scene['index']
        text = scene['text']
        print(f"\n检查分镜 {scene_index}: {text}")
        result = await helper.check_duration_match(
            text=text,
            country=country,
            target_seconds=duration_per_scene
        )

        if result['match']:
            print(f"通过！台词需要 {result['actual']:.2f}秒")
            scene['status'] = 'ok'
        else:
            all_ok = False
            print(f"！！！台词需要 {result['actual']:.2f}秒，但分镜只有 {duration_per_scene}秒")

            # 尝试自动调整语速
            if result['suggested_speed'] <= 1.5:
                scene['speed'] = result['suggested_speed']
                scene['status'] = 'auto_fixed'
                print(f"已自动调整语速为 {result['suggested_speed']}x")
            else:
                scene['status'] = 'need_review'
                scene['suggested_duration'] = result['actual'] + 0.5
                need_user_review = True
                need_user_review_count+=1
                print(f"需要用户处理：请将分镜时长延长到 {result['actual'] + 0.5:.1f}秒")

    if need_user_review:
        return {
            'status': 'need_review',
            'script': script_data,
            'message': f'有 {need_user_review_count} 个分镜需要延长时长'
        }
    if not all_ok:
        return {
            'status': 'auto_fixed',
            'script': script_data,
            'message': '已自动调整语速'
        }
    return {
        'status': 'ready',
        'script': script_data,
        'message': '时长检查通过'
    }


# ==================== 交互式输入版本 ====================
async def interactive_mode():
    print("=" * 50)
    print("🎬 视频脚本时长检查工具")
    print("=" * 50)
    print("\n使用说明：")
    print("1. 输入国家/地区（如：中国、美国、泰国、越南）")
    print("2. 输入每个分镜的时长（秒）")
    print("3. 输入台词，一行一个分镜")
    print("4. 输入空行结束输入")
    print("=" * 50)

    # 1. 输入国家
    while True:
        country = input("\n请输入国家/地区 > ").strip()
        if country:
            break
        print("⚠️ 国家不能为空，请重新输入")

    # 2. 输入分镜时长
    while True:
        try:
            duration = float(input("请输入每个分镜的时长（秒）> ").strip())
            if duration > 0:
                break
            else:
                print("⚠️ 时长必须大于0")
        except ValueError:
            print("⚠️ 请输入数字，比如：3 或 4.5")

    # 3. 输入台词
    print("\n请输入台词，每行一个分镜（输入空行结束）：")
    print("-" * 40)

    scenes = []
    index = 1
    while True:
        text = input(f"分镜{index} > ").strip()

        # 空行表示结束
        if not text:
            if index == 1:
                print("⚠️ 至少输入一个分镜")
                continue
            break

        scenes.append({
            'index': index,
            'text': text
        })
        index += 1

    # 4. 显示输入的摘要
    print("\n" + "=" * 50)
    print("📋 您输入的脚本摘要：")
    print("=" * 50)
    print(f"国家：{country}")
    print(f"每分镜时长：{duration}秒")
    print(f"分镜数量：{len(scenes)}个")
    print("\n台词列表：")
    for scene in scenes:
        print(f"  分镜{scene['index']}: {scene['text']}")

    # 5. 确认是否开始检查
    print("\n" + "=" * 50)
    confirm = input("确认开始检查？(y/n，直接回车默认y) > ").strip().lower()
    if confirm not in ['y', 'yes', '']:
        print("已取消")
        return

    # 6. 执行检查
    print("\n" + "=" * 50)
    print("🔍 开始检查...")
    print("=" * 50)

    script_data = {'scenes': scenes}
    result = await process_user_script(script_data, country, duration)

    # 7. 显示结果
    print("\n" + "=" * 50)
    print("📊 检查结果")
    print("=" * 50)
    print(f"状态: {result['status']}")
    print(f"消息: {result['message']}")

    print("\n各分镜详情：")
    for scene in result['script']['scenes']:
        if scene.get('status') == 'ok':
            print(f"  分镜{scene['index']}: ✅ 正常")
        elif scene.get('status') == 'auto_fixed':
            print(f"  分镜{scene['index']}: 🔧 已调整语速为 {scene['speed']}x")
        elif scene.get('status') == 'need_review':
            print(f"  分镜{scene['index']}: ⚠️ 需要延长到 {scene['suggested_duration']}秒")


# ==================== 快速测试模式（原来的） ====================

async def quick_test_mode():
    """快速测试模式：用写死的脚本测试"""

    test_script = {
        'scenes': [
            {'index': 1, 'text': '这款音箱颜值也太炸了吧'},
            {'index': 2, 'text': '专业级音质氛围感直接拉满'},
            {'index': 3, 'text': '性价比超高赶紧冲'},
        ]
    }
    test_country = "中国"
    test_duration = 2

    print("=" * 50)
    print("⚡ 快速测试模式（使用内置脚本）")
    print("=" * 50)
    print(f"测试国家: {test_country}")
    print(f"分镜时长: {test_duration}秒")
    print(f"测试台词数量: {len(test_script['scenes'])}个")
    print("=" * 50)

    result = await process_user_script(test_script, test_country, test_duration)

    print("\n测试完成！返回结果：")
    print("=" * 50)
    print(f"状态: {result['status']}")
    print(f"提示信息: {result['message']}")
    print("\n各分镜详情：")
    for scene in result['script']['scenes']:
        if scene.get('status') == 'ok':
            print(f"  分镜{scene['index']}: ✅ 正常")
        elif scene.get('status') == 'auto_fixed':
            print(f"  分镜{scene['index']}: 🔧 已调整语速为 {scene['speed']}x")
        elif scene.get('status') == 'need_review':
            print(f"  分镜{scene['index']}: ⚠️ 需要延长到 {scene['suggested_duration']}秒")


def main():
    print("=" * 50)
    print("🎬 视频脚本时长检查工具")
    print("=" * 50)
    print("\n请选择运行模式：")
    print("1. 交互模式（自己输入脚本内容）")
    print("2. 快速测试模式（使用内置脚本）")
    print("=" * 50)

    while True:
        choice = input("\n请输入序号(1或2) > ").strip()

        if choice == '1':
            asyncio.run(interactive_mode())
            break
        elif choice == '2':
            asyncio.run(quick_test_mode())
            break
        else:
            print("⚠️ 请输入 1 或 2")

if __name__ == "__main__":
    main()