# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import cv2
import numpy as np

leftimg = cv2.imread("/Users/brendan/Desktop/rightimg.jpeg")
leftimg = cv2.cvtColor(leftimg,cv2.COLOR_BGR2GRAY)

rightimg = cv2.imread("/Users/brendan/Desktop/leftimg.jpeg")
rightimg = cv2.cvtColor(rightimg,cv2.COLOR_BGR2GRAY)

#Registration
sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(rightimg,None)
kp2, des2 = sift.detectAndCompute(leftimg,None)

cv2.imshow('test',cv2.drawKeypoints(rightimg,kp1,None))
cv2.waitKey(0)
cv2.imshow('test',cv2.drawKeypoints(leftimg,kp1,None))
cv2.waitKey(0)

match = cv2.BFMatcher()
matches = match.knnMatch(des1,des2,k=2)

good = []
for m,n in matches:
    if m.distance < 0.03*n.distance:
        good.append(m)

draw_params = dict(matchColor=(0,255,0),
                   singlePointColor=None,
                   flags=2)

img3 = cv2.drawMatches(rightimg,kp1,leftimg,kp2,good,None,**draw_params)
cv2.imshow("original_image_draw_matches.jpg",img3)
cv2.waitKey(0)

MIN_MATCH_COUNT = 10
if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dst_pts = np.float32([kp1[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    h, w = leftimg.shape
    pts = np.float32([[0,0],[0,h-1],[w-1,h-1],[w-1,0]]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts, M)
    rightimg = cv2.polylines(rightimg, [np.int32(dst)],True,255,3,cv2.LINE_AA)
    cv2.imshow("overlapping",rightimg)
    cv2.waitKey(0)
else:
    print("Not enough matches - %d/%d", (len(good)/MIN_MATCH_COUNT))
