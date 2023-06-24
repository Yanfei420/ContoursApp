import PySimpleGUI as sg
import os
import cv2
import numpy as np
from PIL import Image, ImageTk
import io

def get_img_data(f, maxsize=(1200, 850), first=False):
    """Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)
    
def do_find_contours(f,R_min,G_min,B_min,R_max,G_max,B_max):
    min = np.array([B_min,G_min,R_min])
    max = np.array([B_max,G_max,R_max])
    
    img_def = cv2.imread(f)
    img = np.array(img_def)
    hsv = cv2.cvtColor((img), cv2.COLOR_BGR2HSV)      #HSV変換を施す
    mask = cv2.inRange(hsv, min ,max)               #マスク適用で二値化処理
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(mask,kernel,iterations= 5)  #モルフォロジー変換でくっきりさせる
    thresh = cv2.threshold(dilated, 200, 250, cv2.THRESH_BINARY)[1]
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #輪郭描画前に保存しておく
    cv2.imwrite('srcimg/1default' + '.jpg', img)
    img_color_with_contours = cv2.drawContours(img, contours, -1, (0,255,0), 2)

    
    cv2.imwrite('srcimg/2hsv' + '.jpg', hsv)
    cv2.imwrite('srcimg/3mask'  + '.jpg', mask)
    cv2.imwrite('srcimg/4dilated' + '.jpg', dilated)  
    cv2.imwrite('srcimg/5thresh'  + '.jpg', thresh)
    cv2.imwrite('srcimg/6contours'  + '.jpg', img_color_with_contours)

    img1 = get_img_data("srcimg/1default.jpg", first=True)
    img2 = get_img_data("srcimg/2hsv.jpg", first=True)
    img3 = get_img_data("srcimg/3mask.jpg", first=True)
    img4 = get_img_data("srcimg/4dilated.jpg", first=True)
    img5 = get_img_data("srcimg/5thresh.jpg", first=True)
    img6 = get_img_data("srcimg/6contours.jpg", first=True)
    
    #rtn = [img1,img2,img3,img4,img5,img6]
    #returns 6 imgs
    return img1,img2,img3,img4,img5,img6
    
    #hsv,mask,dilated,thresh,img_color_with_contours

TEXT_WIDTH = 10
TEXT_HEIGHT = 1
sg.theme("Topanga")
dir = "images/1default.jpg"
dir2 = "images/1nodefault.jpg"
img_def_elem = sg.Image(data=get_img_data(dir, first=True))
img_hsv_elem = sg.Image(data=get_img_data("images/2hsv.jpg", first=True))
img_hsv_elem2 = sg.Image(data=get_img_data("images/2hsv.jpg", first=True))
img_hsv_elem3 = sg.Image(data=get_img_data("images/2hsv.jpg", first=True))
img_hsv_elem4 = sg.Image(data=get_img_data("images/2hsv.jpg", first=True))
img_hsv_elem5 = sg.Image(data=get_img_data("images/2hsv.jpg", first=True))
img_noddef_elem = sg.Image(data=get_img_data(dir2, first=True))
img_nod_elem = sg.Image(data=get_img_data("images/2hsv.jpg", first=True))
img_nod_elem2 = sg.Image(data=get_img_data("images/2hsv.jpg", first=True))
img_nod_elem3 = sg.Image(data=get_img_data("images/2hsv.jpg", first=True))
img_nod_elem4 = sg.Image(data=get_img_data("images/2hsv.jpg", first=True))
img_nod_elem5 = sg.Image(data=get_img_data("images/2hsv.jpg", first=True))




img_describe1 = sg.Text("input", size=(8, 2))
img_describe2 = sg.Text("hsv", size=(8, 2))
img_describe3 = sg.Text("masked", size=(8, 2))
img_describe4 = sg.Text("delited", size=(8, 2))
img_describe5 = sg.Text("thresh", size=(8, 2))
img_describe6 = sg.Text("contours", size=(8, 2))
col_img1 = [[img_describe1],[img_def_elem],[img_noddef_elem]]
col_img2 = [[img_describe2],[img_hsv_elem],[img_nod_elem]]
col_img3 = [[img_describe3],[img_hsv_elem2],[img_nod_elem2]]
col_img4 = [[img_describe4],[img_hsv_elem3],[img_nod_elem3]]
col_img5 = [[img_describe5],[img_hsv_elem4],[img_nod_elem4]]
col_img6 = [[img_describe6],[img_hsv_elem5],[img_nod_elem5]]

# define layout, show and read the form
#横に並べたかったら[]の中にcsvで書く。縦なら[],[]みたいにする。
#col = [[img_def_elem,img_hsv_elem,img_hsv_elem2,
#        img_hsv_elem3,img_hsv_elem4,img_hsv_elem5]]
col = [sg.Column(col_img1, justification='c'),
       sg.Column(col_img2, justification='c'),
       sg.Column(col_img3, justification='c'),
       sg.Column(col_img4, justification='c'),
       sg.Column(col_img5, justification='c'),
       sg.Column(col_img6, justification='c')]


Red_Min = Green_Min =  Blue_Min = Red_Max = Green_Max =  Blue_Max = 0
Red_Min_elem = sg.Text(Red_Min, size=(3, 2))
Green_Min_elem = sg.Text(Green_Min, size=(3, 2))
Blue_Min_elem = sg.Text(Blue_Min, size=(3, 2))

Red_Max_elem = sg.Text(Red_Max, size=(3, 2))
Green_Max_elem = sg.Text(Green_Max, size=(3, 2))
Blue_Max_elem = sg.Text(Blue_Max, size=(3, 2))

#スライダーを定義、sizeは横×縦
Red_Min_slider_base = [sg.Text("Red_Min",size=(TEXT_WIDTH,TEXT_HEIGHT)),
                Red_Min_elem,
                sg.Slider(range=(0,255),
                          default_value=0,
                          resolution=1,
                          orientation='h',
                          size=(34.3, 15),
                          enable_events=True,
                          key='Red_Min_slider')]

Green_Min_slider_base =[sg.Text("Green_Min",size=(TEXT_WIDTH,TEXT_HEIGHT)),
                Green_Min_elem,
                sg.Slider(range=(0,255),
                          default_value=0,
                          resolution=1,
                          orientation='h',
                          size=(34.3, 15),
                          enable_events=True,
                          key='Green_Min_slider')]

Blue_Min_slider_base =[sg.Text("Blue_Min",size=(TEXT_WIDTH,TEXT_HEIGHT)),
                Blue_Min_elem,
                sg.Slider(range=(0,255),
                          default_value=0,
                          resolution=1,
                          orientation='h',
                          size=(34.3, 15),
                          enable_events=True,
                          key='Blue_Min_slider')]

Red_Max_slider_base = [sg.Text("Red_Max",size=(TEXT_WIDTH,TEXT_HEIGHT)),
                Red_Max_elem,
                sg.Slider(range=(0,255),
                          default_value=0,
                          resolution=1,
                          orientation='h',
                          size=(34.3, 15),
                          enable_events=True,
                          key='Red_Max_slider')]

Green_Max_slider_base =[sg.Text("Green_Max",size=(TEXT_WIDTH,TEXT_HEIGHT)),
                Green_Max_elem,
                sg.Slider(range=(0,255),
                          default_value=0,
                          resolution=1,
                          orientation='h',
                          size=(34.3, 15),
                          enable_events=True,
                          key='Green_Max_slider')]

Blue_Max_slider_base =[sg.Text("Blue_Max",size=(TEXT_WIDTH,TEXT_HEIGHT)),
                Blue_Max_elem,
                sg.Slider(range=(0,255),
                          default_value=0,
                          resolution=1,
                          orientation='h',
                          size=(34.3, 15),
                          enable_events=True,
                          key='Blue_Max_slider')]


#ボタンをまとめる
col_buttons = [Red_Min_slider_base,Green_Min_slider_base,Blue_Min_slider_base]
col_buttons2 = [Red_Max_slider_base,Green_Max_slider_base,Blue_Max_slider_base]
generate_button = sg.Button('Generate', size=(8, 2),key="Generate")

layout = [col,
          [sg.Column(col_buttons)],
          [sg.Column(col_buttons2),generate_button]]

window = sg.Window('Image Browser', layout, return_keyboard_events=True,
                   location=(0, 0), use_default_focus=False)





while True:
    # read the form
    event, values = window.read()
    #print(event, values)
    # perform button and keyboard operations
    if event == sg.WIN_CLOSED:
        break
    elif event == "Red_Min_slider":
        Red_Min = int(values['Red_Min_slider'])
    elif event == "Blue_Min_slider":
        Blue_Min = int(values['Blue_Min_slider'])
    elif event == "Green_Min_slider":
        Green_Min = int(values['Green_Min_slider'])
    elif event == "Red_Max_slider":
        Red_Max = int(values['Red_Max_slider'])
    elif event == "Blue_Max_slider":
        Blue_Max = int(values['Blue_Max_slider'])
    elif event == "Green_Max_slider":
        Green_Max = int(values['Green_Max_slider'])
    elif event == "Generate":
        #敵がいる画像
        img1,img2,img3,img4,img5,img6,= do_find_contours(dir,Red_Min,Green_Min,Blue_Min,
                                   Red_Max,Green_Max,Blue_Max)
        #敵がいない画像
        nod1,nod2,nod3,nod4,nod5,nod6 = do_find_contours(dir2,Red_Min,Green_Min,Blue_Min,
                                   Red_Max,Green_Max,Blue_Max)
        img_def_elem.update(img1)  #sgウィンドウ用の画像が帰ってきているので変換不要    
        img_hsv_elem.update(img2)
        img_hsv_elem2.update(img3)
        img_hsv_elem3.update(img4) 
        img_hsv_elem4.update(img5) 
        img_hsv_elem5.update(img6) 
        img_noddef_elem.update(nod1)   
        img_nod_elem.update(nod2)
        img_nod_elem2.update(nod3)
        img_nod_elem3.update(nod4) 
        img_nod_elem4.update(nod5) 
        img_nod_elem5.update(nod6) 
    
    #値更新
    Red_Min_elem.update(int(values['Red_Min_slider']))
    Green_Min_elem.update(int(values['Green_Min_slider']))
    Blue_Min_elem.update(int(values['Blue_Min_slider']))
    Red_Max_elem.update(int(values['Red_Max_slider']))
    Green_Max_elem.update(int(values['Green_Max_slider']))
    Blue_Max_elem.update(int(values['Blue_Max_slider']))
    #画像更新
       
    
    

window.close()
