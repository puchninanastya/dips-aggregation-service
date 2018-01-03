from django.shortcuts import render
from urllib.parse import urlparse, urlunparse

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

import requests, sys

""" Services urls """
urlUserService = 'http://127.0.0.1:8001/users/'
urlCourseService = 'http://127.0.0.1:8002/courses/'
urlOrderService = 'http://127.0.0.1:8003/orders/'
urlBillingService = 'http://127.0.0.1:8004/payments/'

def fixResponsePaginationUrls(request, response):
    r = response.json()
    try:
        if r['next'] is not None:
            parsed = urlparse(r['next'])
            nextUrl = parsed._replace(netloc=str(request.META['SERVER_NAME'])+':'+str(request.META['SERVER_PORT']))
            r['next'] = urlunparse(nextUrl)
        if r['previous'] is not None:
            parsed = urlparse(r['previous'])
            prevUrl = parsed._replace(netloc=str(request.META['SERVER_NAME'])+':'+str(request.META['SERVER_PORT']))
            r['previous'] = urlunparse(prevUrl)
        return r
    except:
        return response.json()

def getObjectFromService(url, id):
    try:
        if id is not None:
            response = requests.get(url+str(id)+'/')
            if response.status_code == requests.codes.ok:
                return response.json()
    except:
        return None

class UserList(APIView):
    def get(self, request):
        try:
            # make a request
            serviceResponse = requests.get(urlUserService, params = request.query_params)
            if serviceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, serviceResponse)
                return Response(responseData)
            return Response(responseData, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            r = requests.post(urlUserService, data = request.data)
            if r.status_code == requests.codes.created:
                return Response(r.json(), status=status.HTTP_201_CREATED)
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get(self, request, id):
        try:
            r = requests.get(urlUserService+id+'/')
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            r = requests.put(urlUserService+id+'/', data = request.data)
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            r = requests.delete(urlUserService+id+'/')
            if r.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CourseList(APIView):
    def get(self, request):
        try:
            serviceResponse = requests.get(urlCourseService, params = request.query_params)
            if serviceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, serviceResponse)
                return Response(responseData)
            return Response(responseData, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            r = requests.post(urlCourseService, data = request.data)
            if r.status_code == requests.codes.created:
                return Response(r.json(), status=status.HTTP_201_CREATED)
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CourseDetail(APIView):
    def get(self, request, id):
        try:
            r = requests.get(urlCourseService+id+'/')
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            r = requests.put(urlCourseService+id+'/', data = request.data)
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            r = requests.delete(urlCourseService+id+'/')
            if r.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderList(APIView):
    def get(self, request):
        try:
            serviceResponse = requests.get(urlOrderService, params = request.query_params)
            if serviceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, serviceResponse)
                # TODO: do try except for user and course services requests
                for orderData in responseData['results']:
                    # get user info
                    userId = orderData['user']
                    userInfo = getObjectFromService(urlUserService, userId)
                    if userInfo:
                        orderData['user'] = userInfo
                    # get courses info
                    courses = orderData['courses']
                    coursesResult = []
                    wasNoneCourseInfo = False
                    for courseId in orderData['courses']:
                        courseInfo = getObjectFromService(urlCourseService, courseId)
                        if courseInfo:
                            coursesResult.append(courseInfo)
                        else:
                            wasNoneCourseInfo = True
                    if wasNoneCourseInfo is False:
                        orderData['courses'] = coursesResult
                    else: # TODO: check for needs
                        wasNoneCourseInfo = False
                return Response(responseData)
            return Response(responseData, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            r = requests.post(urlOrderService, data = request.data)
            if r.status_code == requests.codes.created:
                return Response(r.json(), status=status.HTTP_201_CREATED)
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    def get(self, request, id):
        try:
            r = requests.get(urlOrderService+id+'/')
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            r = requests.put(urlOrderService+id+'/', data = request.data)
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            r = requests.delete(urlOrderService+id+'/')
            if r.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PaymentList(APIView):
    def get(self, request):
        try:
            serviceResponse = requests.get(urlBillingService, params = request.query_params)
            if serviceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, serviceResponse)
                return Response(responseData)
            return Response(responseData, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            r = requests.post(urlBillingService, data = request.data)
            if r.status_code == requests.codes.created:
                return Response(r.json(), status=status.HTTP_201_CREATED)
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class PaymentDetail(APIView):
    def get(self, request, id):
        try:
            r = requests.get(urlBillingService+id+'/')
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            r = requests.put(urlBillingService+id+'/', data = request.data)
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            r = requests.delete(urlBillingService+id+'/')
            if r.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
