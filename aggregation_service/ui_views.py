from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
import requests

from .tasks import deleteUserOrders
from .forms import CourseForm, StudentForm, OrderForm, PaymentForm
from .help_functions import (fixResponsePaginationUrls, getObjectFromService,
    getResponseErrorsForForm, getUnavailableErrorData, getServerErrorData)

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
Views for UI Templates
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
                else:
                    return render(request, 'courses_list.html',
                        {'courses': None,})
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
            return render(request, 'courses_list.html',
                {'error_msg': getServerErrorData()['error']})

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
            return render(request, 'course.html',
                {'error_msg': getServerErrorData()['error']})

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
                    return render(request, 'course.html', {'error_msg': getServerErrorData()['error'],})
                else:
                    return render(request, 'new_course.html',
                        {'error_msg': courseServiceResponse.json()['error']})
            except requests.exceptions.ConnectionError:
                return render(request, 'new_course.html',
                    {'error_msg': getUnavailableErrorData(nameCourseService)['error']})
            else:
                return render(request, 'new_course.html',
                    {'error_msg': getServerErrorData()['error']})
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
                if (courseServiceResponse.status_code == requests.codes.ok) or \
                    (courseServiceResponse.status_code == requests.codes.created):
                    courseData = courseServiceResponse.json()
                    if courseData['id']:
                        return HttpResponseRedirect(reverse('course-detail',
                            kwargs={'cid': courseData['id']}))
                elif courseServiceResponse.status_code >= 500:
                    form.add_error(None, getServerErrorData())
                    return render(request, 'new_course.html', {'course_form' : form})
                else:
                    form = getResponseErrorsForForm(form, courseServiceResponse)
                    return render(request, 'new_course.html', {'course_form' : form})
            except requests.exceptions.ConnectionError:
                form.add_error(None, getUnavailableErrorData(nameCourseService)['error'])
                return render(request, 'new_course.html', {'course_form' : form})
            else:
                return render(request, 'new_course.html',
                    {'error_msg': getServerErrorData()['error']})
        else:
            print('not valid')
            return render(request, 'new_course.html', {'course_form' : form})

class GuiDeleteCourseView(APIView):
    def post(self, request, cid):
        try:
            courseServiceResponse = requests.delete(urlCourseService+'courses/'+str(cid)+'/')
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

class GuiStudentListView(APIView):
    def get(self, request):
        try:
            userServiceResponse = requests.get(urlUserService+'users/', params = request.query_params)
            if userServiceResponse.status_code == requests.codes.ok:
                responseData = userServiceResponse.json()
                if responseData['results']:
                    return render(request, 'students_list.html',
                        {'students': responseData['results'],})
                else:
                    return render(request, 'students_list.html',
                        {'students': None,})
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
            return render(request, 'students_list.html',
                {'error_msg': getServerErrorData()['error']})

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
            return render(request, 'student.html',
                {'error_msg': getServerErrorData()['error']})

class GuiChangeStudentView(APIView):
    def get(self, request, sid=None):
        if sid:
            try:
                userServiceResponse = requests.get(urlUserService+'users/'+str(sid)+'/')
                if userServiceResponse.status_code == requests.codes.ok:
                    studentData = userServiceResponse.json()
                    if studentData['id']:
                        #TODO: change profile data (todo just copy list)
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
                    return render(request, 'new_student.html', {'error_msg': getServerErrorData()['error'],})
                else:
                    return render(request, 'new_student.html',
                        {'error_msg': userServiceResponse.json()['error']})
            except requests.exceptions.ConnectionError:
                return render(request, 'new_student.html',
                    {'error_msg': getUnavailableErrorData(nameUserService)['error']})
            else:
                return render(request, 'new_student.html',
                    {'error_msg': getServerErrorData()['error']})
        else:
            return render(request, 'new_student.html',
                {'student_form' : StudentForm(),
                'student_operation': 'Добавить нового студента'})

    def post(self, request, sid=None):
        form = StudentForm(request.data)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                print('here try to edit student')
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

                if (userServiceResponse.status_code == requests.codes.ok) or \
                    (userServiceResponse.status_code == requests.codes.created):
                    studentData = userServiceResponse.json()
                    if studentData['id']:
                        return HttpResponseRedirect(reverse('student-detail',
                            kwargs={'sid': studentData['id']}))
                elif userServiceResponse.status_code >= 500:
                    form.add_error(None, getServerErrorData())
                    return render(request, 'new_student.html', {'student_form' : form})
                else:
                    form = getResponseErrorsForForm(form, userServiceResponse)
                    return render(request, 'new_student.html', {'student_form' : form})
            except requests.exceptions.ConnectionError:
                form.add_error(None, getUnavailableErrorData(nameUserService)['error'])
                return render(request, 'new_student.html', {'student_form' : form})
            else:
                return render(request, 'new_student.html',
                    {'error_msg': getServerErrorData()['error']})
        else:
            print('not valid')
            return render(request, 'new_student.html', {'student_form' : form})

