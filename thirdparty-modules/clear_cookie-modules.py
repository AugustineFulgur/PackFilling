#清除每次请求的cookie

from settings import *
from seleniumwire.request import Request
from seleniumwire.webdriver import Chrome
import drivermodules

def driver_get_target(driver:Chrome,target:str,extra={},extra_conf={}):
    driver.delete_all_cookies()
    drivermodules.driver_get_target(driver,target)

def driver_request_intercept(request:Request,extra={},extra_conf={}):
    del request.headers['Cookie']
    return 