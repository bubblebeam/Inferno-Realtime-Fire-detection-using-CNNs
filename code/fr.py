#code to extract frames from video
import cv2
print(cv2.__version__)
vidcap = cv2.VideoCapture('/home/ramya/Desktop/project/mivia_fire/fire14.avi')
success,image = vidcap.read()
count = 0
success = True
while success:
  cv2.imwrite("/home/ramya/Desktop/project/fire14/frame%d.jpg" % count, image)     # save frame as JPEG file
  success,image = vidcap.read()
  #print 'Read a new frame: ', success
  count += 1
