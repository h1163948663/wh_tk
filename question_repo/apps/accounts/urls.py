from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
urlpatterns = [
# 注册  
    #

url(r'^register/$', views.Register.as_view(), name='register'),
url(r'^register/$', TemplateView.as_view(template_name="accounts/register.html"), name="register"),
# 登录  
url(r'^login/$',views.Login.as_view(), name="login"),
# 退出  
url(r'^logout/$', views.logout, name="logout"),
# 忘记密码  
url(r'^password/forget/$', views.test, name="password_forget"),
# 重置密码  
url(r'^password/reset/token/$',views.test, name="password_reset"),
url(r'^index/$',views.test,name="index"),
#重置密码
    url(r'password/reset/(\w+)/$', views.PasswordReset.as_view(), name="password_reset"),
]
