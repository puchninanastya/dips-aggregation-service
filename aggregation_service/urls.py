from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^users/$', views.UserList.as_view(), name='users-list'),
    url(r'^users/(?P<id>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^courses/$', views.CourseList.as_view(), name='courses-list'),
    url(r'^courses/(?P<id>[0-9]+)/$', views.CourseDetail.as_view(), name='course-detail'),
    url(r'^orders/$', views.OrderList.as_view(), name='orders-list'),
    url(r'^orders/(?P<id>[0-9]+)/$', views.OrderDetail.as_view(), name='order-detail'),
    url(r'^payments/$', views.PaymentList.as_view(), name='payments-list'),
    url(r'^payments/(?P<id>[0-9]+)/$', views.PaymentDetail.as_view(), name='payment-detail'),
]
