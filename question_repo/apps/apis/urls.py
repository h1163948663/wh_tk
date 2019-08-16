from django.conf.urls import url
from . import views
urlpatterns = [
    #生成验证码图片
    url(r'^get_captcha/$', views.get_captcha, name='get_captcha'),
    ##检查电话
    url(r'^get_mobile_captcha/$',views.get_mobile_captcha,name='get_mobile_captcha'),
    #检查验证码
    url(r'^check_captcha/$', views.check_captcha, name='check_captcha'),
    #获取数据接口
    url(r'^questions/$', views.QuestionsView.as_view(), name='questions'),
    url(r'^question/collection/(?P<id>\d+)/$', views.QuestionCollectionView.as_view(), name='question_collection'),
    url(r'^answer/(?P<id>\d+)/$', views.AnswerView.as_view(), name="answer"),
    url(r'^other_answer/(?P<id>\d+)/$', views.OtherAnswerView.as_view(), name="other_answer"),
    url(r'^answer/collection/(?P<id>\d+)/$', views.AnswerCollectionView.as_view(), name='answer_collection'),
    url(r'^change_avator/$', views.ChangeAvator.as_view(), name='change_avator'),
]