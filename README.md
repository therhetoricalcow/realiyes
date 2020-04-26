# realiyes

This is a passion project that I've been working on since the start of college. It takes ideas from Convolutional Neural Networks, 
Image Segmenations, Computer Vision Feature Engineering, Signal Processing, Signal Filtering, and theres lots more to come!

I introduce to you a labeling tool for eye-contouring for a variety of light conditions to help make your training-set
and based on ideas from DeepVOG and other Encoder-Decoder Archicetcures, a Pretrained Model that will give solid accuracy for 
gaze detection as well as estimation. 


Using this we can effectively map the gaze models into a 3d eye-ball model which 
will be used along with the external mappings of the training set to estimate the location of the gaze on the screen using
Extended Kalman Filtering with the Dimensional output of the mapped ellipse to (x,y) and the gaze estimation (two vectors coinciding)
to give us some insight.

Head Movement and Rotation will be corrected with an IMU as well as two TOF sensors for extended Filtering to avoid drift
as well as to give accurate pupil locations. 

The goal is to get this to work Real-time using Python/C++
