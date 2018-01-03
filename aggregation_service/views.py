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
            print(nextUrl)
        if r['previous'] is not None:
            parsed = urlparse(r['previous'])
            prevUrl = parsed._replace(netloc=str(request.META['SERVER_NAME'])+':'+str(request.META['SERVER_PORT']))
            r['previous'] = urlunparse(prevUrl)
            print(prevUrl)
        return r
    except:
        return response.json()


class UserList(APIView):
    url = 'http://127.0.0.1:8001/users/'

    def get(self, request):
        try:
            # make a request
            serviceResponse = requests.get(self.url, params = request.query_params)
            if serviceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, serviceResponse)
                return Response(responseData)
            return Response(responseData, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            r = requests.post(self.url, data = request.data)
            if r.status_code == requests.codes.created:
                return Response(r.json(), status=status.HTTP_201_CREATED)
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    url = 'http://127.0.0.1:8001/users/'

    def get(self, request, id):
        try:
            r = requests.get(self.url+id+'/')
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            r = requests.put(self.url+id+'/', data = request.data)
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            r = requests.delete(self.url+id+'/')
            if r.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CourseList(APIView):
    url = 'http://127.0.0.1:8002/courses/'

    def get(self, request):
        try:
            serviceResponse = requests.get(self.url, params = request.query_params)
            if serviceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, serviceResponse)
                return Response(responseData)
            return Response(responseData, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            r = requests.post(self.url, data = request.data)
            if r.status_code == requests.codes.created:
                return Response(r.json(), status=status.HTTP_201_CREATED)
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CourseDetail(APIView):
    url = 'http://127.0.0.1:8002/courses/'

    def get(self, request, id):
        try:
            r = requests.get(self.url+id+'/')
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            r = requests.put(self.url+id+'/', data = request.data)
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            r = requests.delete(self.url+id+'/')
            if r.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderList(APIView):
    url = 'http://127.0.0.1:8003/orders/'

    def get(self, request):
        try:
            serviceResponse = requests.get(self.url, params = request.query_params)
            if serviceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, serviceResponse)
                return Response(responseData)
            return Response(responseData, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            r = requests.post(self.url, data = request.data)
            if r.status_code == requests.codes.created:
                return Response(r.json(), status=status.HTTP_201_CREATED)
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    url = 'http://127.0.0.1:8003/orders/'

    def get(self, request, id):
        try:
            r = requests.get(self.url+id+'/')
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            r = requests.put(self.url+id+'/', data = request.data)
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            r = requests.delete(self.url+id+'/')
            if r.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PaymentList(APIView):
    url = 'http://127.0.0.1:8004/payments/'

    def get(self, request):
        try:
            serviceResponse = requests.get(self.url, params = request.query_params)
            if serviceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, serviceResponse)
                return Response(responseData)
            return Response(responseData, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            r = requests.post(self.url, data = request.data)
            if r.status_code == requests.codes.created:
                return Response(r.json(), status=status.HTTP_201_CREATED)
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class PaymentDetail(APIView):
    url = 'http://127.0.0.1:8004/payments/'

    def get(self, request, id):
        try:
            r = requests.get(self.url+id+'/')
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            r = requests.put(self.url+id+'/', data = request.data)
            if r.status_code == requests.codes.ok:
                return Response(r.json())
            return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            r = requests.delete(self.url+id+'/')
            if r.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
