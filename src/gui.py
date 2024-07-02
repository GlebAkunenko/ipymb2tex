import tkinter as tk
import tkinter.filedialog
import customtkinter as ctk
import engine

def check_ready():
    start_button.configure(state=(
        'normal' if filepath.get() != "" and dirpath.get() != ""
        else 'disabled'
    ))

def open_file():
    path = tk.filedialog.askopenfilename()
    if path != "":
        filepath.set(path)
        check_ready()

def open_output_dir():
    path = tk.filedialog.askdirectory()
    if path != "":
        dirpath.set(path)
        check_ready()

def run():
    try:
        engine.run(filepath.get(), dirpath.get())
    except:
        message.configure(text='Что-то пошло не так', text_color='red')
        return
    message.configure(text='Успех', text_color='green')


app = ctk.CTk()
app.geometry("700x300")
app.title("Конвертер .ipynb в .tex")

filepath = ctk.StringVar(value='')
dirpath = ctk.StringVar(value='')

file_button = ctk.CTkButton(app, text="Исходный файл", command=open_file)
file_button.grid(column=0, row=0, padx=20, pady=20)
dir_button = ctk.CTkButton(app, text="Папка для сохранения", command=open_output_dir)
dir_button.grid(column=0, row=1, padx=20, pady=20)
filepath_entry = ctk.CTkEntry(app, state='disabled', textvariable=filepath, width=400)
filepath_entry.grid(column=1, row=0, padx=10, pady=20)

dirpath_entry = ctk.CTkEntry(app, state='disabled', textvariable=dirpath, width=400)
dirpath_entry.grid(column=1, row=1, padx=10, pady=20)

start_button = ctk.CTkButton(app, text="Конвертировать", command=run, state='disabled')
start_button.grid(column=0, row=2, sticky='we', columnspan=2, padx=20, pady=20)

message = ctk.CTkLabel(app, text='', font=('Arial', 26))
message.grid(column=0, row=3, sticky='we', columnspan=2, padx=20, pady=20)

version = ctk.CTkLabel(app, text='v1.0.0')
version.grid(column=1, row=4, sticky='e')

link = ctk.CTkLabel(app, text='https://github.com/GlebAkunenko/ipymb2tex')
link.grid(column=0, row=4, sticky='w')

app.mainloop()