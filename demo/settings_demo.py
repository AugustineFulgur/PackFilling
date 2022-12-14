#单个设置文件 配置好后请使用-run选项运行

#在这里编辑爆破过程中的插件 如果还有没写到的，可以直接修改driver文件中的 **submitOnce** 函数
#模块为一个python函数 func(driver:ChromeDriver,input:str,value:str)，其具体输出输出请参照drivermodules下的同名小写函数

DRIVER_GET_TARGET="" #获取爆破页面的插件
DRIVER_BEFORE_SUBMIT_VALUE="" #提交数据前的处理
DRIVER_SUBMIT_VALUE="xpath-modules" #替代提交数据的插件
DRIVER_SUBMIT_ENTER="xpath-modules" #替代发起提交的插件
DRIVER_RESPONSE_INTERCEPT="" #替代/补充响应拦截器
DRIVER_REQUEST_INTERCEPT="" #补充请求拦截器
DRIVER_LOG_INTERCEPT="" #替代输出编写器
DRIVER_LOG_HEAD_INTERCEPT="" #替代输出行首编写器
DRIVER_IDENTIFY_VALUE="xpath-modules" #代替提交验证码的插件

#这里存放输入值，因为某些PATH包含的"会被命令行吃掉

KEYS_PATH=['document.querySelector("body > form > input[type=text]:nth-child(1)")','document.querySelector("body > form > input[type=password]:nth-child(3)")'] #需要爆破的输入框的jsPath，可输入多个
VALUES_PATH=["name.txt","123456"] #对应的值，可为单个值或字典名，类型在type中指明
VALUES_TYPE="10" #传入参数的类型拼接成的二进制，与传入的key一一对应，若为1则value值视为字典名，若不使用此项则视为所有值都为字典名，etc.value=[a,b.txt]，type="01"
IDENTIFY_PATH=['document.querySelector("body > form > input[type=text]:nth-child(5)")','/html/body/form/img'] #若需要识别验证码请使用此选项。传入[验证码输入框的jsPath,验证码图片的**XPATH**]，本插件采用ddddocr进行识别
SUBMIT_PATH='document.querySelector("body > form > input[type=submit]:nth-child(8)")' #发起提交的元素id
SLEEP_INDICATE_PATH='document.querySelector("body > form > input[type=submit]:nth-child(8)")' #等待的指示元素的XPATH，插件将在此元素被加载之后执行下一步，一般可以填写验证码图片的XPATH

#存放其他设置

PROXY="" #代理
TARGET="target" #目标路径
OUTFILE="out.csv" #输出文件路径
SLEEP_TIME=10 #最长等待时间，建议设置得比较长
DELAY=1 #提交请求后的延迟值
INDICATE=['POST','/login.action'] #需要记录的请求包的特征值，默认情况下请填写[请求方法,请求URL关键词]

#其他选项

EAGER=False #交互式加载，有验证码的时候建议关了
HEADLESS=False #无头 看不到运行过程
