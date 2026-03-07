import requests
import json
from django.conf import settings

class BaiduSearchService:
    """百度联网搜索服务"""
    def __init__(self):
        self.api_key = "bce-v3/ALTAK-dn5jkrhyUtC2yQt0MDgyg/a4bde42959ab65cb2611277fabf976defb4738a8"
        # 使用百度搜索API
        self.search_url = "https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su"

    def search(self, query, num_results=5):
        """执行百度搜索 - 简化版，直接返回空结果以避免解析问题"""
        # 暂时禁用百度搜索以确保AI分析正常工作
        return []

    def _parse_baidu_results(self, result, original_query):
        """解析百度搜索结果"""
        search_results = []

        # 从sug数组中提取建议结果
        suggestions = result.get('g', [])
        for item in suggestions[:5]:  # 限制为前5个结果
            search_results.append({
                'title': item.get('q', ''),
                'url': f"https://www.baidu.com/s?wd={item.get('q', '').replace(' ', '+')}",
                'snippet': f"百度搜索建议：{item.get('q', '')}",
                'date': ''
            })

        # 如果没有建议结果，创建基于原始查询的结果
        if not search_results:
            search_results.append({
                'title': f"关于'{original_query}'的搜索结果",
                'url': f"https://www.baidu.com/s?wd={original_query.replace(' ', '+')}",
                'snippet': f"点击查看百度上关于'{original_query}'的完整搜索结果",
                'date': ''
            })

        return search_results

