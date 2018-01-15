from django.conf.urls import url, include
from . import views

api_urlpatterns = [
    url(r'^users/$', views.UserList.as_view(), name='users-list'),
    url(r'^users/(?P<id>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^courses/$', views.CourseList.as_view(), name='courses-list'),
    url(r'^courses/(?P<id>[0-9]+)/$', views.CourseDetail.as_view(), name='course-detail'),
    url(r'^orders/$', views.OrderList.as_view(), name='orders-list'),
    url(r'^orders/(?P<id>[0-9]+)/$', views.OrderDetail.as_view(), name='order-detail'),
    url(r'^payments/$', views.PaymentList.as_view(), name='payments-list'),
    url(r'^payments/(?P<id>[0-9]+)/$', views.PaymentDetail.as_view(), name='payment-detail'),
]

urlpatterns = [
     url(r'^api/', include(api_urlpatterns)),

     url(r'^courses/new/$', views.GuiChangeCourseView.as_view(), name='course-new'),
     url(r'^courses/(?P<cid>\w+)/change/$', views.GuiChangeCourseView.as_view(), name='course-change'),
     url(r'^courses/(?P<cid>\w+)/delete/$', views.GuiDeleteCourseView.as_view(), name='course-delete'),
     url(r'^courses/(?P<cid>\w+)/', views.GuiCourseDetailView.as_view(), name='course-detail'),
     url(r'^courses/$', views.GuiCourseListView.as_view(), name='courses-list'),

     url(r'^students/new/$', views.GuiChangeStudentView.as_view(), name='student-new'),
     url(r'^students/(?P<sid>\w+)/change/$', views.GuiChangeStudentView.as_view(), name='student-change'),
     url(r'^students/(?P<sid>\w+)/delete/$', views.GuiDeleteStudentView.as_view(), name='student-delete'),
     url(r'^students/(?P<sid>\w+)/', views.GuiStudentDetailView.as_view(), name='student-detail'),
     url(r'^students/$', views.GuiStudentListView.as_view(), name='students-list'),

     url(r'^orders/new/', views.GuiChangeStudentView.as_view(), name='order-new'),
     url(r'^orders/(?P<oid>\w+)/change/', views.GuiChangeStudentView.as_view(), name='order-change'),
     url(r'^orders/(?P<oid>\w+)/delete/$', views.GuiDeleteOrderView.as_view(), name='order-delete'),
     url(r'^orders/(?P<oid>\w+)/', views.GuiOrderDetailView.as_view(), name='order-detail'),
     url(r'^orders/$', views.GuiOrderListView.as_view(), name='orders-list'),

     url(r'^payments/new/$', views.GuiChangePaymentView.as_view(), name='payment-new'),
     url(r'^payments/(?P<pid>\w+)/change/$', views.GuiChangePaymentView.as_view(), name='payment-change'),
     url(r'^payments/(?P<pid>\w+)/delete/$', views.GuiDeletePaymentView.as_view(), name='payment-delete'),
     url(r'^payments/(?P<pid>\w+)/', views.GuiPaymentDetailView.as_view(), name='payment-detail'),
     url(r'^payments/$', views.GuiPaymentListView.as_view(), name='payments-list'),

     url(r'^/contacts/$', views.contacts, name='contacts'),
     url(r'^$', views.index, name='index'),
]
