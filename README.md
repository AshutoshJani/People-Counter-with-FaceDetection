# People-Counter-with-FaceDetection
## People counter using Face Detection for Raspberry Pi using CSI Camera Module and Ultrasonic Sensor and upload database to Firebase

This is the code to Count people in a room using Raspberry Pi 3/3b, CSI Camera Module and Ultrasonic sensor along with the codes for all parts of this IoT solution seperately.
To run the entire program just run in the terminal of the Raspberry Pi
```python
python IoT.py
```
---

To upload the number of people in room to Firebase, just add the the Firebase Auth Key in the *Link to Firebase* section of the IoT.py python file.

---

This project work on the basis of Event Detection using the ultrasonic sensor that will detect when a person enters or exits a room by placing it on the frame of the door, when the utrasonic sensor detects an event it switches on the camera and takes images and countes the number of people present in the room using Face Detection of the OpenCV library and the *haarcascade_frontalface_default.xml* data

### Overall Architecture
![architecture.png](https://github.com/AshutoshJani/People-Counter-with-FaceDetection/blob/master/overall%20architecture.png "Overall Architecture")

---

### References
+ [Face Detection Code](https://github.com/shantnu/FaceDetect)
+ [Face Detection Explaination](https://realpython.com/face-recognition-with-python/)
+ [Ultrasonic Sensor Code, Explaination and Circuit Diagram](https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/)
+ [Uploading to Firebase](https://codeloop.org/python-firebase-real-time-database/)
