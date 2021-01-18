import requests
import os
import json
import time
from Crypto.Cipher import AES
import base64
import re
from urllib.parse import quote

requests = requests.session()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}
headers_form = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}
domain_name = 'http://stu.hfut.edu.cn/'
app_id = ''
app_name = ''
file_name = 'info.txt'


def get_post_url():
    url = 'http://stu.hfut.edu.cn/xsfw/sys/emapfunauth/casValidate.do?service=/xsfw/sys/swmxsyqxxsjapp/*default/index.do'
    response = requests.get(url=url, headers=headers)
    return response.url.split('?')[1]


def add_to_16(s):
    while len(s) % 16 != 0:
        s += (16 - len(s) % 16) * chr(16 - len(s) % 16)
    return str.encode(s)  # 返回bytes


def encrypt(text, key):
    aes = AES.new(str.encode(key), AES.MODE_ECB)
    encrypted_text = str(base64.encodebytes(aes.encrypt(add_to_16(text))), encoding='utf8').replace('\n', '')
    return encrypted_text


def check_user_identy(username, password, key):
    password = encrypt(password, key)
    url = 'https://cas.hfut.edu.cn/cas/policy/checkUserIdenty?username=' + username + '&password=' + password + '&_=' + get_stamp().__str__()
    r = requests.get(url=url, headers=headers)
    # print(r.headers)
    # print(r.request.headers)
    # print(r.text)
    return password


def get_stamp():
    return int(round(time.time() * 1000))


def jump_auth_with_key():
    """
    获取cookie
    :return:
    """
    jump_auth_url = 'http://stu.hfut.edu.cn/xsfw/sys/emapfunauth/casValidate.do?service=/xsfw/sys/swmxsyqxxsjapp/*default/index.do'
    requests.get(url=jump_auth_url, headers=headers)
    JSESSIONID_url = 'https://cas.hfut.edu.cn/cas/vercode'
    requests.get(url=JSESSIONID_url, headers=headers)

    LOGIN_FLAVORING_url = 'https://cas.hfut.edu.cn/cas/checkInitVercode?_=' + get_stamp().__str__()
    response = requests.get(url=LOGIN_FLAVORING_url, headers=headers)
    return response.cookies.values()[0]


def login(username, password):
    url = 'https://cas.hfut.edu.cn/cas/login?' + get_post_url()
    data = {
        'username': username,
        'captcha': '',
        'execution': 'e2s1',  # 随意
        '_eventId': 'submit',
        'password': password,
        'geolocation': '',
        'submit': '登录'
    }
    # proxy = {
    #     'http': 'http://192.168.3.14:8888',
    #     'https': 'http://192.168.3.14:8888'
    # }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }

    # response = requests.post(url=url, data=data, headers=headers, proxies=proxy, verify=False)
    response = requests.post(url=url, data=data, headers=headers)
    # print(response.url)
    # print(response.text)
    try:
        global app_id
        global app_name
        html = response.text.replace('\n', '').replace('\r', '').replace(' ', '')
        real_name = re.findall(r'"roleId":"(.+)"}}', html)[0]
        r_list = re.search(r'PATH:path,(.+),RES_SERVER:', html).group(1).replace('"', '').split(',')
        app_id = r_list[0].replace('APPID:', '')
        app_name = r_list[1].replace('APPNAME:', '')
        print('[+]你好,{}...'.format(real_name))
        return True
    except Exception as e:
        print(e.__str__())
        return False


def get_today_date():
    return time.strftime('%Y-%m-%d', time.localtime())


def judge_fill():
    # 判断是否填写了
    judge_url = 'http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/judgeTodayHasData.do'  # 判断今天是否填写
    data = 'data=%7B%22TBSJ%22%3A%22{}%22%7D'.format(get_today_date())
    response = requests.post(url=judge_url, headers=headers_form, data=data).json()
    # print(r1.text)
    # {"code":"0","msg":"成功","data":[]}
    # print(response)
    if response['data'].__len__():
        # 已经填写
        return True
    # 未填
    return False


def pre_post():
    # 为了拿到cookie
    p_url1 = 'http://stu.hfut.edu.cn/xsfw/sys/swpubapp/MobileCommon/getSelRoleConfig.do'  # qw6a
    data = 'data=%7B%22APPID%22%3A%22{}%22%2C%22APPNAME%22%3A%22{}%22%7D'.format(app_id, app_name)
    requests.post(url=p_url1, headers=headers_form, data=data)
    p_url2 = 'http://stu.hfut.edu.cn/xsfw/sys/swpubapp/MobileCommon/getMenuInfo.do'  # 5ngm
    requests.post(url=p_url2, headers=headers_form, data=data)


