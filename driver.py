from time import sleep
import shutil
from settings import * #这里修改使用的配置
from globalsettings import *
from seleniumwire import webdriver #driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from seleniumwire.request import Request
from seleniumwire.request import Response
from importlib import import_module
import ddddocr #验证码识别模块
import sys
import uuid 
import os
import drivermodules
import csv #写报告

#配置开始 1
PROG='''
WpFilling
Version 0.1.0
1.这是做什么的？\n
这是一个用于自动化处理表单填写的脚本，并带有基本的验证码识别功能，在应对WEBPACK时有奇效。\n
2.如何使用它？\n
在使用之前，请先查看globalsettings与settings文件并将其配置好。\n
JSPATH/XPATH可以在Chrome浏览器->检查元素->copy->copy JSPATH/XPATH中获得。\n
3.依赖相关\n
本脚本采用chromedriver驱动chrome浏览器，若需要更换浏览器版本，请确保下载的chromedriver与chrome的版本相适配。\n
如果需要换成其他的浏览器，目前知道的是PhantomJS不能够完成验证码识别功能（不能截图），其余浏览器及其driver需要使用者自己尝试配置。\n
4.替换运行步骤\n
若待填写的表单较为复杂，需要额外处理时，可以考虑参考drivermodules文件下的函数，在thirdparty-modules文件夹下建立同名函数并修改settings配置。\n
若如此做，脚本将执行此函数的以替代原来的函数。\n
'''

#函数部分
class ValueDict: #值的字典类
    STRING=1
    FILE=2
    TYPI_FILE="1" #文件类型的值
    
    #尊是杀鸡用牛刀
    def __init__(self,stri,typi):
        if typi==ValueDict.TYPI_FILE:
            self.filename=stri
            self.file=None 
            self.vOpenFile()
            self.type=ValueDict.FILE
            self.lastline=False #最后读取标志（最后一个是不是读过了）
        else:
            self.stri=stri
            self.type=ValueDict.STRING       
    
    def vOpenFile(self):
        if self.file:
            self.file.close()
        self.file=open(self.filename)
        
    def vReset(self): #重置游标
        if self.type==ValueDict.FILE:
            self.vOpenFile()
        self.lastline=False #重置lastline

    def vNext(self): #返回末位计数
        if self.type==ValueDict.FILE:
            _re=self.file.readline()
            if _re:
                _re=_re.replace("\n","")
                self.this=_re
                return False
            else:
                return True
        else:
            if self.lastline:
                return True #读完了
            else:
                self.lastline=not self.lastline
                self.this=self.stri
                return False

#加载方法的函数(?)
def import_function(target,function):
    return getattr(import_module("{0}.{1}".format(SCRIPT,target)),function)

#请求拦截器
def interceptRequest(request:Request):
    if DRIVER_REQUEST_INTERCEPT:
        import_function(DRIVER_REQUEST_INTERCEPT,"driver_request_intercept",request) #自定义拦截器

#响应拦截器        
def interceptExpire(request:Request,response:Response):
    #修改响应头为允许缓存，使浏览器缓存资源
    if ".js" in request.url:
        del response.headers['Cache-Control']
        response.headers['Cache-Control']="public, max-age=31536000"
    if DRIVER_RESPONSE_INTERCEPT:
        import_function(DRIVER_RESPONSE_INTERCEPT,"driver_response_intercept",request,response)
        
#获取验证码的函数        
def identifyCode(): #验证码采用ddddocr 精度一般 胜在免费 免费的东西就是好东西
    #由于ddddocr识别的图片为二进制，需要先把浏览器的验证码图片down下来，而验证码图片也有两种，一种为真正的图片，另一种为base64的图片内容，所以采用简单粗暴的方式：直接截个图
    _filename=TEMP+str(uuid.uuid4())
    driver.find_element(By.XPATH,IDENTIFY_PATH[1]).screenshot(_filename) #截屏并保存
    return str(docr.classification(open(_filename,"rb").read())) 

