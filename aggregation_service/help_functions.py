from rest_framework.request import Request
from rest_framework.response import Response

from urllib.parse import urlparse, urlunparse

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

def getResponseErrorsForForm(form, response):
    serviceErrors = response.json()['error']
    if isinstance(serviceErrors, dict):
        for errorDataKey in serviceErrors:
            form.add_error(errorDataKey, serviceErrors[errorDataKey])
    else:
        form.add_error(None, serviceErrors)
    return form

def getUnavailableErrorData(serviceName):
    return {'error' : '{} is unavailable.'.format(serviceName)}

def getServerErrorData():
    return {'error' : 'Unknown server error.'}
