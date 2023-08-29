import socket
import cv2
import serial
import numpy as np
from contact_to_server import *
import threading


img=cv2.imread("1.jpg")
print(img.shape[:2])
h,w = img.shape[:2]
img2=img[1:h,1:w]

cv2.imshow("111",img2)
cv2.waitKey(0)



