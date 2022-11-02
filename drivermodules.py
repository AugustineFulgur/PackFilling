from settings import *
from seleniumwire.webdriver import Chrome #driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from seleniumwire.request import Request
from seleniumwire.request import Response

def driver_get_target(driver:Chrome,target:str): #获取登陆页面的处理
    driver.get(target)
    return 

def driver_submit_value(driver:Chrome,nKeys:int,keys:list,values:list): #输入数据的处理
    for m in range(0,nKeys):
        '{0}.value="";'.format(keys[m]) #清空先
        exel='{0}.value="{1}";'.format(keys[m],values[m])
        driver.execute_script(exel) #输入数据
    return
        
def driver_submit_enter(driver:Chrome,enter:str): #提交数据的处理
    driver.execute_script(enter+".click();") #点击下
    return
    
def driver_before_submit_value(values:list): #输入数据前的处理（这里的values是一次爆破的payload列表）
    #Return List
    return values

def driver_response_intercept(request:Request,response:Response): #响应拦截器补充
    return

def driver_log_intercept(driver:Chrome,values:list,writer): #输出编写器
    if len(INDICATE)!=2:
        print("特征值参数不完整！")
        exit(0)
    request:Request
    response:Response
    iter=driver.iter_requests()
    #一个没有dowhile的语言少了很多乐趣
    while(1):
        request=next(iter) #往下查询就对了
        response=request.response
        print(request.method)
        if INDICATE[1] in request.url and INDICATE[0]==request.method:
            #识别出特征
            writer.writerow([str(len(response.body)),str(response.status_code),str(request.params)]+values)
            break
    return 

def driver_log_head_intercept(values:list,writer):
    writer.writerow(["响应长度","响应状态","请求参数"]+values)
    return 