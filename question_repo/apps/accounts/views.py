from django.shortcuts import render,reverse,redirect
from django.shortcuts import HttpResponse
from django.contrib import auth
# Create your views here.
from django.shortcuts import render
from django.views.generic import View
import logging
from django.contrib.auth.hashers import make_password
from .models import User
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm
logger = logging.getLogger('account')

def test(request):
    return render(request,"index.html")
# Create your views here.

class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "accounts/register.html", {"form":form})
        # Ajax提交表单

    def post(self, request):
        from django.core.cache import cache
        ret = {"status": 400, "msg": "调用方式错误"}
        if request.is_ajax():
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                mobile = form.cleaned_data["mobile"]
                mobile_captcha = form.cleaned_data["mobile_captcha"]
                mobile_captcha_reids = cache.get(mobile)
                if mobile_captcha == mobile_captcha_reids:
                    user = User.objects.create(username=username, password=make_password(password))
                    user.save()
                    ret['status'] = 200
                    ret['msg'] = "注册成功"
                    logger.debug(f"新用户{user}注册成功！")
                    user = auth.authenticate(username=username, password=password)
                    if user is not None and user.is_active:
                        auth.login(request, user)
                        logger.debug(f"新用户{user}登录成功")
                    else:
                        logger.error(f"新用户{user}登录失败")
                else:
                    # 验证码错误
                    ret['status'] = 401
                    ret['msg'] = "验证码错误或过期"
            else:
                ret['status'] = 402
                ret['msg'] = form.errors
        logger.debug(f"用户注册结果：{ret}")
        return JsonResponse(ret)

class Login(View):
    # 当加载Login页面时
    def get(self, request):
        # 如果已登录，则直接跳转到index页面
        # request.user 表示的是当前登录的用户对象,没有登录 `匿名用户`
        if request.user.is_authenticated:
            return redirect(reverse('repo:index'))
        form = LoginForm()
        # 设置下一跳转地址
        request.session["next"] =  request.GET.get('next',reverse('repo:index'))
        return render(request, "login.html", {"form":form})


        # Form表单直接提交
    def post(self, request):
        # 表单数据绑定
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            user, flag = form.check_password()
            # user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                logger.info(f"{user.username}登录成功")
                    # 跳转到next
                return redirect(request.session.get("next", '/'))
            msg = "用户名或密码错误"
            logger.error(f"{username}登录失败, 用户名或密码错误")
        else:
            msg = "表单数据不完整"
            logger.error(form.errors)
            logger.error(msg)
        return render(request, "login.html", {"form": form, "msg": msg})


def logout(request):
    auth.logout(request)
    return redirect(reverse("repo:index"))

from apps.usercenter.models import FindPassword
class PasswordReset(View):
    def get(self, request, verify_code):
        import datetime
        create_time_newer = datetime.datetime.utcnow()-datetime.timedelta(minutes=30)
        email = request.GET.get("email")
        # 邮箱、verify_code、status=False、时间近30分钟
        find_password = FindPassword.objects.filter(status=False, verify_code=verify_code, email=email, creat_time__gte=create_time_newer)
        # great_then_equal, lte, lt, gt
        if verify_code and find_password:
            return render(request, "password_reset.html")
        else:
            return HttpResponse("链接失效或有误")

    def post(self, request, verify_code):
        import datetime
        create_time_newer = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password2 == password1:
            try:
                find_password = FindPassword.objects.get(status=False, verify_code=verify_code, creat_time__gte=create_time_newer)
                user = User.objects.get(email=find_password.email)
                user.set_password(password1)
                user.save()
                msg = "重置密码成功，请登录"
                find_password.status = True
                find_password.save()
            except Exception as ex:
                # 记日志 ex
                msg = "出错啦"
        else:
            msg = "两次密码不一致"
        return render(request, "password_reset.html", {"msg":msg})