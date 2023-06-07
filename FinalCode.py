import Adafruit_DHT
import time
from datetime import datetime
import RPi.GPIO as GPIO
import pyrebase
from datetime import datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt
from split_image import split_image
from matplotlib.image import imread

config = {    
  "apiKey": "AIzaSyAVaxr6n1VKLm_dw96nQymhzT82heEyxMs",
  "authDomain": "smart-egg-incubator-3a272.firebaseapp.com",
  "databaseURL":"https://smart-egg-incubator-3a272-default-rtdb.firebaseio.com/",
  "storageBucket": "smart-egg-incubator-3a272.appspot.com"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()

DHT_SENSOR = Adafruit_DHT .DHT11
DHT_PIN = 6
LAMP = 24
PUMP = 26
FAN = 19
TRIG = 5
ECHO = 22
DC1 = 27
DC2 = 17
BUTTON1 = 21
BUTTON2 = 20
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(PUMP,GPIO.OUT)
GPIO.setup(FAN,GPIO.OUT)
GPIO.setup(LAMP,GPIO.OUT)
GPIO.setup(DC1,GPIO.OUT)
GPIO.setup(DC2,GPIO.OUT)
GPIO.setup(BUTTON1,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(BUTTON2,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.output(PUMP, True)
GPIO.output(LAMP, True)
GPIO.output(FAN, True)
type_selected = db.child("current_value").get().val()
type_selected=type_selected.replace('"', '')
incubate_days = db.child("setting").child("kind_properties").child(str(type_selected)).child("incubate days").get().val()
incubate_days_witout_last_3days = incubate_days - 3
print(incubate_days_witout_last_3days)


Range_humidity = db.child("setting").child("kind_properties").child(str(type_selected)).child("Humidity").get().val()
Range_humidity = Range_humidity.split("-")
Range_temperature = db.child("setting").child("kind_properties").child(str(type_selected)).child("Temp").get().val()
Range_temperature = Range_temperature.split("-")
Range_humidity_last_3_days = db.child("setting").child("kind_properties").child(str(type_selected)).child("Humidity in Last 3 days").get().val()
Range_humidity_last_3_days = Range_humidity_last_3_days.split("-")
min_humidity = int (Range_humidity[0])
max_humidity = int (Range_humidity[1])
min_temperature = float (Range_temperature[0])
max_temperature = float (Range_temperature[1])
min_humidity_last_3_days = int (Range_humidity_last_3_days[0])
max_humidity_last_3_days = int (Range_humidity_last_3_days[1])
incubate_days = db.child("setting").child("kind_properties").child(str(type_selected)).child("incubate days").get().val()


loop_run=1

if not db.child("Start time").get().val():
    db.child("Start time").set(time.time())

# last_move_time = time.time()
def loop_fun():
  global loop_run
  
  while loop_run:
      loop_run = int(db.child("loop_run").get().val())
      end_time = time.time()
      db.child("end time").set(end_time)
      start = db.child("Start time").get().val()
      end = db.child("end time").get().val()
      db.child("smart_egg_incubator").child("current incubate time").set(1)
      current_incubate_time = db.child("smart_egg_incubator").child("current incubate time").get().val()
      
      direction = ""
      next_direction = "one"
      last_move_time = time.time()
      button1_state = GPIO.input(BUTTON1)
      button2_state = GPIO.input(BUTTON2)
      if 0 < current_incubate_time < incubate_days-3:
          
          

          direction=next_direction

          if (button1_state == 1 and button2_state == 1) or (time.time()-last_move_time>28800):
              last_move_time = time.time()
              print ("last_move_time= ",last_move_time)

              if direction == "one":
                  print(direction)
                  GPIO.output(DC1, GPIO.LOW)
                  GPIO.output(DC2, GPIO.HIGH)
                    
              elif direction == "two":
                  
                  GPIO.output(DC1, GPIO.HIGH)
                  GPIO.output(DC2, GPIO.LOW)
                      
              elif button1_state == 0 and button2_state == 1:
                  print("button1 pressed")
                  GPIO.output(DC1, GPIO.LOW)
                  GPIO.output(DC2, GPIO.LOW)
                  next_direction="two"
              elif button1_state == 1 and button2_state == 0:
                  print("button2 pressed")
                  next_direction="one"
                  GPIO.output(DC1, GPIO.LOW)
                  GPIO.output(DC2, GPIO.LOW)
                
     
      time.sleep(1)

# fertile and infertile examine
      if current_incubate_time == 7:
          print("yes")
          
          
#           all_camera_idx_available = []
#           for camera_idx in range(10):
#               cap = VideoCapture(camera_idx)
#               if cap.isOpened():
#                   print(f'Camera index available: {camera_idx}')
#                   all_camera_idx_available.append(camera_idx)
#                   cap.release()
#         
#           cam = VideoCapture(all_camera_idx_available[0]) # 0 index0 is for build in camera
#           s, img = cam.read()
#           if s:    # if frame captured without any errors
#               imwrite("filename.jpg",img) #save image
#           input_image = imread("filename.jpg")
#           r,g,b = input_image[:,:,0], input_image[:,:,1], input_image[:,:,2]
#           gamma = 1.04
#           r_const, g_const, b_const = 0.2126, 0.7152, 0.0722
#           grayscale_image = r_const * r ** gamma + g_const * g ** gamma + b_const * b ** gamma
#           imwrite("gray.jpg",grayscale_image)
#           gray =cv2.imread("gray.jpg")
#           img_640_480 =cv2.imread("filename.jpg")
# 
#           w = 213
#           w2 = 426
#           w3 = 640
# 
#           h = 160
#           h2 = 320
#           h3 = 480
#           y = 0
#           x = 0
# 
#           fatima = cv2.rectangle(img_640_480, (x, h2), (x + w, h3), (36, 255, 12), 2)
#           fatima = cv2.rectangle(img_640_480, (w, h2), (w2, h3), (36, 255, 12), 2)
#           fatima = cv2.rectangle(img_640_480, (w2, h2), (w3, h3), (36, 255, 12), 2)
#           cv2.imwrite("egg.jpg", fatima)
# 
#           for i in range (1,4,1):
# 
#               img_crop_1 = gray[y:y+h, ((i-1)*w):(x+(i*w))]
#               fatima = cv2.rectangle(img_640_480, (((i-1)*w), y), ((i*w), h), (36,255,12), 2)
#               imwrite("egg.jpg", fatima)
#    
#               white_pix = np.sum(img_crop_1 > 1)
#               black_pix = np.sum(img_crop_1 < 2)
#               if white_pix > black_pix:
#         
#                   cv2.circle(fatima,center = (int(((i-1)+(1/2))*w), int((y+h)/2)), radius =20, color =(0,0,255), thickness=3)
# 
#           for i in range (1,4,1):
#               img_crop_2 =gray[h:h2, ((i-1)*w):(x+(i*w))]
#               fatima = cv2.rectangle(img_640_480, (((i-1)*w), h), ((i*w), h2), (36,255,12), 2)
#               imwrite("egg.jpg", fatima)
#               white_pix = np.sum(img_crop_2 > 1)
#               black_pix = np.sum(img_crop_2 < 2)
# 
#               if white_pix > black_pix:
#         
#                   cv2.circle(fatima,center = (int(((i-1)+(1/2))*w), int(3*(y+h)/2)), radius =20, color =(0,0,255), thickness=3)
#           for i in range (1,4,1):
#               img_crop_3 = gray[h2:h3, ((i-1)*w):(x+(i*w))]
#               fatima = cv2.rectangle(img_640_480, (((i-1)*w), h2), ((i*w), h3), (36,255,12), 2)
#               imwrite("egg.jpg", fatima)
#               white_pix = np.sum(img_crop_3 > 1)
#     
#               if white_pix > black_pix:
#         
#                   cv2.circle(fatima,center = (int(((i-1)+(1/2))*w), int(5*(y+h)/2)), radius =20, color =(0,0,255), thickness=3)
#       
# #       storage.child("imge.jpg").put("egg.jpg")
#           print("put")   
#           
       
      
      
      
      
      
      
      humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
      if humidity is not None and temperature is not None:
          current_datetime= datetime.now()
          print("Temp={0:0.1f}c  Humidity={1:0.1f}%". format(temperature, humidity))
          
          Start_date = str(current_datetime.year)+"-"+str(current_datetime.month)+"-"+str(current_datetime.day)
          date_st = datetime.strptime(Start_date, '%Y-%m-%d')
          new_date = date_st + timedelta(days=incubate_days) # add 3 days to the datetime object
          new_date_str = new_date.strftime('%Y-%m-%d')
          print(Start_date)
          print(new_date_str)
          data = {
          "Temperature" : temperature,
          "Humidity" : humidity,
          "start date" : Start_date,
          "end date" : new_date_str,
          "loop_run" : 1
          }
          db.child("smart_egg_incubator").set(data)
          
         
          
          if current_incubate_time < (incubate_days_witout_last_3days ):
              if humidity > min_humidity and humidity < max_humidity:
                  print ("pump off")
                  GPIO.output(LAMP, True)
                  print ("ultrasonic off")
                  GPIO.output(FAN,True)
             ## GPIO.output(5,GPIO.HIGH) FOR FAN(FAN GET OFF ON HIGH LEVEL
              else:
             
                  if humidity < min_humidity:
                 
                      print ("ultrasonic on befor")
                      if True:
                          GPIO.output(TRIG, True)
                          time.sleep(1)
                          GPIO.output(TRIG, False)
                          while GPIO.input(ECHO) == 0:
                              pulse_start = time.time()
                          while GPIO.input(ECHO) == 1:
                              pulse_end = time.time()
                          pulse_duration = pulse_end - pulse_start
                          distance = pulse_duration * 17150
                          distance = round(distance, 2)
                          print("distance:", distance, "cm")
                          if distance < 10:
                              print ("pump on")
                              GPIO.output(PUMP, False)
                              if distance < 5:
                                  GPIO.output(PUMP, True)
                                  
                          else:
                              print ("pump off")
                              GPIO.output(PUMP, True)      
                              GPIO.output(TRIG, False)
                              print ("ulterasonic off")
                  else:
                      if humidity > max_humidity:
                          GPIO.output(PUMP, True)
                          GPIO.output(FAN,False)
         
          else:
              if current_incubate_time >= incubate_days_witout_last_3days:
                  if humidity > min_humidity_last_3_days and humidity < max_humidity_last_3_days:
                      print ("pump off")
                      GPIO.output(PUMP, True)
                      print ("ultrasonic off")
                      GPIO.output(TRIG, False)
#                       GPIO.output(FAN,True)
                  else:
                      if humidity < min_humidity_last_3_days:
                 
                          print ("ultrasonic on last 3")
                          if True:
                             GPIO.output(TRIG, True)
                             time.sleep(1)
                             GPIO.output(TRIG, False)
                             while GPIO.input(ECHO) == 0:
                                   pulse_start = time.time()
                             while GPIO.input(ECHO) == 1:
                                   pulse_end = time.time()
                             pulse_duration = pulse_end - pulse_start
                             distance = pulse_duration * 17150
                             distance = round(distance, 2)
                             print("distance:", distance, "cm")
                             if distance < 10:
                                 
                                 print ("pump on")
                                 GPIO.output(PUMP, False)  
                                 if distance < 5:
                                     GPIO.output(PUMP, True)
                                      
                             else:
                                 print ("pump off")
                                 GPIO.output(PUMP, True)      
                                 GPIO.output(TRIG, False)
                                 print ("ulterasonic off")
                      else:
                          if humidity > max_humidity_last_3_days:
                              print ("pump off")
                              GPIO.output(PUMP, True)
                              print ("ultrasonic off")
                              GPIO.output(TRIG, False)
                              print ("FAN oN")
                              GPIO.output(FAN,False)
         
          if temperature > max_temperature:
              print ("LAMB off")
              GPIO.output(LAMP, True)
              print("FAN ON ")
              GPIO.output(FAN,False)
          else:
              
              GPIO.output(FAN,True)
              GPIO.output(LAMP, False)
#               
#           else:
#              
#               if temperature < min_temperature:
#                   print ("LAMB on")
#                   GPIO.output(LAMP, False)
#                  # print ("FAN off")
#                  # GPIO.output(FAN,True)
#                   
#                   ## GPIO.output(5,GPIO.HIGH) FOR FAN(FAN GET OFF ON HIGH LEVEL
#               else:
#                  
#                   if temperature > max_temperature:
#                       
                          
                          
                      
          
#           button1_state = GPIO.input(BUTTON1)
#           button2_state = GPIO.input(BUTTON2)
#           direction = ""
#           next_direction = "one"
#           if 3 < current_incubate_time < incubate_days_witout_last_3days:
# 
#               direction=next_direction # direction one
# 
#               if (button1_state == 1 and button2_state == 1) or (time.time()-last_move_time>10):
# #                   28800 the last move correctly
#                   last_move_time = time.time()
#                   print ("last_move_time= ",last_move_time)
# 
#                   if direction == "one":
#                       GPIO.output(DC1, GPIO.LOW)
#                       GPIO.output(DC2, GPIO.HIGH)
#                     
#                   elif direction == "two":
#                       GPIO.output(DC1, GPIO.HIGH)
#                       GPIO.output(DC2, GPIO.LOW)
#                       
#               elif button1_state == 0 and button2_state == 1:
#                   print("btn1 pressed")
#                   GPIO.output(DC1, GPIO.LOW)
#                   GPIO.output(DC2, GPIO.LOW)
#                   next_direction="two"
#               elif button1_state == 1 and button2_state == 0:
#                   print("btn2 pressed")
#                   GPIO.output(DC1, GPIO.LOW)
#                   GPIO.output(DC2, GPIO.LOW)
#                   next_direction="one"

          
      else:
         
          print("Sensor failure. Check wiring.");
          time.sleep(1);
          
while True:      
  loop_run = int(db.child("loop_run").get().val())
  if(loop_run):
    loop_fun()
    time.sleep(1);
  
  
  