import django.dispatch
mysignal = django.dispatch.Signal(providing_args=['arg1','arg2'])