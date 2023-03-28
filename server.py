# Xin Ran Wang
# 400264245

import argparse
import csv
import socket
import sys
import json
from cryptography.fernet import Fernet

class Server:

    HOSTNAME = "0.0.0.0"
    
    PORT = 50000
    
    RECV_BUFFER_SIZE = 1024 
    MAX_CONNECTION_BACKLOG = 10

    MSG_ENCODING = "utf-8"

    SOCKET_ADDRESS = (HOSTNAME, PORT)

    # Commands mapped to CSV file column names
    COMMANDS = {"GMA": ["Midterm"], "GL1A": ["Lab 1"], "GL2A": ["Lab 2"], "GL3A": ["Lab 3"], "GL4A": ["Lab 4"], "GEA": ["Exam 1", "Exam 2", "Exam 3", "Exam 4"]}

    def __init__(self):
        self.read_file()
        self.create_listen_socket()
        self.process_connections_forever()

    def create_listen_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.socket.bind(Server.SOCKET_ADDRESS)

            self.socket.listen(Server.MAX_CONNECTION_BACKLOG)
            
            print("Listening for connections on port {} ...".format(Server.PORT))

        except Exception as msg:
            print(msg)
            sys.exit(1)

    def process_connections_forever(self):
        try:
            while True:
                self.connection_handler(self.socket.accept())
                
        except Exception as msg:
            print(msg)
            
        except KeyboardInterrupt:
            print()
            
        finally:
            self.socket.close()
            sys.exit(1)

    def read_file(self):
        file = open('course_grades_2023.csv', 'r')
        readCSV = csv.DictReader(file)
        self.grades = dict()
        self.encryption_keys = dict()
        self.student_count = 0

        print("Data read from CSV file: ")

        # Read each row in CSV file
        for row in readCSV:
            self.encryption_keys[row['ID Number']] = row.pop('Key')
            self.grades[row['ID Number']] = row
            
            print(self.grades[row['ID Number']])
            self.student_count += 1
        
        file.close()

    def connection_handler(self, client):
        connection, address_port = client
        print("-" * 72)
        print("Connection received from {}.".format(address_port))
        
        print(client)

        while True:
            try:
                recvd_bytes = connection.recv(Server.RECV_BUFFER_SIZE)
            
                if len(recvd_bytes) == 0:
                    print("Closing client connection ... ")
                    connection.close()
                    break
                
                recvd_str = recvd_bytes.decode(Server.MSG_ENCODING)

                data_entry, encryption_key = self.process_command(recvd_str)

                # Encrypt message for transmission at server
                fernet = Fernet(encryption_key.encode('utf-8'))
                Encrypted_data_entry= fernet.encrypt(data_entry.encode(Server.MSG_ENCODING))

                # Send response back to client
                connection.sendall(Encrypted_data_entry)
                print("Sent: ", data_entry)

            except KeyboardInterrupt:
                print()
                print("Closing client connection ... ")
                connection.close()
                break

            except UserNotFoundError as err:
                print(err)
                print("Closing client connection ...")
                connection.close()
                break

    # Process command and return data
    def process_command(self, cmd):
        command = cmd.split()    # [student ID, command]

        print("Received ", command[1], " command from client")

        # Check if ID matches database entry
        if not (command[0] in self.grades):
            raise UserNotFoundError("User not found")
        
        print("User found")

        # Return all grades for ID number
        if command[1] == "GG":
            return json.dumps(self.grades[command[0]]), self.encryption_keys[command[0]]
        
        # Return grade averages
        return str(self.get_grade_average(command[1])), self.encryption_keys[command[0]]

    # Calculate the grade average
    def get_grade_average(self, cmd_op):
        n = 0
        col = Server.COMMANDS[cmd_op]

        for id in self.grades:
            for c in col:
                n += int(self.grades[id][c])

        return n/(self.student_count * len(col))
    
class UserNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
