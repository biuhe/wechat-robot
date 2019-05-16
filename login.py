# encoding: utf-8

import _thread
from datetime import datetime

import itchat, time
from itchat.content import *
from apscheduler.schedulers.blocking import BlockingScheduler

# 自动登陆，命令行二维码，退出程序后暂存登陆状态
from DateUtil import get_week_day

times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

itchat.auto_login(enableCmdQR=2, hotReload=True)

# 获取指定好友
carling = itchat.search_friends(nickName='Carling')[0]['UserName']
biu = itchat.search_friends(nickName='Biu')[0]['UserName']
alpha_meow = itchat.search_chatrooms(name='阿尔法猫')[0]['UserName']

sched = BlockingScheduler()


# 阿尔法猫本体
def meow(threadName, delay):
    print('meow方法启动')

    # 监听普通消息
    @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
    def text_reply(msg):
        print('普通消息:')
        print(msg)

    # 监听群聊事件
    @itchat.msg_register(TEXT, isGroupChat=True)
    def text_reply(msg):
        print('群组：')
        print(msg)
        if msg['isAt']:
            test = msg['Text']
            act_name = msg['ActualNickName']
            if str(test).find('提醒') > 0:
                new_jobs(sched, test, act_name)

    # itchat.send_msg(notice, toUserName=biu)
    # 保持登陆状态
    itchat.run()


def jobs(threadName, delay):
    print('jobs方法启动')
    # 添加任务
    # day_of_week = 'mon-fri' 表示从周一到周五
    # 订餐 - 每周六12点、21点提醒我订一星期的饭
    sched.add_job(func=job_ordering, trigger='cron', day_of_week='sat', hour=12, minute=00)
    sched.add_job(func=job_ordering, trigger='cron', day_of_week='sat', hour=21, minute=00)
    # 午睡 - 每天中午12点45分提醒我睡觉
    sched.add_job(func=job_siesta, trigger='cron', day_of_week='mon-fri', hour=12, minute=45)
    # 种树 - 每天七点半提醒我收能量
    sched.add_job(func=job_plant_trees, trigger='cron', day_of_week='mon-fri', hour=7, minute=30)
    # 喂鸡 - 每隔4小时提醒我喂鸡
    sched.add_job(func=job_siesta, trigger='interval', hours=4, minutes=30)
    sched.start()


# 订餐提醒定时器
def job_ordering():
    ordering_url = 'http://hy.dmeiwei.com/wx/wxgetcodeurl_dczx.asp'
    notice = '现在是北京时间：' + times + " " + get_week_day(datetime.now()) \
             + '\n阿尔法猫提醒你：小嘉琳记得公司订餐呐\n' \
               '链接是:\n' + ordering_url + '\n请现在立刻马上行动起来！'
    itchat.send_msg(notice, toUserName=alpha_meow)


# 午睡提醒器
def job_siesta():
    notice = '现在是北京时间：' + times + " " + get_week_day(datetime.now()) \
             + '\n阿尔法猫提醒你：已经到午休时间啦，你们快点去睡觉觉/睡'
    itchat.send_msg(notice, toUserName=alpha_meow)


# 种树
def job_plant_trees():
    notice = '现在是北京时间：' + times + " " + get_week_day(datetime.now()) \
             + '\n阿尔法猫提醒你：快去支付宝收能量啦，不然要被偷走了'
    itchat.send_msg(notice, toUserName=alpha_meow)


# 喂鸡提醒器
def job_feeding_chickens():
    notice = '现在是北京时间：' + times + " " + get_week_day(datetime.now()) \
             + '\n阿尔法猫提醒你：要去看看鸡仔饿了没有哦'
    itchat.send_msg(notice, toUserName=alpha_meow)


# 新建提醒
def new_jobs(sched, text, act_name):
    arr = text.split('/')
    date_format = arr[1]
    date = arr[2]
    obj = arr[4]
    todo = arr[-1]

    itchat.send_msg('阿尔法猫已经收到信息了，新建了一个任务\n时间是：' + date + "\n任务内容是：" + todo, toUserName=alpha_meow)

    if date_format == 'longtime':
        t_struct = time.strptime(date, "%Y-%m-%d %H:%M:%S")
        sched.add_job(func=job_notice, trigger='date',
                      run_date=datetime(t_struct.tm_year, t_struct.tm_mon, t_struct.tm_mday,
                                        t_struct.tm_hour, t_struct.tm_min, t_struct.tm_sec),
                      args=[obj, act_name, todo])


def job_notice(obj='我', act_name=None, todo=None):
    if obj == '我':
        obj = act_name

    notice = '现在是北京时间：' + times + " " + get_week_day(datetime.now()) \
             + '\n阿尔法猫提醒你：' + todo + '\n @' + obj + '  '
    itchat.send_msg(notice, toUserName=alpha_meow)


# 创建两个线程
try:
    _thread.start_new_thread(meow, ("Thread-1", 2,))
    _thread.start_new_thread(jobs, ("Thread-2", 4,))
except:
    print("Error: unable to start thread")

while 1:
    pass

# 文件传输助手
# itchat.send('hello world', toUserName='filehelper')
