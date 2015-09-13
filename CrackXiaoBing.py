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
    
    resp=urllib.request.urlopen(CompUrl,
        data=urllib.parse.urlencode(form).encode('utf-8'))
    respUrl=json.loads(resp.read().decode('utf-8'))['content']['imageUrl']
    return respUrl


def saveUrlAsFile(respurl,outfile):
    file_out=open(outfile,'wb')
    resp=urllib.request.urlopen(respurl)
    file_out.write(resp.read())
    file_out.close()


def getScoreImg(inPic, outPic):
    rawurl=getRawImgUrl(inPic)      #no good
    respurl=getRespImgUrl(rawurl)
    saveUrlAsFile(respurl, inPic+'.temp')
    img1=Image.open(inPic+'.temp')
    box=(240,1300,1210,1520)    #(left, upper, right, lower)
    img2=img1.crop(box)
    img1.close()
    img2.save(outPic)#no good
    os.remove(inPic+'.temp')


def getNumViaBaiduOCR(infile):
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
    textStr = content['retData'][0]['word']

    match=re.search(r'\d{2}|\d\.\d',textStr)
    pointStr=match.group(0)
    point=float(pointStr)
    if point <= 10:      # . is identified
        point *= 10
    if point <= 20:      # 7 is identified as 1
        point += 60
    return point


def rank_pic(infile):
    getScoreImg(infile, infile[-13:-4]+'_temp.jpg')
    point=getNumViaBaiduOCR(infile[-13:-4]+'_temp.jpg')
    os.remove(infile[-13:-4]+'_temp.jpg')
    if not 10<point<100: 
        return -1
    return int(point)


#print(rank_pic('141015013.jpg'))
#os.listdir('raw')


list_lock=threading.Lock()
file_lock=threading.Lock()
error_lock=threading.Lock()
def rank_all(path, pic_list, fp, fp2):
    list_lock.acquire()
    while(len(pic_list)>0):
        try:
            pic=pic_list.pop()
        finally:
            list_lock.release()

        if pic:
            try:
                point = rank_pic(path+pic)
                file_lock.acquire()
                fp.write('%s----%d\n'%(pic[-13:-4],point))
                fp.flush()
                file_lock.release()
            except:
                error_lock.acquire()
                fp2.write(pic+'\n')
                fp2.flush()
                error_lock.release()

            print(pic, point)
        list_lock.acquire()

    list_lock.release()


def main():
    pic_list=os.listdir('raw')
    f1 = open('output.txt', 'w')
    f2 = open('error.txt', 'w')
    thread_list = [threading.Thread(target=rank_all, 
        args=('raw/', pic_list, f1, f2)) for i in range(1,7)]
    for i in thread_list:
        i.start()

    for i in thread_list:
        i.join()
    f1.close()
    f2.close()
    print('All is well!')


def scoreSort(infile, outfile):
    fp=open(infile)
    score_list=[]
    for i in fp.readlines():
        #print(i)
        if len(i)<10:continue
        temp=i.strip().split('----')
        temp[1]=int(temp[1])
        score_list.append(temp)
    answer=sorted(score_list,key=lambda stu:stu[1],reverse=True)
    #print(answer)
    f2=open(outfile,'w')
    for i in answer:
        f2.write('%s----%s\n'%(str(i)[2:11], str(i)[14:16]))
    f2.close()


if __name__ == '__main__':
    #main()
    scoreSort('output.txt', 'final15.txt')



''' TODO(lxiange):
Refactor the code to follow the PEP8.
Integrate two funs(getNum&OCR), to provide an API.(DONE)
Enhance multi-threading support. (DONE)
Add ReadMe.md
'''
