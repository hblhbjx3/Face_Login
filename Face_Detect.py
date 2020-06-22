from Facedata_load import Facedata_load
import numpy as np
from tkinter import *
from PIL import Image
from PIL import ImageTk
import face_recognition
import cv2
import time
import os


camera = cv2.VideoCapture(0)
def Face_Detect(img_path,id_list,name_list,sex_list,encoding_list):

    while cv2.waitKey(1):
        success, frame = camera.read()
        cv2.imwrite(img_path, frame)
        test_locations = face_recognition.face_locations(frame)
        test_encodings = face_recognition.face_encodings(frame, test_locations)

        face_name = []
        face_score = []
        face_id = []
        face_sex = []
        for face_encoding in test_encodings:
            face_distances = face_recognition.face_distance(encoding_list, face_encoding)
            best_index = np.argmin(face_distances)

            if face_distances[best_index] <= 0.53:
                face_name.append(name_list[best_index])
                face_id.append(str(id_list[best_index]))
                if sex_list[best_index] == '0':
                    face_sex.append("female")
                else:
                    face_sex.append("male")
            else:
                face_name.append("unknown")
                face_id.append("unknown")
                face_sex.append("unknown")

            face_score.append(face_distances[best_index])

        for i, (top, right, bottom, left) in enumerate(test_locations):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # cv2.imshow("FaceReconition", frame)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # 初始图像是RGB格式，转换成BGR即可正常显示了
        # pilImage = pilImage.resize((image_width, image_height), Image.ANTIALIAS)
        try:
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(cv2image))
        except RuntimeError:
            return 0
        try:
            return imgtk,face_id[-1],face_name[-1],face_sex[-1]
        except IndexError:
            return imgtk,'None','None','None'
        # success, frame = camera.read()
    # cv2.destroyAllWindows()
    # camera.release()

def closecamera():
    camera.release()

def Enter_Face(id):
    img_path = "getpics/" + str(id) + ".jpg"
    while (camera.isOpened()):  # 循环读取每一帧
        success, frame = camera.read()  # 返回两个参数，第一个是bool是否正常打开，第二个是照片数组，如果只设置一个则变成一个tumple包含bool和图片
        cv2.imshow("Press s to save", frame)     # 窗口显示，显示名为 Capture_Test
        k = cv2.waitKey(1) & 0xFF  # 每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
        if k == ord('s'):  # 若检测到按键 ‘s’，打印字符串
            cv2.imwrite(img_path, frame)
            print("success to save" + str(id) + ".jpg")
            print("-------------------------")
            break
        elif k == ord('q'):  # 若检测到按键 ‘q’，退出
            break
    # camera.release()  # 释放摄像头
    cv2.destroyAllWindows()  # 删除建立的全部窗口
    return img_path

def Face_Detect_img(img_path,id_list,name_list,sex_list,encoding_list):
    frame = cv2.imread(img_path)

    test_locations = face_recognition.face_locations(frame)
    test_encodings = face_recognition.face_encodings(frame, test_locations)
    face_name = []
    face_id = []
    for face_encoding in test_encodings:
        face_distances = face_recognition.face_distance(encoding_list, face_encoding)
        best_index = np.argmin(face_distances)

        if face_distances[best_index] <= 0.53:
            face_name.append(name_list[best_index])
            face_id.append(str(id_list[best_index]))
        else:
            face_name.append("unknown")
            face_id.append("unknown")
    day_time = time.strftime("%Y_%m_%d", time.localtime())
    now_time = time.strftime("%H_%M_%S", time.localtime())
    dirs = "face_log/"+ day_time + "/"
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    try:
        img_path2 = dirs + face_id[-1]+ "_" + now_time + ".jpg"
    except IndexError:
        return 'NULL','None',now_time
    # print(type(img_path2))
    for i, (top, right, bottom, left) in enumerate(test_locations):
        pass

    img_save = frame[top-80:bottom+10,left-30:right+10]
    # print(img_save.shape)
    # x, y = img_save.shape[0:2]
    img_save = cv2.resize(img_save, (139, 170))
    cv2.imwrite(img_path2, img_save)
    print("success to save" + face_id[-1] + now_time  + ".jpg")
    return img_path2,face_name[-1],now_time
