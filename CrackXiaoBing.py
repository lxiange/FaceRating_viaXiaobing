# -*- coding: utf-8 -*-
#CrackXiaoBing
import base64, json, time, os, threading, re
import urllib.parse, urllib.request
from PIL import Image

def getRawImgUrl(infile):
    file_in=open(infile,'rb')
    img_base64=base64.b64encode(file_in.read())
    file_in.close()

    uploadUrl='http://kan.msxiaobing.com/Api/Image/UploadBase64'
    resp=urllib.request.urlopen(uploadUrl,data=img_base64)
    imgUrl='http://imageplatform.trafficmanager.cn'+json.loads(resp.read().decode('utf-8'))['Url']
    return imgUrl

def getRespImgUrl(imgUrl):
    sys_time=int(time.time())
    CompUrl='http://kan.msxiaobing.com/Api/ImageAnalyze/Comparison'
    form={
        'msgId':str(sys_time)+'233',
        'timestamp':sys_time,
        'senderId':'mtuId'+str(sys_time-242)+'717',
        'content[imageUrl]':imgUrl,
        }
    
    resp=urllib.request.urlopen(CompUrl,data=urllib.parse.urlencode(form).encode('utf-8'))
    respUrl=json.loads(resp.read().decode('utf-8'))['content']['imageUrl']
    return respUrl

def saveUrlAsFile(respurl,outfile):
    file_out=open(outfile,'wb')
    resp=urllib.request.urlopen(respurl)
    file_out.write(resp.read())
    file_out.close()

'''
def getScoreImg(stuid):
    rawurl=getRawImgUrl(str(stuid)+'.jpg')
    respurl=getRespImgUrl(rawurl)
    saveUrlAsFile(respurl,str(stuid)+'_temp.jpg')
    img1=Image.open(str(stuid)+'_temp.jpg')
    box=(240,1320,1210,1500)    #(left, upper, right, lower)
    img2=img1.crop(box)
    img2.save('socre/'+str(stuid)+'_score.jpg')#no good
    os.remove(str(stuid)+'_temp.jpg')
'''

def getScoreImg(infile):
    rawurl=getRawImgUrl('raw/'+infile)      #no good
    respurl=getRespImgUrl(rawurl)
    saveUrlAsFile(respurl,'temp_'+infile)
    img1=Image.open('temp_'+infile)
    box=(240,1300,1210,1520)    #(left, upper, right, lower)
    img2=img1.crop(box)
    img2.save('score/'+'r_'+infile)#no good
    os.remove('temp_'+infile)

def getStrViaBaiduOCR(infile):
    input_file=open(infile,'rb')
    img_base64=base64.b64encode(input_file.read())
    url = 'http://apis.baidu.com/apistore/idlocr/ocr'
    data={}
    data['fromdevice'] = "pc"
    data['clientip'] = "10.10.10.0"
    data['detecttype'] = "LocateRecognize"
    data['languagetype'] = "CHN_ENG"
    data['imagetype'] = "1"
    data['image'] = img_base64

    decode_data=urllib.parse.urlencode(data)
    req=urllib.request.Request(url,data=decode_data.encode('utf-8'))

    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("apikey", "14cdd85738c717e546a5b6852c3e1631")

    resp=urllib.request.urlopen(req)

    content=json.loads(resp.read().decode('utf-8'))
    #for lines in content['retData']:
    #    print(lines['word'])
    #print(content['retData'][0]['word'])
    return content['retData'][0]['word']


def getNum(textStr):
    match=re.search(r'\d{2}|\d\.\d',textStr)
    pointStr=match.group(0)
    point=float(pointStr)
    if point<10:
        return point*10
    else:
        return point

'''
getScoreImg(1)
getNumViaBaiduOCR('1_score.jpg')
getScoreImg(2)
getNumViaBaiduOCR('2_score.jpg')
getScoreImg(3)
getNumViaBaiduOCR('3_score.jpg')
'''

def loopRank(num):
    for ii in range(num):
        global pic_list, count, err_list
        try:
            pic=pic_list.pop()
            t1=time.time()
            count+=1
            getScoreImg(pic)
            t2=time.time()
            print(pic,':', '%.2f'%(t2-t1), '----', count)
            os.remove('raw/'+pic)
        except:
            err_list.append(ii)
            continue

def multiRank_3(times):
    th1=threading.Thread(target=loopRank, args=(times//3,))
    th2=threading.Thread(target=loopRank, args=(times//3,))
    th3=threading.Thread(target=loopRank, args=(times//3,))
    th1.start()
    th2.start()
    th3.start()

def loopOCR(times,outfile,pic_list):
    of=open(outfile,'a')
    global count
    for ii in range(times):
        try:
            pic=pic_list.pop()
            text=getStrViaBaiduOCR('score/'+pic)
            point=getNum(text)
            if not 10<point<100:continue
            count+=1
            of.write(pic+'----'+str(point)+'\n')
            of.flush()
            print(pic,count)
            os.remove('score/'+pic)
        except:
            continue
    of.close()

def multiOCR_3(times):
    p_list=os.listdir('score')
    th1=threading.Thread(target=loopOCR, args=(times//3,'output1.txt',p_list))
    th2=threading.Thread(target=loopOCR, args=(times//3,'output2.txt',p_list))
    th3=threading.Thread(target=loopOCR, args=(times//3,'output3.txt',p_list))
    th1.start()
    th2.start()
    th3.start()


#pic_list=os.listdir('score')
#print(pic_list)
count=0
multiOCR_3(800)

''' TODO(lxiange):
Refactor the code to follow the PEP8.
Integrate two funs(getNum&OCR), to provide an API.
Enhance multi-threading support. 
Add ReadMe.md
'''