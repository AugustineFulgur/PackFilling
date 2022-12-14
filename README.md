# **PackFilling**
Version 0.3.0

## 安装与使用
在使用之前，您需要：
1. Python 3.8+，pip
2. 安装依赖： `pip install -r requirements.txt`
3. 获取一个Chrome以及与其版本适配的chromedriver：[下载地址](http://chromedriver.storage.googleapis.com/index.html)
4. 查看settings.py并配置
5. 使用命令`python driver.py -run [conf json文件]`，运行脚本

## 参数
- **-run \[conf\]** 运行工具
- **-h** 帮助

### 1.这是做什么的？
这是一个用于自动化处理表单填写的脚本，并带有基本的验证码识别功能，在应对WEBPACK时有奇效。

### 2.如何使用它？
在使用之前，请先查看globalsettings.py与settings.json文件并将其配置好。前者是整个工具的全局设置部分，这些设置能够复用，而后者的大部分内容会随着爆破目标的改变而变化，所以是一次性的内容。也正因如此，两者被分开为两个文件。
在globalsettings.py文件中主要配置的是DRIVERPATH与CHROMEPATH，分别为chromedriver与chrome本体执行文件的路径。
在settings.json中配置的是每次爆破的参数，可以准备多个json文件，在使用时只需要在-run后指明对应的json文件即可，settings.json文件中的参数说明请参照文件中对应的注释：

以下为一个简单的配置例子：
[Demo](/demo/demo.html)
若要爆破此表单，则应依次获得输入框及验证码图片的path，以及提交按钮的path，并拦截一次请求提交的包，获取其请求方式与URL。path的获取方式如下图所示：
![复制path](/demo/1.png)
复制后，将用户名与密码的jspath填入KEYS_PATH中，验证码输入框的jspath与验证码图片的**Xpath**依次填入IDENTIFY_PATH中。
然后，将对应输入框的字典文件路径或单个值填入VALUES_PATH。它的顺序与KEYS_PATH中的输入框顺序相同。若其中包含单个值，则需要在VALUES_TYPE中指明。
然后，将提交按钮的path输入SUBMIT_PATH，将URL输入TARGET。
最后，在INDICATE项中填入[提交的请求方法，提交的路径]，即完成设置。
设置完毕的文件如下[Settings_demo](/demo/settings_demo.py)

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
- 【输入验证码】

插件本质上为一个py文件，其中与设置项中的插件设置名同名小写的函数即为对应步骤的插件。

> etc.若我要编写一个【获取爆破页面】的插件refresh_identify-modules，使脚本在获取爆破页面后点击一次验证码图片使其刷新，则此文件的内容应为一个函数名为driver_get_target（与DRIVER_GET_TARGET同名小写）的函数，其输入输出与drivermodules.py下的同名函数输入输出相同，参考 [refresh_identify-modules](/thirdparty-modules/refresh_identify-modules.py)。
> 在使用时，则将DRIVER_GET_TARGET项设置为其文件名refresh_identify-modules。
> 若如此做，脚本将执行此函数的以drivermodules.py中的函数。

除此之外，也有插件可以替代数个功能，例如[xpath-modules](/thirdparty-modules/xpath-modules.py)，这是因为这个插件文件内有数个函数。
若要编写插件，请参考[drivermodules](drivermodules.py)中的函数及其输入输出，作为插件对应函数的输入输出。

## 更新历史
- **0.1.0** 开天辟地，基础功能完成
- **0.2.0** 增加了终端返回请求原始参数的功能，补全README文档 
- **0.3.0** 增加爆破音叉模式，修改配置文件为.json格式