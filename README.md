# Inferno
FPGA Deployable Fire Detection Model for Real-Time Video Surveillance Systems Using Convolutional Neural Networks


Project Description: The project serves as an alternative method to ordinary fire detection
using short-range smoke and heat sensors. No special hardware is required here, just a camera
and computer analysing the cameras output. We are proposing a cost-effective CNN
framework for flame detection in surveillance videos using images and videos based on deep
learning. Transfer learning has been used in training the model wherein a pre-trained
MobileNet architecture was modified and trained specific to our dataset (3GB) consisting of
fire and non fire images extracted from real time footage. The trained model achieved an
overall accuracy of 98% and was deployed onto a raspberry pi3 (1GB RAM). The time taken
by the model to classify a frame as fire / non-fire is around 0.78 seconds on the raspberry pi.
In case of positive fire detection consecutively for 20 frames, the notification system is
triggered and a fire alarm is raised.

For more details view the research publication for the project, Do cite if used :)

https://ieeexplore.ieee.org/document/8978439
https://www.researchgate.net/publication/336639483_FPGA_Deployable_Fire_Detection_Model_for_Real-Time_Video_Surveillance_Systems_Using_Convolutional_Neural_Networks


Technologies Used: Python3, Deep learning: Convolutional Neural Networks (CNN),
openCV, Tensorflow, Keras, Computer Vision, Cloud Computing, Transfer Learning.
