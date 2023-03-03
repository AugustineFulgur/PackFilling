from time import sleep
from globalsettings import *
from seleniumwire import webdriver #driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from seleniumwire.request import Request
from seleniumwire.request import Response
from importlib import import_module
import sys
import commentjson
import drivermodules
import argparse
import csv #写报告

sys.path.append(SCRIPT) #引入脚本路径

#配置开始 1
DESCRIPTION='''
PackFilling Version 0.3.0
'''
USAGE='''
具体的使用方式请参考README.md
插件的使用请参考ModuleIntroduction.md
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
    #由于这是单线程，请求一定是顺序的（响应不一定）
    if request.method==CONF['INDICATE'][0] and CONF['INDICATE'][1] in request.url:
        registerDict[request.id]=valuesStack[0]
        del valuesStack[0]
    if CONF['DRIVER_REQUEST_INTERCEPT']:
        import_function(CONF['DRIVER_REQUEST_INTERCEPT'],"driver_request_intercept",request,extra,extra_conf) #自定义拦截器

#响应拦截器        
def interceptExpire(request:Request,response:Response):
    #修改响应头为允许缓存，使浏览器缓存资源
    if ".js" in request.url:
        del response.headers['Cache-Control']
        response.headers['Cache-Control']="public, max-age=31536000"
    if request.method==CONF['INDICATE'][0] and CONF['INDICATE'][1] in request.url:
        print("+--输入参数：{0},返回长度:{1}，状态：{2}".format(registerDict[request.id],len(response.body),response.status_code))
        del registerDict[request.id]
    if CONF['DRIVER_RESPONSE_INTERCEPT']:
        import_function(CONF['DRIVER_RESPONSE_INTERCEPT'],"driver_response_intercept",request,response,extra,extra_conf) 

#进行一次提交
def submitOnce(_values:list): 
    valuesStack.append(_values) 
    #获取页面
    if not CONF['DRIVER_GET_TARGET']:
        drivermodules.driver_get_target(driver,CONF['TARGET'])
    else:
        import_function(CONF['DRIVER_GET_TARGET'],"driver_get_target")(driver,CONF['TARGET'],extra,extra_conf)
    if not not CONF['SLEEP_INDICATE_PATH']: #存在指示元素则等待其加载完毕
        WebDriverWait(driver,CONF['SLEEP_TIME'],0.5).until(expected_conditions.visibility_of_element_located((By.XPATH,CONF['SLEEP_INDICATE_PATH'])))
    #输入数据前的处理（主要是对数据的处理）
    if CONF['DRIVER_BEFORE_SUBMIT_VALUE']:
        _values=import_function(CONF['DRIVER_BEFORE_SUBMIT_VALUE'],"driver_before_submit_value")(_values,extra,extra_conf)
    #输入数据
    if not CONF['DRIVER_SUBMIT_VALUE']:
        drivermodules.driver_submit_value(driver,nKeys,CONF['KEYS_PATH'],_values)
    else:
        import_function(CONF['DRIVER_SUBMIT_VALUE'],"driver_submit_value")(driver,nKeys,CONF['KEYS_PATH'],_values,extra,extra_conf)
    #验证码处理
    if isIdentify: #获取验证码
        if not CONF['DRIVER_IDENTIFY_VALUE']:
            drivermodules.driver_identify_value(driver,CONF['IDENTIFY_PATH'][0],CONF['IDENTIFY_PATH'][1],extra)
        else:
            import_function(CONF['DRIVER_IDENTIFY_VALUE'],"driver_identify_value")(driver,CONF['IDENTIFY_PATH'][0],CONF['IDENTIFY_PATH'][1],extra,extra_conf) 
    #提交数据
    if not CONF['DRIVER_SUBMIT_ENTER']:
        drivermodules.driver_submit_enter(driver,CONF['SUBMIT_PATH'])
    else:
        import_function(CONF['DRIVER_SUBMIT_ENTER'],"driver_submit_enter")(driver,CONF['SUBMIT_PATH'],extra,extra_conf)
    sleep(CONF['DELAY'])
        
#（交叉爆破的）递归函数        
def rOvOr(key:int,result:list,f): 
    _diction=diction[CONF['KEYS_PATH'][key]]
    _diction.vReset() #重置游标
    while(1): #遍历本列表里的所有值
        if _diction.vNext():
            break
        else:
            _newresult=result+[_diction.this]
            #添加自己的循环，然后传递给下一个列
            if key>=nKeys-1:
                #传递到最后了，提交咯
                f(_newresult)
            else:
                rOvOr(key+1,_newresult,f)

#（音叉模式的）主循环函数
def pitchfork(key:int):
    while(1):
        _newresult=[]
        for i in range(0,key): #遍历所有字典读取下一个
            if diction[CONF['KEYS_PATH'][i]].vNext():
                _newresult==None
                break
            else:
                _newresult+=[diction[CONF['KEYS_PATH'][i]].this]
        if not _newresult:
            break
        else:
            submitOnce(_newresult)  

#写报告的函数
def writeLog(values:list): 
    try:
        if not CONF['DRIVER_LOG_INTERCEPT']:
            drivermodules.driver_log_intercept(driver,values,writer)
        else:
            import_function(CONF['DRIVER_LOG_INTERCEPT'],"driver_log_intercept")(driver,values,writer,extra,extra_conf)
    except:
        f.close() #中途报错也要关闭文件，否则之前的记录不会保存
           
class ChkVersionAction(argparse.Action):
    
    def __init__(self, nargs=0,**kwargs):
        super().__init__(nargs=nargs,**kwargs)
    
    def __call__(self,parser,namespace,values,option_name=None):
        #比较两个文件的版本数字
        import requests
        with open("version","r") as v:
            v1=float(v.read())
            v2=float(requests.get("https://github.com/AugustineFulgur/PackFilling/blob/main/version").content.decode())
        if v2>v1:
            print("此版本并非最新版本。请访问https://github.com/AugustineFulgur/PackFilling进行更新。")
        else:
            print("最新版本，无需操作。")
        exit(0) 
            
#MAIN    
if __name__=="__main__":
    CONF={}
    #配置开始
    parser=argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-run",type=str,help="配置json文件的路径（包括后缀）")
    parser.add_argument("-values",type=list,help="本次运行的额外配置，覆盖配置文件")
    parser.add_argument("-chv",nargs=0,action=ChkVersionAction,help="检查版本")
    argv=parser.parse_args()
    CONF=commentjson.loads(open(argv.run,"r",encoding="utf-8").read()) #读取配置
    extra_conf={}
    if type(argv.values)==list:
        extra_conf=CONF.update(argv.values) #配置里的额外内容
    extra={} #插件中自设定的额外配置
    if not CONF['DRIVER_INITAL']:
        extra=drivermodules.driver_inital()
    else:
        extra=import_function(CONF['DRIVER_INITAL'],"driver_inital")(extra_conf)
    diction={} #参数字典
    registerDict={} #越写越朴素（？） 存放参数与请求关系的字典 key为请求
    valuesStack=[] #一个栈
    isIdentify=False #是否需要验证码
    nKeys=None #计数
    options=webdriver.ChromeOptions()
    if CONF['EAGER']:
        options.page_load_strategy="eager" #交互式加载
    if CONF['HEADLESS']:
        options.add_argument("--headless") #无头模式
    options.add_argument('disable-blink-features=AutomationControlled') #Anti-Anti-Spider
    options.add_argument('lang=zh_CN.UTF-8')
    options.binary_location=CHROMEPATH #一步到位了
    options.add_argument('ignore-certificate-errors')#关闭SSL证书验证
    options.add_argument('-ignore -ssl-errors')
    options.set_capability("unhandledPromptBehavior","accept") #接受所有弹窗
    pref={'permissions.default.stylesheet':2} #不加载CSS
    options.add_experimental_option("prefs", pref)
    wireproxy={}
    if CONF['PROXY']:
        #设置代理
        wireproxy={
            "proxy":CONF['PROXY'] 
        }    
    driver=webdriver.Chrome(DRIVERPATH,chrome_options=options,seleniumwire_options=wireproxy)
    driver.request_interceptor=interceptRequest
    driver.response_interceptor=interceptExpire  
    #处理下参数列表
    if len(CONF['KEYS_PATH'])!=len(CONF['VALUES_PATH']):
        print("key与value参数数量不同！")
        exit(0)
    nKeys=len(CONF['KEYS_PATH'])
    if not not CONF['VALUES_TYPE']:
        if len(CONF['VALUES_TYPE'])==len(CONF['KEYS_PATH']): #三个参数长度都要相同
            for i in range(0,nKeys):
                #遍历一下
                diction[CONF['KEYS_PATH'][i]]=ValueDict(CONF['VALUES_PATH'][i],CONF['VALUES_TYPE'][i])
        else:
            print("type参数的长度有问题。")
            exit(0)
    else:
        for i in range(0,nKeys):
            diction[CONF['KEYS_PATH'][i]]=ValueDict(CONF['VALUES_PATH'][i],"1")
    if not not CONF['IDENTIFY_PATH']:
        #需要识别验证码
        isIdentify=True
    if not not CONF['OUTFILE']:
        f=open(CONF['OUTFILE'],"w",newline='')
        writer=csv.writer(f) #如果需要输出，就打开文件
        if not CONF['DRIVER_LOG_HEAD_INTERCEPT']:
            drivermodules.driver_log_head_intercept(CONF['KEYS_PATH'],writer,extra,extra_conf)
    else: writer=None 
    if CONF['MODE']=="C" or not CONF['MODE']:
        #默认模式
        rOvOr(0,[],submitOnce)
    elif CONF['MODE']=="P":
        #音叉模式
        pitchfork(nKeys)
    else:
        #没有switch的日子不好过呀
        print("请选择正确的模式！")
        exit(0) 
    if writer:
        print("将记录输出值。")
        rOvOr(0,[],writeLog)
        f.close()
    

            