class GuiDeleteStudentView(APIView):
    def post(self, request, sid):
        try:
            userServiceResponse = requests.delete(urlUserService+'users/'+str(sid)+'/')
            if userServiceResponse.status_code == requests.codes.no_content:
                # delete user orders
                #deleteUserOrders.delay(id)
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif userServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=userServiceResponse.status_code)
            else:
                return Response(userServiceResponse.json(), status=userServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(nameUserService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
                    print(orderData)
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
                    print(orderData)
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
            return render(request, 'order.html',
                {'error_msg': getServerErrorData()['error']})

class GuiChangeOrderView(APIView):
    def get(self, request, oid=None):
        if oid:
            try:
                orderServiceResponse = requests.get(urlOrderService+'orders/'+str(oid)+'/')
                if orderServiceResponse.status_code == requests.codes.ok:
                    orderData = orderServiceResponse.json()
                    if orderData['id']:
                        orderData['order_date'] = datetime.strptime(orderData['order_date'], "%Y-%m-%d %H:%M:%S")
                        coursesCommaString = ''
                        for course in orderData['courses']:
                            if coursesCommaString:
                                coursesCommaString = coursesCommaString + ',' + str(course['course_id'])
                            else:
                                coursesCommaString = str(course['course_id'])
                        #TODO: check is paid?
                        orderData['courses'] = coursesCommaString
                        return render(request, 'new_order.html',
                            {'order_form' : OrderForm(orderData),
                            'order_operation': 'Изменить данные о order'})
                elif orderServiceResponse.status_code >= 500:
                    return render(request, 'course.html', {'error_msg': getServerErrorData()['error'],})
                else:
                    return render(request, 'course.html',
                        {'error_msg': courseServiceResponse.json()['error']})
            except requests.exceptions.ConnectionError:
                return render(request, 'new_order.html',
                    {'error_msg': getUnavailableErrorData(nameOrderService)['error']})
            else:
                return render(request, 'new_order.html',
                    {'error_msg': getServerErrorData()['error']})
        else:
            return render(request, 'new_order.html',
                {'order_form' : OrderForm(),
                'order_operation': 'Добавить новый order'})

    def post(self, request, oid=None):
        form = OrderForm(request.data)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                coursesCommaList = cd.pop('courses', None)
                if coursesCommaList:
                    coursesList = [{'course_id': int(x),} for x in coursesCommaList.split(',')]
                    cd['courses'] = coursesList
                if cd['order_date'] is not None:
                    cd['order_date'] = str(cd['order_date'])
                else:
                    cd.pop('order_date')
                print(cd)
                if oid:
                    orderServiceResponse = requests.put(urlOrderService+'orders/'+str(oid)+'/', json = cd)
                else:
                    orderServiceResponse = requests.post(urlOrderService+'orders/', json = cd)
                if (orderServiceResponse.status_code == requests.codes.ok) or \
                    (orderServiceResponse.status_code == requests.codes.created):
                    orderData = orderServiceResponse.json()
                    if orderData['id']:
                        return HttpResponseRedirect(reverse('order-detail',
                            kwargs={'oid': orderData['id']}))
                elif orderServiceResponse.status_code >= 500:
                    form.add_error(None, getServerErrorData())
                    return render(request, 'new_order.html', {'order_form' : form})
                else:
                    print(orderServiceResponse.json())
                    form = getResponseErrorsForForm(form, orderServiceResponse)
                    return render(request, 'new_order.html', {'order_form' : form})
            except requests.exceptions.ConnectionError:
                form.add_error(None, getUnavailableErrorData(nameOrderService)['error'])
                return render(request, 'new_order.html', {'order_form' : form})
            else:
                return render(request, 'new_order.html',
                    {'error_msg': getServerErrorData()['error']})
        else:
            print('not valid')
            return render(request, 'new_order.html', {'order_form' : form})

class GuiDeleteOrderView(APIView):
    def post(self, request, oid):
        try:
            orderServiceResponse = requests.delete(urlOrderService+'orders/'+str(oid)+'/')
            if orderServiceResponse.status_code == requests.codes.no_content:
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif orderServiceResponse.status_code >= 500:
                return Response(getServerErrorData(), status=orderServiceResponse.status_code)
            else:
                return Response(orderServiceResponse.json(), status=orderServiceResponse.status_code)
        except requests.exceptions.ConnectionError:
            return JsonResponse(getUnavailableErrorData(nameOrderService), status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
            return render(request, 'payments_list.html',
                {'error_msg': getServerErrorData()['error']})

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
            return render(request, 'payment.html',
                {'error_msg': getServerErrorData()['error']})

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
                    return render(request, 'new_payment.html',
                        {'error_msg': billingServiceResponse.json()['error']})
            except requests.exceptions.ConnectionError:
                return render(request, 'new_payment.html',
                    {'error_msg': getUnavailableErrorData(nameBillingService)['error']})
            else:
                return render(request, 'new_payment.html',
                    {'error_msg': getServerErrorData()['error']})
        else:
            return render(request, 'new_payment.html',
                {'payment_form' : PaymentForm(),
                'payment_operation': 'Добавить новый платеж'})

    def post(self, request, pid=None):
        form = PaymentForm(request.data)
        billingServiceSuccess = Falses
        if form.is_valid():
            try:
                cd = form.cleaned_data
                if cd['payment_date'] is not None:
                    cd['payment_date'] = str(cd['payment_date'])
                else:
                    cd.pop('payment_date')
                print(cd)
                if pid:
                    billingServiceResponse = requests.put(urlBillingService+'payments/'+str(pid)+'/', json = cd)
                else:
                    billingServiceResponse = requests.post(urlBillingService+'payments/', json = cd)
                if (billingServiceResponse.status_code == requests.codes.ok) or \
                    (billingServiceResponse.status_code == requests.codes.created):
                    print('billing success')
                    billingServiceSuccess = True
                    # change order payment status
                    paymentData = billingServiceResponse.json()
                    orderId = paymentData['order_id']
                    amountPaid = paymentData['amount_paid']
                    if (orderId is not None) and (amountPaid is not None):
                        requestStatusData = { 'is_paid' : True }
                        orderServiceResponse = requests.patch(urlOrderService+'orders/'+str(orderId)+'/',
                            json = requestStatusData, params = {'paid' : amountPaid})
                        if orderServiceResponse.status_code == requests.codes.ok:
                            #TODO: check payment status
                            return HttpResponseRedirect(reverse('payment-detail',
                                kwargs={'pid': paymentData['id']}))
                        else:
                            form = PaymentForm()
                            # TODO: ROLLBACK
                            # TODO: display errors
                            #return Response(orderServiceResponse.json(), status=orderServiceResponse.status_code)
                elif billingServiceResponse.status_code >= 500:
                    form.add_error(None, getServerErrorData())
                    return render(request, 'new_payment.html', {'payment_form' : form})
                else:
                    # Rollback: delete created payment in billing service
                    paymentId = billingServiceResponse.json()['id']
                    if paymentId is None:
                        form.add_error(None, getServerErrorData()['error'])
                        return render(request, 'new_payment.html', {'payment_form' : form})
                    rollbackResponse = requests.delete(urlBillingService+'payments/'+str(paymentId)+'/')
                    if rollbackResponse.status_code == requests.codes.no_content:
                        form.add_error(None, getUnavailableErrorData("Service")['error'])
                        return render(request, 'new_payment.html', {'payment_form' : form})
                    # TODO: billing service can become unavailable, need to process this case
                    form.add_error(None, getServerErrorData(nameBillingService)['error'])
                    return render(request, 'new_payment.html', {'payment_form' : form})
            except requests.exceptions.ConnectionError:
                # rollback: delete created payment
                if not billingServiceSuccess:
                    form.add_error(None, getUnavailableErrorData(nameBillingService)['error'])
                    return render(request, 'new_payment.html', {'payment_form' : form})
                else:
                    # Rollback: delete created payment in billing service
                    paymentId = billingServiceResponse.json()['id']
                    if paymentId is None:
                        form.add_error(None, getServerErrorData()['error'])
                        return render(request, 'new_payment.html', {'payment_form' : form})
                    rollbackResponse = requests.delete(urlBillingService+'payments/'+str(paymentId)+'/')
                    if rollbackResponse.status_code == requests.codes.no_content:
                        form.add_error(None, getUnavailableErrorData("Service")['error'])
                        return render(request, 'new_payment.html', {'payment_form' : form})
                    # TODO: billing service can become unavailable, need to process this case
                    form.add_error(None, getServerErrorData(nameBillingService)['error'])
                    return render(request, 'new_payment.html', {'payment_form' : form})
            else:
                return render(request, 'new_payment.html',
                    {'error_msg': getServerErrorData()['error']})

        return render(request, 'new_payment.html', {'payment_form' : form})

class GuiDeletePaymentView(APIView):
    def post(self, request, pid):
        try:
            billingServiceResponse = requests.delete(urlBillingService+'payments/'+str(pid)+'/')
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
