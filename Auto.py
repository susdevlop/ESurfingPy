import main
import time
import psutil as p


# 打印
def prints(msg):
    print(time.strftime("\r[%Y-%m-%d %H:%M:%S]", time.localtime()), msg, end="  ")


# 带时间打印
def printst(msg):
    print(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()), msg)


# 获取当前上行或下行速率
def getspeed(mode):
    if mode == "upload":
        before = p.net_io_counters().bytes_sent
        time.sleep(1)
        after = p.net_io_counters().bytes_sent
    elif mode == "download":
        before = p.net_io_counters().bytes_recv
        time.sleep(1)
        after = p.net_io_counters().bytes_recv
    else:
        return False
    return round((after - before) / 1024 / 1024, 2)  # 转为 x.xx MB/s


# 监控传输速率模式
def speed_mode(mode):
    # 触发网速
    while True:
        objspeed = input("输入触发重登校园网的上传或下载网速（单位 MB/s）：")
        try:
            objspeed = float(objspeed)
            break
        except:
            continue
    lowtimes = 0  # 低速次数
    finish = 0  # 低于 0.1 MB/s 时判定疑似传输完成的次数
    traffic = [p.net_io_counters().bytes_sent, p.net_io_counters().bytes_recv]
    while True:
        speed = getspeed(mode)
        if mode == 'upload':
            thistraffic = round((p.net_io_counters().bytes_sent - traffic[0]) / 1024 / 1024, 2)
            prints("本次流量：{} MB  上传速度：{} MB/s  低速触发：{}/10  完成触发：{}/10".format(thistraffic, speed, lowtimes, finish))
        elif mode == 'download':
            speed = getspeed(mode)
            thistraffic = round((p.net_io_counters().bytes_recv - traffic[1]) / 1024 / 1024, 2)
            prints("本次流量：{} MB  下载速度：{} MB/s  低速触发：{}/10  完成触发：{}/10".format(thistraffic, speed, lowtimes, finish))
        if speed <= 0.1:  # 速率低于 0.1 MB/s ，疑似传输完成
            finish += 1
            if finish == 10:
                input("检测到网速低于 0.1 MB/s，请确认是否已上传或下载完成，按回车继续")
                finish = 0
        elif speed < objspeed:  # 速率低于指定值，疑似被限速
            finish = 0
            lowtimes += 1
            if lowtimes == 10:
                printst("疑似被限速，重新登录中")
                main.logout()
                main.login()
                # 重置
                lowtimes = 0
                finish = 0
                traffic = [p.net_io_counters().bytes_sent, p.net_io_counters().bytes_recv]
        else:  # 速率高于指定值
            lowtimes = 0
            finish = 0


# 传输达到一定量模式
def traffic_mode(mode):
    # 触发流量
    while True:
        objtraffic = input("输入触发重登校园网的上传或下载流量（单位：MB）：")
        try:
            objtraffic = int(objtraffic)
            break
        except:
            continue
    if mode == 'upload':
        traffic = p.net_io_counters().bytes_sent
        while True:
            delta = int((p.net_io_counters().bytes_sent - traffic) / 1024 / 1024)
            speed = getspeed(mode)
            prints('上传速率：{} MB/s  流量触发：{}/{} MB'.format(speed, delta, objtraffic))
            if delta >= objtraffic:
                printst("重新登录中")
                main.logout()
                main.login()
                traffic = p.net_io_counters().bytes_sent
    elif mode == 'download':
        traffic = p.net_io_counters().bytes_recv
        while True:
            delta = int((p.net_io_counters().bytes_sent - traffic) / 1024 / 1024)
            speed = getspeed(mode)
            prints('下载速率：{} MB/s  流量触发：{}/{} MB'.format(speed, delta, objtraffic))
            if delta >= objtraffic:
                printst("重新登录中")
                main.logout()
                main.login()
                traffic = p.net_io_counters().bytes_recv


def interval_mode():
    # 间隔时间
    while True:
        intervaltime = input("输入触发重登校园网的间隔时间（单位 s）：")
        try:
            intervaltime = int(intervaltime)
            break
        except:
            continue

    timecal = 0
    while True:
        prints("即将于 {}s 后重新登录".format(intervaltime - timecal))
        if intervaltime - timecal == 0:
            printst()
            main.logout()
            main.login()
            timecal = 0
        else:
            timecal += 1
        time.sleep(1)


def manual_mode():
    while True:
        input(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + ' 按回车键以重新登录校园网')
        main.logout()
        main.login()


# 选择自动重登的方式
printst('当前共有以下 6 种模式')
printst('【1】上行速率低于指定值')
printst('【2】下行速率低于指定值')
printst('【3】上传数据量达指定值')
printst('【4】下载数据量达指定值')
printst('【5】间隔指定时间')
printst('【6】手动')

while True:
    mode = input(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + ' 选择触发重登校园网的模式：')
    if mode == '1':
        speed_mode('upload')
    elif mode == '2':
        speed_mode('download')
    elif mode == '3':
        traffic_mode('upload')
    elif mode == '4':
        traffic_mode('download')
    elif mode == '5':
        interval_mode()
    elif mode == '6':
        manual_mode()
    else:
        continue
