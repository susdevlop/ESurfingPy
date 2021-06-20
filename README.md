# GDEsurfingPy

------

## 简介

基于 Python 实现登录和登出广东天翼校园网，广东天翼校园网的限速机制可以通过重新登录实现曲线破解，这是我开发这个程序的原因。

------

## 依赖

如果要运行此项目的 .py 文件，需要安装部分第三方模块和 Tesseract 程序。

如果要运行已经打包好的 .exe 文件，只需要安装 Tesseract 程序即可。

### 第三方模块

此项目用到了 `psutil` 、 `pytesseract` 、`execjs` 等模块。

可以执行 `pip install psutil` 命令安装，网络不畅通可以用豆瓣镜像源代替：

`pip install psutil -i http://pypi.douban.com/simple --trusted-host pypi.douban.com`

其他的模块替换上述命令中的 `psutil` 即可。

### Tesseract - 离线识别验证码

广东天翼校园网网页登录方式需要验证码，此项目调用 Tesseract 实现离线识别验证码。

[【官方】tesseract-ocr-w64-setup-v5.0.0.20190623.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0.20190623.exe)

[【分流】tesseract-ocr-w64-setup-v5.0.0.20190623.exe](https://wwa.lanzoui.com/iG1WHqhz7ni)

首先下载并安装 `Tesseract`，安装完成后打开此项目的 `config.json` 将里面的 `Tesseract` 的值改成 `Tesseract` 安装目录下的 `tesseract.exe` 的绝对路径，注意要用 \\\\ 代替 \\ 否则会报错。

实例：``C:\\Users\\Aixzk\\AppData\\Local\\Tesseract-OCR\\tesseract.exe``

------

## 配置

运行程序前需打开 `config.json` 填入正确的参数。

```json
{
    "ESurfingURL": "enet.10000.gd.cn:10001",
    "Wlanacip": "1.1.1.1",
    "Wlanuserip": "1.1.1.1",
    "Account": "123456789",
    "Password": "123456",
    "Signature": "XXXXXXXXXXXXXXXXXXXX",
    "Tesseract": "C:\\Users\\Aixzk\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"
}
```

+ `ESurfingURL` 为校园网登录页面的部分网址

  注：在未登陆校园网的情况下访问 `enet.10000.gd.cn:10001` 可能会提示 `DNS 服务器出错`，可以在手动登陆校园网后手动 `ping enet.10000.gd.cn` 解析得到 IP，然后用 IP:端口 代替，例如 `61.140.12.23:10001`。

+ `Wlanacip` 和 `Wlanuserip` 可以在自动弹出的登录网页的网址中找到

+ `Account` 和 `Password` 为校园网账号和密码

+ `Signature` 用于登出账号，无需手动设置，在登录成功后会自动抓取

+ `Tesseract` 用于识别验证码，填入 `tesseract.exe` 的绝对路径，需用 \\\\ 代替 \\

------

# 使用

## 自动重登

重登广东天翼校园网可以实现 ”破解“ 限速，因此我做了个自动重登的 Auto.py

Auto.py 中有四种模式可以触发重新登录校园网，分别为：

1. 上传模式，程序实时监控上行速率，在低于设定的值时自动重登校园网；
2. 下载模式，程序实时监控下行速率，在低于设定的值时自动重登校园网；
3. 间隔模式，程序每间隔设定的时间，就会自动重登校园网。
4. 手动模式，手动回车后自动重登校园网。

上传和下载模式在连续 10 次监控速率低于设定值时才会触发动作，同时为防止上传或下载完成后处于空闲状态时误判成限速状态，在连续 10 次低于 0.1 MB/s 时会暂停程序，这两判定系统在程序中有实时显示。

------

# 不足

1. 如果有网络的话识别验证码只需调用网络 API 即可，但此项目性质特殊，本身就是用于登录校园网以连接互联网。在断网识别验证码的方法中，我选择了调用 Tesseract 来实现离线识别验证码，效率实测高效，准确率也不错，但缺点是在新电脑中使用此程序时需要安装 Tesseract。
2. 登录校园网过程中需要将 账号、密码和验证码 三者拼接后经 RSA 加密计算得到 loginkey 发送到服务器请求登录，但我不懂 RSA 加密算法，因此项目通过将校园网的实现 RSA 加密的原 js 文件魔改后，使用 `execjs` 模块在 Python 中传入参数来获得 loginkey，缺点是效率会低很多。

如果对以上两点有改进想法和能力的欢迎参与开发此项目。