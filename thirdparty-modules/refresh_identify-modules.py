from settings import *
from seleniumwire.webdriver import Chrome #driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

def driver_get_target(driver:Chrome,target:str): #获取登陆页面的处理
    driver.get(target)
    WebDriverWait(driver,SLEEP_TIME,0.5).until(expected_conditions.visibility_of_element_located((By.XPATH,IDENTIFY_PATH[1])))
    driver.find_element(By.XPATH,IDENTIFY_PATH[1]).click()
    return 