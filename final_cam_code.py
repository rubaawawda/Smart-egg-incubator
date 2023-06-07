from cv2 import (VideoCapture, namedWindow, imshow, waitKey, destroyWindow, imwrite)
import numpy as np
import cv2
import matplotlib
import matplotlib.pyplot as plt
from split_image import split_image
from matplotlib.image import imread
import pyrebase

config = {    
  "apiKey": "AIzaSyAVaxr6n1VKLm_dw96nQymhzT82heEyxMs",
  "authDomain": "smart-egg-incubator-3a272.firebaseapp.com",
  "databaseURL": "https://smart-egg-incubator-3a272-default-rtdb.firebaseio.com",
  "projectId": "smart-egg-incubator-3a272",
  "storageBucket": "smart-egg-incubator-3a272.appspot.com",
  "messagingSenderId": "269936679585",
  "appId": "1:269936679585:web:b2ba9b949606da7a136ee0",
  "databaseURL":"https://smart-egg-incubator-3a272-default-rtdb.firebaseio.com/",
  "serviceAccount": "serviceAccount.json"
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
db = firebase.database()

all_camera_idx_available = []

for camera_idx in range(10):
    cap = VideoCapture(camera_idx)
    if cap.isOpened():
        print(f'Camera index available: {camera_idx}')
        all_camera_idx_available.append(camera_idx)
        cap.release()
        
cam = VideoCapture(all_camera_idx_available[0]) # 0 index0 is for build in camera
s, img = cam.read()
if s:    # if frame captured without any errors
    imwrite("filename.jpg",img) #save image
input_image = imread("filename.jpg")
r,g,b = input_image[:,:,0], input_image[:,:,1], input_image[:,:,2]
gamma = 1.04
r_const, g_const, b_const = 0.2126, 0.7152, 0.0722
grayscale_image = r_const * r ** gamma + g_const * g ** gamma + b_const * b ** gamma
imwrite("gray.jpg",grayscale_image)
gray =cv2.imread("gray.jpg")
img_640_480 =cv2.imread("filename.jpg")


w = 213
w2 = 426
w3 = 640

h = 160
h2 = 320
h3 = 480
y = 0
x = 0

fatima = cv2.rectangle(img_640_480, (x, h2), (x + w, h3), (36, 255, 12), 2)
fatima = cv2.rectangle(img_640_480, (w, h2), (w2, h3), (36, 255, 12), 2)
fatima = cv2.rectangle(img_640_480, (w2, h2), (w3, h3), (36, 255, 12), 2)
cv2.imwrite("egg.jpg", fatima)

for i in range (1,4,1):

    img_crop_1 = gray[y:y+h, ((i-1)*w):(x+(i*w))]
    fatima = cv2.rectangle(img_640_480, (((i-1)*w), y), ((i*w), h), (36,255,12), 2)
    imwrite("egg.jpg", fatima)
   
    white_pix = np.sum(img_crop_1 > 1)
    black_pix = np.sum(img_crop_1 < 2)
    if white_pix > black_pix:
        
        cv2.circle(fatima,center = (int(((i-1)+(1/2))*w), int((y+h)/2)), radius =20, color =(0,0,255), thickness=3)

         
         
for i in range (1,4,1):
    img_crop_2 =gray[h:h2, ((i-1)*w):(x+(i*w))]
    fatima = cv2.rectangle(img_640_480, (((i-1)*w), h), ((i*w), h2), (36,255,12), 2)
    imwrite("egg.jpg", fatima)
    white_pix = np.sum(img_crop_2 > 1)
    black_pix = np.sum(img_crop_2 < 2)
    
   
    if white_pix > black_pix:
        
        cv2.circle(fatima,center = (int(((i-1)+(1/2))*w), int(3*(y+h)/2)), radius =20, color =(0,0,255), thickness=3)
       

for i in range (1,4,1):
    img_crop_3 = gray[h2:h3, ((i-1)*w):(x+(i*w))]
    fatima = cv2.rectangle(img_640_480, (((i-1)*w), h2), ((i*w), h3), (36,255,12), 2)
    imwrite("egg.jpg", fatima)
    white_pix = np.sum(img_crop_3 > 1)
    
    if white_pix > black_pix:
        
        cv2.circle(fatima,center = (int(((i-1)+(1/2))*w), int(5*(y+h)/2)), radius =20, color =(0,0,255), thickness=3)
# 
# 
# for i in range (1,5,1):
#     img_crop_4 = img_640_480[h3:h4, ((i-1)*w):(x+(i*w))]
#     fatima = cv2.rectangle(img_640_480, (((i-1)*w), h3), ((i*w), h4), (36,255,12), 2)
#     imwrite("fatima.jpg", fatima)
#     white_pix = np.sum(img_crop_4 > 120)
#     black_pix = np.sum(img_crop_4 < 110)
#     if white_pix > black_pix:
#         
#         cv2.circle(fatima,center = (int(((i-1)+(1/2))*w), int(7*(y+h)/2)), radius =20, color =(0,0,255), thickness=3)
#    
         
storage.child("imge.jpg").put("egg.jpg")
print("put")        