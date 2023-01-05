from seleniumwire.webdriver import Chrome #driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

def driver_get_target(driver:Chrome,target:str,extra={},extra_conf={}): #获取登陆页面的处理
    driver.get(target)
    WebDriverWait(driver,extra_conf['SLEEP_TIME'],0.5).until(expected_conditions.visibility_of_element_located((By.XPATH,extra_conf['IDENTIFY_PATH'][1])))
    driver.find_element(By.XPATH,extra_conf['IDENTIFY_PATH'][1]).click()
    return 