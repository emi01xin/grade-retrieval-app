# Xin Ran Wang
# 400264245

import socket
import sys
from cryptography.fernet import Fernet

from server import Server

class Client:

    SERVER_HOSTNAME = socket.gethostname()
    RECV_BUFFER_SIZE = 1024

    # Decryption keys
    D_KEYS = {
        "1803933":"M7E8erO15CIh902P8DQsHxKbOADTgEPGHdiY0MplTuY=",
        "1884159":"PWMKkdXW4VJ3pXBpr9UwjefmlIxYwPzk11Aw9TQ2wZQ=",
        "1853847":"UVpoR9emIZDrpQ6pCLYopzE2Qm8bCrVyGEzdOOo2wXw=",
        "1810192":"bHdhydsHzwKdb0RF4wG72yGm2a2L-CNzDl7vaWOu9KA=",
        "1891352":"iHsXoe_5Fle-PHGtgZUCs5ariPZT-LNCUYpixMC3NxI=",
        "1811313":"IR_IQPnIM1TI8h4USnBLuUtC72cQ-u4Fwvlu3q5npA0=",
        "1804841":"kE8FpmTv8d8sRPIswQjCMaqunLUGoRNW6OrYU9JWZ4w=",
        '1881925':"_B__AgO34W7urog-thBu7mRKj3AY46D8L26yedUwf0I=",
        "1877711":"dLOM7DyrEnUsW-Q7OM6LXxZsbCFhjmyhsVT3P7oADqk=",
        '1830894':"aM4bOtearz2GpURUxYKW23t_DlljFLzbfgWS-IRMB3U=",
        '1855191':"-IieSn1zKJ8P3XOjyAlRcD2KbeFl_BnQjHyCE7-356w=",
        '1821012':"Lt5wWqTM1q9gNAgME4T5-5oVptAstg9llB4A_iNAYMY=",
        '1844339':"M6glRgMP5Y8CZIs-MbyFvev5VKW-zbWyUMMt44QCzG4=",
        '1898468':"SS0XtthxP64E-z4oB1IsdrzJwu1PUq6hgFqP_u435AA=",
        '1883633':"0L_o75AEsOay_ggDJtOFWkgRpvFvM0snlDm9gep786I=",
        '1808742':"9BXraBysqT7QZLBjegET0e52WklQ7BBYWXvv8xpbvr8=",
        '1863450':"M0PgiJutAM_L9jvyfrGDWnbfJOXmhYt_skL0S88ngkU=",
        '1830190':"v-5GfMaI2ozfmef5BNO5hI-fEGwtKjuI1XcuTDh-wsg=",
        '1835544':"LI14DbKGBfJExlwLodr6fkV4Pv4eABWkEhzArPbPSR8=",
        '1820930':"zoTviAO0EACFC4rFereJuc0A-99Xf_uOdq3GiqUpoeU="
    }

    # Commands
    COMMANDS = {
        "GMA": "Get Midterm Average",
        "GL1A": "Get Lab 1 Average",
        "GL2A": "Get Lab 2 Average",
        "GL3A": "Get Lab 3 Average",
        "GL4A": "Get Lab 4 Average",
        "GEA": "Get Exams Average",
        "GG": "Getting Grades" 
    }

    def __init__(self):
        while(True):
            try:
                self.get_socket()
                self.connect_to_server()
                self.send_console_input_once()
                
            except Exception as msg:
                print(msg)
                continue
       

    def get_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect_to_server(self):
        self.socket.connect((Client.SERVER_HOSTNAME, Server.PORT))
        print("Connected to \"{}\" on port {}".format(Client.SERVER_HOSTNAME, Server.PORT))

    def get_console_input(self):
        self.input_text = input("Input: ")
        if self.input_text == "":
            raise Exception("Empty command")

        # Return command entered
        print("Command entered: ", self.input_text)
        
        command = self.input_text.split() # [student ID, command]
        self.decryption_key = Client.D_KEYS.get(command[0], Fernet.generate_key())
        
        # Output message for command
        print(Client.COMMANDS[command[1]])

    # Sends console input once and then closes connection
    def send_console_input_once(self):
        try:
            self.get_console_input()
            self.connection_send()
            self.connection_receive()
        except Exception as err:
            print(err)
            print("Closing server connection ...")
            self.socket.close()

    def connection_send(self):
        try:
            self.socket.sendall(self.input_text.encode(Server.MSG_ENCODING))
            
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connection_receive(self):
        try:
            recvd_bytes = self.socket.recv(Client.RECV_BUFFER_SIZE)

            if len(recvd_bytes) == 0:
                print("Closing server connection ... ")
                self.socket.close()
                retu

            # Decrypt message after reception at the client
            encryption_key_bytes = self.decryption_key.encode('utf-8')
            fernet = Fernet(encryption_key_bytes)
            decrypted_message_bytes =fernet.decrypt(recvd_bytes)
            received_message = decrypted_message_bytes.decode('utf-8')
            print("Server response: ", received_message)

        except Exception as msg:
            print(msg)
            sys.exit(1)
