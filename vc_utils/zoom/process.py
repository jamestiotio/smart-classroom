# coding: utf-8
# Collect & Process Zoom Video Data Stream
# Created by James Raphael Tiovalen (2020)

# Import libraries
import cv2
import numpy as np
import settings

stream_url = settings.stream_url + "/" + settings.stream_key
cap = cv2.VideoCapture(stream_url)

while True:
    ret, frame = cap.read()
    cv2.imshow("Stream Data", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()