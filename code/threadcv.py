#The program that is run on the raspberrypi
#Ensure that a raspberry pi camera module is connected to the pi for video streaming
#It does the final realtime prediction by taking continuous video feed from the camera, inputting each frame to the model and performing prediction on each frame abd outputting result
#Connect a Speaker to the raspberry pi to hear siren after positive fire detection


from __future__ import print_function
class PiVideoStream:
    def __init__(self, resolution=(320, 240), framerate=32):
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

class VideoStream:
    def __init__(self, src=0, usePiCamera=False, resolution=(320, 240),
        framerate=32):
        # check to see if the picamera module should be used
        if usePiCamera:
            # only import the picamera packages unless we are
            # explicity told to do so -- this helps remove the
            # requirement of `picamera[array]` from desktops or
            # laptops that still want to use the `imutils` package
            from pivideostream import PiVideoStream
 
            # initialize the picamera stream and allow the camera
            # sensor to warmup
            self.stream = PiVideoStream(resolution=resolution,
                framerate=framerate)
 
        # otherwise, we are using OpenCV so initialize the webcam
        # stream
        else:
            self.stream = WebcamVideoStream(src=src)

    def start(self):
        # start the threaded video stream
        return self.stream.start()
 
    def update(self):
        # grab the next frame from the stream
        self.stream.update()
 
    def read(self):
        # return the current frame
        return self.stream.read()
 
    def stop(self):
        # stop the thread and release any resources
        self.stream.stop()
            

import cv2
import imutils
import keras
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from imutils.video import VideoStream
from imutils.video import FPS
from threading import Thread
import numpy as np
import time
import os
from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.video.pivideostream import PiVideoStream
import datetime
from pygame import mixer
 

# initialize the total number of frames that *consecutively* contain fire
# along with threshold required to trigger the fire alarm
TOTAL_CONSEC = 0
TOTAL_THRESH = 20
# initialize the fire alarm
FIRE = False


# load the model
print("[INFO] loading model...")
MODEL_PATH = '/home/pi/Desktop/raks_model14.h5'
model = keras.models.load_model(MODEL_PATH)

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
#vs = VideoStream(src=0).start()
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
start = time.time()
#fps = FPS().start()
f = 0

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    #A variable f to keep track of total number of frames read
    f += 1
    frame = imutils.resize(frame, width=400)
    # prepare the image to be classified by our deep learning network
    image = cv2.resize(frame, (224, 224))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
 
    # classify the input image and initialize the label and
    # probability of the prediction
    begin = time.time()
    (fire, notFire) = model.predict(image)[0]
    terminate = time.time()

    label = "Not Fire"
    proba = notFire
    # check to see if fire was detected using our convolutional
    # neural network
    if fire > notFire:
        # update the label and prediction probability
        label = "Fire"
        proba = fire
 
        # increment the total number of consecutive frames that
        # contain fire
        TOTAL_CONSEC += 1
        if not FIRE and TOTAL_CONSEC >= TOTAL_THRESH:
            # indicate that fire has been found
            FIRE = True
            #CODE FOR NOTIFICATION SYSTEM HERE
	    #A siren will be played indefinitely on the speaker
            mixer.init()
            mixer.music.load('/home/pi/Desktop/siren.mp3')
            mixer.music.play(-1)
            # otherwise, reset the total number of consecutive frames and the
    # fire alarm
    else:
        TOTAL_CONSEC = 0
        FIRE = False
        
        # build the label and draw it on the frame
    label = "{}: {:.2f}%".format(label, proba * 100)
    frame = cv2.putText(frame, label, (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    #fps.update()
 
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        print("[INFO] classification took {:.5} seconds".format(terminate - begin))
        end = time.time()
        break

# do a bit of cleanup
print("[INFO] cleaning up...")
seconds = end - start
print("Time taken : {0} seconds".format(seconds))
fps  = f/ seconds
print("Estimated frames per second : {0}".format(fps))
#fps.stop()
#print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
#print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
