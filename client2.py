import socket
import tkinter as tk
from tkinter import messagebox


def login():
    global client_socket

    login_val = login_entry.get()
    password_val = password_entry.get()

    client_socket.sendall(login_val.encode('utf-8'))
    client_socket.sendall(password_val.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    if response == 'OK':
        messagebox.showinfo("Zalogowano", "Zalogowano pomyślnie!")
        show_main_window()
    else:
        messagebox.showerror("Błąd logowania", "Błędne dane logowania. Spróbuj ponownie.")
        login_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        login_entry.focus()


def send_message():
    message_val = message_entry.get()
    chat_box.insert(tk.END, f"You: {message_val}\n")
    client_socket.sendall(message_val.encode('utf-8'))

    if message_val.lower() == 'exit':
        client_socket.close()
        root.destroy()
    else:
        data = client_socket.recv(1024)
        chat_box.insert(tk.END, f"Serwer: {data.decode('utf-8')}\n")


def show_login_window():
    main_frame.pack_forget()
    login_frame.pack()


def show_main_window():
    login_frame.pack_forget()
    main_frame.pack()


def clear_entries():
    login_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


root = tk.Tk()
root.title("Aplikacja Klient/Serwer")

root.minsize(400, 300)

default_font = ('Segoe UI', 10)
bg_color = '#ffffff'
fg_color = '#000000'
root.configure(bg=bg_color)

login_frame = tk.Frame(root, bg=bg_color)
login_label = tk.Label(login_frame, text="Login:", font=default_font, bg=bg_color, fg=fg_color)
login_label.pack()
login_entry = tk.Entry(login_frame, font=default_font)
login_entry.pack()
password_label = tk.Label(login_frame, text="Password:", font=default_font, bg=bg_color, fg=fg_color)
password_label.pack()
password_entry = tk.Entry(login_frame, show="*", font=default_font)
password_entry.pack()
login_button = tk.Button(login_frame, text="Login", command=login, font=default_font, bg="#9b02fa", fg=fg_color)
login_button.pack()
login_frame.pack()

main_frame = tk.Frame(root, bg=bg_color)
chat_box = tk.Text(main_frame, height=20, width=50, font=default_font)
chat_box.pack()
message_entry = tk.Entry(main_frame, width=40, font=default_font)
message_entry.pack()
send_button = tk.Button(main_frame, text="Send", command=send_message, font=default_font, bg="#9b02fa", fg=fg_color)
send_button.pack(side=tk.BOTTOM)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('10.206.0.76', 55128)
client_socket.connect(server_address)

show_login_window()

root.mainloop()