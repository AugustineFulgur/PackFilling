#输入的XPATH版本

from settings import *
from seleniumwire.webdriver import Chrome #driver
from selenium.webdriver.common.by import By

def driver_get_target(driver:Chrome,target:str): #获取登陆页面的处理
    driver.get(target)
    return 

def driver_submit_value(driver:Chrome,nKeys:int,keys:list,values:list): #输入数据的处理
    for m in range(0,nKeys):
        driver.find_element(By.XPATH,keys[m]).clear()
        driver.find_element(By.XPATH,keys[m]).send_keys(values[m])
    return
        
def driver_submit_enter(driver:Chrome,enter:str): #提交数据的处理
    driver.find_element(By.XPATH,enter).click() #点击下
    return
    
def driver_identify_value(driver:Chrome,path:str,code:str):
    driver.find_element(By.XPATH,path).clear()
    driver.find_element(By.XPATH,path).send_keys(code)
    return 