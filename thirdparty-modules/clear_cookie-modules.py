#清除每次请求的cookie

from settings import *
from seleniumwire.request import Request
from seleniumwire.webdriver import Chrome
import drivermodules

def driver_get_target(driver:Chrome,target:str):
    driver.delete_all_cookies()
    drivermodules.driver_get_target(driver,target)

def driver_request_intercept(request:Request):
    del request.headers['Cookie']
    return 