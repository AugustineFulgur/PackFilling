#清除每次请求的cookie

from settings import *
from seleniumwire.request import Request

def driver_request_intercept(request:Request):
    del request.headers['Cookie']
    return 