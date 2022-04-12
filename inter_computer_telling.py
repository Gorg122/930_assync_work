import json
import os
import shutil
import time

status_1 = "Not working"
status_2_1 = "Waiting"
status_2 = "In progress"
status_3 = "Sending data"
status_4 = "Offline"
status_66 = "Error: Need service"
user = "email_here"
start_time = "none"

# def json_work():
#     with open("status.json", "r") as read_file:
#         data = json.load(read_file)

def change_status(data, pc_id, status, user_id):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    data[pc_id]["status"] = status
    data[pc_id]["user"] = user_id
    data[pc_id]["start_time"] = current_time
    with open('status.json', 'w') as f:
        json.dump(data, ensure_ascii=False, indent=4)

def start_main_siquence(data, pc_id, f_path, main_path):   #  Эта функция запускает весь сценарий. Тут будет функция загрузки прошивки в общую папку
    if os.path.exists(f_path):
        print("good")
        if os.path.exists(main_path):
            print("very good")
            shutil.copy(f_path, main_path)
            change_status(data, pc_id, status_2_1, data[pc_id]["user"])
            while True:
                with open(main_path+"status_id.json", "r") as read_file:
                    data = json.load(read_file)




def download_main_chain(f_path): # Функция проверяет ствтус компьютеров f_path - путь к файлу который скачали, main_path - путь по которому будем копировать файл
    with open("status.json", "r") as read_file:
        data = json.load(read_file)
        print(data["pc_id_1"])
    while True:
        for pc in data:
            for common_data in data[pc]:
                if common_data["status"] == status_1:
                    main_path = common_data["main_folder_path"]
                    print("Start_process")
                    start_main_siquence(data, pc, f_path, main_path)








        # if pc['status'] == status_1:
        #     print("some")



if __name__ == '__main__':
    download_main_chain()