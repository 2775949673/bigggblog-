from django.shortcuts import render,HttpResponse,redirect,reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm,LoginForm
from django.contrib.auth import get_user_model,login,logout
from django.contrib.auth.models import User

User = get_user_model()


# Create your views here.
@require_http_methods(['GET','POST'])
def wxlogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            remember = form.cleaned_data.get('remember')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                #登录
                login(request, user)
                #记住我
                if remember:
                    # 设置了记住我，使用settings中配置的SESSION_COOKIE_AGE
                    pass  # Django会自动使用SESSION_COOKIE_AGE
                else:
                    # 没有设置记住我，会话在浏览器关闭时过期
                    request.session.set_expiry(0)
                return redirect('/')
            else:
                form.add_error('email','邮箱或密码错误！')
                # return render(request, 'login.html',context={'form':form})
                return redirect('wxauth:login')

def wxlogout(request):
    logout(request)
    return redirect('/')

@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email = email, username = username, password = password)
            return redirect(reverse('wxauth:login'))
        else:
            print(form.errors)
            return redirect(reverse('wxauth:register'))



#发送邮箱
def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code":400,"message":"必须传递邮箱！"})
    #生成验证码四位阿拉伯数字
    captcha = "".join(random.sample(string.digits,4))
    #存储到数据库中
    CaptchaModel.objects.update_or_create(email=email,defaults={'captcha':captcha})
    send_mail("万象笔记注册验证码",message=f"注册验证码是：{captcha}",recipient_list=[email],from_email="2775949673@qq.com")
    return JsonResponse({"code":200,"message":"验证码发送成功！"})

