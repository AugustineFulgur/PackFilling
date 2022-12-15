#在输入数据前先点击某个元素

from settings import *
from seleniumwire.webdriver import Chrome #driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

def driver_get_target(driver:Chrome,target:str,extra:dict={},extra_conf:dict={}): #获取登陆页面的处理
    if not "click-modules_element" in extra_conf:
        #没有设置
        print("未设置点击元素，请返回设置或移除此插件！")
        exit(0) 
    driver.get(target)
    WebDriverWait(driver,SLEEP_TIME,0.5).until(expected_conditions.visibility_of_element_located((By.XPATH,extra_conf["click-modules_element"])))
    driver.find_element(By.XPATH,extra_conf["click-modules_element"]).click()
    return 