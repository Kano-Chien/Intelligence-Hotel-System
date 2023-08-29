import threading
import time
import copy
import numpy as np
import serial
import concurrent.futures
from typing import List
import dlib
import os
import cv2
from contact_to_server import *
from glob import glob
from datetime import datetime

import keyboard


def cv2_imread(filename, img_type: str = 'bgr', max_workers: int = 8):
    def imread(filepath):
        img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), -1)
        if img.ndim == 2 and img_type.lower() == "bgr":
            return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif img.ndim == 3 and img_type.lower() == "gray":
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            return img

    if isinstance(filename, str):
        return imread(filename)
    elif isinstance(filename, list):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            return list(executor.map(imread, filename))
    else:
        print("傳入內容並非陣列或字串")
        return None


arduinoSerial = serial.Serial('COM4', 9600)
time.sleep(1)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

new_imgs = []
descriptors = []
imgs = []
face_recognition_result = False


def loading_img():
    while True:
        try:
            global imgs, new_imgs, descriptors
            # img_tmp = get_person_img()
            # new_imgs = [i[..., 0] for i in np.split(img_tmp, img_tmp.shape[-1], axis=3)]
            new_imgs = [cv2.imread(img) for img in glob(r'D:\PycharmProjects\mian\frames\*.png')]
            time.sleep(1)

            if (np.sum(np.array(imgs)) != np.sum(np.array(new_imgs))):
                descriptors = []
                imgs = copy.deepcopy(new_imgs)
                print("圖片變化，更新特徵")
                time.sleep(1)
                for img in imgs:
                    # 1.人臉偵測
                    dets = detector(img, 0)
                    for d in dets:
                        # 2.特徵點偵測
                        shape = predictor(img, d)
                        # 3.取得描述子，128維特徵向量
                        face_descriptor = facerec.compute_face_descriptor(img, shape)
                        # 轉換numpy array格式
                        v = np.array(face_descriptor)
                        descriptors.append(v)

            time.sleep(10)

        except:
            print("錯誤")
            time.sleep(10)


def camera():
    # time.sleep(10)
    # 讀取攝影機每一幀
    cap = cv2.VideoCapture(0)
    global face_recognition_result
    while True:
        time.sleep(0.1)
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # 1.人臉偵測
        dets = detector(frame, 0)
        d_test = None
        for d in dets:
            # 2.特徵點偵測
            shape = predictor(frame, d)
            # 3.取得描述子，128維特徵向量
            face_descriptor = facerec.compute_face_descriptor(frame, shape)
            # 轉換numpy array格式
            d_test = np.array(face_descriptor)

        score = 1
        for descriptor in descriptors:
            if d_test is None:
                d_test = np.ones_like(descriptor)
            dist = np.linalg.norm(descriptor - d_test)
            score = dist if dist < score else score

        if score < 0.3:
            cv2.putText(frame, "Yes " + str(round(score, 3)), (10, 30), cv2.FONT_HERSHEY_DUPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)
            face_recognition_result = True
        else:
            cv2.putText(frame, "No " + str(round(score, 3)), (10, 30), cv2.FONT_HERSHEY_DUPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)
            face_recognition_result = False

        cv2.imshow('live', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


t1 = threading.Thread(target=loading_img)
t1.start()
t2 = threading.Thread(target=camera)
t2.start()

send_data = ""


def send_data_func():
    global send_data
    while True:
        try:
            send_data = arduinoSerial.readline().decode().strip()
            time.sleep(1)
        except:
            _ = 0


t4 = threading.Thread(target=send_data_func)
t4.start()

car_state = 1

while True:
    time.sleep(1)
    # print(send_data)
    if send_data == '人在房門前':
        send_data = ''
        car_state = get_car_status()
        time.sleep(1)
        cleaning_session = get_cleaning_session()
        if len(cleaning_session) > 1:
            if cleaning_session[0] <= datetime.now().hour <= cleaning_session[1]:
                car_state = 1

        if car_state == 0:
            print("車不在")
            send_data = 'car_false'
            arduinoSerial.write(send_data.encode())
        elif car_state == 1:
            print("車在")
            send_data = 'car_true'
            arduinoSerial.write(send_data.encode())

    if send_data == 'face_recognition':
        print("開始辨識")
        while not face_recognition_result:
            if len(cleaning_session) > 1:
                if cleaning_session[0] <= datetime.now().hour <= cleaning_session[1]:
                    break
            time.sleep(1)
        print("python辨識成功")
        arduinoSerial.write('recognition_true'.encode())
        time.sleep(1)
        send_data = ''
    if send_data == "進入房門，送人在房間到server":
        update_person_status(1)
        print("python:進入房門，送人在房間到server")
        send_data = ""
    if send_data == "人剛出房間，送人不在房間到server":
        update_person_status(0)
        print("python:人剛出房間，送人不在房間到server")
        send_data = ""

    time.sleep(0.01)
    # 車不在
