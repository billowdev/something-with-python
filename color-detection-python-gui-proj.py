# pre processsing python tkinter gui
# หากเราสั่ง plt.plot(….) มันจะสร้างกราฟเส้นทันที (ถ้าจะ plot กราฟประเภทอื่นต้องสั่งด้วยคำสั่งอื่น) โดยเราสามารถระบุค่า x และ ค่า y ที่ต้องการได้ ดังนี้
from email.mime import image
from tkinter import ttk, filedialog
from glob import glob
from turtle import left
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import cv2  # เป็นคำสั่งที่ใช้ในการค้นสิ่งที่ต้องการจากรูปภาพเป็นคำสั่งที่ใช้ในการค้นสิ่งที่ต้องการจากรูปภาพ
# ทำให้เราเรียกใช้งานฟังก์ชันเป็นคุณสมบัติหลักของ NumPy มีลักษณะคล้ายกับ list ยกเว้น สมาชิกทุกตัวใน array จะต้องเป็นข้อมูลชนิดเดียวกัน โดยทั่วไปแล้วข้อมูล ที่เก็บจะเป็นตัวเลขเช่น int หรือ float.
import numpy as np
import tkinter as Tk
root = Tk.Tk()
root.title('Detection')
root.geometry('1366x768')

# ---------------- browse file
# กำหนดรูปภาพค่าเริ่มต้น red2.jpg
image_name = "red2.jpg"
# อ่านภาพเป็น array เพื่อกำหนดภาพเริ่มต้น และกำหนดตัวแปรเริ่มต้มของ ภาพสีแต่ละสี เพื่อไม่ให้โปรแกรม Error
im_array = cv2.imread(image_name)
img_green = ImageTk.PhotoImage(image=Image.fromarray(im_array))
img_red = ImageTk.PhotoImage(image=Image.fromarray(im_array))
img_dark = ImageTk.PhotoImage(image=Image.fromarray(im_array))
img_original = ImageTk.PhotoImage(image=Image.fromarray(im_array))
# สร้างตัวแปร image_name_label เพื่อแสดงค่า รูปภาพ และ ที่อยู่ของรูปภาพ
image_name_label = Tk.Label(root, text=image_name, font=('Georgia 13'))
image_name_label.pack(pady=15)
# ฟังก์ชัน โหลดรูปภาพพร้อมทำการ แยกสี
def open_file():
    # อ้างอิง ถึงตัวแปร รูปภาพที่ได้กำหนด เป็นค่าเริ่มต้นไว้ก่อนหน้านี้
    global image_name, img_green, img_red, img_dark, img_original
    # ทำการอ่านที่อยู่ไฟล์โดยใช้ฟังก์ชัน filedialog
    file = filedialog.askopenfile(
        mode='r', filetypes=[('image Files', ['*.png', '*.jpg'])])
    # กำหนดให้ที่อยู่ไฟล์ อยู่ในตัวแปร  image_name
    image_name = file.name
    # ทำการเปลี่ยนค่า (ลาเบล) ที่แสดง เป็นข้อความ ของที่อยู่ไฟล์
    image_name_label.config(text = f"คุณกำลังอ่านภาพ -- {str(image_name).split('/')[-1]} -- จาก {image_name}")
    # -------------------------------- เริ่มต้น โค้ดในส่วน การแยกสี -----------------------------
    # ใช้อ่านภาพจากไฟล์เข้ามาเป็นอาเรย์ของ numpy
    frame = cv2.imread(image_name)
    # แปลงจาก RGB เป็น HSV ก็จะใช้ cv2.COLOR_RGB2HSV ถ้ากลับกันก็จะเป็น cv2.COLOR_HSV2RGB
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # เวลาที่จะแปลงจากระบบ BGR ใน opencv ให้เป็น RGB เช่นเพื่อใช้ใน matplotlib อาจใช้ cv2.cvtColor โดยใส่ cv2.COLOR_BGR2RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # ทำการตรวจจับสีเเดง
    # หาค่าต่ำสุดของสีเเดง มาเก็บไวใน นัมพายาบทที่ทำการตั้งชื่อเป็น np
    low_red = np.array([161, 155, 84])
    # หาค่าสูงสุดของสีเเดง มาเก็บไว้ใน นัมพายที่ทำการตั้งชื่อเป็น np
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    # มาร์กสีเเดงที่ใช้เเล้วทำการเทียบสีจริงโดยที่ดคงออกมาเฉพาะสีเเดงเท่านั้น
    red = cv2.bitwise_and(frame, frame, mask=red_mask)
    # นำภาพบิตมาทำการหาค่าสีเเดง โดยใช้เเอน ว่าเป็นสีเเดงให้ทำการโชว์ ถ้าไม่เป็นสีเเดงไม่ต้องโชว์

    # ทำการตรวจจับสีเขียว
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, mask=green_mask)

    # ทำการตรวจจับสีดำ
    low_darkmagenta = np.array([0, 0, 0])
    high_darkmagenta = np.array([105, 105, 105])
    darkmagenta_mask = cv2.inRange(
        hsv_frame, low_darkmagenta, high_darkmagenta)
    darkmagenta = cv2.bitwise_and(frame, frame, mask=darkmagenta_mask)
     # -------------------------------- สิ้นสุด โค้ดในส่วน การแยกสี -----------------------------
     
     # -------------------------------- โค้ด ด้านล่าง เป็นการเปลี่ยนค่า จาก ภาพ array เป็นภาพของ GUI 
    img_green = ImageTk.PhotoImage(image=Image.fromarray(green))
    img_red = ImageTk.PhotoImage(image=Image.fromarray(red))
    img_dark = ImageTk.PhotoImage(image=Image.fromarray(darkmagenta))
    img_original = ImageTk.PhotoImage(image=Image.fromarray(frame))


