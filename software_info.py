import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import winreg
import webbrowser

root = tk.Tk()
root.title("Список программ ver. 0.0.1_alfa") #Шапка окна
root.geometry("1280x600")  # Изменяем размер окна

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

software_info = tk.Text(frame, wrap=tk.WORD)
software_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar.config(command=software_info.yview)
software_info.config(yscrollcommand=scrollbar.set)

# функция для получения списка установленных программ для программного и машинного контекстов
def get_installed_software(root_key, software_dir):
    software_list = []
    with winreg.OpenKey(root_key, software_dir) as key:
        try:
            index = 0
            while True:
                sub_key_name = winreg.EnumKey(key, index)
                with winreg.OpenKey(key, sub_key_name) as sub_key:
                    try:
                        software_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                        software_list.append(software_name)
                    except OSError:
                        pass
                index += 1
        except OSError:
            pass
    return software_list

def display_installed_software(software_list):
    for i, (software_name) in enumerate(software_list, start=1):
        software_info.insert(tk.END, f"{i}. {software_name}\n")

def display_all_info():
    software_info.delete('1.0', tk.END)  # Очищаем текстовое поле

    root_key_machine = winreg.HKEY_LOCAL_MACHINE
    software_dir_machine = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
    installed_software_machine = get_installed_software(root_key_machine, software_dir_machine)
    sorted_list_machine = sorted(installed_software_machine, key=lambda x: x[0])
    software_info.insert(tk.END, "Установленные программы (Машина):\n")
    display_installed_software(sorted_list_machine)

def display_user_info():
    software_info.delete('1.0', tk.END)

    root_key_user = winreg.HKEY_CURRENT_USER
    software_dir_user = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
    installed_software_user = get_installed_software(root_key_user, software_dir_user)
    sorted_list_user = sorted(installed_software_user, key=lambda x: x[0])
    software_info.insert(tk.END, "Установленные программы (Пользователь):\n")
    display_installed_software(sorted_list_user)
    
def open_link1():
    url = "https://github.com/MIOZ-git/software_info"
    webbrowser.open(url)
    
def exit_program():
    root.destroy()

# Размещаем кнопку с отступом
button_show_all = ttk.Button(root, text="Установленные программы (Машина)", command=display_all_info)
button_show_all.pack(anchor="n", fill=X)  

button_show_user = ttk.Button(root, text="Установленные программы (Пользователь)", command=display_user_info)
button_show_user.pack(anchor="n",fill=X)

button_open_link1 = ttk.Button(root, text="Актуальная версия на GIThub", command=open_link1)
button_open_link1.pack(anchor="n", fill=X)

# Кнопка для выхода из программы
button4 = Button(root, text="Выход", command=exit_program)
button4.pack(anchor="s",pady=10)

root.mainloop()
