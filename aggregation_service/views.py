from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from urllib.parse import urlparse, urlunparse
from datetime import datetime
import requests

from .tasks import deleteUserOrders
from .forms import CourseForm, StudentForm, PaymentForm

""" Services settings """
nameUserService = 'User service'
urlUserService = 'http://127.0.0.1:8001/'
nameCourseService = 'Course service'
urlCourseService = 'http://127.0.0.1:8002/'
nameOrderService = 'Order service'
urlOrderService = 'http://127.0.0.1:8003/'
nameBillingService = 'Billing service'
urlBillingService = 'http://127.0.0.1:8004/'

'''
Helper functions
'''

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

def getUnavailableErrorData(serviceName):
    return {'error' : '{} is unavailable.'.format(serviceName)}

def getServerErrorData():
    return {'error' : 'Unknown server error.'}


'''
Views for RESTful API
'''

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
            return JsonResponse(getUnavailableErrorData(nameUserService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameUserService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameUserService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameUserService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameUserService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameCourseService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameCourseService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameCourseService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameCourseService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameCourseService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameOrderService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameOrderService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameOrderService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameOrderService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameOrderService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameBillingService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
                return JsonResponse(getUnavailableErrorData(nameBillingService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
            else:
                # Rollback: delete created payment in billing service
                paymentId = billingServiceResponse.json()['id']
                if paymentId is None:
                    return Response(getServerErrorData(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                rollbackResponse = requests.delete(urlBillingService+'payments/'+str(paymentId)+'/')
                if rollbackResponse.status_code == requests.codes.no_content:
                    return JsonResponse(getUnavailableErrorData("Service"), status=status.HTTP_503_SERVICE_UNAVAILABLE)
                # TODO: billing service can become unavailable, need to process this case
                return Response(getServerErrorData(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
            return JsonResponse(getUnavailableErrorData(nameBillingService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameBillingService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return JsonResponse(getUnavailableErrorData(nameBillingService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


'''
Views for GUI Templates
'''

def index(request):
	return render(request, 'index.html')

def contacts(request):
    return render(request, 'contacts.html')

class GuiCourseListView(APIView):
    def get(self, request):
        try:
            courseServiceResponse = requests.get(urlCourseService+'courses/', params = request.query_params)
            if courseServiceResponse.status_code == requests.codes.ok:
                responseData = courseServiceResponse.json()
                if responseData['results']:
                    return render(request, 'courses_list.html',
                        {'courses': responseData['results'],})
            elif courseServiceResponse.status_code >= 500:
                return render(request, 'courses_list.html',
                    {'error_msg': getServerErrorData()['error'],})
            else:
                responseData = courseServiceResponse.json()
                if responseData['error']:
                    return render(request, 'courses_list.html',
                        {'error_msg': responseData['error']})
        except requests.exceptions.ConnectionError:
            return render(request, 'courses_list.html',
                {'error_msg': getUnavailableErrorData(nameCourseService)['error']})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GuiCourseDetailView(APIView):
    def get(self, request, cid):
        try:
            courseServiceResponse = requests.get(urlCourseService+'courses/'+str(cid)+'/')
            if courseServiceResponse.status_code == requests.codes.ok:
                courseData = courseServiceResponse.json()
                if courseData['id']:
                    return render(request, 'course.html', {'course': courseData,})
            elif courseServiceResponse.status_code >= 500:
                return render(request, 'course.html', {'error_msg': getServerErrorData()['error'],})
            else:
                responseData = courseServiceResponse.json()
                if responseData['error']:
                    return render(request, 'course.html', {'error_msg': responseData['error']})
        except requests.exceptions.ConnectionError:
            return render(request, 'course.html',
                {'error_msg': getUnavailableErrorData(nameCourseService)['error']})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GuiChangeCourseView(APIView):
    def get(self, request, cid=None):
        if cid:
            try:
                courseServiceResponse = requests.get(urlCourseService+'courses/'+str(cid)+'/')
                if courseServiceResponse.status_code == requests.codes.ok:
                    courseData = courseServiceResponse.json()
                    if courseData['id']:
                        return render(request, 'new_course.html',
                            {'course_form' : CourseForm(courseData),
                            'course_operation': 'Изменить данные о курсе'})
                elif courseServiceResponse.status_code >= 500:
                    # TODO: display errors
                    form = CourseForm()
                    #return Response(getServerErrorData(), status=courseServiceResponse.status_code)
                else:
                    # TODO: display errors
                    form = CourseForm()
                    #return Response(courseServiceResponse.json(), status=courseServiceResponse.status_code)
            except requests.exceptions.ConnectionError:
                # TODO: display errors
                form = CourseForm()
                #return JsonResponse(getUnavailableErrorData(nameCourseService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
            else:
                # TODO: display errors
                form = CourseForm()
                #return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return render(request, 'new_course.html',
                {'course_form' : CourseForm(),
                'course_operation': 'Добавить новый курс'})

    def post(self, request, cid=None):
        form = CourseForm(request.data)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                cd['start_date'] = str(cd['start_date'])
                cd['end_date'] = str(cd['end_date'])
                if cid:
                    courseServiceResponse = requests.put(urlCourseService+'courses/'+str(cid)+'/', json = cd)
                else:
                    courseServiceResponse = requests.post(urlCourseService+'courses/', json = cd)
                if courseServiceResponse.status_code == requests.codes.ok:
                    courseData = courseServiceResponse.json()
                    if courseData['id']:
                        return HttpResponseRedirect(reverse('course-detail',
                            kwargs={'cid': courseData['id']}))
                elif courseServiceResponse.status_code >= 500:
                    # TODO: display errors
                    form = CourseForm()
                    #return Response(getServerErrorData(), status=courseServiceResponse.status_code)
                else:
                    # TODO: display errors
                    form = CourseForm()
                    #return Response(courseServiceResponse.json(), status=courseServiceResponse.status_code)
            except requests.exceptions.ConnectionError:
                # TODO: display errors
                form = CourseForm()
                #return JsonResponse(getUnavailableErrorData(nameCourseService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
            else:
                # TODO: display errors
                form = CourseForm()
                #return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            # TODO: display errors
            form = CourseForm()
        return render(request, 'new_course.html', {'course_form' : form})

class GuiStudentListView(APIView):
    def get(self, request):
        try:
            userServiceResponse = requests.get(urlUserService+'users/', params = request.query_params)
            if userServiceResponse.status_code == requests.codes.ok:
                responseData = userServiceResponse.json()
                if responseData['results']:
                    return render(request, 'students_list.html',
                        {'students': responseData['results'],})
            elif userServiceResponse.status_code >= 500:
                return render(request, 'students_list.html',
                    {'error_msg': getServerErrorData()['error'],})
            else:
                responseData = userServiceResponse.json()
                if responseData['error']:
                    return render(request, 'students_list.html',
                        {'error_msg': responseData['error']})
        except requests.exceptions.ConnectionError:
            return render(request, 'students_list.html',
                {'error_msg': getUnavailableErrorData(nameUserService)['error']})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GuiStudentDetailView(APIView):
    def get(self, request, sid):
        try:
            userServiceResponse = requests.get(urlUserService+'users/'+str(sid)+'/')
            if userServiceResponse.status_code == requests.codes.ok:
                studentData = userServiceResponse.json()
                if studentData['id']:
                    return render(request, 'student.html', {'student': studentData,})
            elif userServiceResponse.status_code >= 500:
                return render(request, 'student.html', {'error_msg': getServerErrorData()['error'],})
            else:
                responseData = userServiceResponse.json()
                if responseData['error']:
                    return render(request, 'student.html', {'error_msg': responseData['error']})
        except requests.exceptions.ConnectionError:
            return render(request, 'student.html',
                {'error_msg': getUnavailableErrorData(nameUserService)['error']})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GuiChangeStudentView(APIView):
    def get(self, request, sid=None):
        if sid:
            try:
                userServiceResponse = requests.get(urlUserService+'users/'+str(sid)+'/')
                if userServiceResponse.status_code == requests.codes.ok:
                    studentData = userServiceResponse.json()
                    if studentData['id']:
                        #TODO: change profile data
                        studentData['phone_number'] = studentData['profile'].pop('phone_number', None)
                        studentData['birth_date'] = studentData['profile'].pop('birth_date', None)
                        studentData['height'] = studentData['profile'].pop('height', None)
                        studentData['bust'] = studentData['profile'].pop('bust', None)
                        studentData['waist'] = studentData['profile'].pop('waist', None)
                        studentData['hips'] = studentData['profile'].pop('hips', None)
                        studentData['shoe'] = studentData['profile'].pop('shoe', None)
                        studentData['eyes'] = studentData['profile'].pop('eyes', None)
                        studentData['hair'] = studentData['profile'].pop('hair', None)
                        return render(request, 'new_student.html',
                            {'student_form' : StudentForm(studentData),
                            'student_operation': 'Изменить данные о студенте'})
                elif userServiceResponse.status_code >= 500:
                    # TODO: display errors
                    form = StudentForm()
                    #return Response(getServerErrorData(), status=courseServiceResponse.status_code)
                else:
                    # TODO: display errors
                    form = StudentForm()
                    #return Response(courseServiceResponse.json(), status=courseServiceResponse.status_code)
            except requests.exceptions.ConnectionError:
                # TODO: display errors
                form = StudentForm()
                #return JsonResponse(getUnavailableErrorData(nameCourseService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
            else:
                # TODO: display errors
                form = StudentForm()
                #return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return render(request, 'new_student.html',
                {'student_form' : StudentForm(),
                'student_operation': 'Добавить нового студента'})

    def post(self, request, sid=None):
        form = StudentForm(request.data)
        if form.is_valid():
            try:
                print(10001)
                cd = form.cleaned_data
                cd['profile'] = {}
                cd['profile']['phone_number'] = cd.pop('phone_number', None)
                cd['profile']['birth_date'] = str(cd.pop('birth_date', None))
                cd['profile']['height'] = cd.pop('height', None)
                cd['profile']['bust'] = cd.pop('bust', None)
                cd['profile']['waist'] = cd.pop('waist', None)
                cd['profile']['hips'] = cd.pop('hips', None)
                cd['profile']['shoe'] = cd.pop('shoe', None)
                cd['profile']['eyes'] = cd.pop('eyes', None)
                cd['profile']['hair'] = cd.pop('hair', None)
                print(cd)
                if sid:
                    userServiceResponse = requests.put(urlUserService+'users/'+str(sid)+'/', json = cd)
                else:
                    userServiceResponse = requests.post(urlUserService+'users/', json = cd)

                if userServiceResponse.status_code == requests.codes.ok:
                    studentData = userServiceResponse.json()
                    if studentData['id']:
                        return HttpResponseRedirect(reverse('student-detail',
                            kwargs={'sid': studentData['id']}))
                elif userServiceResponse.status_code >= 500:
                    # TODO: display errors
                    form = StudentForm()
                    #return Response(getServerErrorData(), status=courseServiceResponse.status_code)
                else:
                    # TODO: display errors
                    form = StudentForm()
                    #return Response(courseServiceResponse.json(), status=courseServiceResponse.status_code)
            except requests.exceptions.ConnectionError:
            #    form.add_error(stgetUnavailableErrorData(nameUserService))
                form = StudentForm()
                #return JsonResponse(getUnavailableErrorData(nameCourseService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
            else:
                print(200)
                #form.add_error(None, "Something is wrong")
                return render(request, 'new_student.html', {'student_form' : form})
                #return Response(status=status.HTTP_400_BAD_REQUEST)
        return render(request, 'new_student.html', {'student_form' : form})

class GuiOrderListView(APIView):
    def get(self, request):
        try:
            orderServiceResponse = requests.get(urlOrderService+'orders/', params = request.query_params)
            if orderServiceResponse.status_code == requests.codes.ok:
                responseData = orderServiceResponse.json()
                # TODO: pagination
                for orderData in responseData['results']:
                    #TODO: error msg if service is unavailable
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

                    print(responseData)
                    return render(request, 'orders_list.html',
                        {'orders': responseData['results'],})

            elif orderServiceResponse.status_code >= 500:
                return render(request, 'orders_list.html',
                    {'error_msg': getServerErrorData()['error'],})
            else:
                responseData = orderServiceResponse.json()
                if responseData['error']:
                    return render(request, 'orders_list.html',
                        {'error_msg': responseData['error']})
        except requests.exceptions.ConnectionError:
            return render(request, 'orders_list.html',
                {'error_msg': getUnavailableErrorData(nameOrderService)['error']})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GuiOrderDetailView(APIView):
    def get(self, request, oid):
        try:
            orderServiceResponse = requests.get(urlOrderService+'orders/'+str(oid)+'/')
            if orderServiceResponse.status_code == requests.codes.ok:
                orderData = orderServiceResponse.json()
                if orderData['id']:
                    return render(request, 'order.html', {'order': orderData,})
            elif orderServiceResponse.status_code >= 500:
                return render(request, 'order.html', {'error_msg': getServerErrorData()['error'],})
            else:
                responseData = orderServiceResponse.json()
                if responseData['error']:
                    return render(request, 'order.html', {'error_msg': responseData['error']})
        except requests.exceptions.ConnectionError:
            return render(request, 'order.html',
                {'error_msg': getUnavailableErrorData(nameOrderService)['error']})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GuiPaymentListView(APIView):
    def get(self, request):
        try:
            billingServiceResponse = requests.get(urlBillingService+'payments/', params = request.query_params)
            if billingServiceResponse.status_code == requests.codes.ok:
                responseData = billingServiceResponse.json()
                if responseData['results']:
                    return render(request, 'payments_list.html',
                        {'payments': responseData['results'],})
            elif billingServiceResponse.status_code >= 500:
                return render(request, 'payments_list.html',
                    {'error_msg': getServerErrorData()['error'],})
            else:
                responseData = userServiceResponse.json()
                if responseData['error']:
                    return render(request, 'payments_list.html',
                        {'error_msg': responseData['error']})
        except requests.exceptions.ConnectionError:
            return render(request, 'payments_list.html',
                {'error_msg': getUnavailableErrorData(nameBillingService)['error']})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GuiPaymentDetailView(APIView):
    def get(self, request, pid):
        try:
            billingServiceResponse = requests.get(urlBillingService+'payments/'+str(pid)+'/')
            if billingServiceResponse.status_code == requests.codes.ok:
                paymentData = billingServiceResponse.json()
                if paymentData['id']:
                    return render(request, 'payment.html', {'payment': paymentData,})
            elif billingServiceResponse.status_code >= 500:
                return render(request, 'payment.html', {'error_msg': getServerErrorData()['error'],})
            else:
                responseData = billingServiceResponse.json()
                if responseData['error']:
                    return render(request, 'payment.html', {'error_msg': responseData['error']})
        except requests.exceptions.ConnectionError:
            return render(request, 'payment.html',
                {'error_msg': getUnavailableErrorData(nameBillingService)['error']})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GuiChangePaymentView(APIView):
    def get(self, request, pid=None):
        if pid:
            try:
                billingServiceResponse = requests.get(urlBillingService+'payments/'+str(pid)+'/')
                if billingServiceResponse.status_code == requests.codes.ok:
                    paymentData = billingServiceResponse.json()
                    if paymentData['id']:
                        paymentData['payment_date'] = datetime.strptime(paymentData['payment_date'], "%Y-%m-%d %H:%M:%S")
                        return render(request, 'new_payment.html',
                            {'payment_form' : PaymentForm(paymentData),
                            'payment_operation': 'Изменить данные о платеже'})
                elif billingServiceResponse.status_code >= 500:
                    # TODO: display errors
                    form = PaymentForm()
                    #return Response(getServerErrorData(), status=courseServiceResponse.status_code)
                else:
                    # TODO: display errors
                    form = PaymentForm()
                    #return Response(courseServiceResponse.json(), status=courseServiceResponse.status_code)
            except requests.exceptions.ConnectionError:
                # TODO: display errors
                form = PaymentForm()
                #return JsonResponse(getUnavailableErrorData(nameCourseService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
            else:
                # TODO: display errors
                form = PaymentForm()
                #return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return render(request, 'new_payment.html',
                {'payment_form' : PaymentForm(),
                'payment_operation': 'Добавить новый платеж'})

    def post(self, request, pid=None):
        form = PaymentForm(request.data)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                cd['payment_date'] = str(cd['payment_date'])
                if pid:
                    billingServiceResponse = requests.put(urlBillingService+'payments/'+str(pid)+'/', json = cd)
                else:
                    billingServiceResponse = requests.post(urlBillingService+'payments/', json = cd)
                if billingServiceResponse.status_code == requests.codes.ok:
                    paymentData = billingServiceResponse.json()
                    if paymentData['id']:
                        return HttpResponseRedirect(reverse('payment-detail',
                            kwargs={'pid': paymentData['id']}))
                elif billingServiceResponse.status_code >= 500:
                    # TODO: display errors
                    form = PaymentForm()
                    #return Response(getServerErrorData(), status=courseServiceResponse.status_code)
                else:
                    # TODO: display errors
                    form = PaymentForm()
                    #return Response(courseServiceResponse.json(), status=courseServiceResponse.status_code)
            except requests.exceptions.ConnectionError:
                # TODO: display errors
                form = PaymentForm()
                #return JsonResponse(getUnavailableErrorData(nameCourseService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
            else:
                # TODO: display errors
                form = PaymentForm()
                #return Response(status=status.HTTP_400_BAD_REQUEST)
        return render(request, 'new_payment.html', {'payment_form' : form})
