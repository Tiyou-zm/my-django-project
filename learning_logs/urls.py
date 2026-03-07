"""定义learning_logs的URL模式"""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # 主页
    path('', views.index, name='index'),
    # 显示所有的主题
    path('topics/', views.topics, name='topics'),
    # 显示单个主题的详细页面
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # 用于添加新主题的网页
    path('new_topic/', views.new_topic, name='new_topic'),
    # 用于添加新条目的页面
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # 编辑主题
    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    # 编辑条目
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # 删除主题
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    # 删除条目
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    # AI分析条目
    path('analyze_entry/<int:entry_id>/', views.analyze_entry, name='analyze_entry'),
    # AI优化条目内容
    path('optimize_entry/<int:entry_id>/', views.optimize_entry, name='optimize_entry'),
    # 学习进度追踪
    path('progress/', views.progress, name='progress'),
]