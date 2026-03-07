import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def markdownify(text):
    """将Markdown文本转换为HTML"""
    if not text:
        return ""
    # 启用扩展以支持表格等
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'codehilite'])
    return mark_safe(md.convert(text))