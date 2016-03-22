import socket
import time
from messages import HELLO, PLAYER_GREET, GUESS, CORRECT, WELCOME

HOST = "localhost"
PORT = 4000
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def play():  
    game_over = False
    guess_count = 0
    start_time = time.time()
    global sock    
    while ((not game_over) and (guess_count < 5) ):
        guess_count += 1
        data = raw_input(GUESS + ' ')
        sock.sendall(data)
        data = sock.recv(BUFFER_SIZE)
        print data
        if data == CORRECT:
            game_over = True
    print "Congratulations! It took you: "  + str(guess_count) + "guesses in" + str(time.time() - start_time) + "seconds."
    if guess_count == 5:
        print "Sorry, you used all of your guesses. it took you" + str(time.time() -start_time)
    raw_input("Press Enter to quit...")
        
        
    
    
sock.sendall(HELLO)
data = sock.recv(BUFFER_SIZE)
if data == PLAYER_GREET:
    print WELCOME
    play()
    

