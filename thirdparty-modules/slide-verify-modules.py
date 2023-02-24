#滑动验证码绕过
from seleniumwire.webdriver import Chrome #driver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

def driver_identify_value(driver:Chrome,slider_path:str,slider_root_path:str,extra:dict={},extra_conf:dict={}):
    #本函数中slider_path与slider_root_path分别为滑块与滑轨（那个比较大的）的元素路径 
    #对应填写的是path、img_path 也就是设置文件里
    slider=driver.find_element(By.XPATH,slider_path)
    slider_root=driver.find_element(By.XPATH,slider_root_path)
    ActionChains(driver).drag_and_drop_by_offset(slider,slider_root.size['width'],slider.size['height']).perform()