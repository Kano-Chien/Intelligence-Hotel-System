import socket
import cv2
from paddleocr import PaddleOCR
import serial
import numpy as np



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
    #['174' '143' '229' '260' '姓老张学彬']
    return bboxs


# 建立串口物件
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver_ip = '接收端的IP地址'
receiver_port = 12345


cap = cv2.VideoCapture(0)


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

while True:
    try:
        ser = serial.Serial('COM4', 9600)
        ser.close()
        # 打開串口
        ser.open()
        if ser.is_open:
            print('已打開串口:', ser.name)
    except:
        print("COM3還沒開啟")
    received_data = ser.readline()
    while(received_data.decode()[:-2] == "car"):
        print("READ_IMAGE")
        ret,frame = cap.read()
        BOX = ocr_info_to_location(ocr.ocr(frame)[0])
        if BOX is not None:
            break
    ser.close()



