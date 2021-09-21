"""
### https://pypi.org/project/opencv-python/
- pip install opencv-python
### https://pypi.org/project/numpy/
- pip install numpy

haarcascades for face and eye
"""
# https://github.com/opencv/opencv/tree/master/data/haarcascades

import os
import cv2
import numpy as np

def face_detection(frame):
	# to gray
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# detect faces
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x, y, w, h) in faces:
		img = frame[y-10:y+h+10, x-10:x+w+10][:,:,::-1]
		
		dets = cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
		# พื้นที่ใบหน้า
		
		g = gray[y:y+h, x:x+h]
		c = img[y:y+h, x:x+h]

		# Detect eye
		eyes = eye_cascade.detectMultiScale(g)
		
		# for eye
		for (ex, ey, ew, eh) in eyes:
			# วาดสี่เหลี่ยม
			cv2.rectangle(c, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)
	
	cv2.imshow('img', img)
	

if __name__ == "__main__":
	# https://stackoverflow.com/questions/918154/relative-paths-in-python
	"""
	import os
	dirname = os.path.dirname(__file__)
	filename = os.path.join(dirname, 'relative/path/to/file/you/want')

	"""
	# --- เตรียม haarcascade eye และ face --- #
	dirname = os.path.dirname(__file__)
	h_eye = os.path.join(dirname, 'haarcascade_eye.xml')
	h_face = os.path.join(dirname, 'haarcascade_frontalface_default.xml')

	eye_cascade = cv2.CascadeClassifier(h_eye)
	face_cascade = cv2.CascadeClassifier(h_face)

	# ใช้กล้อง
	cap = cv2.VideoCapture(0)

	while True:
		_, frame = cap.read()
		face_detection(frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

