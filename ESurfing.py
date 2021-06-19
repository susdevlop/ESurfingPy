import re
import time
import json
import execjs
import requests
import pytesseract  # 用于图片转文字
from PIL import Image  # 用于打开图片和对图片处理

# 读取并编译 Js
RSA = execjs.compile(open("RSA.js").read())


# 带时间前缀的输出
def printfun(msg):
    print(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()), msg)


# 识别验证码（调用 Tesseract 离线识别验证码）
def codeocr(Tesseract, ObjCodeFile):
    pytesseract.pytesseract.tesseract_cmd = Tesseract
    CodeImage = Image.open(ObjCodeFile)  # 读取验证码
    CodeImage = CodeImage.convert("L")  # 转灰度
    pixdata = CodeImage.load()  # 加载
    w, h = CodeImage.size
    threshold = 160
    # 遍历所有像素，大于阈值的为黑色
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    images = CodeImage
    data = images.getdata()
    w, h = images.size
    black_point = 0
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            mid_pixel = data[w * y + x]  # 中央像素点像素值
            if mid_pixel < 50:  # 找出上下左右四个方向像素点像素值
                top_pixel = data[w * (y - 1) + x]
                left_pixel = data[w * y + (x - 1)]
                down_pixel = data[w * (y + 1) + x]
                right_pixel = data[w * y + (x + 1)]
                # 判断上下左右的黑色像素点总个数
                if top_pixel < 10:
                    black_point += 1
                if left_pixel < 10:
                    black_point += 1
                if down_pixel < 10:
                    black_point += 1
                if right_pixel < 10:
                    black_point += 1
                if black_point < 1:
                    images.putpixel((x, y), 255)
                black_point = 0

    result = pytesseract.image_to_string(images)  # 图片转文字
    resultj = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", result)  # 去除识别出来的特殊字符
    return resultj[0:4]  # 只获取前4个字符


# 登录
def login(ESurfingURL, Wlanacip, Wlanuserip, Account, Password, Tesseract):
    LogTime = {0: time.time()}
    FailTimes = 0  # 登录失败次数

    while True:
        # 获取 JSESSIONID
        try:
            printfun('正在获取 JSESSIONID ...')
            URL = 'http://{}/qs/index_gz.jsp?wlanacip={}&wlanuserip={}'.format(ESurfingURL, Wlanacip,
                                                                               Wlanuserip)
            PageContent = requests.get(URL)
            JSESSIONID = PageContent.cookies['JSESSIONID']
            # printfun('成功获取 JSESSIONID: {}'.format(JSESSIONID))
            printfun('成功获取 JSESSIONID')
        except Exception as e:
            printfun('未能获取 JSESSIONID 原因：\n{}'.format(e))
            return False, e

        while True:
            # 获取验证码
            try:
                printfun('正在获取验证码...')
                CodeIMG = re.search("/common/image_code\.jsp\?time=\d+", str(PageContent.content)).group()
                CodeURL = "http://{}{}".format(ESurfingURL, CodeIMG)
                # printfun("CODEURL: {}".format(CodeURL))
                Headers = {
                    'Cookie': 'JSESSIONID=' + JSESSIONID,
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                }
                CodeGet = requests.get(url=CodeURL, headers=Headers)
                with open('Code.jpg', 'wb') as CodeFile:  # 保存到 Code.jpg
                    CodeFile.write(CodeGet.content)
                printfun('成功获取验证码')
            except Exception as e:
                printfun('未能获取验证码，原因：\n{}'.format(e))
                return False, e

            # 识别验证码
            try:
                printfun("正在识别验证码...")
                LogTime[1] = time.time()
                CodeResult = codeocr(Tesseract, 'Code.jpg')
                TakeTime = round(time.time() - LogTime[1], 2)
                if len(CodeResult) == 4:  # 验证码识别结果不是 4 位
                    printfun("识别验证码结果：{} 耗时：{}s".format(CodeResult, TakeTime))
                    break
                printfun("识别结果不符合条件")
            except Exception as e:
                printfun("未能识别验证码，原因：\n{}".format(e))
                return False, e

        # 计算 Loginkey
        LogTime[2] = time.time()
        printfun("正在计算 Loginkey ...")
        Loginkey = RSA.call("login", Account, Password, CodeResult)
        TakeTime = round(time.time() - LogTime[2], 2)
        printfun("完成计算，耗时：{}s".format(TakeTime))

        # 发送登录请求
        printfun("发送登录请求...")
        LoginUrl = "http://{}/ajax/login".format(ESurfingURL)
        data = "loginKey=" + Loginkey + "&wlanuserip=" + Wlanuserip + "&wlanacip=" + Wlanacip
        headers = {
            'Cookie': 'loginUser={}; JSESSIONID={}'.format(Account, JSESSIONID),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        Response = requests.post(url=LoginUrl, data=data, headers=headers)
        resultCode = json.loads(Response.text)['resultCode']
        resultInfo = json.loads(Response.text)['resultInfo']
        if resultCode == "0":  # 登录成功
            TakeTime = round(time.time() - LogTime[0], 2)
            printfun("登录成功，总耗时 {}s，失败 {} 次".format(TakeTime, FailTimes))
            return True, Response.cookies['signature']
        elif resultCode == "13002000":  # 重复登录（本身已登录）
            printfun(resultInfo)
            return True, Response.cookies['signature']
        elif resultCode == "11063000":  # 验证码错误
            printfun(resultInfo)
            FailTimes += 1
            continue
        elif resultCode == "13005000":  # 请求认证超时
            printfun(resultInfo)
            FailTimes += 1
            continue
        else:  # 其他情况
            printfun('其他状态码：{}  信息：{}'.format(resultCode, resultInfo))
            return False, resultInfo


# 登出
def logout(ESurfingURL, Wlanacip, Wlanuserip, Account, Signature):
    url = 'http://{}/ajax/logout'.format(ESurfingURL)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0',
        'Cookie': 'signature={}; loginUser={}'.format(Signature, Account),
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    data = "wlanuserip=" + Wlanuserip + "&wlanacip=" + Wlanacip
    LogoutResult = requests.post(url=url, data=data, headers=headers)

    resultCode = json.loads(LogoutResult.text)['resultCode']
    resultInfo = json.loads(LogoutResult.text)['resultInfo']
    if resultCode == "0":
        printfun("登出成功")
        return True, None
    else:
        printfun("登出失败，可能 signature 参数错误，返回信息：{} {}".format(resultCode, resultInfo))
        return False, "登出失败，可能 signature 参数错误，返回信息：{} {}".format(resultCode, resultInfo)
