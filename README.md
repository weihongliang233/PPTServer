# PPTServer
这是一个Django后台的程序，它开放了几个接口，概述和使用方法如下。
每个人（无论是学生还是老师），都有一组信息跟他对应，分别是：
userID  Name  School Group password filename Identity
通过向url:"https://www.weihongliang.club/pptserver/"发送请求可以实现不同操作。
目前开放的操作是: 

1.check操作，用于用过ID和password来校验身份
2.modifyPassword
3.query
4.upload

请求中附带的参数都应该写在header中。
通过header中的"action"键来指定操作，比方说你想执行check操作的话，就必须得在header中创建一个键值对"action":"check"来指定。
同时，执行不同操作是需要附带不同的其它信息（通过header来指定)的，具体列表如下：

1.check操作：需要指定三个参数：userID password action。指定了以上几个参数的请求就会被处理，返回一个字符串，这个字符串有几个取值:"Student","Teacher","No ID exist", "No match"

2.modifyPassword操作：需要指定三个参数：userID password action newpassword，如果修改成功的话会返回一个字符串，是修改后的密码

3.query操作：三个参数userID password content action content,content是你要查询的该人的具体信息，如Name等,会返回该信息。

4.upload操作：应当是POST方法，指定四个参数userID password content action filename. Upload成功以后，会返回字符串'Success'

接下来附上一个样例请求，这个请求已经测试过，没有问题。

POST /pptserver/ HTTP/1.1
Host: www.weihongliang.club
userID: 320180934321
password: 222
action: upload
content: School
newpassword: 222
filename: Hongliang.xlsx
Cookie: csrftoken=bGjZy4DV5hnhEMFEFG13W7Uztvs9m5jXhQz6xSjnGBIF1wq3BF6099iF9tX5tmt7
Content-Length: 207
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="/G:/Temp/物理科学与技术学院-科普大赛.xls"
Content-Type: application/vnd.ms-excel

(data)
----WebKitFormBoundary7MA4YWxkTrZu0gW
