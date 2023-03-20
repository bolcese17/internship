# This is a sample Python script.
/Users/brendan/PycharmProjects/internship_test/main.py
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import cv2
import numpy as np

clip1 = cv2.VideoCapture('video stitching/here/finaldash1.mp4')
clip2 = cv2.VideoCapture('video stitching/here/finalhood1.mp4')
'''
#Just plays both videos in seperate windows 

while (clip1.isOpened() and clip2.isOpened()):
    # Capture frame-by-frame
    ret, frame = clip1.read()
    ret1,frame1 = clip2.read()
    if ret == True:

        # Display the resulting frame
        cv2.imshow('Frame', frame)
        cv2.imshow('Frame1', frame1)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break


while (clip2.isOpened()):
    # Capture frame-by-frame
    ret, frame = clip2.read()
    if ret == True:

        # Display the resulting frame
        cv2.imshow('Frame', frame)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

'''

#plays both videos horizontally stacked
width = clip1.get(cv2.CAP_PROP_FRAME_WIDTH)
height = clip1.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = clip1.get(cv2.CAP_PROP_FPS)
print('fps:', fps)

video_format = cv2.VideoWriter_fourcc(*'MP42')  # .avi
final_clip = cv2.VideoWriter('output.avi', video_format, fps, (int(width), int(height)))

delay = int(1000 / fps)
print('delay:', delay)

while True:

    ret1, fakeframe1 = clip1.read()
    ret2, frame2 = clip2.read()

    if not ret1 or not ret2:
        break

    final_frame = np.hstack([fakeframe1, frame2])  # two videos in one row
    final_clip.write(final_frame)

    cv2.imshow('Video', final_frame)
    key = cv2.waitKey(delay) & 0xFF

    if key == 27:
        break

cv2.destroyWindow('Video')


minutes = 0
seconds = 10
frame_id = int(fps*(minutes*60 + seconds))

#grabs single frames
clip1.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
ret, frame1 = clip1.read()

clip2.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
ret, frame2 = clip2.read()

#shows frames
cv2.imshow('frame1', frame1)
cv2.imshow('frame2', frame2)
cv2.waitKey(0)

sift = cv2.SIFT_create()
kp = sift.detect(frame1,None)

img = cv2.drawKeypoints(frame1,kp,frame1)

kp2 = sift.detect(frame1,None)

img2 = cv2.drawKeypoints(frame2,kp2,frame2)

cv2.imshow('keypoints1',img)
cv2.imshow('keypoints2',img2)
cv2.waitKey(0)

#run on each from, match and stitch for each frame
