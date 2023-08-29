import socket
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 12345

car_list = ["AKS-5555"]  # OK
waiting_person = 0  # OK
car_status = 0 #ok
person_status = 0
cleaning_session = []  # OK
id_list=[]
person_img=[]  #OK
s.bind((host, port))

while True:
    s.listen(1)
    print('等待連接...')

    conn, addr = s.accept()
    print('已連接:', addr)
    received_data = conn.recv(1024)
    print('接收到的數據:', received_data.decode())

    if (received_data.decode() == "car_information"):
        data = pickle.dumps(car_list)
        conn.sendall(data)
        conn.close()
    elif (received_data.decode() == "update_car_information"):
        s.listen(1)
        data = b""
        while True:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet
        car_list = pickle.loads(data)
        print(car_list)
        conn.close()
    elif (received_data.decode() == "increase_waiting_person"):
        waiting_person += 1
        print("person+1!!!!")
    elif (received_data.decode() == "decrease_waiting_person"):
        waiting_person -= 1
        print("person-1!!!!")
    elif (received_data.decode() == "update_cleaning_session"):
        s.listen(1)
        data = b""
        while True:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet
        cleaning_session = pickle.loads(data)
        print(cleaning_session)
        conn.close()
    elif (received_data.decode() == "get_cleaning_session"):
        data = pickle.dumps(cleaning_session)
        conn.sendall(data)
        conn.close()
    elif (received_data.decode() == "update_person_img"):
        s.listen(1)
        data = b""
        while True:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet
        person_img= pickle.loads(data)
        print(person_img)
        conn.close()
    elif (received_data.decode() == "get_person_img"):
        data = pickle.dumps(person_img)
        conn.sendall(data)
        conn.close()
    elif (received_data.decode() == "get_car_status"):
        data = pickle.dumps(car_status)
        conn.sendall(data)
        conn.close()
    elif (received_data.decode() == "update_car_status"):
        s.listen(1)
        data = b""
        while True:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet
        car_status= pickle.loads(data)
        print(car_status)
        conn.close()
    elif (received_data.decode() == "get_person_status"):
        data = pickle.dumps(person_status)
        conn.sendall(data)
        conn.close()
    elif (received_data.decode() == "update_person_status"):
        s.listen(1)
        data = b""
        while True:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet
        person_status= pickle.loads(data)
        print(person_status)
        conn.close()
    elif (received_data.decode() == "get_id_list"):
        data = pickle.dumps(id_list)
        conn.sendall(data)
        conn.close()
    elif (received_data.decode() == "update_id_list"):
        s.listen(1)
        data = b""
        while True:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet
        id_list= pickle.loads(data)
        print(id_list)
        conn.close()



