import cv2
import requests
import json
from PIL import Image
from io import BytesIO
import numpy as np

#欲轉換圖片之URL
imgUrl ='https://i0.wp.com/tu1.whhost.net/uploads/20190213/16/1550046269-nPaumwgiRj.jpg'
#輸出檔名
outputFile = 'out.txt'
#欲描繪輪廓之符號
drawSymbol = 'a'
#輸出長寬
dim = (70,70)

def drawContour(countoursImg,startLine,endLine):
    imgWidth = dim[1]-6
    output = []
    for i in range(startLine,endLine,1):
        line_str = ''
        for j in range(0,imgWidth):
            if countoursImg[i][j] == 0:
                line_str += drawSymbol
            else:
                line_str += ' '
        output.append(line_str)
        
    #輪廓輸出
    with open(outputFile, 'w', newline='') as f:
        for i in range(len(output)):
            f.write(output[i]+'\n')

def foundStartLine(countoursImg):
    imgHeight = dim[0]-6
    imgWidth = dim[1]-6
    #刪除不必要的資料
    countoursImg = countoursImg[3:-3]
    countoursImgResize = np.zeros((imgHeight,imgWidth))
    for i in range(imgHeight):
        countoursImgResize[i] = countoursImg[i][3:-3]
    countoursImg = np.array(countoursImgResize)

    #找出起始、結束行
    allWhite = np.full(imgWidth,255)
    startLine = 0
    endLine = 0 
    startLineNotFound = True
    for i in range(imgHeight):
        if countoursImg[i].all() == allWhite.all() and startLineNotFound:
            startLine = i
        if not(countoursImg[i].all() == allWhite.all()):
            endLine = i
            startLineNotFound = False

    drawInfo = []
    drawInfo.append(countoursImg)
    drawInfo.append(startLine)
    drawInfo.append(endLine)

    return drawInfo

def foundContour(url):
    #讀取圖片
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = np.array(img)
    img = img.astype('uint8')

    #圖片轉灰階
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    #圖片經模糊化處理
    cv2.GaussianBlur(img,(5,5),0)

    #圖片經二值化處理
    _,new_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    #找出輪廓
    countours, hierarchy = cv2.findContours(new_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #面積小於10之輪廓不取
    countoursNew = []
    for item in countours:
        area = cv2.contourArea(item)
        area = int(area)
        if area > 10:
            countoursNew.append(item)

    #畫出輪廓
    imgHeight,imgWidth = img.shape
    countoursImg = np.full((imgHeight,imgWidth),255)
    cv2.drawContours(countoursImg,countoursNew,-1,(0,255,0),1)
    return countoursImg

def posttoapi(url, data, headers={'Content-type': 'application/json', 'Accept': 'text/plain'}):
   response = requests.get(url,params=data)
   responseJson = json.loads(response.text)
   if 'error' in responseJson.keys():
       return 0
   return responseJson['dest']

if __name__ == '__main__':
    url = 'http://api.resmush.it/ws.php'
    data = {'img':imgUrl}
    imgCompressUrl = posttoapi(url,data)
    if imgCompressUrl == 0:
        print('error')
    else:
        countoursImg = foundContour(imgUrl)
        drawInfo = foundStartLine(countoursImg)
        drawContour(drawInfo[0],drawInfo[1],drawInfo[2])
    print('end')
