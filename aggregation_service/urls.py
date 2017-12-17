from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^courses/$', views.CourseList.as_view(), name='courses-list'),
    url(r'^courses/(?P<id>[0-9]+)/$', views.CourseDetail.as_view(), name='course-detail'),
]
