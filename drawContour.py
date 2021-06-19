from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
import pyperclip
import pyautogui
import cv2
import numpy as np
import os

url = 'https://www.google.com.tw/imghp?hl=zh-TW'
#圖片圖存之檔名
file_name = 'searchImage.jpg'
#圖片存放之路徑
file_path = 'D:\\python_training\\openSource'
#輸出輪廓之檔名
output_file = 'out.txt'
#欲描繪之圖案
search_str = '山羊'
#欲描繪輪廓之符號
draw_symbol = 'a'


def drawContour():
    global countoursImg,startLine,endLine

    output = []
    for i in range(startLine,endLine,2):
        line_str = ''
        for j in range(0,dim[1]-6):
            if countoursImg[i][j] == 0:
                line_str += draw_symbol
            else:
                line_str += ' '
        output.append(line_str)
    #輪廓輸出
    with open(output_file, 'w', newline='') as f:
        for i in range(len(output)):
            f.write(output[i]+'\n')

def foundStartLine():
    global dim,countoursImg,startLine,endLine
    #刪除不必要的資料
    countoursImg = countoursImg[3:-3]
    countoursImg_resize = np.zeros((dim[0]-6,dim[1]-6))
    for i in range(dim[0]-6):
        countoursImg_resize[i] = countoursImg[i][3:-3]

    countoursImg = np.array(countoursImg_resize)

    #找出起始、結束行
    draw_array = []
    startLine = 0
    endLine = 0 
    startLineNotFound = True
    for i in range(dim[0]-6):
        pre_pixel = countoursImg[i][0]
        draw_array.append([])
        draw_array[i].append([pre_pixel,1])
        for j in range(1,dim[1]-6):
            if countoursImg[i][j] == pre_pixel:
                draw_array[i][-1][1] += 1
            else:
                draw_array[i].append([countoursImg[i][j],1])
            pre_pixel = countoursImg[i][j]
        if draw_array[i][0] == [255.0,dim[1]-6] and startLineNotFound :
            startLine = i
        if not(draw_array[i][0] == [255.0,dim[1]-6]):
            endLine = i
            startLineNotFound = False


def foundContour():
    global dim,countoursImg
    #讀取圖片
    file_path_new = file_path + '\\' + file_name
    img = cv2.imread(file_path_new)
    dim = (70,70)
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #圖片經模糊化處理
    cv2.GaussianBlur(img,(5,5),0)
    #圖片經二值化處理
    _,new_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    new_img = 255 - new_img
    #找出輪廓
    countours, hierarchy = cv2.findContours(new_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #面積小於10之輪廓不取
    countours_new = []
    for item in countours:
        area = cv2.contourArea(item)
        area = int(area)
        if area > 10:
            countours_new.append(item)

    imgH,imgW = img.shape
    countoursImg = np.full((imgH,imgH),255)
    #畫出輪廓
    cv2.drawContours(countoursImg,countours_new,-1,(0,255,0),1)


def chromeGetImg():
    global browser
    global search_str
    search_str += ' 卡通'
    
    #找到查詢之element
    search_element_XPATH = '//*[@id="sbtc"]/div/div[2]/input'
    WebDriverWait(browser,30).until(EC.presence_of_element_located((By.XPATH,search_element_XPATH)))
    search_element = browser.find_element_by_xpath(search_element_XPATH)
    search_element.send_keys(search_str + '\n')
    
    #找到第一張圖片
    search_img_XPATH = '//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img'
    WebDriverWait(browser,30).until(EC.presence_of_element_located((By.XPATH,search_img_XPATH)))
    search_img = browser.find_element_by_xpath(search_img_XPATH)
    
    #另存圖片
    ActionChains(browser).move_to_element(search_img).context_click(search_img).perform()
    pyautogui.typewrite('v')
    sleep(1)
    pyperclip.copy(file_name)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.typewrite(['tab','tab','tab','tab','tab','tab','enter'])
    sleep(1)
    pyperclip.copy(file_path)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.typewrite(['enter'])
    pyautogui.hotkey('alt', 's')
    sleep(3)
    #若檔名已存在，取代它
    if os.path.isfile(file_name):
        pyautogui.typewrite('y')
        sleep(3)

def connetChrome():
    global browser
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(chrome_options=options) 
    browser.get(url)

if __name__ == "__main__":
    connetChrome()
    chromeGetImg()
    foundContour()
    foundStartLine()
    drawContour()
