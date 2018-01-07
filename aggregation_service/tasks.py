import requests, logging
from dips_aggregation_service.celery import app

""" Services urls """
urlOrderService = 'http://127.0.0.1:8003/'

@app.task
#@app.task(autoretry_for=(RequestException,), retry_backoff=True)
def deleteUserOrders(user_id):
    try:
        orderServiceResponse = requests.delete(urlOrderService+'users/'+user_id+'/orders')
        if orderServiceResponse.status_code == 204 or orderServiceResponse.status_code == 404:
            logging.info( u'Delete user orders completed' )
        else:
            logging.error( u'Delete user orders error status code' )
    except requests.exceptions.ConnectionError as exc:
        logging.warning( u'Order service is unavailable, can not delete user orders now')
        deleteUserOrders.retry(exc=exc, countdown=60) #max_retries=5)
