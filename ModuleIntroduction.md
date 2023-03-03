以下为thirdparty-modules文件夹下插件文件的介绍

## clear_cookie-modules
### 使用时机
- 【请求拦截器】
- 【获取爆破页面】
### 功能
在获取页面/提交数据时，删除cookie（时机取决于插件的使用时机）。
但在获取页面时使用此插件会永久删除cookie，提交数据时使用仅在提交的请求中删除cookie。

## refresh_identify-modules
### 使用时机
- 【获取爆破页面】
### 功能
在获取页面之后点击一次验证码图片以刷新验证码。用于刷新页面验证码不会自动刷新的情况。

## xpath-modules
### 使用时机
- 【输入数据】
- 【输入验证码】
- 【提交数据】
### 功能
使用此插件后，对应的输入path应变更为xpath。将工具模拟输入的方式从执行js代码变为selenium模拟操作，避免前端报错“未输入用户名”等。

## click-modules
### 使用时机
- 【获取爆破页面】
### 功能
使用此插件，可以在页面加载之后提交数据之前点击某个元素，适用于登陆框需要提前交互的情况。
要使用此插件，请将settings.py中EXTRA字典的key"click-modules"置为需要被点击的元素xpath。

## slide_verify-modules
### 使用时机
- 【输入验证码】
### 功能
使用此插件后，配置IDENTIFY_PATH应填写为\[滑块的元素XPATH路径,滑轨的元素XPATH路径（比较长的那条）\]。插件能够模拟滑动验证。