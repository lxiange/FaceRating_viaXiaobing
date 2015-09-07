

'''What the fuck?!

this code is toooooooooo fucking ugly!!!

It seems to be written five month ago, with py2. 

I will refactor it with py3, following th PEP8.

No matter how short the code is, it shall be elegant!

As is said by etone:
"To improve you taste."

'''

Dict4={111010001:"文学院",111020001:"历史学系",111030001:"法学院",111040001:"哲学系",111050001:"新闻传播学院",111060001:"政府管理学院",111070001:"信息管理系",111080001:"社会学院",111090001:"商学院",111100001:"外国语学院",111110001:"数学系",111120001:"物理学院",111130001:"化学化工学院",111140001:"生命科学学院",111150001:"地球科学与工程学院",111160001:"地理与海洋科学学院",111170001:"大气科学学院",111180001:"电子科学与工程学院",111190001:"现代工程与应用科学学院",111200001:"环境学院",111210001:"天文学系",111220001:"计算机科学与技术系",111230001:"医学院",111240001:"匡亚明学院",111250001:"软件学院",111270001:"工程管理学院",111280001:"海外教育学院",111290001:"建筑与城市规划学院"}



grade=14

import urllib
import os
os.mkdir('temp')
depart=9
suffix=9
for iii in range(1,32):
    #if iii==10 : continue
    depart=iii*10+suffix
    #print depart
    
    for num in range(100):
        stu_id=grade*10000000+1000000+depart*1000+num
        url='http://desktop.nju.edu.cn:8080/jiaowu/Data/Photos/'+str(grade)+'/'+str(stu_id)+'.JPG'
        #print url
        #print "download", num
        pic=urllib.urlopen(url)
        if pic.code==200 :
            print 'download', stu_id
            file("temp\\%d.jpg" %stu_id, "wb").write(pic.read())



