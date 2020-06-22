import sqlite3
import numpy as np
import face_recognition
import csv

#CSV表格数据读取
def Facedata_read_csv(csv_path):
    with open(csv_path, 'r', encoding='utf8')as fp:
        # 使用列表推导式，将读取到的数据装进列表
        ID_list = [i[0] for i in csv.reader(fp)][1:]  # csv.reader 读取到的数据是list类型
        ID_list = [int(i) for i in ID_list]
        #print(ID_list)
    with open(csv_path, 'r', encoding='utf8')as fp:
        Name_list = [i[1] for i in csv.reader(fp)][1:]
        #print(Name_list)
    with open(csv_path, 'r', encoding='utf8')as fp:
        SEX_list = [i[2] for i in csv.reader(fp)][1:]
        #print(SEX_list)
    return ID_list,Name_list,SEX_list

def Facedata_write(csv_path,sql_path):
    ID_list,Name_list,SEX_list = Facedata_read_csv(csv_path)

    path_file = 'facedata/'

    conn = sqlite3.connect(sql_path)
    c = conn.cursor()

    for i in range(len(ID_list)):
        img_path = path_file + str(ID_list[i]) + '.jpg'
        # print(img_path)
        img = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(img)[0]
        encoding_list = encoding.tolist()  # 将encoding转为list再转为str以储存
        encoding_str = map(str, encoding_list)
        encoding_str = ','.join(encoding_str)  # 用，将数据分割开
        c.execute("INSERT INTO facedata (ID,NAME,SEX,ENCODING) \
           VALUES ('{}','{}','{}','{}')".format(ID_list[i], Name_list[i], SEX_list[i], encoding_str))  # 写进表格

    conn.commit()
    conn.close()


#数据库读取
def Facedata_read_sql(sql_path):
    conn = sqlite3.connect(sql_path)
    c = conn.cursor()

    c.execute("SELECT ID,NAME,SEX,ENCODING  from Facedata")
    results = c.fetchall()
    # print(results)

    # 建立人脸数据列表
    id_list = []
    name_list = []
    sex_list = []
    encoding_list = []

    for row in results:
        # ID读取
        row_id = row[0]
        id_list.append(row_id)

        # 姓名读取
        row_name = row[1]
        name_list.append(row_name)

        # 性别读取
        row_sex = row[2]
        sex_list.append(row_sex)

        # 人脸编码数据读取
        row_encoding = row[3].strip(' ').split(',')
        row_encoding_list = list(map(float, row_encoding))
        encoding = np.array(row_encoding_list)
        encoding_list.append(encoding)
    # print ("ID_list = ", id_list, "type=",type(id_list))
    # print ("NAME_list = ", name_list, "type=",type(name_list))
    # print ("SEX_list = ", sex_list, "type=",type(sex_list))
    # print ("ENCODING_list = ", encoding_list, "type=",type(encoding_list))

    conn.close()
    return id_list,name_list,sex_list,encoding_list



#读取csv数据并与数据库数据进行对比
def Facedata_load(csv_path,sql_path):
    id_list,name_list,sex_list,encoding_list = Facedata_read_sql(sql_path)
    ID_list,Name_list,SEX_list = Facedata_read_csv(csv_path)

    #人脸数据减少 需要删除
    dif_list_del = list(set(ID_list).difference(set(id_list)))

    # 人脸数据库增加 需要添加
    dif_list_add = list(set(id_list).difference(set(ID_list)))
    text = ""

    #num文件用于判断是否为第一次运行文件
    #number=0 没有运行（或数据库被重置）
    #number=1 本次运行不是第一次运行
    t = open('num.txt', 'r')
    number = t.read()  # 递增，用来保存文件名
    t.close()

    if number == '0': #
        Facedata_write(csv_path, sql_path)
        number = '1'
        t = open('num.txt', 'w')
        t.write(number)
        t.close()
        text = "数据初次加载成功"

    elif id_list != ID_list:
        #如果数据库有改变 则提醒检查数据
        if dif_list_add and dif_list_del:
            text = "数据有增减,请检查数据库"
        elif dif_list_add:
            text = "数据有增加,请检查数据库"
        else:
            text = "数据有删减,请检查数据库"
    else:
        #数据库无修改 不进行任何操作
        text = "数据加载成功，数据无修改"
    return id_list,name_list,sex_list,encoding_list,text

def Facedata_insert(sql_path,id,name,sex,img_path):
    conn = sqlite3.connect(sql_path)
    c = conn.cursor()
    try:
        img = face_recognition.load_image_file(img_path)
    except FileNotFoundError:
        return 0
    encoding = face_recognition.face_encodings(img)[0]
    # print(encoding,type(encoding))
    encoding_list = encoding.tolist()  # 将encoding转为list再转为str以储存
    encoding_str = map(str, encoding_list)
    encoding_str = ','.join(encoding_str)  # 用，将数据分割开
    c.execute("INSERT INTO facedata (ID,NAME,SEX,ENCODING) \
               VALUES ('{}','{}','{}','{}')".format(id, name, sex, encoding_str))  # 写进表格
    conn.commit()
    conn.close()
    return 1


# id_list,name_list,sex_list,encoding_list,text = Facedata_load('facedata.csv','Facedata_0.db')
# print(text)