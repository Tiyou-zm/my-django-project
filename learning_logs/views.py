from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from .services import DeepSeekService
from django.contrib import messages
from django.db.models import Count

# Create your views here.

def index(request):
    """学习笔记的主页"""
    # 获取统计信息用于进度追踪
    total_topics = Topic.objects.count()
    total_entries = Entry.objects.count()
    recent_entries = Entry.objects.order_by('-date_added')[:5]

    context = {
        'total_topics': total_topics,
        'total_entries': total_entries,
        'recent_entries': recent_entries,
    }
    return render(request, 'learning_logs/index.html', context)

def topics(request):
    """显示所有的主题"""
    topics = Topic.objects.annotate(entry_count=Count('entry')).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    topic = get_object_or_404(Topic, id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '主题创建成功！')
            return redirect('learning_logs:topics')

    # 显示空表单或指出表单数据无效
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id):
    """在特定主题中添加新条目"""
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = EntryForm()
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            messages.success(request, '条目添加成功！点击"AI分析"按钮获取智能建议。')
            return redirect('learning_logs:topic', topic_id=topic_id)

    # 显示空表单或指出表单数据无效
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_topic(request, topic_id):
    """编辑主题"""
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method != 'POST':
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '主题更新成功！')
            return redirect('learning_logs:topics')

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_topic.html', context)

def edit_entry(request, entry_id):
    """编辑条目"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '条目更新成功！点击"AI分析"按钮获取新的智能建议。')
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

def delete_topic(request, topic_id):
    """删除主题"""
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == 'POST':
        topic.delete()
        messages.success(request, '主题删除成功！')
        return redirect('learning_logs:topics')

    context = {'topic': topic}
    return render(request, 'learning_logs/delete_topic.html', context)

def delete_entry(request, entry_id):
    """删除条目"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    if request.method == 'POST':
        entry.delete()
        messages.success(request, '条目删除成功！')
        return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic}
    return render(request, 'learning_logs/delete_entry.html', context)

def analyze_entry(request, entry_id):
    """单独分析条目"""
    entry = get_object_or_404(Entry, id=entry_id)

    if request.method == 'POST':
        # 添加短暂延迟确保loading状态可见
        import time
        time.sleep(0.5)

        ai_service = DeepSeekService()
        analysis = ai_service.analyze_note(entry.text)
        entry.ai_analysis = analysis
        entry.save()
        messages.success(request, '🤖 AI分析完成！DeepSeek已为您分析了笔记内容。')

    return redirect('learning_logs:topic', topic_id=entry.topic.id)

def optimize_entry(request, entry_id):
    """优化条目内容"""
    entry = get_object_or_404(Entry, id=entry_id)

    if request.method == 'POST':
        # 添加短暂延迟确保loading状态可见
        import time
        time.sleep(0.5)

        ai_service = DeepSeekService()
        optimized_content = ai_service.optimize_content(entry.text)
        entry.text = optimized_content

        # 重新分析优化后的内容
        analysis = ai_service.analyze_note(optimized_content)
        entry.ai_analysis = analysis
        entry.save()
        messages.success(request, '✨ 内容优化完成！DeepSeek已重新组织您的笔记。')

    return redirect('learning_logs:topic', topic_id=entry.topic.id)

def progress(request):
    """显示学习进度统计"""
    from django.db.models import Count, Avg
    from django.db.models.functions import Length

    # 基本统计
    total_topics = Topic.objects.count()
    total_entries = Entry.objects.count()

    # 主题统计
    topics_with_entries = Topic.objects.annotate(entry_count=Count('entry')).filter(entry_count__gt=0)
    avg_entries_per_topic = topics_with_entries.aggregate(avg=Avg('entry_count'))['avg'] or 0

    # 条目统计
    entries_with_analysis = Entry.objects.exclude(ai_analysis__isnull=True).exclude(ai_analysis='')
    analyzed_entries_count = entries_with_analysis.count()

    # 最近活动
    recent_topics = Topic.objects.order_by('-date_added')[:5]
    recent_entries = Entry.objects.order_by('-date_added')[:10]

    # 内容长度统计
    avg_entry_length = Entry.objects.annotate(text_length=Length('text')).aggregate(avg=Avg('text_length'))['avg'] or 0

    context = {
        'total_topics': total_topics,
        'total_entries': total_entries,
        'topics_with_entries': topics_with_entries.count(),
        'avg_entries_per_topic': round(avg_entries_per_topic, 1),
        'analyzed_entries_count': analyzed_entries_count,
        'analysis_percentage': round((analyzed_entries_count / total_entries * 100), 1) if total_entries > 0 else 0,
        'recent_topics': recent_topics,
        'recent_entries': recent_entries,
        'avg_entry_length': round(avg_entry_length, 0),
    }
    return render(request, 'learning_logs/progress.html', context)
