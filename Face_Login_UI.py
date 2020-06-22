from tkinter import *
import tkinter.simpledialog
import time
import cv2
import os

from Facedata_load import Facedata_load,Facedata_insert
from Face_Detect import Face_Detect,closecamera,Enter_Face,Face_Detect_img
from Face_Live import Face_Live
from tkinter import filedialog
from PIL import ImageTk
from PIL import Image

BOARD_WIDTH = 1280
BOARD_HEIGHT = 720


main = Tk()

main.title("Face_Login_System")
main.geometry('1280x720')
# 禁止改变窗口大小
main.resizable(width=False, height=False)
# 修改图标
main.iconbitmap('image/face_logo.ico')

c1 = Canvas(main, background='#DAE3F3',
    width=BOARD_WIDTH, height=BOARD_HEIGHT)
c1.pack()


#图片链接
bg_img = PhotoImage(file='image/bg_img.png')
bnt_1 = PhotoImage(file='image/bnt_1.png')
bnt_2 = PhotoImage(file='image/bnt_2.png')
bnt_3 = PhotoImage(file='image/bnt_3.png')
bnt_4 = PhotoImage(file='image/bnt_4.png')
bnt_5 = PhotoImage(file='image/bnt_5.png')
bnt_6 = PhotoImage(file='image/bnt_6.2.png')
bnt_7 = PhotoImage(file='image/bnt_7.png')
open_img = PhotoImage(file='image/open.png')
close_img = PhotoImage(file='image/close.png')
# face_img = PhotoImage(file='face_log/173020001_2020_06_17 19_24_27.jpg')
#背景
c1.create_image(BOARD_WIDTH /2, BOARD_HEIGHT/2, image=bg_img)
str_jieguo = StringVar()#结果显示
str_jieguo2 = StringVar()#登录结果显示
str_id = StringVar()
str__name = StringVar()
str_sex = StringVar()
# enter_str_id = StringVar()
# enter_str__name = StringVar()
# enter_str_sex = StringVar()
# str_id.set('unknown')
# str__name.set('unknown')
# str_sex.set('unknown')
# id_list = []
# name_list = []
# sex_list = []
# encoding_list = []

imgDict = {}
def getImgWidget(filePath):
    if os.path.exists(filePath) and os.path.isfile(filePath):
        if filePath in imgDict and imgDict[filePath]:
            return imgDict[filePath]
        img = Image.open(filePath)
        #print(img.size)
        img = ImageTk.PhotoImage(img)
        imgDict[filePath] = img
        return img
    return None
def Camera_detect():
    c2.place(relx=0.309, rely=0.411, anchor=CENTER)
    id.place(relx=0.8, rely=0.47, anchor=CENTER)
    name.place(relx=0.8, rely=0.52, anchor=CENTER)
    sex.place(relx=0.8, rely=0.57, anchor=CENTER)
    while (True):
        try:
            camera_img,face_id,face_name,face_sex = Face_Detect(img_path,id_list,name_list,sex_list,encoding_list)
        except TypeError:
            return 0
        c2.create_image(0, 0, anchor='nw', image=camera_img)
        str_id.set(face_id)
        str__name.set(face_name)
        str_sex.set(face_sex)
        main.update()
        # main.after(10)

def Close_camera():
    c2.place_forget()
    c3.place_forget()
    id.place_forget()
    name.place_forget()
    sex.place_forget()
    result2.place_forget()
    str_jieguo.set('摄像头已暂停')


def Enter_message():
    c2.place(relx=0.309, rely=0.411, anchor=CENTER)
    id = tkinter.simpledialog.askinteger(title = '获取信息',prompt='请输入学号：')
    name = tkinter.simpledialog.askstring(title='获取信息', prompt='请输入姓名：')
    sex = tkinter.simpledialog.askstring(title='获取信息', prompt='请输入性别(0/女，1/男)：')
    flag = 0
    if id!=None and name!=None and sex!=None:
        img_path = filedialog.askopenfilename()
        flag = Facedata_insert(sql_path,id,name,sex,img_path)
    else:
        pass
    if flag == 1:
        str_jieguo.set(name+'人脸添加成功'+'重置生效')
    else:
        str_jieguo.set("未录入人脸")



def Enter_message_camera():
    id = tkinter.simpledialog.askinteger(title = '获取信息',prompt='请输入学号：')
    name = tkinter.simpledialog.askstring(title='获取信息', prompt='请输入姓名：')
    sex = tkinter.simpledialog.askstring(title='获取信息', prompt='请输入性别(0/女，1/男)：')
    flag = 0
    # str_jieguo.set('按下s保存,按下q退出')
    if id!=None and name!=None and sex!=None:
        img_path = Enter_Face(id)
        flag = Facedata_insert(sql_path,id,name,sex,img_path)
    else:
        pass
    if flag == 1:
        str_jieguo.set(name+'人脸添加成功'+'重置生效')
    else:
        str_jieguo.set("未录入人脸")

def Refresh():
    id_list_new, name_list_new, sex_list_new, encoding_list_new, text = Facedata_load(csv_path, sql_path)
    id_list.append(id_list_new[-1])
    name_list.append(name_list_new[-1])
    sex_list.append(sex_list_new[-1])
    encoding_list.append(encoding_list_new[-1])
    main.update()
    str_jieguo.set('刷新成功')

