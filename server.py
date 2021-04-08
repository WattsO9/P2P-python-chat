import socket
import threading
import sys


class Server:
    def __init__(self):
        self.clients_list = []
        self.clients_addr = []
        self.HOST = '127.0.0.1'
        self.PORT = 5002
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.bind((self.HOST, self.PORT))
        self.my_socket.listen(2)
        self.my_socket.setblocking(False)

        accept = threading.Thread(target=self.accept_connection)
        process = threading.Thread(target=self.process_connection)

        accept.daemon = True
        accept.start()

        process.daemon = True
        process.start()

        print('Server is running...')
        while True:
            msg = input('->')
            if msg == 'end':
                self.my_socket.close()
                for element in self.clients_addr:
                    print('Connection finished with: '+element)
                sys.exit()
            else:
                pass

    def send_messages(self, msg, client):
        for c in self.clients_list:
            try:
                if c != client:
                    c.send(msg)
            except:
                self.clients_list.remove(c)

    def accept_connection(self):
        while True:
            try:
                conn, addr = self.my_socket.accept()
                conn.setblocking(False)
                self.clients_list.append(conn)
                self.clients_addr.append(str(addr))
            except:
                pass

    def process_connection(self):
        while True:
            if len(self.clients_list) > 0:
                for c in self.clients_list:
                    try:
                        data = c.recv(1024)
                        if data:
                            self.send_messages(data, c)
                    except:
                        pass


server = Server()

