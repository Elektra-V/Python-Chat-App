import socket
import threading


class MultiClientServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_list = []
        self.client_sockets = []
        # create a threading lock to avoid race conditions when modifying client lists
        self.lock = threading.Lock()

    def start_server(self):
        # create a socket object and set options
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to the specified host and port
        self.server_socket.bind((self.host, self.port))

        # listen for incoming connections with a backlog of 5
        self.server_socket.listen(5)

        print(f"Server listening on {self.host}:{self.port}")

        while True:
            # accept a new client connection
            client_socket, client_address = self.server_socket.accept()

            print(f"New client connected from {client_address[0]}:{client_address[1]}")
            # acquire the lock to add the new client socket to the client_sockets list
            self.lock.acquire()
            self.client_sockets.append(client_socket)
            self.lock.release()

            # create a new thread to handle the client connection
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))

            # acquire the lock to add the new client address to the client_list
            self.lock.acquire()
            self.client_list.append(client_address[0])
            self.lock.release()

            # start the new thread
            client_thread.start()

            # print the current list of client addresses
            print(self.client_list)

    def handle_client(self, client_socket, client_address):
        while True:
            try:
                # receive data from the client
                data = client_socket.recv(1024)

                # if data is received
                if data:
                    # format and print a message indicating the source of the message
                    message = f"Received message from {client_address[0]}:{client_address[1]}: {data.decode('utf-8').strip()}"
                    print(message)

                    # iterate over the list of client sockets and send the message to all clients except the sender
                    for socket in self.client_sockets:
                        if socket != client_socket:
                            socket.send(message.encode('utf-8'))
               
                # if no data is received, assume the client has disconnected 
                else:
                    print(f"Client {client_address[0]}:{client_address[1]} disconnected")

                    # acquire the lock to remove the client address and socket from the client lists
                    self.lock.acquire()
                    self.client_list.remove(client_address[0])
                    self.client_sockets.remove(client_socket)
                    self.lock.release()

                    # close the client socket and return from the function
                    client_socket.close()
                    break

            except:
                print(f"Error occurred while receiving message from {client_address[0]}:{client_address[1]}")

                # acquire the lock to remove the client address from the client_list
                self.lock.acquire()
                self.client_list.remove(client_address[0])
                self.lock.release()

                # close the client socket and return from the function
                client_socket.close()
                break


if __name__ == '__main__':
    server = MultiClientServer('localhost', 5000)
    server.start_server()