
import urllib.request
import os


Dict4={
'101':{'college':'文学院', 'detail':{'0':'汉语言文学','5':'戏剧影视文学'}},
'102':'历史学系',
'103':'法学院',
'104':'哲学系',
'105':'新闻传播学院',
'106':{'college':'政府管理学院', 'detail':{'0':'公共管理类', '1':'运动员班'}},
'107':'信息管理系',
'108':'社会学院',
'109':{'college':'商学院', 'detail':{'0':'经济学类', '9':'工商管理类'}},
'110':{'college':'外国语学院', 'detail':{'0':'英语系', '2':'俄语系', '3':'日语系', 
        '4':'法语系', '5':'德语系', '6':'西语系', '9':'朝鲜语系'}},
'111':'数学系',
'112':'物理学院',
'113':'化学化工学院',
'114':'生命科学学院',
'115':'地球科学与工程学院',
'116':'地理与海洋科学学院',
'117':'大气科学学院',
'118':'电子科学与工程学院',
'119':'现代工程与应用科学学院',
'120':'环境学院',
'121':'天文学系',
'122':'计算机科学与技术系',
'123':{'college':'医学院', 'detail':{'0':'临床医学', '2':'口腔医学'}},
'124':{'college':'匡亚明学院', 'detail':{'2':'匡亚明学院'}},
'125':'软件学院',
'127':{'college':'工程管理学院', 'detail':{'0':'自动化类', '9':'管理科学与工程类'}},
'128':'海外教育学院',
'129':{'college':'建筑与城市规划学院', 'detail':{'0':'建筑学', '2':'城乡规划'}},
}


def downPic(stu_id, save_path, grade, platform_num):   #str, str, int, int
    platform=[
    'http://desktop.nju.edu.cn:8080/jiaowu/',
    'http://jwas2.nju.edu.cn:8080/jiaowu/',
    'http://jwas3.nju.edu.cn:8080/jiaowu/',
    ]
    req_url=platform[platform_num]+'Data/Photos/'+str(grade)+'/'+stu_id+'.JPG'
    pic=urllib.request.urlopen(req_url)
    if pic.code==200:
        print('download %s'%stu_id)
        with open(save_path+stu_id+'.jpg', 'wb') as f1:
            f1.write(pic.read())


def download_all(grade, save_path, id_dict, platform_num):
    for depart in id_dict.items():
        if isinstance(depart[1], dict):
            os.mkdir((save_path+depart[1]['college']).encode('gbk'))
            sub_dict = depart[1]['detail']
            for sub_dp in sub_dict.items():
                os.mkdir((save_path+depart[1]['college']+'/'+sub_dp[1]).encode('gbk'))
                for id_nums in range(1, 222):
                    stu_id = str(grade*10000000+int(depart[0])*10000+int(sub_dp[0])*1000+id_nums)
                    try:
                        downPic(stu_id, save_path+depart[1]['college']+'/'+sub_dp[1]+'/', grade, platform_num)
                    except:
                        continue

        elif isinstance(depart[1],str):
            os.mkdir((save_path+depart[1]).encode('gbk'))
            for id_nums in range(1, 222):
                stu_id = str(grade*10000000+int(depart[0])*10000+id_nums)
                try:
                    downPic(stu_id, save_path+depart[1]+'/', grade, platform_num)
                except:
                    continue


if __name__ == '__main__':
    if not os.path.exists('数据'):
        os.mkdir('数据'.encode('gbk'))#not good, should check if exist.
    download_all(15, '数据/',Dict4, 2)