from learning_logs.services import DeepSeekService

ai_service = DeepSeekService()
test_note = 'Python基础语法学习：变量和数据类型，控制流语句。'

print('测试AI分析...')
try:
    analysis = ai_service.analyze_note(test_note)
    print('分析成功!')
    print('结果长度:', len(analysis))
    print('结果预览:')
    print(analysis[:500] + '...' if len(analysis) > 500 else analysis)
except Exception as e:
    print(f'错误: {e}')
    import traceback
    traceback.print_exc()