import SocketServer
from _ssl import PROTOCOL_SSLv3
import os
from random import randint
import ssl
import threading

from messages import ADMIN_GREET, WHO, HELLO, PLAYER_GREET
from messages import CLOSE, WAY_OFF, CORRECT


PLAYER_PORT = 4000
ADMIN_PORT = 4001
LOCALHOST = "localhost"
BUFFER_SIZE = 1024

connected_clients = []

class AdminTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
# uncomment the init method for ssl

#     def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):        
#         SocketServer.TCPServer.__init__(self, server_address, 
#                                         RequestHandlerClass, False)
# 
#         cur_dir = os.getcwd()
#         key_file = os.path.join(cur_dir + "\\Certificate\\", '100189688.key')
#         cert_file = os.path.join(cur_dir + "\\Certificate\\", '100189688.crt')
#         ca_certs_file = os.path.join(cur_dir + "\\Certificate\\", 'root-ca.crt')
#         
#         self.socket = ssl.wrap_socket(self.socket, 
#                                       keyfile=key_file, 
#                                       certfile=cert_file, 
#                                       server_side=True, 
#                                       cert_reqs=ssl.CERT_REQUIRED,
#                                       ca_certs=ca_certs_file,
#                                       ssl_version=PROTOCOL_SSLv3)
# 
#         if bind_and_activate:
#             self.server_bind()
#             self.server_activate()
    
class AdminHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            if not self.hand_shake():
                return
            data = self.request.recv(BUFFER_SIZE)
            if data == WHO:
                self.who()                   
        except:            
            return
        
    def hand_shake(self):        
        data = self.request.recv(BUFFER_SIZE)
        if data != HELLO:
            return False
        self.request.sendall(ADMIN_GREET)
        return True
        
    def who(self):
        global connected_clients
        message_list = []
        for client in connected_clients:
            message_list.append(client[0].strip("'") + ' ' + str(client[1]))
        message = '\r\n'.join(message_list)
        self.request.sendall(message)
                    

class PlayerTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
    
class PlayerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global connected_clients
        connected_clients.append(self.request.getpeername())
        self.magic_number = randint(0, 20)
        self.guess_error = 3
        try:
            if not self.hand_shake():
                return            
            self.play()
        except Exception as e:
            print e
            return     
        finally:
            connected_clients.remove(self.request.getpeername())
              
        
    def hand_shake(self):
        data = self.request.recv(BUFFER_SIZE)
        if data != HELLO:
            return False
        self.request.sendall(PLAYER_GREET)
        return True
    
    def check_guess(self, guess):
        current_guess_error = abs(self.magic_number - guess)
        if current_guess_error > self.guess_error:
            return WAY_OFF
        if current_guess_error == 0:
            return CORRECT
        if current_guess_error <= self.guess_error:
            return CLOSE
                        
    def play(self):
        game_over = False
        guess_count = 0
        while not game_over and guess_count < 5:
            data = self.request.recv(BUFFER_SIZE)
            try:
                check = self.check_guess(int(data))
                if check == CORRECT:
                    game_over = True
                self.request.sendall(check)
                guess_count += 1
            except ValueError:
                self.request.sendall(WAY_OFF)
                 
                
if __name__ == "__main__":
    admin_server = AdminTCPServer((LOCALHOST, ADMIN_PORT), AdminHandler)
    admin_thread = threading.Thread(target=admin_server.serve_forever)
    admin_thread.daemon = True
    
    play_server = PlayerTCPServer((LOCALHOST, PLAYER_PORT), PlayerHandler)
    play_thread = threading.Thread(target=play_server.serve_forever)
    play_thread.daemon = True
    
    admin_thread.start()
    play_thread.start()
    
    # wait for some quit input
    raw_input("Press Enter to quit...")
    
    admin_server.shutdown()
    play_server.shutdown()
    
    
    
        
