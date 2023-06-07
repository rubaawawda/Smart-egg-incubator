import RPi.GPIO as GPIO
import time
import pyrebase


config = {    
  "apiKey": "AIzaSyAVaxr6n1VKLm_dw96nQymhzT82heEyxMs",
  "authDomain": "smart-egg-incubator-3a272.firebaseapp.com",
  "databaseURL":"https://smart-egg-incubator-3a272-default-rtdb.firebaseio.com/",
  "storageBucket": "smart-egg-incubator-3a272.appspot.com"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

GPIO.setwarnings(False)
DC1 = 27
DC2 = 17
BUTTON1 = 21
BUTTON2 = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(DC1,GPIO.OUT)
GPIO.setup(DC2,GPIO.OUT)
GPIO.setup(BUTTON1,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(BUTTON2,GPIO.IN, pull_up_down = GPIO.PUD_UP)

type_selected = db.child("current_value").get().val()
type_selected=type_selected.replace('"', '')
incubate_days = db.child("setting").child("kind_properties").child(str(type_selected)).child("incubate days").get().val()

# current_incubate_time = db.child("current incubate time").get().val()/60/60/24

direction = ""
next_direction = "one"
last_move_time = time.time()
try:
    while True:
        button1_state = GPIO.input(BUTTON1)
        button2_state = GPIO.input(BUTTON2)
        if 0 < 7 < incubate_days-3:

            direction=next_direction

            if (button1_state == 1 and button2_state == 1) or (time.time()-last_move_time>10):
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


except keyboardInterrupt:
    GPIO.cleanup()    
        
