# Face_Login
用于人脸识别登陆的系统(含界面)

整个系统较为基础 所有代码仅供学习使用

若有代码问题可以发邮件到 1144722271@qq.com

---
## 配置环境
* python == 3.6.2
* tensorflow-gpu == 1.13.1
* opencv-python == 4.2.0.34
* dlib == 19.9.0
* 活体检测使用[百度API接口](https://ai.baidu.com/ai-doc/FACE/yk37c1u4t)

## 界面展示
![image](https://github.com/hblhbjx3/Face_Login/blob/master/image/UI.png)

---
# 功能介绍
### 录入模块 （图片录入/摄像头录入）
* 输入新添加人脸学号、姓名、性别（1/0）；
* 图片录入，最后需选择一张仅有一张人脸的图片；
* 摄像头录入，最后需拍摄一张图片(按下s拍照，q退出)如果未录入人脸则提示‘未录入人脸’需重新录入；
* 录入成功，根据提示按下重置按钮，更新数据库；

### 检测模块 (打开摄像头/活体检测)
* 按下打开摄像头按钮，开始检测；
* 左边信息框显示‘None’表示摄像头范围内无人脸，调整摄像头位置，若摄像头无画面则重启程序，重启无效说明摄像头正被占用；
* 左边信息框显示‘unknown’表示无此人脸数据，若为新人脸数据则需录入，否则为陌生人脸，视为外来人员；
* 活体检测按钮，按下按钮进行人脸活体检测，如果无人脸则显示，未进行活体检测，若非真实人脸则显示：“活体检测未通过! ”或者“合成图检测未通过! ”，否则出错显示：“something wrong!”，若人脸通过活体检测，则显示：“通过活体&合成图检测!”；

### 登陆按钮
* 按下登陆按钮，若提示‘数据库无此人’则表示，该人未录入数据库；
* 按下登陆按钮，若提示‘图像内无人脸’，则表示需要调整摄像头位置保证拍摄到人脸；
* 按下登陆按钮的同时会进行活体检测，若人脸数据正确，且通过活体检测，则登陆成功；
* 所有登陆记录，包括失败记录都会记录在‘Login_log.txt’文件内

### 重置按钮
* 录入人脸数据后按下此按钮以更新人脸数据库

### 暂停按钮
* 暂停显示摄像头内容，并清除信息框、照片框，恢复初始显示；
* 注意：此时摄像头并未关闭，直到程序关闭摄像头资源才释放；

---
# 使用方法
测试运行(数据库为测试使用)：

### 初次运行
替换facedata中的173020001.jpg为自己照片

修改facedata.csv中第一行名字与性别

修改后直接运行“Face_Login_UI.py”，即可开始使用

### 自己人脸数据使用方法
*	数据准备：facedata导入人脸数据照片，以‘学号’命名，格式JPEG，csv存入相应的学号、姓名、性别，注意：facedata内的照片一定要与csv表格一一对应才能完成数据库的建立；
*	准备好数据后，打开Facedata_create.py文件，修改，sql_path，运行Python Facedata_create.py，进行数据库的创建，记得修改数据库名字，防止重名冲突；
*	打开num.txt将数字改为0，打开Face_Login_UI.py文件 修改__main__内的sql_path，与上一步骤一样的路径名字；
*	在修改好所有数据后即可使用自己的人脸数据库进行人脸登陆；
*	__!!! 注 !!!__：如果初次打开界面，提示‘数据有增减,请检查数据库’之类的提示，则代表数据库(.db文件)与数据列表(.csv文件)内容不匹配，在录入人后记得讲getpics内的人脸数据转移至facedata并修改csv表格数据；

__PS__:修改文件\数据后记得保存，保存！！！

access_token过期请到百度自行申请新的access_token[方法链接](https://ai.baidu.com/ai-doc/FACE/yk37c1u4t)

申请后修改Face_Live.py中的access_token值

