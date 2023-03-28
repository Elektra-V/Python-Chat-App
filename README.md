# Python-Chat-App
This is a simple chat application that allows users to connect to a server and chat with other users in real-time. The application is built using Python and the Tkinter library for the graphical user interface.

How to Use :

	1	Start the server by running server.py in a terminal.
	2	Start the client by running client.py in a separate terminal or on a separate machine.
	3	Enter the server's IP address and port number when prompted by the client.
	4	Enter a username when prompted by the client.
	5	Start chatting with other users who are connected to the same server.

Features :

	•	Real-time messaging: Messages are displayed in real-time as they are sent and received.
	•	Usernames: Each user is assigned a unique username which is displayed with their messages.
	•	Easy-to-use GUI: The graphical user interface is simple and easy to use.
	•	Cross-platform: The application can be run on any machine that has Python installed.

Dependencies :

This project requires Python 3 and the tkinter library. The code was developed and tested using Python 3.9.2, but should work with other Python 3 versions as well. The tkinter library should be included in most Python 3 installations, but if it is missing, it can be installed using pip: pip install tkinter.

How the Application Works :

The chat application uses a client-server architecture, where multiple clients connect to a single server to send and receive messages. The client is implemented using the Client class, which creates a socket connection to the server and sends and receives messages using that connection. The GUI is implemented using the ChatGUI class, which creates a graphical interface for the user to enter and display messages.

When the user starts the chat application, the ChatGUI class is instantiated, which creates the main window and prompts the user to enter the server's IP address and port number, as well as their username. If the connection to the server is successful, a new thread is started to receive messages from the server. The user can then enter messages in the entry box and send them to the server using the "Send" button or the Enter key. When a message is received from the server, it is displayed in the chat history text box.

License :

This project is licensed under the MIT License. See the LICENSE file for more information.