def Live_detect():
    result,flag = Face_Live(img_path)
    str_jieguo.set(result)

def Face_login():
    result,flag = Face_Live(img_path)
    face_img_path,name,now_time = Face_Detect_img(img_path, id_list, name_list, sex_list, encoding_list)
    day_time = time.strftime("%Y_%m_%d", time.localtime())
    if name == 'unknown':
        result =  '登录失败' + '\n' + '[原因]数据库无此人'
        face_img = getImgWidget(face_img_path)
        c3.place(relx=0.7082, rely=0.241, anchor=CENTER)
        c3.create_image(0, 0, anchor='nw', image=face_img)
        f = open('Login_log.txt', 'a+')
        f.write('{' + day_time + '  ' + now_time + '}:' + '[登录失败]' + name)
        f.write('[原因]数据库无此人' + '\n')
        f.close()
    elif name == 'None':
        result = '登录失败' + '\n' + '[原因]图像内无人脸'
    else:
        if flag == 1:
            result = name + '\n' + '登录成功'
            face_img = getImgWidget(face_img_path)
            c3.place(relx=0.7082, rely=0.241, anchor=CENTER)
            c3.create_image(0, 0, anchor='nw', image=face_img)
            #写入日志
            f = open('Login_log.txt', 'a+')
            f.write('{' + day_time + '  ' + now_time + '}:'+'[登录成功]'+name+'\n')
            f.close()
        else:
            face_img = getImgWidget(face_img_path)
            c3.place(relx=0.7082, rely=0.241, anchor=CENTER)
            c3.create_image(0, 0, anchor='nw', image=face_img)
            #写入日志
            f = open('Login_log.txt', 'a+')
            f.write('{' + day_time + '  ' + now_time + '}:' + '[登录失败]' + name)
            f.write('[原因]' + result + '\n')
            f.close()
            result = name + '\n' + '登录失败'+ '\n' + result

    str_jieguo2.set(result)



#图片录入按钮
Button(main, text='图片录入', relief=FLAT, cursor = "hand2",bg='#DAE3F3',command =  Enter_message,
       image=bnt_1).place(relx=0.136, rely=0.895, anchor=CENTER)
#摄像头录入按钮
Button(main, text='摄像头录入', relief=FLAT, cursor = "hand2",bg='#DAE3F3',command = Enter_message_camera,
       image=bnt_2).place(relx=0.292, rely=0.895, anchor=CENTER)
#摄像头检测按钮
Button(main, text='摄像头检测', relief=FLAT, cursor = "hand2",bg='#DAE3F3', command = Camera_detect,
       image=bnt_3).place(relx=0.5, rely=0.895, anchor=CENTER)
#活体检测按钮
Button(main, text='活体检测', relief=FLAT, cursor = "hand2",bg='#DAE3F3', command = Live_detect,
       image=bnt_4).place(relx=0.656, rely=0.895, anchor=CENTER)
#数据库重置按钮
Button(main, text='数据库重置', relief=FLAT, cursor = "hand2",bg='#DAE3F3',command = Refresh,
       image=bnt_5).place(relx=0.826, rely=0.895, anchor=CENTER)
#关闭摄像头按钮
Button(main, text='关闭摄像头', relief=FLAT, cursor = "hand2",bg='#DAE3F3', command = Close_camera,
       image=bnt_6).place(relx=0.916, rely=0.895, anchor=CENTER)
#登录/录入按钮
Button(main, text='登录/录入', relief=FLAT, cursor = "hand2",bg='#F2F2F2', command = Face_login,
       image=bnt_7).place(relx=0.856, rely=0.33, anchor=CENTER)


#相机画布
c2 = Canvas(main, background='#F2F2F2',
    width=640, height=480)

c3 = Canvas(main, background='#F2F2F2',
    width=139, height=170)





# c3.create_image(0, 0, anchor='nw', image=face_img )
# c2.create_image(0, 0, anchor='nw', image=open_img )

#结果文字显示
id = Label(main, textvariable = str_id, font = ('汉仪晓波折纸体简',15), foreground = 'black',bg='white')
name = Label(main, textvariable = str__name, font = ('汉仪晓波折纸体简',15), foreground = 'black',bg='white')
sex = Label(main, textvariable = str_sex, font = ('汉仪晓波折纸体简',15), foreground = 'black',bg='white')
result = Label(main, textvariable = str_jieguo, font = ('汉仪晓波折纸体简',18), foreground = 'red',bg='#F2F2F2')
result2 = Label(main, textvariable = str_jieguo2, font = ('汉仪晓波折纸体简',16), foreground = 'red',bg='#F2F2F2')
# str_jieguo2.set('name:xxx'+'\n'+'测试结果成功')
result.place(relx=0.82, rely=0.7, anchor= CENTER)
result2.place(relx=0.856, rely=0.18, anchor= CENTER)



if __name__ == "__main__":
    csv_path = 'facedata.csv'
    sql_path = 'Facedata_0.db'
    img_path = r'./getpics/temp.jpg'

    id_list, name_list, sex_list, encoding_list, text = Facedata_load(csv_path, sql_path)
    str_jieguo.set(text)

    main.mainloop()
    closecamera()