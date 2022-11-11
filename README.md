# **PackFilling**
Version 0.2.0

## 安装与使用
在使用之前，您需要：
1. Python 3.8+，pip
2. 安装依赖： `pip install -r requirements.txt`
3. 获取一个Chrome以及与其版本适配的chromedriver：[下载地址](http://chromedriver.storage.googleapis.com/index.html)
4. 查看settings.py并配置
5. 使用命令`python driver.py -run`，运行脚本

## 参数
- **-run** 运行工具
- **-h** 帮助

### 1.这是做什么的？
这是一个用于自动化处理表单填写的脚本，并带有基本的验证码识别功能，在应对WEBPACK时有奇效。

### 2.如何使用它？
在使用之前，请先查看globalsettings与settings文件并将其配置好。前者是整个工具的全局设置部分，这些设置能够复用，而后者的大部分内容会随着爆破目标的改变而变化，所以是一次性的内容。也正因如此，两者被分开为两个文件。
在globalsettings文件中主要配置的是DRIVERPATH与CHROMEPATH，分别为chromedriver与chrome本体执行文件的路径。
在settings中配置的是每次爆破的参数，以下是settings文件的配置说明：
```
#-settings.py
#单个设置文件 配置好后请使用-run选项运行

#以下为插件设置，插件名为thirdparty-modules下的py文件名
DRIVER_GET_TARGET="" #【获取爆破页面】的插件 etc.在获取页面前sleep(1)
DRIVER_BEFORE_SUBMIT_VALUE="" #【提交数据前】的插件 etc.在开始输入前将字典中的所有name替换为ast
DRIVER_SUBMIT_VALUE="" #【输入数据】的插件 
DRIVER_SUBMIT_ENTER="" #【提交数据】的插件
DRIVER_RESPONSE_INTERCEPT="" #【响应拦截器】的插件，允许你在执行中捕获响应并进行相应的操作
DRIVER_REQUEST_INTERCEPT="" #【请求拦截器】的插件，允许你在执行中捕获请求并在请求发出前对其进行修改
DRIVER_LOG_INTERCEPT="" #【输出】的插件，允许你自定义输出CSV文件的编写
DRIVER_LOG_HEAD_INTERCEPT="" #【输出行首】的插件，允许你自定义输出CSV文件的文件头
DRIVER_IDENTIFY_VALUE="" #【提交验证码】的插件

#以下存放输入值 etc.输入框元素的XPATH/JSPATH 默认状态下以下所有PATH为JSPATH
#元素的JSPATH可以在浏览器中点击检查元素->copy->copy jspath获得
KEYS_PATH=['',''] #需要爆破的输入框的jsPath，可输入多个
VALUES_PATH=["",""] #对应的值，可为单个值或字典名，类型在type中指明
VALUES_TYPE="" #传入参数的类型拼接成的二进制，与传入的key一一对应，若为1则value值视为字典名，若不使用此项则视为所有值都为字典名，etc.value=[a,b.txt]，type="01"
IDENTIFY_PATH=['',''] #若需要识别验证码请使用此选项。传入[验证码输入框的jsPath,验证码图片的**XPATH**]
SUBMIT_PATH='' #发起提交的元素JSPATH
SLEEP_INDICATE_PATH='' #等待的指示元素的XPATH，脚本将在此元素被加载之后执行再进行填写与提交

#存放其他设置
PROXY="" #代理
TARGET="" #目标路径
OUTFILE="out.csv" #输出文件路径
SLEEP_TIME=10 #最长等待时间，建议设置得比较长
DELAY=1 #提交请求后的延迟值
INDICATE=['POST',''] #需要记录的请求包的特征值，默认情况下请填写[请求方法（全部大写）,请求URL关键词]

#其他选项
EAGER=False #交互式加载，有验证码的时候建议关了
HEADLESS=False #无头 看不到运行过程
```


### 3.依赖相关
本脚本采用chromedriver驱动chrome浏览器，若需要更换浏览器版本，请确保下载的chromedriver与chrome的版本相适配。
如果需要换成其他的浏览器则需要重写部分代码。目前知道的是PhantomJS不能够完成验证码识别功能（不能截图），其余浏览器及其driver需要使用者自己尝试配置。

### 4.插件
目前，使用者能够编写插件的功能有：
- 【获取爆破页面】
- 【提交数据前】
- 【输入数据】
- 【提交数据】
- 【请求拦截器】
- 【输出】
- 【输出行首】
- 【提交验证码】

插件本质上为一个py文件，其中与设置项中的插件设置名同名小写的函数即为对应步骤的插件。

> etc.若我要编写一个【获取爆破页面】的插件refresh_identify-modules，使脚本在获取爆破页面后点击一次验证码图片使其刷新，则此文件的内容应为一个函数名为driver_get_target（与DRIVER_GET_TARGET同名小写）的函数，其输入输出与drivermodules.py下的同名函数输入输出相同，参考 [refresh_identify-modules](/thirdparty-modules/refresh_identify-modules.py)。
> 在使用时，则将DRIVER_GET_TARGET项设置为其文件名refresh_identify-modules。
> 若如此做，脚本将执行此函数的以drivermodules.py中的函数。

除此之外，也有插件可以替代数个功能，例如[xpath-modules](/thirdparty-modules/xpath-modules.py)，这是因为这个插件文件内有数个函数。
若要编写插件，请参考[drivermodules](drivermodules.py)中的函数及其输入输出，作为插件对应函数的输入输出。

## 更新历史
- **0.1.0** 开天辟地，基础功能完成
- **0.2.0** 增加了终端返回请求原始参数的功能，补全README文档 