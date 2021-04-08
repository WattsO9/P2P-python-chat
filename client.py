import socket
import threading
import pickle
import sys
from tkinter import *


class Client:
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 5002
        self.host_name = input("Ingrese su nombre: ")
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.connect((self.HOST, self.PORT))

        self.window = Tk()
        self.window.title('Ventana de ' + self.host_name)
        self.window.minsize(width=500, height=300)

        self.received_label = Label(text="Message received:", font=('Arial', 14, 'bold'))
        self.received_label.grid(column=1, row=0)
        self.received_input = Entry(width=30)
        self.received_input.grid(column=2, row=0)

        self.sent_label = Label(text="Message to be sent:", font=('Arial', 14, 'bold'))
        self.sent_label.grid(column=1, row=2)
        self.sent_input = Entry(width=30)
        self.sent_input.grid(column=2, row=2)

        self.button = Button(text='Send message', command=self.button_clicked)
        self.button.grid(column=3, row=2)

        self.image_button = Button(text='Send image')
        self.image_button.grid(column=3, row=4)

        show_message = threading.Thread(target=self.show_message)
        show_message.daemon = True
        show_message.start()

        self.window.mainloop()

    def button_clicked(self):
        msg = self.sent_input.get()
        if msg != 'end':
            self.send_message(msg)
        else:
            self.my_socket.close()
            sys.exit()

    def show_message(self):
        while True:
            try:
                data = self.my_socket.recv(1024)
                if data:
                    print(pickle.loads(data))
                    self.received_input.delete(0, END)
                    self.received_input.insert(0, pickle.loads(data))
                    self.sent_input.delete(0, END)
            except:
                pass

    def send_message(self, msg):
        print(msg)
        self.my_socket.send(pickle.dumps(msg))
        with open('./back_up.txt', 'a') as back_up_file:
            back_up_file.writelines(self.host_name + ': ' + msg)


client = Client()

