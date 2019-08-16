from django.shortcuts import render,HttpResponse
# Create your views here.
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from .models import Category,Questions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.http import JsonResponse
import logging
from .models import User
def test(request):
    return HttpResponse("题库视图")

@login_required
def index(requeset):
    userlog = UserLog.objects.all()[:10]
    print(userlog)
    #dict将数据转成字典
    operator = dict(UserLog.OPERATE)
    for log in userlog:
        log.operate_cn =operator[int(log.operate)]
        #distinct去重
    recent_user_ids = [item['user'] for  item in UserLog.objects.all().values('user').distinct()[:10]]
    recent_user = User.objects.filter(id__in=recent_user_ids)
    kwgs = {
        "userlog":userlog,
        "recent_user":recent_user
    }
    return render(requeset,"index.html",kwgs)

# class  QuestionsList(View):
#     def get(self,request):
#         return render(request, 'questions.html')

class QuestionsList(LoginRequiredMixin,View):
    def get(self, request):
        category = Category.objects.all().values("id", "name")
        grades = Questions.DIF_CHOICES
        search = request.GET.get("search","")
        kwgs = {"category":category, "grades":grades,"search":search }

        return render(request, 'questions.html', kwgs)



from .models import Answers,AnswersCollection,UserLog
from django.views.generic import DetailView
import json
from django.core import serializers
import logging
logger = logging.getLogger("repo")
class QuestionDetail(LoginRequiredMixin,DetailView):
    model = Questions
    pk_url_kwarg = 'id'
    template_name = "question_detail.html"
    # 默认名：object
    context_object_name = "object"
    print(context_object_name)
    # 额外传递my_answer
    def get_context_data(self, **kwargs):
        # kwargs：字典、字典中的数据返回给html页面
        # self.get_object() => 获取当前id的数据（问题）
        question = self.get_object()  # 当前这道题目
        kwargs["my_answer"] = Answers.objects.filter(question=question, user=self.request.user)
        return super().get_context_data(**kwargs)

    def post(self, request, id):
        from django.db import transaction
        try:
            with transaction.atomic():
            # 没有回答过。create
            # 更新回答。get->update
            # 获取对象，没有获取到直接创建对象
                new_answer = Answers.objects.get_or_create(question=self.get_object(), user=self.request.user)
                # 元组：第一个元素获取/创建的对象， True（新创建）/False（老数据）
                print(new_answer)
                new_answer[0].answer = request.POST.get("answer", "没有提交答案信息")
                new_answer[0].save()
                print(self.get_object())
                my_answer = json.loads(serializers.serialize("json", [new_answer[0]]))[0]["fields"]
                UserLog.objects.create(user=self.request.user,question=self.get_object(), operate=3,answer=new_answer[0])
                msg = "提交成功"
                code = 200
            result = {"status": code, "msg": msg,}
            return JsonResponse(result)
        except Exception as ex:
            logger.error(ex)
            my_answer = {}
            msg = "提交失败"
            code = 500
        result = {"status": code, "msg": msg, "my_answer": my_answer}
        return JsonResponse(result)

class OtherAnswerView(LoginRequiredMixin, View):
    def get(self, request, id):
        # other_answer = list(Answers.objects.filter(question=id).values())
        # other_answer = serializers.serialize('json', Answers.objects.filter(question=id))
        # return JsonResponse(other_answer, safe=False)

        my_answer = Answers.objects.filter(question=id, user=request.user)
        if not my_answer:
            html = "请回答后再查看其他答案"
            return HttpResponse(html)

        # other_answer = Answers.objects.filter(question=id).exclude(user=request.user)
        other_answer = Answers.objects.filter(question=id)

        if other_answer:
            for answer in other_answer:
                if AnswersCollection.objects.filter(answer=answer, user=request.user, status=True):
                    answer.collect_status = 1   # => 控制爱心=>空心/实心
                # 外键 AnswersCollectionObject.answer=>related_name
                # answer被收藏哪些人收藏了
                # answer.answers_collection_set.filter(status=True)
                answer.collect_nums = answer.answers_collection_set.filter(status=True).count()
                # answer.answers_collection_set
            # 通过后端渲染出HTML
            # html = loader.render_to_string('question_detail_other_answer.html', {"other_answer": other_answer})
            html = loader.get_template('question_detail_other_answer.html').render({"other_answer": other_answer})
        else:
            html = "暂无回答"
        return HttpResponse(html)


class Question(LoginRequiredMixin, View):
    def post(self, request):
        print(request.POST)
        try:
            title = request.POST.get("title")
            category = request.POST.get("category")
            content = request.POST.get("content")
            if category:
                Questions.objects.create(title=title, category_id=category, content=content, contributor=request.user)
            else:
                Questions.objects.create(title=title, content=content, contributor=request.user)
        except Exception as ex:
            logger.error(ex)
            return HttpResponse("提交失败!")
        return HttpResponse("提交成功")