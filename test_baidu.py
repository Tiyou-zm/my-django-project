#!/usr/bin/env python
# 测试百度搜索API
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from learning_logs.services import BaiduSearchService

def test_baidu_search():
    search_service = BaiduSearchService()
    results = search_service.search("Python编程学习方法", num_results=3)

    print("🔍 百度搜索测试结果：")
    print(f"找到 {len(results)} 个结果")

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   摘要: {result['snippet'][:100]}...")

if __name__ == "__main__":
    test_baidu_search()