# ป้ายแสดง ข้อความ "กดเพื่อโหลดรูปภาพ"
label = Tk.Label(root, text="กดเพื่อโหลดรูปภาพ", font=('Georgia 13'))
label.pack(pady=10)

# ปุ่ม เพื่อทำการ โหลดที่อยู่ภาพ
a = Tk.Button(root, text="Browse", command=open_file).pack(pady=20)
# ---------------- browse file

# ตั้งค่ากรอบเพื่อ แสดงรูปภาพ
canvas1 = Tk.Canvas(root, width=500, height=500)
canvas1.place(x=500, y=140)


# ฟังก์ชันสำหรับ เปลี่ยนรูปภาพ เพื่อโชว์ ในเฟรม
def callCreate(canvas1, img):
    return canvas1.create_image(20, 20, anchor="nw", image=img)

# ฟังชันก์สำหรับ แสดงรูปภาพ สีดำ
def on_click_dark(event):
    global canvas1, img_dark
    return callCreate(canvas1, img_dark)

# ฟังชันก์สำหรับ แสดงรูปภาพ ต้นฉบับ
def on_click_original(event):
    global canvas1, img_original
    return callCreate(canvas1, img_original)

# ฟังชันก์สำหรับ แสดงรูปภาพ สีเขียว
def on_click_green(event):
    global canvas1, img_green
    return callCreate(canvas1, img_green)

# ฟังชันก์สำหรับ แสดงรูปภาพ สีแดง
def on_click_red(event):
    global canvas1, img_red
    return callCreate(canvas1, img_red)

# ปุุ่ม เพื่อแสดงภาพ จากการแยกสี (ต้นฉบับ)
original_canvas = Tk.Button(root, height=5, width=10, text="original")
original_canvas.place(x=200, y=10)
original_canvas.bind("<Button-1>", on_click_original)
original_canvas.focus_set()

# ปุุ่ม เพื่อแสดงภาพ จากการแยกสี (สีเขียว)
green_button = Tk.Button(root, height=5, width=10,
                         text="unripe", justify='left')
green_button.bind("<Button-1>", on_click_green)
green_button.place(x=100, y=10)
green_button.focus_set()

# ปุุ่ม เพื่อแสดงภาพ จากการแยกสี (สีแดง)
red_canvas = Tk.Button(root, height=5, width=10, text="ripe")
red_canvas.bind("<Button-1>", on_click_red)
red_canvas.place(x=100, y=110)
red_canvas.focus_set()

# ปุุ่ม เพื่อแสดงภาพ จากการแยกสี (สีดำ)
dark_canvas = Tk.Button(root, height=5, width=10, text="unripe")
dark_canvas.bind("<Button-1>", on_click_dark)
dark_canvas.place(x=200, y=110)
dark_canvas.focus_set()

# กำหนดให้โปรแกรมทำงาน จนกว่าจะถูกปิดโปรแกรม
root.mainloop()
