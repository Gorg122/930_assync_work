from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.ttk import Progressbar

###########################  Функции  ################################

def clicked_find():  ## Функция запускающая скрипт поиска плат и выводящая результаты в лог
    print("soneon")

def del_log():
    log_find_fpga.delete(1.0, END)
###############################################################

window = Tk()
window.title('Настройка лаборатореого стенда.')
window.geometry('600x800')

#########################          Фреймы           ###############################

f_top_log = Frame(window)
f_top_log.pack(side=TOP)
f_rigth_top_log = LabelFrame(f_top_log, text="Ybpe")
f_left_top_log = LabelFrame(f_top_log, text="Верх")
f_rigth_top_log.pack(side=RIGHT)
f_left_top_log.pack(side=LEFT)
# f_rigth_top_log = LabelFrame(text="право")
# f_left_top_log = LabelFrame(text="лево")




####################### Настройка кнопок и их рассположения #############
lbl = Label(f_left_top_log, text="Поиск всевозможных подключенных плат", font=("Arial Bold", 14))
# lbl.grid(column=0, row=0)
lbl.pack(side=TOP)

settings_button = Button(f_left_top_log, text="Начать поиск")
settings_button.pack(side=BOTTOM)
# settings_button.grid(column=0, row=1)


start_work_button = Button(window, text="Начать работу лабраторного стенда")
# start_work_button.grid(column=0, row=10)


clearlog_button = Button(f_left_top_log, text="Очистить лог", command=del_log)
clearlog_button.pack(side=BOTTOM)
# clearlog_button.grid(column=1, row=5)
#########################################################################
###########################Добавление эллементов для вывода консоли##################################

log_find_fpga = scrolledtext.ScrolledText(f_left_top_log, width=40, height=10, state="disabled")
log_find_fpga.pack(side=TOP)
# log_find_fpga.grid(column=1, row=0)

######################################################################
######################### Окна ошибок  ############################

# messagebox.showwarning('Заголовок', 'Текст')  # показывает предупреждающее сообщение
# messagebox.showerror('Заголовок', 'Текст')  # показывает сообщение об ошибке

##################################################################

window.mainloop()
