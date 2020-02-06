#libraries
import RPi.GPIO as GPIO
import time
import cv2
from firebase import firebase
from datetime import datetime

#GPIO Moode (BOARD/BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN/OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

cap = cv2.VideoCapture(0)

# Create the haar cascade
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Link to firebase database
firebase = firebase.FirebaseApplication('Enter your Firebase Auth here', None)

def distance():
    #set Trigger yo HIGH
    GPIO.output(GPIO_TRIGGER, True)
    
    #set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    
    StartTime = time.time()
    StopTime = time.time()
    
    #save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        
    #save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    
    #time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    #multiply with the sonic speed (34300 cm/s)
    #and divide by 2, because there and back
    distance = (TimeElapsed*34300)/2
    
    return distance

def database(curr_date, curr_time, count):
    data = { 'Date': curr_date,
             'Time': curr_time,
             'Number of people in room': count
            }
    firebase.post('/example-room-number-42', data)

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" %dist)
            time.sleep(0.1)
            
            if dist < 80:
                i = 30
                
                while i>0:
                    ret, frame = cap.read()

                    # Our operations on the frame come here
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # Detect faces in the image
                    faces = faceCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.2,
                        minNeighbors=5,
                        minSize=(30, 30)
                        #flags = cv2.CV_HAAR_SCALE_IMAGE
                    )

                    print("Found {0} faces!".format(len(faces)))

                    # Draw a rectangle around the faces
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


                    # Display the resulting frame
                    cv2.imshow('frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    
                    i -= 1
                    
                now = datetime.now()
                curr_date = now.strftime("%d/%m/%Y")
                curr_time = now.strftime("%H:%M:%S")
                count = format(len(faces))
                print(count + ' people in the room on ' + curr_date + ' and time ' + curr_time)
                database(curr_date, curr_time, count)
                                   
    except KeyboardInterrupt:        
        print("Measurement stopped by User")
        GPIO.cleanup()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

                


