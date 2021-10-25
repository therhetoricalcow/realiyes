from Pupil_Camera import Pupil_Camera
import numpy

p = Pupil_Camera()
p.assignVideoCaps('/home/pi/Desktop/1.mp4','/home/pi/Desktop/2.mp4')
p.start()
j = 0

while(j<100):
	p.write()
	print(j)
	j = j+1
p.stop()
