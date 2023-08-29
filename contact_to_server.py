import pickle
import socket
import time
import cv2

receiver_ip = "192.168.137.76" #'192.168.1.197'
receiver_port = 12345


# car_information
def get_car_information():
    # 建立Socket連接
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # receiver_ip = '192.168.1.197'
    # receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    # 要傳送的數據
    data = 'car_information'
    # 傳送數據
    s.sendall(data.encode())
    data = b""
    while True:
        packet = s.recv(4096)
        if not packet:
            break
        data += packet
    car_list = pickle.loads(data)
    s.close()

    return car_list


# update_car_information
def update_car_information(car_list):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # receiver_ip = '192.168.1.197'
    # receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    # 要傳送的數據
    data = 'update_car_information'
    # 傳送數據
    s.sendall(data.encode())
    # 更新car_list
    time.sleep(1)
    data = pickle.dumps(car_list)
    s.sendall(data)
    print(car_list)
    s.close()


# increase_waiting_person
def increase_waiting_person():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 10000
    # receiver_ip = '192.168.1.197'
    # receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    # 要傳送的數據
    data = 'increase_waiting_person'
    # 傳送數據
    s.sendall(data.encode())


def decrease_waiting_person():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 10000
    # receiver_ip = '192.168.1.197'
    # receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    # 要傳送的數據
    data = 'decrease_waiting_person'
    # 傳送數據
    s.sendall(data.encode())
def get_cleaning_session():
    # get_person_img
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # receiver_ip = '192.168.1.197'
    # receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    # 要傳送的數據
    data = 'get_cleaning_session'
    # 傳送數據
    s.sendall(data.encode())
    data = b""
    while True:
        packet = s.recv(4096)
        if not packet:
            break
        data += packet
    cleanning_session = pickle.loads(data)
    s.close()
    return cleanning_session

# update_cleaning_session
def update_cleaning_session(cleaning_session):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # receiver_ip = '192.168.1.197'
    # receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    # 要傳送的數據
    data = 'update_cleaning_session'
    # 傳送數據
    s.sendall(data.encode())
    # 更新car_list
    time.sleep(1)
    data = pickle.dumps(cleaning_session)
    s.sendall(data)
    s.close()


# update_person_img
def update_person_img(img):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # receiver_ip = '192.168.1.197'
    # receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    # 要傳送的數據
    data = 'update_person_img'
    # 傳送數據
    s.sendall(data.encode())
    # 更新car_list
    time.sleep(1)
    data = pickle.dumps(img)
    s.sendall(data)
    s.close()


def get_person_img():
    # get_person_img
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # receiver_ip = '192.168.1.197'
    # receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    # 要傳送的數據
    data = 'get_person_img'
    # 傳送數據
    s.sendall(data.encode())
    data = b""
    while True:
        packet = s.recv(4096)
        if not packet:
            break
        data += packet
    person_img = pickle.loads(data)
    s.close()
    return person_img


def get_car_status():
    # get_person_img
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # receiver_ip = '192.168.1.197'
    # receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    # 要傳送的數據
    data = 'get_car_status'
    # 傳送數據
    s.sendall(data.encode())
    data = b""
    while True:
        packet = s.recv(4096)
        if not packet:
            break
        data += packet
    car_status = pickle.loads(data)
    s.close()
    return car_status


def update_car_status(car_status):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # receiver_ip = '192.168.1.197'
    # receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    # 要傳送的數據
    data = 'update_car_status'
    # 傳送數據
    s.sendall(data.encode())
    # 更新car_list
    time.sleep(1)
    data = pickle.dumps(car_status)
    s.sendall(data)
    s.close()


def get_person_status():
    # get_person_img
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # receiver_ip = '192.168.1.197'
    # receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    # 要傳送的數據
    data = 'get_person_status'
    # 傳送數據
    s.sendall(data.encode())
    data = b""
    while True:
        packet = s.recv(4096)
        if not packet:
            break
        data += packet
    person_status = pickle.loads(data)
    s.close()
    return person_status


def update_person_status(person_status):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # receiver_ip = '192.168.1.197'
    # receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    # 要傳送的數據
    data = 'update_person_status'
    # 傳送數據
    s.sendall(data.encode())
    # 更新car_list
    time.sleep(1)
    data = pickle.dumps(person_status)
    s.sendall(data)
    s.close()


def get_id_list():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((receiver_ip, receiver_port))
    # 要傳送的數據
    data = 'get_id_list'
    # 傳送數據
    s.sendall(data.encode())
    data = b""
    while True:
        packet = s.recv(4096)
        if not packet:
            break
        data += packet
    id_list = pickle.loads(data)
    s.close()
    return id_list


def update_id_list(id_list):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # receiver_ip = '192.168.1.197'
    # receiver_port = 12345
    s.connect((receiver_ip, receiver_port))
    # 要傳送的數據
    data = 'update_id_list'
    # 傳送數據
    s.sendall(data.encode())
    # 更新car_list
    time.sleep(1)
    data = pickle.dumps(id_list)
    s.sendall(data)
    s.close()


"""










"""