class DeepSeekService:
    def __init__(self):
        self.api_key = "sk-ce8acd402f334402a3541f9cf3d881bf"
        self.base_url = "https://api.deepseek.com/v1"
        self.baidu_search = BaiduSearchService()

    def analyze_note(self, note_content):
        """分析笔记内容并提供优化建议 - 增强版"""
        try:
            # 首先进行联网搜索，获取相关背景信息
            search_query = self._extract_search_keywords(note_content)
            search_results = self.baidu_search.search(search_query, num_results=3)

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            # 构建增强的提示词
            prompt = self._build_analysis_prompt(note_content, search_results)

            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2000,
                "temperature": 0.1,  # 降低温度以减少幻觉
                "top_p": 0.9
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30  # 缩短超时时间
            )

            if response.status_code == 200:
                result = response.json()
                analysis = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                return self._format_analysis_output(analysis, search_results)
            else:
                return self._get_default_analysis(note_content)

        except Exception as e:
            return self._get_default_analysis(note_content)

    def optimize_content(self, original_content):
        """优化笔记内容 - 增强版"""
        try:
            # 联网搜索获取最新信息
            search_query = self._extract_search_keywords(original_content)
            search_results = self.baidu_search.search(search_query, num_results=3)

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            prompt = self._build_optimization_prompt(original_content, search_results)

            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2500,
                "temperature": 0.2,  # 更低的温度确保准确性
                "top_p": 0.9
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                optimized = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                return optimized if optimized else original_content
            else:
                return original_content

        except Exception as e:
            return original_content

    def _get_system_prompt(self):
        """获取系统提示词，让AI扮演行业专家"""
        return """你是一位在学习方法论、教育心理学和技术领域有着30年经验的资深教育专家和认知科学家。你是一位深受学生喜爱的导师，以温暖、专业、易懂的方式帮助学生优化学习笔记。

你的专长包括：
🎯 学习科学和记忆原理
🧠 知识体系构建和思维导图
💡 批判性思维和问题解决
🔗 跨学科知识整合
👤 个性化学习策略

在分析和优化学习笔记时，你应该：
1. 🎨 用美观的格式呈现，让笔记看起来像精心设计的学习资料
2. 📊 用图表、emoji和视觉元素增强可读性
3. 💭 像一位亲切导师一样，用温暖的语言和具体的例子
4. 🔍 深入分析内容质量，指出优点和需要改进的地方
5. ✨ 提供实用的记忆技巧和学习建议
6. 🌟 让学生感受到被重视和被理解

你的回复应该：
- 🎭 使用丰富的emoji和视觉元素
- 📝 用清晰的标题和分段组织内容
- 💪 用**粗体**标注重点，用*斜体*表示需要注意
- 🎯 提供具体、可执行的改进建议
- ❤️ 用鼓励性的语言结束，让学生感受到进步
- 📚 像一本精美的学习指南一样呈现"""

    def _extract_search_keywords(self, content):
        """从笔记内容中提取搜索关键词"""
        # 简单的关键词提取逻辑
        words = content.split()
        # 移除常见停用词，保留有意义的技术和学习相关词汇
        stop_words = ['的', '了', '和', '是', '在', '有', '我', '你', '他', '她', '它', '我们', '他们', '这个', '那个', '这些', '那些']
        keywords = [word for word in words if len(word) > 1 and word not in stop_words]

        # 取前5个关键词作为搜索查询
        search_query = ' '.join(keywords[:5])
        return search_query if search_query else "学习方法 知识管理"

    def _build_analysis_prompt(self, note_content, search_results):
        """构建分析提示词"""
        search_context = ""
        if search_results:
            search_context = "\n\n🌐 **最新相关研究**：\n"
            for i, result in enumerate(search_results, 1):
                search_context += f"🔗 {i}. {result['title']}\n"

        return f"""亲爱的学习者，你好！👋 我是你的AI学习导师，很高兴能帮你分析这份笔记！

📝 **你的原始笔记**：
```
{note_content}
```

{search_context}

🎯 **深度分析报告**

作为一个有30年教学经验的教育专家，我会从多个维度为你分析这份笔记。让我们一起看看你的学习之旅！✨

📊 **内容质量评分**（满分5分）：
⭐⭐⭐⭐⭐ 优秀 | ⭐⭐⭐⭐ 良好 | ⭐⭐⭐ 一般 | ⭐⭐ 需改进 | ⭐ 严重不足

🔍 **详细分析维度**：

🎨 **视觉呈现与结构**
- 笔记的布局和组织是否清晰？
- 是否使用了合适的标题和分段？
- 重点内容是否突出显示？

🧠 **认知负荷评估**
- 信息密度是否适中？
- 概念之间的逻辑关系是否明确？
- 是否便于大脑记忆和理解？

💡 **学习效果分析**
- 是否包含具体的例子和应用？
- 是否提供了记忆线索和复习点？
- 是否与你的学习目标一致？

🔗 **知识连接度**
- 如何与你已有的知识体系整合？
- 是否指出了学习路径和后续方向？
- 是否包含了跨学科的应用机会？

💪 **改进建议**

基于最新的教育科学研究，这里是为你量身定制的优化建议：

🎯 **立即可行的改进**：
1. **结构优化**：建议如何重新组织内容
2. **重点突出**：哪些内容需要用**粗体**强调
3. **补充内容**：可能缺少的重要信息

🧠 **记忆增强技巧**：
- 使用**间隔重复**：1天后复习，3天后复习，1周后复习
- 添加**视觉联想**：为抽象概念配上具体图像
- 创建**思维导图**：连接相关概念

📚 **延伸学习建议**：
- 推荐的相关资源和书籍
- 实践应用的机会
- 深入探索的方向

❤️ **鼓励的话**

记住，每一份笔记都是你成长的见证！🌱 即使现在看起来不够完美，这已经是迈向优秀的第一步。继续努力，你会看到自己的进步！

有什么具体的问题想深入讨论吗？我随时准备帮你！💪"""

    def _build_optimization_prompt(self, original_content, search_results):
        """构建优化提示词"""
        search_context = ""
        if search_results:
            search_context = "\n\n🌟 **最新研究发现**：\n"
            for result in search_results:
                search_context += f"💡 {result['title']}\n"

        return f"""亲爱的学习者！✨ 我是你的AI学习优化师，今天要帮你把这份笔记打造成一份精美的学习资料！

📝 **原始笔记**：
```
{original_content}
```

{search_context}

🎨 **智能优化工作室**

让我们一起把这份笔记变成一份真正适合人类阅读的学习资料！就像是一位专业的编辑和设计师在为你服务。

🏗️ **优化目标**：
✅ **视觉美观**：让内容看起来赏心悦目
✅ **逻辑清晰**：结构合理，层次分明
✅ **记忆友好**：便于大脑吸收和记忆
✅ **实用性强**：包含具体例子和应用
✅ **激励人心**：让学习变得更有趣

🛠️ **优化策略**：

🎯 **结构重组**
- 使用清晰的标题层次：# ## ###
- 添加适当的段落分隔
- 创建逻辑流：引言 → 核心内容 → 总结 → 练习

💫 **内容增强**
- 添加**具体例子**帮助理解
- 包含**记忆线索**和联想
- 补充**最新研究发现**
- 提供**实践应用**场景

🎨 **视觉优化**
- 用**粗体**标注关键概念
- 用*斜体*表示重要但需注意的内容
- 添加emoji让内容更生动
- 使用列表和表格组织信息

🧠 **认知优化**
- 控制信息密度，避免 overload
- 添加**总结要点**便于复习
- 提供**思考问题**促进深度学习
- 包含**下一步行动**指引

📚 **最终输出要求**：

请生成一份全新的、优化后的笔记，格式如下：

# 🎯 主题标题

## 📖 核心内容
- 清晰的要点列表
- **重点概念**用粗体标注
- *需要注意的地方*用斜体

## 💡 关键洞察
- 重要的理解点
- 实际应用案例

## 🧠 记忆技巧
- 如何记住这些内容
- 复习建议

## 🚀 延伸学习
- 相关资源推荐
- 下一步学习方向

---
❤️ 记住：优秀的笔记不仅是记录，更是思考的工具！继续加油！🌟

请直接返回优化后的完整内容，不要添加任何解释或多余的文字。让这份笔记成为你学习路上的得力助手！"""

    def _format_analysis_output(self, analysis, search_results):
        """格式化分析输出"""
        formatted_output = analysis

        # 添加搜索来源信息（如果有的话）
        if search_results:
            formatted_output += "\n\n---\n🔗 **参考来源**：\n"
            for result in search_results:
                formatted_output += f"🌐 [{result['title']}]({result['url']})\n"

        # 添加页脚
        formatted_output += "\n\n---\n🎓 **AI学习导师** | 基于最新教育科学研究 | 让学习更有趣、更有效！"

        return formatted_output

    def _get_default_analysis(self, note_content):
        """提供默认的分析结果"""
        word_count = len(note_content)
        lines = note_content.split('\n')
        line_count = len([line for line in lines if line.strip()])

        analysis = f"""
# 🤖 AI学习导师的温馨分析

亲爱的学习者，你好！👋 虽然现在网络连接有些小问题，但我依然可以为你提供一些基础的学习建议！

## 📊 笔记基本信息

| 项目 | 数值 |
|------|------|
| 📝 总字数 | {word_count} 个字符 |
| 📄 行数 | {line_count} 行 |
| 🎯 学习状态 | 正在努力中！💪 |

## 🎨 视觉与结构建议

### ✅ 你的优点
- ✨ **内容完整**：你已经开始记录学习笔记了！
- 📚 **主题明确**：有清晰的学习方向
- 💡 **主动学习**：主动整理知识的行为很棒！

### 🔧 可优化之处
- 🎯 **重点突出**：可以用**粗体**标注重要概念
- 📋 **结构化**：考虑使用列表和分点组织内容
- 🖼️ **视觉化**：添加一些emoji让笔记更生动

## 🧠 认知科学小贴士

### 💭 记忆增强技巧
1. **间隔重复**：学习后1小时、1天、3天、1周复习
2. **主动回忆**：尝试不看笔记回忆内容
3. **联想记忆**：为抽象概念找具体例子

### 🎯 学习策略建议
- 📖 **精读精记**：不要贪多，质量胜于数量
- 💬 **讨论交流**：和朋友分享你的学习心得
- 📝 **定期复习**：建立个人知识库

## 🌟 鼓励的话

🌱 **记住**：每一位优秀的学习者都是从这样的笔记开始的！你已经在正确的道路上了！

🚀 **下一步**：试着用我们建议的方式重新整理这份笔记，你会发现学习变得更有趣！

❤️ **AI导师说**：你很棒，继续保持这种学习的热情！有什么具体的问题都可以问我哦！

---
*本分析基于认知科学和学习心理学的最佳实践*
"""
        return analysis