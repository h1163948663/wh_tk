import urllib.request
import urllib
import json
import logging

logger = logging.getLogger('apis')


def send_sms(mobile, captcha):
    # flag用于标记发送短信是否成功
    flag = True
    # 这个是短信API地址
    url = "https://open.ucpaas.com/ol/sms/sendsms"
    # 准备一下头,声明body的格式
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    # 还有我们准备用Post传的值，这里值用字典的形式
    values = {
        "sid": "074ab94b632b2edf9d450a080d72e0d2",
        "token": "6c9206a8d85a3ddb756f0d70603483fa",
        "appid": "f4a124b2dbce4a63bc487f020832716a",
        "templateid": "489849",
        "param": f"{str(captcha)},300",
        "mobile": mobile,
    }

    try:
        # 将字典格式化成bytes格式
        data = json.dumps(values).encode('utf-8')
        logger.info(f"即将发送短信: {data}")
        # 创建一个request,放入我们的地址、数据、头
        request = urllib.request.Request(url, data, headers)
        html = urllib.request.urlopen(request).read().decode('utf-8')
        # html = '{"code":"000000","count":"1","create_date":"2018-07-23 13:34:06","mobile":"15811564298","msg":"OK","smsid":"852579cbb829c08c917f162b267efce6","uid":""}'
        code = json.loads(html)["code"]
        if code == "000000":
            logger.info(f"短信发送成功：{html}")
            flag = True
        else:
            logger.info(f"短信发送失败：{html}")
            flag = False
    except Exception as ex:
        logger.info(f"出错了,错误原因：{ex}")
        flag = False
    return flag


if __name__ == "__main__":
    # 测试短信接口是否是管用
    send_sms("17673124518",'123456')