#进行一次提交
def submitOnce(_values:list): 
    #获取页面
    if not DRIVER_GET_TARGET:
        drivermodules.driver_get_target(driver,TARGET)
    else:
        import_function(DRIVER_GET_TARGET,"driver_get_target")(driver,TARGET)
    if not not SLEEP_INDICATE_PATH: #存在指示元素则等待其加载完毕
        WebDriverWait(driver,SLEEP_TIME,0.5).until(expected_conditions.visibility_of_element_located((By.XPATH,SLEEP_INDICATE_PATH)))
    #输入数据前的处理（主要是对数据的处理）
    if DRIVER_BEFORE_SUBMIT_VALUE:
        _values=import_function(DRIVER_BEFORE_SUBMIT_VALUE,"driver_before_submit_value")(_values)
    #输入数据
    if not DRIVER_SUBMIT_VALUE:
        drivermodules.driver_submit_value(driver,nKeys,KEYS_PATH,_values)
    else:
        import_function(DRIVER_SUBMIT_VALUE,"driver_submit_value")(driver,nKeys,KEYS_PATH,_values)
    #验证码处理
    if isIdentify:
        '{0}.value="";'.format(IDENTIFY_PATH[0])
        driver.execute_script('{0}.value="{1}";'.format(IDENTIFY_PATH[0],identifyCode())) #获取验证码
    #提交数据
    if not DRIVER_SUBMIT_ENTER:
        drivermodules.driver_submit_enter(driver,SUBMIT_PATH)
        sleep(1)
    else:
        import_function(DRIVER_SUBMIT_ENTER,"driver_submit_enter")(driver,SUBMIT_PATH)
        
#递归函数        
def rOvOr(key:int,result:list,f): 
    _diction=diction[KEYS_PATH[key]]
    _diction.vReset() #重置游标
    while(1): #遍历本列表里的所有值
        if _diction.vNext():
            break
        else:
            _newresult=result+[_diction.this]
            #添加自己的循环，然后传递给下一个列
            if key>=nKeys-1:
                #传递到最后了，提交咯
                try:
                    f(_newresult)
                except:
                    continue #不能因为网络波动停止
            else:
                rOvOr(key+1,_newresult,f)

#写报告的函数
def writeLog(values:list): 
    try:
        if not DRIVER_LOG_INTERCEPT:
            drivermodules.driver_log_intercept(driver,values,writer)
        else:
            import_function(DRIVER_LOG_INTERCEPT,"driver_log_intercept")(driver,values,writer)
    except:
        f.close() #中途报错也要关闭文件，否则之前的记录不会保存
    
if __name__=="__main__":
    #配置开始
    argvs=sys.argv[1:]
    if "-h" in argvs:
        print(PROG)
        exit(0)
    if not "-run" in argvs:
        exit(0)
    if os.path.exists(TEMP):
        shutil.rmtree(TEMP)
    os.makedirs(TEMP,777) #创建缓存目录    
    docr=ddddocr.DdddOcr(show_ad=False) #识别模块
    diction={} #参数字典
    isIdentify=False #是否需要验证码
    nKeys=None #计数
    options=webdriver.ChromeOptions()
    if EAGER:
        options.page_load_strategy="eager" #交互式加载
    if HEADLESS:
        options.add_argument("--headless") #无头模式
    options.add_argument('lang=zh_CN.UTF-8')
    options.binary_location=CHROMEPATH #一步到位了
    options.add_argument('ignore-certificate-errors')#关闭SSL证书验证
    options.add_argument('-ignore -ssl-errors')
    options.set_capability("unhandledPromptBehavior","accept") #接受所有弹窗
    pref={'permissions.default.stylesheet':2} #不加载CSS
    options.add_experimental_option("prefs", pref)
    wireproxy={}
    if PROXY:
        #设置代理
        wireproxy={
            "proxy":{
                "https":"https://"+PROXY,
                "http":"http://"+PROXY
            }
        }    
    driver=webdriver.Chrome(DRIVERPATH,chrome_options=options,seleniumwire_options=wireproxy)
    driver.response_interceptor=interceptExpire  
    #处理下参数列表
    if len(KEYS_PATH)!=len(VALUES_PATH):
        print("key与value参数数量不同！")
        exit(0)
    nKeys=len(KEYS_PATH)
    if not not VALUES_TYPE:
        if len(VALUES_TYPE)==len(KEYS_PATH): #三个参数长度都要相同
            for i in range(0,nKeys):
                #遍历一下
                diction[KEYS_PATH[i]]=ValueDict(VALUES_PATH[i],VALUES_TYPE[i])
        else:
            print("type参数的长度有问题。")
            exit(0)
    else:
        for i in range(0,nKeys):
            diction[KEYS_PATH[i]]=ValueDict(VALUES_PATH[i],"1")
    if not not IDENTIFY_PATH:
        #需要识别验证码
        isIdentify=True

    if not not OUTFILE:
        f=open(OUTFILE,"w",newline='')
        writer=csv.writer(f) #如果需要输出，就打开文件
        if not DRIVER_LOG_HEAD_INTERCEPT:
            drivermodules.driver_log_head_intercept(KEYS_PATH,writer)
    else: writer=None #没有?:的世界
    rOvOr(0,[],submitOnce)
    if writer:
        print("将记录输出值。")
        rOvOr(0,[],writeLog)
        f.close()
    

            
