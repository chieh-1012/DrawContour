# DrawContour
## 介紹
輸入想要描繪之圖案  
程式將自動至goole圖片搜尋圖片  
描繪出輪廓並輸出成txt檔
## 工具說明
* selenium  
* time模組的sleep  
* pyperclip  
* pyautogui  
* os  
* numpy  
## 使用說明

* 下載 `drawContour.py`  
* 下載 `chromedrive.exe`並放在同一資料夾  
* 資料更改
```python
#填入檔案路徑  
file_path = 'D:\\python_training\\openSource'
#輸出檔案名稱可自行更改
output_file = 'out.txt'
#填入欲轉換之圖案
search_str = '山羊' 
#填入描繪輪廓之符號
draw_symbol = 'a'
```
* 執行程式
 ```bash
$ python drawContour.py
```
## 執行流程
```python
#進入google圖片網站
connetChrome()
#取得圖片，另存圖片於程式碼檔案同個資料夾中
chromeGetImg()
#讀取圖片，找出圖片之輪廓
foundContour()
#紀錄起始、結束行
foundStartLine()
#以txt檔儲存圖片之輪廓
drawContour()
```
## 執行結果
### 原圖  
![searchImage](https://user-images.githubusercontent.com/72730771/122646616-a030ac80-d152-11eb-90b0-5ef61312b8be.jpg)
### out.txt  
<img width="575" alt="山羊" src="https://user-images.githubusercontent.com/72730771/122646654-d5d59580-d152-11eb-8910-c21b52c39de0.png">
