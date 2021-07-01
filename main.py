import json
import ESurfing

# 读取配置信息
configData = json.loads(open('config.json', 'r').read())
ESurfingURL = configData['ESurfingURL']  # 可能会出现 DNS 未能找到 IP 所以可以采用手动解析后的 IP 代替
Wlanacip = configData['Wlanacip']
Wlanuserip = configData['Wlanuserip']
Account = configData['Account']
Password = configData['Password']
Signature = configData['Signature']
Tesseract = configData['Tesseract']


# 登录
def login():
    global Signature
    result = ESurfing.login(ESurfingURL, Wlanacip, Wlanuserip, Account, Password, Tesseract)
    if not result[0]:
        input("登录过程中出错：{}".format(result[1]))
    else:
        Signature = result[1]
        with open('config.json', 'w') as confile:
            Data = {
                "ESurfingURL": ESurfingURL,
                "Wlanacip": Wlanacip,
                "Wlanuserip": Wlanuserip,
                "Account": Account,
                "Password": Password,
                "Signature": Signature,
                "Tesseract": Tesseract
            }
            confile.write(json.dumps(Data, indent=4))


# 登出
def logout():
    result = ESurfing.logout(ESurfingURL, Wlanacip, Wlanuserip, Account, Signature)
    if not result[0]:
        input(result[1])