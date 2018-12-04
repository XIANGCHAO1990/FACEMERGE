import base64
import json
import requests

#在face++上注册账号然后申请api
key = ""
secret = ''

# 通过接口获取图片脸部信息
def find_face(imgpath):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    data = {"api_key":key, "api_secret":secret, "image_url": imgpath, "return_landmark":1}
    files = {"image_file":open(imgpath, 'rb')}
    response = requests.post(http_url, data=data, files=files)
    req_con = response.content.decode('utf-8')
    req_dict = json.loads(req_con)

    faces = req_dict['faces']
    list0 = faces[0]
    rectangle = list0['face_rectangle']
    return rectangle

# 获取脸部信息之后,合并,写入文件
def add_face(image_url_1, image_url_2, image_url, number):
    ff1 = find_face(image_url_1)
    ff2 = find_face(image_url_2)

    rectangle1 = str(str(ff1['top']) + "," + str(ff1['left']) + "," + str(ff1['width']) + ',' + str(ff1['height']))
    rectangle2 = str(str(ff2['top']) + "," + str(ff2['left']) + "," + str(ff2['width']) + ',' + str(ff2['height']))

    url_add = "https://api-cn.faceplusplus.com/imagepp/v1/mergeface"

    f1 = open(image_url_1, 'rb')
    f1_64 = base64.b64encode(f1.read())
    f1.close()
    f2 = open(image_url_2, 'rb')
    f2_64 = base64.b64encode(f2.read())
    f2.close()

    data = {"api_key":key, "api_secret":secret, "template_base64":f1_64, "template_rectangle":rectangle1,"merge_base64":f2_64,"merge_rectangle":rectangle2,"merge_rate":number}

    response = requests.post(url_add, data=data)
    req_con = response.content.decode('utf-8')
    req_dict = json.loads(req_con)

    result = req_dict['result']
    imgdata = base64.b64decode(result)
    file = open(image_url, 'wb')
    file.write(imgdata)
    file.close()

def add_many(list_face):
    print("正在合成第1-2张")
    image_now = r'/Users/xiangchao/Desktop/faced.jpg'
    add_face(list_face[0], list_face[1], image_now, 50)

    for index in range(2,len(list_face)):
        print("正在合成第"+str(index+1)+"张")
        add_face(image_now, list_face[index], image_now, 50)


list = []
# list.append(r'/Users/xiangchao/Desktop/jordan.jpg')
# list.append(r'/Users/xiangchao/Desktop/curry.jpg')
list.append(r'/Users/xiangchao/Desktop/kobe.jpeg')
list.append(r'/Users/xiangchao/Desktop/yaoming.jpg')
# list.append(r'/Users/xiangchao/Desktop/oneill.jpg')
add_many(list)

