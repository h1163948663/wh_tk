from django.core.signals import request_finished
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import UserLog
#当请求完成后，打印一个日志
@receiver(request_finished)
def all_log(sender,**kwargs):
    print(sender,kwargs)
    print("使用信号记日志")

#当创建一条记录Maillo
"""
@receiver(post_save,sender=MailLoG)
def send_mail(sender,instance,**kwargs)
    pass
"""


@receiver(post_save,sender=UserLog)
def send_mail(sender,instance,**kwargs):
    print(sender,instance,kwargs)
    import time
    time.sleep(20)
    print("XXXXXXXX发送邮件需要20sXXXXXXX")

