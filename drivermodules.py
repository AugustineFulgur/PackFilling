from seleniumwire.webdriver import Chrome #driver
from selenium.webdriver.common.by import By
from seleniumwire.request import Request
from seleniumwire.request import Response
import ddddocr #验证码识别模块

def driver_get_target(driver:Chrome,target:str,extra:dict={},extra_conf:dict={}): #获取登陆页面的处理
    driver.get(target)
    return 

def driver_submit_value(driver:Chrome,nKeys:int,keys:list,values:list,extra:dict={},extra_conf:dict={}): #输入数据的处理
    for m in range(0,nKeys):
        #'{0}.value="";'.format(keys[m]) #清空先
        exel='{0}.value="{1}";'.format(keys[m],values[m])
        driver.execute_script(exel) #输入数据
    return
        
def driver_submit_enter(driver:Chrome,enter:str,extra:dict={},extra_conf:dict={}): #提交数据的处理
    driver.execute_script(enter+".click();") #点击下
    return
    
def driver_before_submit_value(values:list,extra:dict={},extra_conf:dict={}): #输入数据前的处理（这里的values是一次爆破的payload列表）
    #Return List
    return values

def driver_request_intercept(request:Request,extra:dict={},extra_conf:dict={}): #请求拦截器
    return 

def driver_response_intercept(request:Request,response:Response,extra:dict={},extra_conf:dict={}): #响应拦截器补充
    return

def driver_log_intercept(driver:Chrome,values:list,writer,extra:dict={},extra_conf:dict={}): #输出编写器 writer的类型是_csv._writer
    if len(extra_conf['INDICATE'])!=2:
        print("特征值参数不完整！")
        exit(0)
    request:Request
    response:Response
    iter=driver.iter_requests()
    #一个没有dowhile的语言少了很多乐趣
    while(1):
        request=next(iter) #往下查询就对了
        response=request.response
        if extra_conf['INDICATE'][1] in request.url and extra_conf['INDICATE'][0]==request.method:
            #识别出特征
            writer.writerow([str(len(response.body)),str(response.status_code),str(request.params)]+values)
            break
    return 

def driver_log_head_intercept(values:list,writer,extra:dict={},extra_conf:dict={}): #输出CSV的头部编写器
    writer.writerow(["响应长度","响应状态","请求参数"]+values)
    return 

def driver_identify_value(driver:Chrome,path:str,img_path:str,extra:dict={},extra_conf:dict={}): #验证码填写器 #extra可为任意对象
    #验证码采用ddddocr 精度一般 胜在免费 免费的东西就是好东西
    #由于ddddocr识别的图片为二进制，需要先把浏览器的验证码图片down下来，而验证码图片也有两种，一种为真正的图片，另一种为base64的图片内容，所以采用简单粗暴的方式：直接截个图
    dot=str(extra["ocr"].classification(driver.find_element(By.XPATH,img_path).screenshot_as_png))
    driver.execute_script('{0}.value="{1}";'.format(path,dot))

def driver_inital(extra_conf:dict={}): #初始化
    #这样一说，弱类型也挺方便的
    dic={}
    dic["ocr"]=ddddocr.DdddOcr(show_ad=False) #识别模块]
    return dic #返回一个dict，作为初始化的结果