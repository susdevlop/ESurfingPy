import main
import time
import psutil as p

# 输出
def prints(msg):
    print(time.strftime("\r[%Y-%m-%d %H:%M:%S]", time.localtime()), msg, end="  ")

# 获取当前上行或下行速率
def getspeed(mode):
    if mode == "1":
        before = p.net_io_counters().bytes_sent
        time.sleep(1)
        after = p.net_io_counters().bytes_sent
    elif mode == "2":
        before = p.net_io_counters().bytes_recv
        time.sleep(1)
        after = p.net_io_counters().bytes_recv
    else:
        return False
    speed = round((after - before) / 1024 / 1024, 2)  # 转为 MB/s
    return speed

# 选择自动重登的方式
print("当前共有以下 4 种模式\n【1】上传低于指定值\n【2】下载低于指定值\n【3】间隔指定时间\n【4】手动")
while True:
    mode = input("输入选择：")
    if mode in ["1", "2", "3", "4"]:
        break
if mode in ["1", "2"]:
    # 触发网速
    while True:
        objspeed = input("输入触发重登校园网的上传或下载网速（上传一般为 1， 下载一般为 3，单位 MB/s）：")
        try:
            objspeed = float(objspeed)
            break
        except:
            continue
elif mode == "3":
    # 间隔时间
    while True:
        intervaltime = input("输入触发重登校园网的间隔时间（单位 s）：")
        try:
            intervaltime = int(intervaltime)
            break
        except:
                continue


# 上传或下载
if mode in ["1", "2"]:
    finish = 0  # 上传或下载完成
    lowspeed = 0  # 被限速
    traffic = [p.net_io_counters().bytes_sent, p.net_io_counters().bytes_recv]
    while True:
        speed = getspeed(mode)
        if mode == "1":
            thistraffic = round((p.net_io_counters().bytes_sent - traffic[0]) / 1024 / 1024, 2)
            prints("\r本次流量：{} MB  上传速度：{} MB/s  低速触发：{}/10  完成触发：{}/10".format(thistraffic, speed, lowspeed, finish))
        elif mode == "2":
            thistraffic = round((p.net_io_counters().bytes_recv - traffic[1]) / 1024 / 1024, 2)
            prints("\r本次流量：{} MB  下载速度：{} MB/s  低速触发：{}/10  完成触发：{}/10".format(thistraffic, speed, lowspeed, finish))

        if speed <= 0.1:
            finish += 1
            if finish == 10:
                input("检测到网速低于 0.1 MB/s，请确认是否已上传或下载完成，按回车继续")
                finish = 0
        elif speed < objspeed:
            finish = 0
            lowspeed += 1
            if lowspeed == 10:
                print("疑似被被限速，重新登录中")
                main.logout()
                main.login()
                # 重置
                lowspeed = 0
                finish = 0
                traffic = [p.net_io_counters().bytes_sent, p.net_io_counters().bytes_recv]
        else:
            lowspeed = 0
            finish = 0


# 间隔
if mode == "3":
    timecal = 0
    while True:
        prints("即将于 {}s 后重新登录".format(intervaltime - timecal))
        if intervaltime - timecal == 0:
            print()
            main.logout()
            main.login()
            timecal = 0
        else:
            timecal += 1
        time.sleep(1)


# 手动
if mode == "4":
    while True:
        input("按回车键以重新登录校园网")
        main.logout()
        main.login()
        continue
