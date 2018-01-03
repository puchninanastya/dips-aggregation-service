from django.shortcuts import render
from urllib.parse import urlparse, urlunparse

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

import requests, sys

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


class UserList(APIView):
    urlUserService = 'http://127.0.0.1:8001/users/'

    def get(self, request):
        try:
            # make a request
            serviceResponse = requests.get(self.urlUserService, params = request.query_params)
            if serviceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, serviceResponse)
                return Response(responseData)
            return Response(responseData, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            r = requests.post(self.urlUserService, data = request.data)
            if r.status_code == requests.codes.created:
                return Response(r.json(), status=status.HTTP_201_CREATED)
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    urlUserService = 'http://127.0.0.1:8001/users/'

    def get(self, request, id):
        try:
            r = requests.get(self.urlUserService+id+'/')
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            r = requests.put(self.urlUserService+id+'/', data = request.data)
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            r = requests.delete(self.urlUserService+id+'/')
            if r.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CourseList(APIView):
    urlCourseService = 'http://127.0.0.1:8002/courses/'

    def get(self, request):
        try:
            serviceResponse = requests.get(self.urlCourseService, params = request.query_params)
            if serviceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, serviceResponse)
                return Response(responseData)
            return Response(responseData, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            r = requests.post(self.urlCourseService, data = request.data)
            if r.status_code == requests.codes.created:
                return Response(r.json(), status=status.HTTP_201_CREATED)
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CourseDetail(APIView):
    urlCourseService = 'http://127.0.0.1:8002/courses/'

    def get(self, request, id):
        try:
            r = requests.get(self.urlCourseService+id+'/')
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            r = requests.put(self.urlCourseService+id+'/', data = request.data)
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            r = requests.delete(self.urlCourseService+id+'/')
            if r.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderList(APIView):
    urlOrderService = 'http://127.0.0.1:8003/orders/'
    urlUserService = 'http://127.0.0.1:8001/users/'

    def get(self, request):
        try:
            serviceResponse = requests.get(self.urlOrderService, params = request.query_params)
            if serviceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, serviceResponse)
                # TODO: do try except for user service request
                print('we are here')
                for userData in responseData['results']:
                    userId = userData['user']
                    if userId is not None:
                        print(userId)
                        userServiceResponse = requests.get(self.urlUserService+str(userId)+'/')
                        print(userServiceResponse)
                        if userServiceResponse.status_code == requests.codes.ok:
                            userData['user'] = userServiceResponse.json()
                print('we are here2')
                return Response(responseData)

            return Response(responseData, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            r = requests.post(self.urlOrderService, data = request.data)
            if r.status_code == requests.codes.created:
                return Response(r.json(), status=status.HTTP_201_CREATED)
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    urlOrderService = 'http://127.0.0.1:8003/orders/'

    def get(self, request, id):
        try:
            r = requests.get(self.urlOrderService+id+'/')
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            r = requests.put(self.urlOrderService+id+'/', data = request.data)
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            r = requests.delete(self.urlOrderService+id+'/')
            if r.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PaymentList(APIView):
    urlBillingService = 'http://127.0.0.1:8004/payments/'

    def get(self, request):
        try:
            serviceResponse = requests.get(self.urlBillingService, params = request.query_params)
            if serviceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, serviceResponse)
                return Response(responseData)
            return Response(responseData, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            r = requests.post(self.urlBillingService, data = request.data)
            if r.status_code == requests.codes.created:
                return Response(r.json(), status=status.HTTP_201_CREATED)
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class PaymentDetail(APIView):
    urlBillingService = 'http://127.0.0.1:8004/payments/'

    def get(self, request, id):
        try:
            r = requests.get(self.urlBillingService+id+'/')
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            r = requests.put(self.urlBillingService+id+'/', data = request.data)
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            r = requests.delete(self.urlBillingService+id+'/')
            if r.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
