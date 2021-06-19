# GDEsurfingPy

## 简介

基于 Python 实现登录和登出广东天翼校园网。

## 依赖

如果要运行此项目的 .py 文件，需要安装部分第三方模块和 Tesseract 程序。

如果要运行已经打包好的 .exe 文件，只需要安装 Tesseract 程序即可。

### 第三方模块

此项目用到了 `psutil` 、 `pytesseract` 等模块。

可以执行 `pip install psutil` 命令安装，网络不畅通可以用以下命令代替：

`pip install psutil -i http://pypi.douban.com/simple --trusted-host pypi.douban.com`

### Tesseract - 离线识别验证码

广东天翼校园网网页登录方式需要验证码，此项目调用 Tesseract 实现离线识别验证码。

[【官方】tesseract-ocr-w64-setup-v5.0.0.20190623.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0.20190623.exe)

[【分流】tesseract-ocr-w64-setup-v5.0.0.20190623.exe](https://wwa.lanzoui.com/iG1WHqhz7ni)

首先下载并安装 `Tesseract`，安装完成后打开此项目的 `config.json` 将里面的 `Tesseract` 的值改成 `Tesseract` 安装目录下的 `tesseract.exe` 的绝对路径，注意要用 \\\\ 代替 \\ 否则会报错。

实例：``C:\\Users\\Aixzk\\AppData\\Local\\Tesseract-OCR\\tesseract.exe``

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
    "Pytesseract": "C:\\Users\\Aixzk\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"
}
```

+ ESurfingURL 为校园网登录页面的部分网址

  注：在未登陆校园网的情况下访问 enet.10000.gd.cn:10001 可能会提示 DNS 服务器出错，可以在手动登陆校园网后手动 `ping enet.10000.gd.cn` 解析得到 IP，然后用 IP:端口 代替，例如 `61.140.12.23:10001`。

+ Wlanacip 和 Wlanuserip 可以在自动弹出的登录网页的网址中找到

+ Account 和 Password 为校园网账号和密码

+ Signature 用于登出，无需手动设置，在登录成功后会自动抓取
+ Pytesseract 填入 tesseract.exe 的绝对路径，需用 \\\\ 代替 \\

## 拓展

Auto.py 中有四种模式触发自动登出、登录校园网，在上传或下载大文件时**限速可通过登出又登录曲线绕过限速机制**。