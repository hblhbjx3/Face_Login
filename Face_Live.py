from aip import AipFace
import base64
import requests
import json
import cv2
import matplotlib.pyplot as plt

# APP_ID = '20434703'
# API_KEY = '4sG48WEs3W474fsnGL7v8Wl7'
# SECRET_KEY = 'Uj1fN2C6j7bcgvODoUGA1B8z2kobGZmX'
access_token = '24.47de152ae393cb140b90d0b65feb88c7.2592000.1594965051.282335-20434703'
#过期请修改

# 图片转码
def encoding_img(img_path):
    f = open(r'%s' % img_path, 'rb')
    # print(f.read())
    #要求为提交base64文件
    #先进行图片转换
    pic1 = base64.b64encode(f.read())
    f.close()
    params = json.dumps(
        [{"image": str(pic1, 'utf-8'), "image_type": "BASE64", "face_field": "age,beauty,spoofing", "option": "COMMON"}]
    )
    return params.encode(encoding='UTF8')

def Face_Live(img_path):
    result = '未进行活体检测' #活体检测结果
    # 图片转码
    params = encoding_img(img_path)
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceverify"
    # access_token = '24.47de152ae393cb140b90d0b65feb88c7.2592000.1594965051.282335-20434703'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}

    response = requests.post(request_url, data=params, headers=headers)
    if response:
        data = response.json()
    else:
        return result,0

    try:
        liveness = data['result']['face_liveness']
    except TypeError:
        result += '无人脸数据'
        return result,0
    # 采用千分之一误拒率的阈值
    threshold1 = data["result"]["thresholds"]["frr_1e-3"]
    flag = 0
    # 合成图概率
    spoofing = data["result"]["face_list"][0]["spoofing"]
    # 合成图阈值 （官方推荐阈值）
    threshold2 = 0.00048
    if liveness > threshold1 and spoofing < threshold2:
        result = '通过活体&合成图检测!'
        flag = 1
    elif liveness <= threshold1:
        result = "活体检测未通过!"
    elif spoofing >= threshold2:
        result = "合成图检测未通过!"
    else:
        result = 'something wrong!'

    # print(f"活体概率： {liveness}")
    # print(f"合成图概率： {spoofing}")
    # print(f"活体检测结果: {status}")

    return result,flag

# result = Face_Live(r'./getpics/173020006.jpg')
# print(result)