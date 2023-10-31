from django.shortcuts import render,redirect
from django_redis import get_redis_connection

from index.models import *
from user.models import Users
def rankingView(request):
    # 歌曲分类列表
    All_list = Song.objects.values('song_type').distinct()
    # 歌曲列表信息
    song_type = request.GET.get('type', '')
    if song_type:
        song_info = Dynamic.objects.select_related('song').filter(song__label_id=song_type).order_by('-dynamic_vote').all()
    else:
        song_info = Dynamic.objects.select_related('song').order_by('-dynamic_vote').all()
    return render(request, 'ranking.html', locals())

def Vote(request):
    sid = request.GET.get('id')
    dynamic = Dynamic.objects.get(dynamic_id=sid)
    #验证登录
    username = request.session.get('username')
    if not username:
        return redirect('/user/login.html')
    else:
        #验证单设备
        token = request.session.get('token')
        redis_conn = get_redis_connection("default")
        redis_token = redis_conn.get(username).decode('utf-8')
        if token != redis_token:
            request.session.flush()
            return redirect('/user/login.html')
    user = Users.objects.get(username=username)
    if user.votes > 0:
        user.votes -= 1
        user.save()
        dynamic.dynamic_vote += 1
        dynamic.save()
    return redirect('/ranking.html')

# 通用视图
from django.views.generic import ListView
class RankingList(ListView):
    # context_object_name设置Html模版的某一个变量名称
    context_object_name = 'song_info'
    # 设定模版文件
    template_name = 'ranking.html'
    # 查询变量song_info的数据
    def get_queryset(self):
        # 获取请求参数
        song_type = self.request.GET.get('type', '')
        if song_type:
            song_info = Dynamic.objects.select_related('song').filter(song__song_type=song_type).order_by('-dynamic_vote').all()[:10]
        else:
            song_info = Dynamic.objects.select_related('song').order_by('-dynamic_vote').all()[:10]
        return song_info

    # 添加其他变量
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 所有歌曲分类
        context['All_list'] = Song.objects.values('song_type').distinct()
        return context
