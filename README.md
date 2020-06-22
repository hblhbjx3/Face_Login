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
![image]()

---
# 使用方法
### 录入模块 （图片录入/摄像头录入）
* 输入新添加人脸学号、姓名、性别（1/0）；
* 图片录入，最后需选择一张仅有一张人脸的图片；
* 摄像头录入，最后需拍摄一张图片(按下s拍照，q退出)如果未录入人脸则提示‘未录入人脸’需重新录入；
* 录入成功，根据提示按下重置按钮，更新数据库；

### 检测模块 ()
