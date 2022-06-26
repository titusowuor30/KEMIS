from django.urls import path, include
from .views import *
from .payment_views import *

urlpatterns = [
    path('payment/<int:id>/', select_pay_method, name='pay_method'),
    path('invoice/reject/<int:id>/', reject_invoice,name="reject_invoice"),
    path('access/token', getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa', lipa_na_mpesa_online, name='lipa_na_mpesa'),
    path('callback/', MpesaCallBack, name='callback'),
    path('result/', displaymsg, name='display'),
    path('delete_invoice/<int:id>/', delete_invoice, name='delete_invoice'),
    path('confirm_delivery/<int:id>/', confirm_delivery, name="confirm_delivery"),
    path('settings', sys_list, name='sys_list'),
    path('update_sys_settings/<int:id>/', update_sys_settings, name='update_sys_settings'),
    path('reports/', reports, name='reports'),
]
