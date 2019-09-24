from django.utils.deprecation import MiddlewareMixin
import time

class MD1(MiddlewareMixin):

    def process_request(self, request):
        start_time = time.time()
        print("MD1里面的 process_request")


class MD2(MiddlewareMixin):
    def process_request(self, request):
        coretime = time.time()
        print("MD2里面的 process_request")
