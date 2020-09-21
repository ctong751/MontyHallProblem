#Chris Tong
import sys
import socket
import random
import _thread

# Error checking for command line arguments. Makes sure only 2 arguments are added and that the port number is a number.
if len(sys.argv) != 3:
    print("Incorrect usage: python MH_Client.py [server ip address] [port number]")
    exit()
else:
    server_ip = sys.argv[1]
    port_number = sys.argv[2]
    if (not port_number.isnumeric()):
        print("Incorrect usage: python MH_Server.py [port number]")
        exit()

# Creates a new socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Uses the server ip and port number from the command line arguments to connect to the server.
server_address = (server_ip, int(port_number))
sock.connect(server_address)
# Receive connection message.
receive = sock.recv(4096)
print(receive.decode('utf-8'))
# Recieve either READY TO PLAY or BUSY message.
receive = sock.recv(4096)
print(receive.decode('utf-8'))

# Notifies the client and exits if the server is already busy.
if receive == b'Server is busy with a player. Try to connect again later.':
    exit()

# If the client is not busy, the game begins.
# Asks for input until the player gives a valid door number and then sends it to the server.
while True:
    choice = input("Select Door 1, 2 or 3: ")
    if (choice.isnumeric()) and int(choice) > 0 and int(choice) < 4:
        sock.sendall(choice.encode('utf-8'))
        break

# Reveal the door that is not the winning door.
receive = sock.recv(4096)
print(receive.decode('utf-8'))

# Asks for input until the player gives a valid door number and then sends it to the server.
while True:
    choice = input("Select Door 1, 2 or 3: ")
    if (choice.isnumeric()) and int(choice) > 0 and int(choice) < 4:
        sock.sendall(choice.encode('utf-8'))
        break

# Recieve decision of whether the player wins or not
receive = sock.recv(4096)
print(receive.decode('utf-8'))

# Recieve message to disconnect from the server
receive = sock.recv(4096)
print(receive.decode('utf-8'))
