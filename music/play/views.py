import json
import redis
from django_redis import get_redis_connection

from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
from index.models import *
from user.models import *


# 歌曲播放页面
def playView(request, song_id):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:6]
    # 歌曲信息
    song_info = Song.objects.get(song_id=int(song_id))
    # 播放列表
    play_list = request.session.get('play_list', [])
    song_exist = False
    if play_list:
        for i in play_list:
            if int(song_id) == i['song_id']:
                song_exist = True
    if song_exist == False:
        play_list.append(
            {'song_id': int(song_id), 'song_singer': song_info.song_singer, 'song_name': song_info.song_name,
             'song_time': song_info.song_time})
    request.session['play_list'] = play_list
    # 歌词
    if song_info.song_lyrics != '暂无歌词':
        f = open('static/songLyric/' + song_info.song_lyrics, 'r', encoding='utf-8')
        song_lyrics = f.read()
        f.close()
    # 相关歌曲
    dynamic = Dynamic.objects.get(song=song_info)
    song_vote = dynamic.dynamic_vote
    song_type = Song.objects.values('song_type').get(song_id=song_id)['song_type']
    song_relevant = Dynamic.objects.select_related('song').filter(song__song_type=song_type).order_by(
        '-dynamic_plays').all()[:6]
    # 添加播放次数
    # 扩展功能：可使用session实现每天只添加一次播放次数
    dynamic_info = Dynamic.objects.filter(song_id=int(song_id)).first()
    # 判断歌曲动态信息是否存在，存在就在原来基础上加1
    if dynamic_info:
        dynamic_info.dynamic_plays += 1
        dynamic_info.save()
    # 动态信息不存在则创建新的动态信息
    else:
        dynamic_info = Dynamic(dynamic_plays=1, dynamic_search=0, dynamic_down=0, song_id=song_id)
        dynamic_info.save()
    return render(request, 'play.html', locals())


# 歌曲下载
def downloadView(request, song_id):
    # 根据song_id查找歌曲信息
    song_info = Song.objects.get(song_id=int(song_id))
    # 添加下载次数
    dynamic_info = Dynamic.objects.filter(song_id=int(song_id)).first()
    # 判断歌曲动态信息是否存在，存在就在原来基础上加1
    if dynamic_info:
        dynamic_info.dynamic_down += 1
        dynamic_info.save()
    # 动态信息不存在则创建新的动态信息
    else:
        dynamic_info = Dynamic(dynamic_plays=0, dynamic_search=0, dynamic_down=1, song_id=song_id)
        dynamic_info.save()
    # 读取文件内容
    file = 'static/songFile/' + song_info.song_file

    def file_iterator(file, chunk_size=512):
        with open(file, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    # 将文件内容写入StreamingHttpResponse对象，并以字节流方式返回给用户，实现文件下载
    filename = str(song_id) + '.mp3'
    response = StreamingHttpResponse(file_iterator(file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
    return response

#歌曲收藏
def collectView(request, song_id):
    username = request.session.get('username')
    #验证登录
    if not username :
        data = {
            "islogin": False,

        }
        return JsonResponse(data)
    else:
        #验证单设备
        token = request.session.get('token')
        redis_conn = get_redis_connection("default")
        redis_token = redis_conn.get(username).decode('utf-8')
        if token != redis_token:
            request.session.flush()
            data = {
                "islogin": False,

            }
            return JsonResponse(data)
        user = Users.objects.get(username=username)
        song = Song.objects.get(song_id=song_id)
        try:
            user.collect.get(song_id=song_id)
        except:
            print("---------------2----------------------")
            user.collect.add(song)
            data = {
                "islogin": True,
                "collect": True,
            }
        else:
            user.collect.remove(song)
            print("---------------1----------------------")
            data = {
                "islogin": True,
                "collect": False,
            }
        user.save()
    return JsonResponse(data)

#歌曲投票
def voteView(request, song_id):
    username = request.session.get('username')
    print('----------------', song_id,username)
    #验证登录
    if not username:
        print(11111111111111)
        data = {
           "islogin":False
        }
        return JsonResponse(data)
    else:
        #验证单设备
        print(2222222222222222222)
        token = request.session.get('token')
        redis_conn = get_redis_connection("default")
        redis_token = redis_conn.get(username).decode('utf-8')
        if token != redis_token:
            request.session.flush()
            data = {
                "islogin": False
            }
            return JsonResponse(data)
        user = Users.objects.get(username=username)
        song = Song.objects.get(song_id=song_id)
        dynamic = Dynamic.objects.get(song=song)
        if user.votes > 0:
            user.votes -= 1
            user.save()
            dynamic.dynamic_vote += 1
            dynamic.save()
            data = {
                "islogin":True,
                "success":True,
                "dynamic_vote":dynamic.dynamic_vote,
            }
        else:
            data = {
                "islogin": True,
                "success": False,
                "dynamic_vote": dynamic.dynamic_vote,
            }
        return JsonResponse(data)
