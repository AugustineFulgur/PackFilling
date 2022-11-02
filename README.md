**WpFilling**
Version 0.1.0

## 安装与使用
安装依赖 pip install -r requirements.txt 
使用 提前配置好settings.py 然后运行 python driver.py -run

### 1.这是做什么的？
这是一个用于自动化处理表单填写的脚本，并带有基本的验证码识别功能，在应对WEBPACK时有奇效。

### 2.如何使用它？
在使用之前，请先查看globalsettings与settings文件并将其配置好。
JSPATH/XPATH可以在Chrome浏览器->检查元素->copy->copy JSPATH/XPATH中获得。

### 3.依赖相关
本脚本采用chromedriver驱动chrome浏览器，若需要更换浏览器版本，请确保下载的chromedriver与chrome的版本相适配。
如果需要换成其他的浏览器，目前知道的是PhantomJS不能够完成验证码识别功能（不能截图），其余浏览器及其driver需要使用者自己尝试配置。

### 4.替换运行步骤
若待填写的表单较为复杂，需要额外处理时，可以考虑参考drivermodules文件下的函数，在thirdparty-modules文件夹下建立同名函数并修改settings配置。
若如此做，脚本将执行此函数的以替代原来的函数。
