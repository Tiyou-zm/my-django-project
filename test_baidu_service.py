from learning_logs.services import BaiduSearchService

search_service = BaiduSearchService()
results = search_service.search('Python编程学习方法', num_results=3)

print('🔍 百度搜索服务测试结果：')
print(f'找到 {len(results)} 个结果')

for i, result in enumerate(results, 1):
    print(f'\n{i}. {result["title"]}')
    print(f'   URL: {result["url"]}')
    print(f'   摘要: {result["snippet"]}')