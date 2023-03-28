import socket
import threading
import tkinter as tk
from tkinter import simpledialog


class Client:
    def __init__(self):
        self.host = None
        self.port = None
        self.username = None

    def connect(self):
        # create a new client socket and prompt the user to enter the server's IP address and port number
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host = simpledialog.askstring("Host", "Please enter the server's IP address:")
            self.port = simpledialog.askinteger("Port", "Please enter the server's port number:")

            # connect to the server using the host and port entered by the user
            self.client_socket.connect((self.host, self.port))

            # prompt the user to enter their username
            self.username = simpledialog.askstring("Username", "Please enter your name:")

            # send a message to the server indicating that the user has joined the chat
            self.send_message(self.username + " has joined the chat.")
            return True
        
        except:
            return False

    def start_receiving(self, chat_history):
        while True:
            try:
                # receive data from the server
                data = self.client_socket.recv(1024)

                if data:
                    # decode the data and add it to the chat history
                    message = data.decode('utf-8')
                    chat_history.config(state=tk.NORMAL)
                    chat_history.insert(tk.END, message + "\n")
                    chat_history.config(state=tk.DISABLED)
                
                else:
                    self.client_socket.close()
                    break
            
            except:
                self.client_socket.close()
                break

    def send_message(self, message):
        try:
            # encode the message and send it to the server
            self.client_socket.send((self.username + ": " + message).encode('utf-8'))
        
        except:
            print("Error occurred while sending message to server")

class ChatGUI:
    def __init__(self):
        # create the main window for the chat app
        self.window = tk.Tk()
        self.window.title("Chat App")

        # create a text box for displaying the chat history
        self.chat_history = tk.Text(self.window, state=tk.DISABLED)
        self.chat_history.pack(fill=tk.BOTH, expand=True)

        # create an entry box for entering messages
        self.message_entry = tk.Entry(self.window)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", self.send_message)

        # create a button for sending messages
        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        # set a callback function for when the user closes the window
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.client = Client()

        connected = self.client.connect()
        if connected:
            # if the connection is successful, start a new thread for receiving messages from the server
            self.start_receiving_thread()

    def start_receiving_thread(self):
        # create a new thread for receiving messages from the server
        receive_thread = threading.Thread(target=self.client.start_receiving, args=(self.chat_history,))
        receive_thread.start()

    def send_message(self, event=None):
        # get the message from the entry box
        message = self.message_entry.get()

        # send the message to the server
        self.client.send_message(message)

        # add the message to the chat history
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, self.client.username + ": " + message + "\n")
        self.chat_history.config(state=tk.DISABLED)

        # clear the message entry box
        self.message_entry.delete(0, tk.END)

    def close_window(self):
        # send a message to the server to indicate that the user has left the chat
        self.client.send_message(self.client.username + " has left the chat.")

        # close the socket and destroy the window
        self.client.client_socket.close()
        self.window.destroy()

    def start(self):
        self.window.mainloop()


if __name__ == '__main__':
    gui = ChatGUI()
    gui.start()