def pre():

    def get_desktop_id():
        url = 'http://stu.hfut.edu.cn/xsfw/sys/emappagelog/config/xggzptapp.do'
        return requests.get(url=url, headers=headers).json()[0]['id']

    def get_str_time():
        time_str = time.strftime('%H:%M:%S', time.localtime())
        return quote(time_str)
    data = [
        {
            'id': get_desktop_id(),
            "device": "pc",
            "eventTime": get_str_time(),
            "params": ''
        }
    ]
    data = 'd={}'.format(quote(json.dumps(data, ensure_ascii=False).replace(' ', ''))).replace('%2B', '+')
    url = 'http://stu.hfut.edu.cn/xsfw/sys/emappagelog/push.do'
    requests.post(url=url, headers=headers_form, data=data)


def pre1():
    url = 'http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa.do'
    response = requests.post(url=url, headers=headers_form, data='*json=1').json()
    response = requests.post(url=url, headers=headers_form, data='*json=1').json()



def fill_form(username, address):
    # 开始填写表单
    # pre_post() # 后面都使用5ngm
    # 下面开始填写表单
    pre()
    pre1()
    def make_data():
        # 提交的数据
        url = 'http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/getStuXx.do'
        data = 'data=%7B%7D'
        url1 = 'http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/getSetting.do'
        requests.post(url=url1, headers=headers_form, data=data)
        # 看看是不是这里导致显示未进行填报
        response = requests.post(url=url, headers=headers_form, data=data)
        requests.post(url=url1, headers=headers_form, data=data)
        r_json = json.loads(response.text)
        post_data = r_json['data']
        return post_data

    post_data = make_data()
    if not post_data.__len__():
        print('[+]你是第一次填写哦！第一次填写请使用客户端填写，之后再使用该工具！')
        return
    post_data['DZ_SFSB'] = '1'
    post_data.update({
        #"isToday": True,
        "GCKSRQ": "",
        "GCJSRQ": "",
        "DFHTJHBSJ": "",
        "WID": get_today_date() + '-' + username,
        "DZ_TBDZ": address,
        "BY1": "1"
    })

    data = 'data={}'.format(quote(json.dumps(post_data, ensure_ascii=False).replace(' ', '')))
    post_url = 'http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/saveStuXx.do'
    response = requests.post(url=post_url, headers=headers_form, data=data)
    print(response.text)


def query_fill_state():
    url = 'http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/getStuTbData.do'  # 每天填写的状态信息
    data = 'data=%7B%22pageNumber%22%3A1%2C%22pageSize%22%3A10%2C%22KSRQ%22%3A%22%22%2C%22JSRQ%22%3A%22%22%7D'
    response = requests.post(url=url, headers=headers_form, data=data).json()
    state_info = response['data'][0]
    print('你好，{}，你的学号：{},当前日期：{}，状态：{}，当前获得{}'.format(state_info['XM'], state_info['XSBH'], state_info['TBSJ'], state_info['DZ_SFSB_DISPLAY'], state_info['BY1_DISPLAY']))


def logout():
    requests.cookies.clear()


def pre_auto_submit():
    if not os.path.exists(file_name):
        fp = open(file_name, 'w', encoding='utf-8')
        fp.write('201xxxxx 123xxxxx 安徽省合肥市包河区亲民路 [模板示例，请删除该行]')
        fp.close()
        print('第一次使用，请在info.txt文件中按照格式添加信息哦！')
        print()
        print('地址是你在今日校园上的定位信息，所以这里你可以任意填写，火星月亮都可，（建议最好填个地址）')
        print('中间记得用一个空格隔开。。。')
        print('下面给一个模板.....')
        print('201xxxxx 123xxxxx 安徽省合肥市包河区亲民路')
        print()
        print('所以你可以在info.txt文件中添加n个人的信息，这样就可以实现批量填写了...')
        print('github:https://github.com/moddemod/Campus-daily-crack')
        os.system('pause')
        return False
    return True


def auto_submit():
    # 自动提交
    with open(file_name, 'r', encoding='utf-8') as f:
        count = 0
        while True:
            message = f.readline().strip('\n')
            if len(message) == 0:
                if count == 0:
                    print('info.txt中填写信息...')
                    return
                break
            try:
                username, password, address = tuple(message.split(' '))
            except Exception as e:
                print(e.__str__())
                print('请按照格式填写信息哦....')
                break
            count += 1
            print('[+]{}: [{} {} {}]'.format(count, username, password, address))
            key = jump_auth_with_key()
            password = check_user_identy(username, password, key)
            ok = login(username, password)
            if ok:
                pre_post()
                fill_form(username=username, address=address)
                print('提交成功！')
                query_fill_state()
                judge_fill()
            logout()
            time.sleep(2)
            os.system('cls 2>nul 1>nul')

def main():
    if not pre_auto_submit():
        return
    auto_submit()

if __name__ == '__main__':
    main()