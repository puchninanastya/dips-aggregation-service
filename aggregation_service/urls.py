from django.conf.urls import url, include
from . import api_views, ui_views

api_urlpatterns = [
    url(r'^users/$', api_views.UserList.as_view(), name='users-list'),
    url(r'^users/(?P<id>[0-9]+)/$', api_views.UserDetail.as_view(), name='user-detail'),
    url(r'^courses/$', api_views.CourseList.as_view(), name='courses-list'),
    url(r'^courses/(?P<id>[0-9]+)/$', api_views.CourseDetail.as_view(), name='course-detail'),
    url(r'^orders/$', api_views.OrderList.as_view(), name='orders-list'),
    url(r'^orders/(?P<id>[0-9]+)/$', api_views.OrderDetail.as_view(), name='order-detail'),
    url(r'^payments/$', api_views.PaymentList.as_view(), name='payments-list'),
    url(r'^payments/(?P<id>[0-9]+)/$', api_views.PaymentDetail.as_view(), name='payment-detail'),
]

urlpatterns = [
     url(r'^api/', include(api_urlpatterns)),

     url(r'^courses/new/$', ui_views.GuiChangeCourseView.as_view(), name='course-new'),
     url(r'^courses/(?P<cid>\w+)/change/$', ui_views.GuiChangeCourseView.as_view(), name='course-change'),
     url(r'^courses/(?P<cid>\w+)/delete/$', ui_views.GuiDeleteCourseView.as_view(), name='course-delete'),
     url(r'^courses/(?P<cid>\w+)/', ui_views.GuiCourseDetailView.as_view(), name='course-detail'),
     url(r'^courses/$', ui_views.GuiCourseListView.as_view(), name='courses-list'),

     url(r'^students/new/$', ui_views.GuiChangeStudentView.as_view(), name='student-new'),
     url(r'^students/(?P<sid>\w+)/change/$', ui_views.GuiChangeStudentView.as_view(), name='student-change'),
     url(r'^students/(?P<sid>\w+)/delete/$', ui_views.GuiDeleteStudentView.as_view(), name='student-delete'),
     url(r'^students/(?P<sid>\w+)/', ui_views.GuiStudentDetailView.as_view(), name='student-detail'),
     url(r'^students/$', ui_views.GuiStudentListView.as_view(), name='students-list'),

     url(r'^orders/new/', ui_views.GuiChangeOrderView.as_view(), name='order-new'),
     url(r'^orders/(?P<oid>\w+)/change/', ui_views.GuiChangeOrderView.as_view(), name='order-change'),
     url(r'^orders/(?P<oid>\w+)/delete/$', ui_views.GuiDeleteOrderView.as_view(), name='order-delete'),
     url(r'^orders/(?P<oid>\w+)/', ui_views.GuiOrderDetailView.as_view(), name='order-detail'),
     url(r'^orders/$', ui_views.GuiOrderListView.as_view(), name='orders-list'),

     url(r'^payments/new/$', ui_views.GuiChangePaymentView.as_view(), name='payment-new'),
     url(r'^payments/(?P<pid>\w+)/change/$', ui_views.GuiChangePaymentView.as_view(), name='payment-change'),
     url(r'^payments/(?P<pid>\w+)/delete/$', ui_views.GuiDeletePaymentView.as_view(), name='payment-delete'),
     url(r'^payments/(?P<pid>\w+)/', ui_views.GuiPaymentDetailView.as_view(), name='payment-detail'),
     url(r'^payments/$', ui_views.GuiPaymentListView.as_view(), name='payments-list'),

     url(r'^contacts/$', ui_views.contacts, name='contacts'),
     url(r'^$', ui_views.index, name='index'),
]
