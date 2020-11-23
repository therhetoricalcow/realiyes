from __future__ import print_function
import FPS
import Pupil_Tracker
import argparse
import cv2
import tflite_model

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=10000,help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=1,help="Whether or not frames should be displayed")
args = vars(ap.parse_args())
model = tflite_model.tflite_model(model_file='/home/avaneesh/Downloads/model.tflite')

print("[INFO] sampling frames from webcam...")


pupil1 = Pupil_Tracker.Pupil_Tracker(src=-1)
pupil2 = Pupil_Tracker.Pupil_Tracker(src=2)
pupil1.start()
pupil2.start()

fps1 = FPS.FPS().start()
fps2 = FPS.FPS().start()
while fps1._numFrames < args["num_frames"]:

    frame1 = pupil1.read()
    frame2 = pupil2.read()

    if args["display"] > 0:
        cv2.imshow("Predicted_Frame1", model.predict(pupil1.preprocess(frame=frame1)))
        key1 = cv2.waitKey(1) & 0xFF
        cv2.imshow("Predicted_Frame2", model.predict(pupil2.preprocess(frame=frame2)))
        key2 = cv2.waitKey(1) & 0xFF
        cv2.imshow("Frame1", (frame1))
        key1 = cv2.waitKey(1) & 0xFF
        cv2.imshow("Frame2", (frame2))
        key2 = cv2.waitKey(1) & 0xFF
	# update the FPS counter
    fps1.update()
    fps2.update()
# stop the timer and display FPS information
fps1.stop()
fps2.stop()
print("[INFO] elasped (Camera1) time: {:.2f}".format(fps1.elapsed()))
print("[INFO] approx. (Camera1) FPS: {:.2f}".format(fps1.fps()))
# do a bit of cleanup
cv2.destroyAllWindows()
pupil1.stop()
pupil2.stop()