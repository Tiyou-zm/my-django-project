import requests
import json

# 测试百度搜索API
search_url = 'https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su'

params = {
    'wd': 'Python编程学习方法',
    'json': 1
}

try:
    response = requests.get(search_url, params=params, timeout=15)
    print(f'状态码: {response.status_code}')
    if response.status_code == 200:
        content = response.text
        print('响应格式检查:')
        print(f'以 window.baidu.sug( 开头: {content.startswith("window.baidu.sug(")}')
        print(f'以 ); 结尾: {content.endswith(");")}')
        print()

        # 解析JSONP响应
        if content.startswith('window.baidu.sug(') and content.endswith(');'):
            json_str = content[18:-2]  # 移除 'window.baidu.sug(' 和 ');'
            print('提取的JSON字符串:')
            print(json_str[:200] + '...')
            print()

            result = json.loads(json_str)
            print('解析成功!')
            suggestions = result.get('g', [])
            print(f'建议数量: {len(suggestions)}')
            for i, item in enumerate(suggestions[:3], 1):
                print(f'{i}. {item.get("q", "无内容")}')
        else:
            print('响应格式不正确')
    else:
        print(f'搜索失败: {response.text}')
except Exception as e:
    print(f'错误: {e}')