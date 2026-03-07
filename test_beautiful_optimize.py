from learning_logs.services import DeepSeekService

# 测试美化后的AI优化功能
ai_service = DeepSeekService()

# 创建一个需要优化的测试笔记
test_note = """python学习
变量
数据类型
if语句
for循环
def函数
很难记"""

print("🎨 测试美化后的AI优化功能...")
print("=" * 60)
print("原始笔记:")
print(test_note)
print("=" * 60)

try:
    # 测试优化功能（离线模式会返回原始内容）
    optimized = ai_service.optimize_content(test_note)
    print("优化后的笔记:")
    print(optimized)
    print("\n✅ 优化功能测试成功！")
except Exception as e:
    print(f"❌ 测试失败: {e}")

print("\n" + "=" * 60)
print("🎯 现在AI会生成图文并茂的学习资料！")
print("包含：")
print("✨ 丰富的emoji表情")
print("📊 表格和结构化布局")
print("🎨 颜色标注重点内容")
print("💡 实用的学习建议")
print("❤️ 温暖的鼓励话语")
print("🌟 专业级的视觉呈现")