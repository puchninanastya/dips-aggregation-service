from django.shortcuts import render
from django.http import JsonResponse

from urllib.parse import urlparse, urlunparse

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

import requests

""" Services urls """
urlUserService = 'http://127.0.0.1:8001/'
urlCourseService = 'http://127.0.0.1:8002/'
urlOrderService = 'http://127.0.0.1:8003/'
urlBillingService = 'http://127.0.0.1:8004/'

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
            response = requests.get(url+id+'/')
            if response.status_code == requests.codes.ok:
                return response.json()
    except:
        return None

def getUnavailableErrorData():
    return {'error' : 'Service is unavailable.'}

class UserList(APIView):
    def get(self, request):
        try:
            userServiceResponse = requests.get(urlUserService+'users/', params = request.query_params)
            print(0)
            if userServiceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, userServiceResponse)
                return Response(responseData)
            return Response(responseData, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            userServiceResponse = requests.post(urlUserService+'users', data = request.data)
            if userServiceResponse.status_code == requests.codes.created:
                return Response(userServiceResponse.json(), status=status.HTTP_201_CREATED)
            return Response(userServiceResponse.json(), status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get(self, request, id):
        try:
            userServiceResponse = requests.get(urlUserService+'users/'+id+'/')
            if userServiceResponse.status_code == requests.codes.ok:
                return Response(userServiceResponse.json())
            return Response(userServiceResponse.json(), status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            userServiceResponse = requests.put(urlUserService+'users/'+id+'/', data = request.data)
            if userServiceResponse.status_code == requests.codes.ok:
                return Response(userServiceResponse.json())
            return Response(userServiceResponse.json(), status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            userServiceResponse = requests.delete(urlUserService+'users/'+id+'/')
            if userServiceResponse.status_code == 204:
                # delete user orders
                orderServiceResponse = requests.delete(urlOrderService+'users/'+id+'/orders')
                if orderServiceResponse.status_code == 204 or orderServiceResponse.status_code == 404:
                    return Response(status=status.HTTP_204_NO_CONTENT)
                #else:
                    # TODO: ROLLBACK OR QUEUE REQUEST
            return Response(status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CourseList(APIView):
    def get(self, request):
        try:
            courseServiceResponse = requests.get(urlCourseService+'courses', params = request.query_params)
            if courseServiceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, courseServiceResponse)
                return Response(responseData)
            return Response(responseData, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            courseServiceResponse = requests.post(urlCourseService+'courses', data = request.data)
            if courseServiceResponse.status_code == requests.codes.created:
                return Response(courseServiceResponse.json(), status=status.HTTP_201_CREATED)
            return Response(courseServiceResponse.json(), status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CourseDetail(APIView):
    def get(self, request, id):
        try:
            courseServiceResponse = requests.get(urlCourseService+'courses/'+id+'/')
            if courseServiceResponse.status_code == requests.codes.ok:
                return Response(courseServiceResponse.json())
            return Response(courseServiceResponse.json(), status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            courseServiceResponse = requests.put(urlCourseService+'courses/'+id+'/', data = request.data)
            if courseServiceResponse.status_code == requests.codes.ok:
                return Response(courseServiceResponse.json())
            return Response(courseServiceResponse.json(), status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            courseServiceResponse = requests.delete(urlCourseService+'courses/'+id+'/')
            if courseServiceResponse.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderList(APIView):
    def get(self, request):
        try:
            orderServiceResponse = requests.get(urlOrderService+'orders', params = request.query_params)
            if orderServiceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, orderServiceResponse)
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
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            orderServiceResponse = requests.post(urlOrderService+'orders', data = request.data)
            if orderServiceResponse.status_code == requests.codes.created:
                return Response(orderServiceResponse.json(), status=status.HTTP_201_CREATED)
            return Response(orderServiceResponse.json(), status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    def get(self, request, id):
        try:
            orderServiceResponse = requests.get(urlOrderService+'orders/'+id+'/')
            if orderServiceResponse.status_code == requests.codes.ok:
                return Response(orderServiceResponse.json())
            return Response(orderServiceResponse.json(), status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            orderServiceResponse = requests.put(urlOrderService+'orders/'+id+'/', data = request.data)
            if orderServiceResponse.status_code == requests.codes.ok:
                return Response(orderServiceResponse.json())
            return Response(orderServiceResponse.json(), status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            orderServiceResponse = requests.delete(urlOrderService+'orders/'+id+'/')
            if orderServiceResponse.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PaymentList(APIView):
    def get(self, request):
        try:
            billingServiceResponse = requests.get(urlBillingService+'payments', params = request.query_params)
            if billingServiceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, billingServiceResponse)
                return Response(responseData)
            return Response(responseData, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            billingServiceResponse = requests.post(urlBillingService+'payments/', data = request.data)
            if billingServiceResponse.status_code == requests.codes.created:
                # change order payment status
                payment = billingServiceResponse.json()
                orderId = payment['order_id']
                amountPaid = payment['amount_paid']
                if (orderId is not None) and (amountPaid is not None):
                    requestStatusData = { 'is_paid' : True }
                    orderServiceResponse = requests.patch(urlOrderService+'orders/'+str(orderId)+'/',
                        json = requestStatusData, params = {'paid' : amountPaid})
                    if orderServiceResponse.status_code == requests.codes.ok:
                        #TODO: check payment status
                        return Response(billingServiceResponse.json(), status=status.HTTP_201_CREATED)
                    #else:
                        # TODO: ROLLBACK OR QUEUE REQUEST
            #TODO: change Response: delete body
            return Response(billingServiceResponse.json(), status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class PaymentDetail(APIView):
    def get(self, request, id):
        try:
            billingServiceResponse = requests.get(urlBillingService+'payments/'+id+'/')
            if billingServiceResponse.status_code == requests.codes.ok:
                return Response(billingServiceResponse.json())
            return Response(billingServiceResponse.json(), status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            billingServiceResponse = requests.put(urlBillingService+'payments/'+id+'/', data = request.data)
            if billingServiceResponse.status_code == requests.codes.ok:
                return Response(billingServiceResponse.json())
            return Response(billingServiceResponse.json(), status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            billingServiceResponse = requests.delete(urlBillingService+'payments/'+id+'/')
            if billingServiceResponse.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
