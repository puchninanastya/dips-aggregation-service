from django.shortcuts import render
from django.http import JsonResponse

from urllib.parse import urlparse, urlunparse

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

import requests

from aggregation_service.tasks import deleteUserOrders

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
            response = requests.get(url+str(id)+'/')
            if response.status_code == requests.codes.ok:
                return response.json()
    except:
        return None

def getUnavailableErrorData():
    return {'error' : 'Service is unavailable.'}

def getServerErrorData():
    return {'error' : 'Unknown server error.'}

class UserList(APIView):
    def get(self, request):
        try:
            userServiceResponse = requests.get(urlUserService+'users/', params = request.query_params)
            if userServiceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, userServiceResponse)
                return Response(responseData)
            elif userServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=userServiceResponse.status_code)
            else:
                return Response(userServiceResponse.json(), status=userServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            userServiceResponse = requests.post(urlUserService+'users/', json = request.data)
            if userServiceResponse.status_code == requests.codes.created:
                return Response(userServiceResponse.json(), status=status.HTTP_201_CREATED)
            elif userServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=userServiceResponse.status_code)
            else:
                return Response(userServiceResponse.json(), status=userServiceResponse.status_code)
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
            elif userServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=userServiceResponse.status_code)
            else:
                return Response(userServiceResponse.json(), status=userServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            userServiceResponse = requests.put(urlUserService+'users/'+id+'/', json = request.data)
            if userServiceResponse.status_code == requests.codes.ok:
                return Response(userServiceResponse.json())
            elif userServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=userServiceResponse.status_code)
            else:
                return Response(userServiceResponse.json(), status=userServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            userServiceResponse = requests.delete(urlUserService+'users/'+id+'/')
            if userServiceResponse.status_code == 204:
                # delete user orders
                deleteUserOrders.delay(id)
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif userServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=userServiceResponse.status_code)
            else:
                return Response(userServiceResponse.json(), status=userServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CourseList(APIView):
    def get(self, request):
        try:
            courseServiceResponse = requests.get(urlCourseService+'courses/', params = request.query_params)
            if courseServiceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, courseServiceResponse)
                return Response(responseData)
            elif courseServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=courseServiceResponse.status_code)
            else:
                return Response(courseServiceResponse.json(), status=courseServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            courseServiceResponse = requests.post(urlCourseService+'courses/', json = request.data)
            if courseServiceResponse.status_code == requests.codes.created:
                return Response(courseServiceResponse.json(), status=status.HTTP_201_CREATED)
            elif courseServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=courseServiceResponse.status_code)
            else:
                return Response(courseServiceResponse.json(), status=courseServiceResponse.status_code)
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
            elif courseServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=courseServiceResponse.status_code)
            else:
                return Response(courseServiceResponse.json(), status=courseServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            courseServiceResponse = requests.put(urlCourseService+'courses/'+id+'/', json = request.data)
            if courseServiceResponse.status_code == requests.codes.ok:
                return Response(courseServiceResponse.json())
            elif courseServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=courseServiceResponse.status_code)
            else:
                return Response(courseServiceResponse.json(), courseServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            courseServiceResponse = requests.delete(urlCourseService+'courses/'+id+'/')
            if courseServiceResponse.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif courseServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=courseServiceResponse.status_code)
            else:
                return Response(courseServiceResponse.json(), courseServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderList(APIView):
    def get(self, request):
        try:
            orderServiceResponse = requests.get(urlOrderService+'orders/', params = request.query_params)
            if orderServiceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, orderServiceResponse)
                # TODO: do try except for user and course services requests
                for orderData in responseData['results']:
                    # get user info
                    userId = orderData['user']
                    userInfo = getObjectFromService(urlUserService+'users/', userId)
                    if userInfo:
                        orderData['user'] = userInfo
                    # get courses info
                    courses = orderData['courses']
                    coursesResult = []
                    # Only if all information is available
                    wasNoneCourseInfo = False
                    for course in orderData['courses']:
                        if 'course_id' in course:
                            courseId = course['course_id']
                            courseInfo = getObjectFromService(urlCourseService+'courses/', courseId)
                            if courseInfo:
                                coursesResult.append(courseInfo)
                            else:
                                wasNoneCourseInfo = True
                    if wasNoneCourseInfo is False:
                        orderData['courses'] = coursesResult
                    else: # TODO: check for needs
                        wasNoneCourseInfo = False
                return Response(responseData)
            elif orderServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=orderServiceResponse.status_code)
            else:
                return Response(orderServiceResponse.json(), status=orderServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            orderServiceResponse = requests.post(urlOrderService+'orders/', json = request.data)
            if orderServiceResponse.status_code == requests.codes.created:
                return Response(orderServiceResponse.json(), status=status.HTTP_201_CREATED)
            elif orderServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=orderServiceResponse.status_code)
            else:
                return Response(orderServiceResponse.json(), status=orderServiceResponse.status_code)
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
            elif orderServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=orderServiceResponse.status_code)
            else:
                return Response(orderServiceResponse.json(), status=orderServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            orderServiceResponse = requests.put(urlOrderService+'orders/'+id+'/',
                params = request.query_params, json = request.data)
            if orderServiceResponse.status_code == requests.codes.ok:
                return Response(orderServiceResponse.json())
            elif orderServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=orderServiceResponse.status_code)
            else:
                return Response(orderServiceResponse.json(), status=orderServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            orderServiceResponse = requests.delete(urlOrderService+'orders/'+id+'/')
            if orderServiceResponse.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif orderServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=orderServiceResponse.status_code)
            else:
                return Response(orderServiceResponse.json(), status=orderServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PaymentList(APIView):
    def get(self, request):
        try:
            billingServiceResponse = requests.get(urlBillingService+'payments/', params = request.query_params)
            if billingServiceResponse.status_code == requests.codes.ok:
                responseData = fixResponsePaginationUrls(request, billingServiceResponse)
                return Response(responseData)
            elif billingServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=billingServiceResponse.status_code)
            else:
                return Response(billingServiceResponse.json(), status=billingServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        billingServiceSuccess = False
        billingServiceResponse = None
        try:
            billingServiceResponse = requests.post(urlBillingService+'payments/', json = request.data)
            if billingServiceResponse.status_code == requests.codes.created:
                billingServiceSuccess = True
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
                    else:
                        return Response(orderServiceResponse.json(), status=orderServiceResponse.status_code)
                        # TODO: ROLLBACK
            #TODO: change Response: delete body
            elif billingServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=billingServiceResponse.status_code)
            else:
                return Response(billingServiceResponse.json(), status=billingServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            if not billingServiceSuccess:
                return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
            else:
                # Rollback: delete created payment in billing service
                paymentId = billingServiceResponse.json()['id']
                if paymentId is None:
                    return Response(getServerErrorData(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                rollbackResponse = requests.delete(urlBillingService+'payments/'+str(paymentId)+'/')
                if rollbackResponse.status_code == requests.codes.no_content:
                    return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
                # TODO: billing service can become unavailable, need to process this case
                return Response(getServerErrorData(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

#TODO: fix str(id) bugs
class PaymentDetail(APIView):
    def get(self, request, id):
        try:
            billingServiceResponse = requests.get(urlBillingService+'payments/'+id+'/')
            if billingServiceResponse.status_code == requests.codes.ok:
                return Response(billingServiceResponse.json())
            elif billingServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=billingServiceResponse.status_code)
            else:
                return Response(billingServiceResponse.json(), status=billingServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            billingServiceResponse = requests.put(urlBillingService+'payments/'+id+'/', json = request.data)
            if billingServiceResponse.status_code == requests.codes.ok:
                return Response(billingServiceResponse.json())
            elif billingServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=billingServiceResponse.status_code)
            else:
                return Response(billingServiceResponse.json(), status=billingServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            billingServiceResponse = requests.delete(urlBillingService+'payments/'+id+'/')
            if billingServiceResponse.status_code == 204:
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif billingServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=billingServiceResponse.status_code)
            else:
                return Response(billingServiceResponse.json(), status=billingServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
