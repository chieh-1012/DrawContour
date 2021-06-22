# 留言神器
##  介紹
科技的進步，人們也越來越依賴社群軟體，
不論是facebook或是instagram
都可自由地在貼文底下留言，
而instagram的留言區無法留下圖片十分可惜，
因此圖片轉成文字的方式將更方便在instagram留言時以圖片表達內心情感。 
## 功能
取得一張欲轉換圖片之URL，且圖片格式須為JPG, 
PNG, GIF, BMP, TIFF, WEBP，API發出請求時夾帶的img參數為上述之URL，
API回傳一串URL，此為壓縮後之圖片URL，
經過影像處理演算法描繪出圖像輪廓，最終以txt檔輸出。
## 套件說明
* python
* cv2
```bash
$ pip install cv2
```
* requests
```bash
$ pip install request
```
* json 
```bash
$ pip install json
```
* Image  
```bash
$ pip install Pillow
```
* BytesIO   
* numpy  
```python
$ pip install numpy
```
## 使用說明

* 下載 `drawContour.py`  
* 資料修改
```python
#欲轉換圖片之URL
imgUrl = 'https://miro.medium.com/max/676/1*XEgA1TTwXa5AvAdw40GFow.png'
#輸出檔案之名稱
output_file = 'out.txt'
#描繪輪廓之符號
drawSymbol = 'a'
#輸出檔案之長寬
dim = (70,70)
```
* 執行程式
 ```bash
$ python drawContour.py
```
## API說明
* 此作品用到的是[reSmush.it](https://resmush.it/)提供之[API](http://api.resmush.it/ws.php)
* API無須註冊
* http://api.resmush.it/ws.php?img= ，img=>圖片URL
* API output
  * the source URL (if using GET or POST method) (parameter src)
  * the url of the optimized picture (parameter dest)
  * the original file size (parameter src_size)
  * the optimized file size (parameter dest_size)
  * the percentage of gain (parameter percent)
  * the date when the file will be deleted from the server (parameter expires)
  * the error code (parameter error)
  * the error description (parameter error_long)
## 執行流程
### 1. 串接API  
* API回傳的值儲存在response，用json.loads()將JSON物件轉為Python資料類型
* 查看回傳結果有無error之key，若無則可進行輪廓描繪
```python
response = requests.get(url,params=data)
responseJson = json.loads(response.text)
if 'error' in responseJson.keys():
    return 0
return responseJson['dest']
```
### 2. 讀取圖片，找出圖片之輪廓
* requests能以位元組的方式訪問請求響應體，以請求返回的二進位制資料建立一張圖片
```python
response = requests.get(url)
img = Image.open(BytesIO(response.content))
img = np.array(img)
```
* 接著將圖片改變大小、轉灰階、模糊化處理、二值化處理
```python
img = img.astype('uint8')
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
cv2.GaussianBlur(img,(5,5),0)
_,new_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```
* 找出圖片輪廓、面積過小之輪廓不取、將輪廓存於countoursImg
```python
countours, hierarchy = cv2.findContours(new_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

countoursNew = []
for item in countours:
    area = cv2.contourArea(item)
    area = int(area)
    if area > 10:
        countoursNew.append(item)

imgHeight,imgWidth = img.shape
countoursImg = np.full((imgHeight,imgWidth),255)

cv2.drawContours(countoursImg,countoursNew,-1,(0,255,0),1)
```
  * countoursNew的結果
  <img width="172" alt="企鵝" src="https://user-images.githubusercontent.com/72730771/122921379-fc830e80-d394-11eb-98bf-f1b4d3e948e6.png">

### 紀錄起始、結束行
* 刪除四周的黑線
```python
countoursImg = countoursImg[3:-3]
countoursImgResize = np.zeros((imgHeight,imgWidth))
for i in range(imgHeight):
    countoursImgResize[i] = countoursImg[i][3:-3]

countoursImg = np.array(countoursImg_resize)
```
  * 此時countoursNew的結果
  <img width="164" alt="企鵝2" src="https://user-images.githubusercontent.com/72730771/122922021-c5f9c380-d395-11eb-8995-ff3f4679b56d.png">

* 減少上方空白行，紀錄起始、結束行
```python
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
```
### 以txt檔儲存圖片之輪廓
* output儲存輸出的內容
```python
imgWidth = dim[1]-6
output = []
for i in range(startLine,endLine,2):
        line_str = ''
        for j in range(0,imgWidth):
            if countoursImg[i][j] == 0:
                line_str += drawSymbol
            else:
                line_str += ' '
        output.append(line_str)
```
* 輸出結果至txt檔
```python
with open(outputFile, 'w', newline='') as f:
    for i in range(len(output)):
        f.write(output[i]+'\n')
```
## 執行結果
### 原圖  
![searchImage](https://user-images.githubusercontent.com/72730771/122928780-c3e73300-d39c-11eb-9377-998e16976b2a.jpg)
### out.txt  
<img width="399" alt="企鵝結果" src="https://user-images.githubusercontent.com/72730771/122928939-ec6f2d00-d39c-11eb-8c0c-bbe8ac98728c.png">  

## 參考資料  
* https://www.minwt.com/webdesign-dev/html/21781.html  
* https://resmush.it/api   
* https://ithelp.ithome.com.tw/articles/10220161  
