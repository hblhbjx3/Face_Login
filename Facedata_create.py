import csv
import sqlite3
import face_recognition

#修改人脸数据请修改sql_name!!!
sql_path = 'FaceData_0.db'  #格式 'xxx.db'
#修改人脸数据请修改sql_name!!!


#创建数据库
conn = sqlite3.connect(sql_path)
c = conn.cursor()
c.execute('''CREATE TABLE Facedata
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    DEFAULT 'NONE',
       SEX            CHAR(1),
       ENCODING     VARCHAR);''')#四个数据 ID为主键
conn.commit()
conn.close()


"""
#加载csv表格 读取初始数据库
with open('facedata.csv','r',encoding='utf8')as fp:
    # 使用列表推导式，将读取到的数据装进列表
    ID_list = [i[0] for i in csv.reader(fp)][1:]  # csv.reader 读取到的数据是list类型
    ID_list = [int(i) for i in ID_list]
    print(ID_list)
with open('facedata.csv','r',encoding='utf8')as fp:
    Name_list = [i[1] for i in csv.reader(fp)][1:]
    print(Name_list)
with open('facedata.csv','r',encoding='utf8')as fp:
    SEX_list = [i[2] for i in csv.reader(fp)][1:]
    print(SEX_list)

path_file = 'facedata'#图片库


#将csv的数据写入数据库
conn = sqlite3.connect('Facedata_1.db')
c = conn.cursor()

for i in range(len(ID_list)):
    img_path = path_file+'/'+str(ID_list[i])+'.jpg'
    #print(img_path)
    img = face_recognition.load_image_file(img_path)
    encoding = face_recognition.face_encodings(img)[0]
    encoding_list = encoding.tolist() #将encoding转为list再转为str以储存
    encoding_str = map(str,encoding_list)
    encoding_str = ','.join(encoding_str) #用，将数据分割开
    c.execute("INSERT INTO facedata (ID,NAME,SEX,ENCODING) \
       VALUES ('{}','{}','{}','{}')".format(ID_list[i], Name_list[i],SEX_list[i] ,encoding_str ))#写进表格

conn.commit()
conn.close()
"""