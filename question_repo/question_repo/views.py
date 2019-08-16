from django.shortcuts import render,HttpResponse
import logging
from django.views.generic import View


# apis为settings中Logging配置中的loggers
logger = logging.getLogger('apis')


def logtest(request):
    logger.info("欢迎访问")
    return HttpResponse('日志测试')

def index(request):
    return render(request,'index.html')
def login(request):
    return render(request,'login.html',)
def question_detail(request):
    return render(request,"question_detail.html")
def questions(request):
    return render(request, "questions.html")
def uc_profile(request):
    return render(request,"uc_profile.html")



from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.shortcuts import render
from apps.repo.models import Questions
def paginator(request):
    questions_list =  Questions.objects.all()
    paginator1 = Paginator(questions_list,25)
    page = request.GET.get("page")
    try:
        contacts = paginator1.page(page)
    except PageNotAnInteger:
        contacts = paginator1.page(1)
    except EmptyPage:
        contacts = paginator1.page(paginator1.num_pages)

    return render(request,'questions1.html',{'contacts':contacts})