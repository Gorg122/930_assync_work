import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import Tk, Frame, Menu
from tkinter import messagebox
from tkinter.ttk import Progressbar



############################  Стандартные размеры ################################
common_button_height = 2
###########################  Функции  ################################
class TextWrapper:
    text_field: tk.Text

    def __init__(self, text_field: tk.Text):
        self.text_field = text_field

    def write(self, text: str):
        self.text_field.insert(tk.END, text)

    def flush(self):
        self.text_field.update()


def clicked_find():  ## Функция запускающая скрипт поиска плат и выводящая результаты в лог
    print("soneon")

def del_log():
    log_find_fpga.delete(1.0, END)

def change_frame():
    f_top_log.pack()
    f_bottom_log.pack_forget()

def change_frame_back():
    f_top_log.pack_forget()
    f_bottom_log.pack()

def start_work():
    print("some", file=TextWrapper(log_work_fpga))

def pause_work():
    print("pause", file=TextWrapper(log_work_fpga))
###############################################################

window = Tk()
window.title('Настройка лаборатореого стенда.')
window.geometry('400x800')
# window.resizable(width=False, height=False)

#########################          Фреймы           ###############################

f_top_log = Frame(window)
f_top_log.pack()
f_left_top_log = LabelFrame(f_top_log, text="лево")
f_rigth_top_log = LabelFrame(f_top_log, text="право")
text_result = LabelFrame(f_top_log, text="Низ")

f_left_top_log.pack()
f_rigth_top_log.pack()
text_result.pack()



f_bottom_log = Frame(window)
f_bottom_log.pack_forget()
f_top_annonse = LabelFrame(f_bottom_log, text="Самый верх")
f_top_bottom_log = LabelFrame(f_bottom_log, text="Вверх")
f_bottom_bottom_log = LabelFrame(f_bottom_log, text="НИЗ")

f_top_annonse.pack()
f_top_bottom_log.pack()
f_bottom_bottom_log.pack()

############################## Меню и подменю ################################

mainmenu = Menu(window)
window.config(menu=mainmenu)
mainmenu.add_command(label='Поиск плат', command=change_frame) ####, command=change_frame
mainmenu.add_command(label='Работа лабораторного стенда', command=change_frame_back) ### , command=change_frame_back


####################### Настройка кнопок и их рассположения #############
lbl = Label(f_left_top_log, text="Поиск всевозможных \n подключенных плат", font=("Arial Bold", 14), width=100)
lbl.pack(side=TOP,  fill=X)

settings_button = Button(f_left_top_log, text="Начать поиск", width=30, height=common_button_height)
settings_button.pack(side=BOTTOM)

clearlog_button = Button(f_rigth_top_log, text="Очистить лог", command=del_log, width=30, height=common_button_height)
clearlog_button.pack(side=BOTTOM)

c = Canvas(text_result, height=30, bg='white')
c.pack(fill=Y)

# Кнопки второго окна &&&&&&&&&&&&&&&&&&

start_work_button = Button(f_top_bottom_log, text="Запуск", width=30, command=start_work, height=common_button_height)
start_work_button.pack(side=LEFT)
stop_work_button = Button(f_top_bottom_log, text="Стоп", width=30, command=pause_work, height=common_button_height)
stop_work_button.pack(side=RIGHT)


c = Canvas(f_top_annonse, height=30, bg='white')
c.pack(fill=Y)



# clearlog_button.grid(column=1, row=5)
#########################################################################
###########################   Добавление эллементов для вывода консоли   ##################################

log_find_fpga = scrolledtext.ScrolledText(f_rigth_top_log, height=25)
log_find_fpga.pack(side=TOP, fill=X)

log_work_fpga = scrolledtext.ScrolledText(f_bottom_bottom_log, height=25)
log_work_fpga.pack(side=TOP, fill=X)
######################################################################
######################### Окна ошибок  ############################

# messagebox.showwarning('Заголовок', 'Текст')  # показывает предупреждающее сообщение
# messagebox.showerror('Заголовок', 'Текст')  # показывает сообщение об ошибке

##################################################################

window.mainloop()
