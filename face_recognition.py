"""
### https://pypi.org/project/opencv-python/
- pip install opencv-python
### https://pypi.org/project/numpy/
- pip install numpy
"""
import os 
import cv2  # Open-CV
import numpy as np

# https://github.com/opencv/opencv/tree/master/data/haarcascades
# --- เตรียม haarcascade eye และ face --- #
dirname = os.path.dirname(__file__)  # เช็ค path
h_eye = os.path.join(dirname, 'haarcascade_eye.xml')  # path ของ haarcascade eye
h_face = os.path.join(dirname, 'haarcascade_frontalface_default.xml')  # path ของ haarcascade face
eye_cascade = cv2.CascadeClassifier(h_eye)  # โหลด haarcascade eye
face_cascade = cv2.CascadeClassifier(h_face)  # โหลด haarcascade face


# ฟังก์ชันสำหรับ ตรวจจับใบหน้า
def face_detection_filter(faces, filter_img, gray, ret, img, o_filter_h, o_filter_w, img_h, img_w):
	for (x, y, w, h) in faces:
		# พิกัดใบหน้า
		face_w, face_h = w, h
		face_x1, face_x2 = x, (x + face_w)
		face_y1, face_y2 = y, y + face_h
		
		# ทำให้ฟิลเตอร์สัมพันธ์กับใบหน้าโดยการสเกล
		filter_width = int(1.5 * face_w)
		filter_height = int(filter_width * o_filter_h / o_filter_w)

		# ตั้งค่าพิกัดของฟิลเตอร์
		filter_x1 = face_x2 - int(face_w/2) - int(filter_width/2)
		filter_x2 = filter_x1 + filter_width
		filter_y1 = face_y1 - int(face_h*1.25)
		filter_y2 = filter_y1 + filter_height

		# เข็คเพื่อไม่ให้หลุดเฟรม
		if filter_x1 < 0:
			filter_x1 = 0
		if filter_y1 < 0:
			filter_y1 = 0

		if filter_x2 > img_w:
			filter_x2 = img_w
		if filter_y2 > img_h:
			filter_y2 = img_h

		# การเปลี่ยนแปลงของเฟรม
		filter_width = filter_x2 - filter_x1
		filter_height = filter_y2 - filter_y1

		# ลดขนาด ฟิลเตอร์ให้พอดีกับใบหน้า โดยการอินเทอร์โพเลชัน
		filter_img = cv2.resize(filter_img, (filter_width, filter_height), interpolation = cv2.INTER_AREA)
		mask = cv2.resize(o_mask_inv, (filter_width, filter_height), interpolation = cv2.INTER_AREA)
		mask_inv = cv2.resize(o_mask_inv, (filter_width, filter_height), interpolation = cv2.INTER_AREA)

		# rectangular region of interest (ROI)
		# รับ ROI ของฟิลเตอร์ จากพื้นหลัง
		roi = img[filter_y1:filter_y2, filter_x1:filter_x2]

		# รูปภาพต้นฉบับในพื้นหลังที่ไม่มีฟิลเตอร์
		roi_bg = cv2.bitwise_and(roi, roi, mask=mask)
		roi_fg = cv2.bitwise_and(filter_img, filter_img, mask = mask_inv)
		# ภาพเอาท์พุทที่ขนาดเท่ากันกับภาพดั้งเดิม
		dst = cv2.add(roi_bg, roi_fg)

		# ใส่กลับในภาพดั้งเดิม
		img[filter_y1:filter_y2, filter_x1:filter_x2] = dst


		break


# อ่านภาพ ฟิลเตอร์
filter_img = cv2.imread('_filter/rabbit.png')

# ดึงรูปร่างของฟิลเตอร์มา
o_filter_h, o_filter_w, filter_channels = filter_img.shape

# แปลงเป็นสีเทา
filter_gray = cv2.cvtColor(filter_img, cv2.COLOR_BGR2GRAY)

# สร้างหน้ากาก 
ret, o_mask = cv2.threshold(filter_gray, 10, 255, cv2.THRESH_BINARY_INV)
# inverse ฟิลเตอร์
o_mask_inv = cv2.bitwise_not(o_mask)

# ใช้กล้อง
cap = cv2.VideoCapture(0)
ret, img = cap.read()
img_h, img_w = img.shape[:2]

while True:
	# อ่านภาพจาก เฟรม
	ret, img = cap.read()
	# แปลงเป็นภาพระดับเทา
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# หาหน้าในภาพ โดยใช้ classififier
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	# ใช้ฟังก์ชันที่ประกาศไว้สำหรับตรวจจับหน้าและทำการใส่ฟิลเตอร์
	face_detection_filter(faces, filter_img, gray, ret, img, o_filter_h, o_filter_w, img_h, img_w)
		
	# แสดงภาพ
	cv2.imshow('img', img)

	# สำหรับหยุดการรัน
	if cv2.waitKey(1) == ord('q'):
		break

# ปิดกล้อง
cap.release()
# ปิดหน้าต่าง figure
cv2.destroyAllWindows() 
