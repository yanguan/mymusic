import hashlib
import io
import uuid
import random

import redis
from PIL import Image, ImageDraw, ImageFont
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django_redis import get_redis_connection

from index.models import *
from music import settings
from user.models import  Users
import datetime
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def sign(request):
    # 验证登录
    username = request.session.get('username')
    if not username:
        return redirect('/user/login.html')
    else:
        # 单设备登录
        token = request.session.get('token')
        redis_conn = get_redis_connection("default")
        redis_token = redis_conn.get(username).decode('utf-8')
        if token != redis_token:
            request.session.flush()
            return redirect('/user/login.html')
        # 获取用户
        user = Users.objects.get(username=username)
        vote_time = user.vote_time
        print(vote_time)
        time_now = str(datetime.datetime.now())[:10]
        print(time_now)
        if vote_time == time_now:
            data = {
                'message': '已签到',
                'vote': f"打榜票数：{user.votes}"
            }
        else:
            user.vote_time = str(datetime.datetime.now())[:10]
            user.votes += 5
            user.is_vote = True
            user.save()
            data = {
                'message': '未签到',
                'vote': f"打榜票数：{user.votes}"
            }
        # return render(request, 'home.html', data)
        return redirect('/user/home/1.html')


# 设置用户登录限制
def homeView(request, page):
    username = request.session.get('username')
    # 验证是否登录
    if not username:
        return redirect('/user/login.html')
    else:
        # 单设备登录
        token = request.session.get('token')
        redis_conn = get_redis_connection("default")
        redis_token = redis_conn.get(username).decode('utf-8')
        if token != redis_token:
            request.session.flush()
            return redirect('/user/login.html')
        # 热门歌曲
        search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:4]
        # 分页功能
        user = Users.objects.get(username=username)
        vote_time = user.vote_time
        print(vote_time)
        time_now = str(datetime.datetime.now())[:10]
        print('1111111', user.is_vote)
        if vote_time == time_now:
            user.is_vote = True
            user.save()
        else:
            user.is_vote = False
            user.save()
        # song_info = request.session.get('play_list', [])
        song_list = user.collect.all()
        print(song_list)
        paginator = Paginator(song_list, 3)
        user = Users.objects.get(username=request.session.get("username"))
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'home.html', locals())


#
#
# # 退出登录
def logoutView(request):
    logout(request)
    return redirect('/')


def loginView(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        email = request.POST.get('mail')
        password = request.POST.get('password')
        code = request.POST.get("code")
        login_code = request.session.get('login_code')
        encode_pwd = password.encode()  # 把字符串转为字节类型
        md5_pwd = hashlib.md5(encode_pwd)
        psd = md5_pwd.hexdigest()

        user = Users.objects.get(mail=email)
        if not email or not password or not user or not code:
            data = {
                'tips': '账号或密码错误'
            }
            return render(request, 'login.html', data)
        elif code.upper() != login_code:
            data = {
                'tips': '验证码错误'
            }
            return render(request, 'login.html', data)
        elif user.password == psd:
            token = str(uuid.uuid4())[:32]
            request.session['token'] = token
            request.session['username'] = user.username
            redis_conn = get_redis_connection("default")
            redis_conn.set(user.username, token)

            return redirect('/user/home/1.html')
        else:
            data = {
                'tips': '账号已存在'
            }

        return render(request, 'login.html', data)


def registerView(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        email = request.POST.get('mail')
        username = request.POST.get('username')
        code = request.POST.get('code')
        password = request.POST.get('password')
        vfcode = request.session.get("active_key")

        if not username or not password or not code:
            return redirect('/user/register.html')
        elif code != vfcode:
            data = {
                'tips': '验证码错误'
            }
        else:
            encode_pwd = password.encode()
            md5_pwd = hashlib.md5(encode_pwd)
            psd = md5_pwd.hexdigest()
            print("------------注册密码-----------", psd)
            try:
                user = Users.objects.create(mail=email, username=username, password=psd)
                user.save()
                data = {
                    'tips': '注册成功'
                }
                return render(request, 'login.html', data)
            except:
                data = {
                    'tips': '注册失败'
                }
        return render(request, 'register.html', data)


def login_code(request):
    width = 110
    height = 40

    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), random.randrange(20, 100))
    im = Image.new("RGB", (width, height), bgcolor)

    # 2 创建画笔
    draw = ImageDraw.Draw(im)

    # 3 生成噪点
    for i in range(0, 100):
        # 绘制噪点
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        # 参数1：点的位置
        # 参数2：点的颜色
        draw.point(xy, fill)

    # 4 生成随机验证码
    base_str = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM"
    code_str = ""
    for i in range(0, 4):
        code_str += random.choice(base_str)
    print("--------------code_str =", code_str)

    # 5 构造字体对象
    # 参数1：字体文件路径  C:\Windows\Fonts\AdobeArabic-Bold.otf
    # 参数2：字体大小
    font = ImageFont.truetype("C:\Windows\Fonts\BASKVILL.TTF", 30)

    # 6 写入内容
    # 参数1：位置
    # 参数2：内容
    # 参数font：字体
    # 参数fill：颜色
    draw.text((5, 2), code_str[0], font=font, fill=(255, random.randrange(0, 255), 255, random.randrange(0, 255)))
    draw.text((25, 2), code_str[1], font=font, fill=(255, random.randrange(0, 255), 255, random.randrange(0, 255)))
    draw.text((50, 2), code_str[2], font=font, fill=(255, random.randrange(0, 255), 255, random.randrange(0, 255)))
    draw.text((75, 2), code_str[3], font=font, fill=(255, random.randrange(0, 255), 255, random.randrange(0, 255)))

    # 7 释放
    del draw

    # 8 内存文件操作
    buf = io.BytesIO()
    im.save(buf, "png")

    # 9 写入session
    path = request.GET.get('from')

    request.session["login_code"] = code_str.upper()

    # 10 响应验证码数据
    return HttpResponse(buf.getvalue(), "image/png")


# 邮箱验证码
def send(request):
    mail = request.GET.get("mail")
    print(mail)
    active_key = str(uuid.uuid4())[:6]
    request.session["active_key"] = active_key
    request.session.set_expiry(300)
    send_mail("我的音乐|验证码", "您的验证为：%s,请在5分钟内完成操作" % (active_key), settings.EMAIL_HOST_USER, [mail])
    data = {
        "success": True
    }
    return JsonResponse(data)
