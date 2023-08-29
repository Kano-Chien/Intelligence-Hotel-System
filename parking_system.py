import socket
import cv2
from paddleocr import PaddleOCR
import serial
import numpy as np
from contact_to_server import *
import threading


def ocr_info_to_location(ocr_info, acc=0):
    bboxs = None
    for info in ocr_info:
        if info[1][1] >= acc:
            info[0] = np.array(info[0], dtype=np.uint32)
            bbox = np.array([info[0][:, 1].min(), info[0][:, 0].min(
            ), info[0][:, 1].max(), info[0][:, 0].max(), info[1][0]])
            bboxs = np.array(
                [bbox]) if bboxs is None else np.vstack(
                (bboxs, bbox))
    # ['174' '143' '229' '260' '姓老张学彬']
    return bboxs


# 建立串口物件
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
car_in_list = []
car_status = 0
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# ret, frame = cap.read()

frame = None
BOX = []


def camera():
    time.sleep(3)
    global frame
    while True:
        ret, frame = cap.read()
        try:
            if(len(BOX)==2):
                cv2.putText(frame, BOX[1][4], (0, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 4, cv2.LINE_AA)
            else:
                cv2.putText(frame, "not detect", (0, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 4, cv2.LINE_AA)
        except:
            print("!!!")
        cv2.imshow("123", frame)
        cv2.waitKey(1)


t1 = threading.Thread(target=camera)
t1.start()
image = np.zeros((100, 200, 3), np.uint8)
ocr = PaddleOCR(use_angle_cls=True,
                lang='en',
                use_gpu=False,
                enable_mkldnn=True,
                # rec_batch_num=30,
                det_max_side_len=3200,
                # drop_score=0,
                det_db_score_mode='slow',
                # det_db_box_thresh=0,
                # det_db_thresh=0.01
                )

try:
    ser = serial.Serial('COM5', 9600)
    ser.close()
    # 打開串口
    ser.open()
    ser.flushInput()
    ser.flushOutput()
    if ser.is_open:
        print('已打開串口:', ser.name)
except:
    print("還沒開啟")
    exit()

while True:
    ser.flushInput()
    ser.flushOutput()
    received_data = ser.readline()
    if (received_data.decode()[:-2] == "car"):
        print("READ_IMAGE")
        # ret, frame = cap.read()

        BOX = ocr_info_to_location(ocr.ocr(frame)[0])
        if BOX is not None:
            car_list = get_car_information()
            try:
                if (BOX[1][4] in car_list):
                    data = "in"
                    car_status = 1
                    car_in_list.append(BOX[0][4])
                else:
                    data = "not in list"
            except:
                continue
            time.sleep(2)
            update_car_status(car_status)
            ser.write(data.encode("utf-8"))
            ser.flush()
            time.sleep(2)
            increase_waiting_person()
            print(BOX)
            print(data)
    if (received_data.decode()[:-2] == "car_out"):
        print("READ_IMAGE_car_out")
        BOX = ocr_info_to_location(ocr.ocr(frame)[0])
        person_status = get_person_status()
        if BOX is not None:
            if person_status == 1:
                data = "close"
            else:
                data = "open"
                car_status = 0
            time.sleep(2)
            ser.write(data.encode("utf-8"))
            ser.flush()
            time.sleep(2)
            update_car_status(car_status)
            print(BOX)
            print(data)
