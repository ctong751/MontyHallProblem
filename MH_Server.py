# Chris Tong
import sys
import socket
import random
import _thread

# Function that runs when a player starts the game. Takes a connection parameter
# so that it can communicate with the player through the new socket.
def startGame(connection):
    print("New Game Thread spawned")
    # Generates the winning door number which is between 1 and 3.
    winning_door = random.randint(1,3)
    print("WINNING NUMBER IS", winning_door)
    connection.sendall(b'Lets begin!')
    # Gets the player's first choice and converts it to int.
    first_choice = int(connection.recv(4096))
    print("Player first selected door is: ", first_choice)

    if winning_door == 1 and first_choice != 2:
        print("Revealing Door 2 is NOT the winning door and asking the player if they want to switch their door.")
        connection.sendall(b'Let me reveal that Door 2 is NOT the WINNING door! Do you want to stick to this or select another door? Your probablility of winning might increase!')
    elif (winning_door == 1 and first_choice != 3):
        print("Revealing Door 3 is NOT the winning door and asking the player if they want to switch their door.")
        connection.sendall(b'Let me reveal that Door 3 is NOT the WINNING door! Do you want to stick to this or select another door? Your probablility of winning might increase!')
    elif (winning_door == 2 and first_choice != 1):
        print("Revealing Door 1 is NOT the winning door and asking the player if they want to switch their door.")
        connection.sendall(b'Let me reveal that Door 1 is NOT the WINNING door! Do you want to stick to this or select another door? Your probablility of winning might increase!')
    elif (winning_door == 2 and first_choice != 3):
        print("Revealing Door 3 is NOT the winning door and asking the player if they want to switch their door.")
        connection.sendall(b'Let me reveal that Door 3 is NOT the WINNING door! Do you want to stick to this or select another door? Your probablility of winning might increase!')
    elif (winning_door == 3 and first_choice != 1):
        print("Revealing Door 1 is NOT the winning door and asking the player if they want to switch their door.")
        connection.sendall(b'Let me reveal that Door 1 is NOT the WINNING door! Do you want to stick to this or select another door? Your probablility of winning might increase!')
    elif (winning_door == 3 and first_choice != 2):
        print("Revealing Door 2 is NOT the winning door and asking the player if they want to switch their door.")
        connection.sendall(b'Let me reveal that Door 2 is NOT the WINNING door! Do you want to stick to this or select another door? Your probablility of winning might increase!')

    # Gets the player's final choice and converts it to int.
    final_choice = int(connection.recv(4096))
    print("Player new selected Door is: ", final_choice)

    # If they guessed right, the player wins, else, they got it wrong.
    if winning_door == final_choice:
        print("The player WON the cash!")
        connection.sendall(b'The player WON the cash!')
    else:
        print("The player guessed the WRONG door!")
        connection.sendall(b'Sorry, you guessed the WRONG door!')

    # Send a message and close the connection with the player and release the lock so that other players can play.
    connection.sendall(b'Disconnecting from MontyHall server. Game is over!')
    connection.close()
    thread_lock.release()
    return

    

# Error checking for command line arguments. Makes sure they only specify the port and makes sure the port is a number.
if len(sys.argv) != 2:
    print("Incorrect usage: python MH_Server.py [port number]")
    exit()
else:
    port_number = sys.argv[1]
    if (not port_number.isnumeric()):
        print("Incorrect usage: python MH_Server.py [port number]")
        exit()

# Creates the socket, starts the server, and prints that it's ready.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', int(port_number))
sock.bind(server_address)
print("Server is ready to Play!")

# Waits for an incoming connection to the server
sock.listen(1)

# Create a new connection when a client connects and sends them a confirmation message.
connection, client_address = sock.accept()
connection.sendall(b'Welcome to Monty Hall!')
# Create a lock so that only one player can play at a time.
thread_lock = _thread.allocate_lock()
thread_lock.acquire()
# Create a new thread to play the game using the startGame function and passing a connection socket for communication.
game_thread = _thread.start_new_thread(startGame, (connection,)) 
print("Current number of available players is 1")

# Continuously listens for new connections.
while True:
    connection, client_address = sock.accept()
    connection.sendall(b'Welcome to Monty Hall!')
    # Checks to see if a player is already playing.
    if (thread_lock.locked()):
        # If a player is already playing, notifies the other client and closes their connection.
        print("A new player is trying to connect to the Host server on ", client_address[0], ":", client_address[1])
        print("Game is still going! Please wait!")
        connection.sendall(b'Server is busy with a player. Try to connect again later.')
        connection.close()
    else:
        # Starts a new thread for the game and acquires the lock so only one player can play.
        thread_lock.acquire()
        game_thread = _thread.start_new_thread(startGame, (connection,)) 
        print("Current number of available players is 1")

