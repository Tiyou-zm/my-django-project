from learning_logs.services import DeepSeekService

# 测试美化后的AI分析功能
ai_service = DeepSeekService()

# 创建一个简单的测试笔记
test_note = """Python编程基础
1. 变量和数据类型
2. 条件语句和循环
3. 函数定义

我觉得很难记语法"""

print("🎨 测试美化后的AI分析功能...")
print("=" * 50)
print("原始笔记:")
print(test_note)
print("=" * 50)

try:
    # 测试默认分析（离线模式）
    analysis = ai_service._get_default_analysis(test_note)
    print("AI分析结果预览:")
    print(analysis[:800] + "...")
    print("\n✅ 默认分析测试成功！")
except Exception as e:
    print(f"❌ 测试失败: {e}")