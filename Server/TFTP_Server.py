
# Protocol Implementated:- TFTP
# Group Number:-           C13

# -------------------------------------
# Group Members      |     Roll No.    |
# -------------------------------------|
# Shubham Kendre     |     129         |
# Vaibhav Patil      |     131         |
# Yash Jaware        |     139         |
# -------------------------------------

import socket
import time
from os import  system,path,mkdir
import TFTP_Introduction

SERVERNAME="V"
TERMINATING_DATA_LENGTH = 516
BYTE_RANGE=65535
TFTP_TRANSFER_MODE = b'netascii'
TFTP_OPCODES = {
    'unknown': 0,
    'read': 1,  # RRQ
    'write': 2,  # WRQ
    'data': 3,  # DATA
    'ack': 4,  # ACKNOWLEDGMENT
    'error': 5}  # ERROR

TFTP_MODES = {
    'unknown': 0,
    'netascii': 1,
    'octet': 2,
    'mail': 3
    }

server_error_msg = {
    0: "Not defined, see error message (if any).",
    1: "File not found.",
    2: "Access violation.",
    3: "Disk full or allocation exceeded.",
    4: "Illegal TFTP operation.",
    5: "Unknown transfer ID.",
    6: "File already exists.",
    7: "No such user.",
    8: "Find server."
}

PORT=69
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=("",PORT)
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(ADDR)

def start_listening():
    data,addr=sock.recvfrom(1024)
    opcode=f'{(int.from_bytes(data[0:1], "little") )}{(int.from_bytes(data[1:2], "little"))}'
    if(opcode=='08'):
        print("Request recieved for find")
        print("Client: ",addr)
        return ['08','','',addr]
    data=data[2:].decode("utf-8").split("\x00")
    fileName=data[0]
    mode=data[1]

    print("********************Request header*************************\n")
    print( "  2 bytes   string     1 byte  string    1 byte\n -----------------------------------------------")
    print(f"| {opcode} |  {fileName}  |   0  |    {mode}    |   0  |\n -----------------------------------------------")
    return [opcode,fileName,mode,addr]

def send_error(errorCode,addr):
    opcode=bytearray()
    opcode.append(0)
    opcode.append(5)
    error_code=bytearray()
    error_code.append(0)
    error_code.append(errorCode)
    error_msg=bytearray(server_error_msg[errorCode].encode("utf-8"))
    error_msg.append(0)
    sock.sendto(opcode+error_code+error_msg,addr)

def send_ack(ack_data, server):
    ack = bytearray(ack_data)
    ack[0] = 0
    ack[1] = TFTP_OPCODES['ack']
    sock.sendto(ack, server)

def server_error(data):
    opcode = data[:2]
    return int.from_bytes(opcode, byteorder='big') == TFTP_OPCODES['error']

def send_data(filename,opcode,addr):
    parent_dir=path.dirname(path.realpath(__file__))
    try:
        file=open(f"{parent_dir}/tftpboot/{filename}","rb")
    except FileNotFoundError:
        send_error(1,addr)
        return
    counter=0
    data=file.read(512)
    dataHeader=bytearray()
    dataHeader.append(int(opcode[0]))
    dataHeader.append(int(opcode[1]))
    while data:
        sock.sendto(dataHeader+counter.to_bytes(2, 'little')+data,addr)
        ack,add=sock.recvfrom(4)
        if server_error(ack):
            error_code = int.from_bytes(data[2:4], byteorder='big')
            print(server_error_msg[error_code])
            break
        data=file.read(512)
        counter+=1
        counter%=BYTE_RANGE
def recieve_data(fileName):
    parent_dir=path.dirname(path.realpath(__file__))
    file = open(f"{parent_dir}/tftpboot/{fileName}", "wb")
    while True:
        # Wait for the data from the server
        data, client = sock.recvfrom(600)
        if server_error(data):
            error_code = int.from_bytes(data[2:4], byteorder='big')
            print(server_error_msg[error_code])
            break

        send_ack(data[0:4], client)
        content = data[4:]
        file.write(content)

        opcode=int.from_bytes(data[:2], byteorder='big')
        block=int.from_bytes(data[2:4], byteorder='big')
        print("*********************DATA**************************")
        print(" 2 bytes    2 bytes       n bytes\n---------------------------------")
        print(f"| {opcode}  |  {block}  |    Data    |\n---------------------------------")

        if len(data) < TERMINATING_DATA_LENGTH:
            break
    file.close()
def send_server_info(addr):
    opcode=bytearray()
    opcode.append(0)
    opcode.append(6)
    sock.sendto(opcode+SERVERNAME.encode('utf-8'),addr)

def loading():
    for i in range(5):
        print("[STARTING] server is starting \\")
        time.sleep(0.2)
        system('cls')
        print("[STARTING] server is starting |")
        time.sleep(0.2)
        system('cls')
        print("[STARTING] server is starting /")
        time.sleep(0.2)
        system('cls')
        print("[STARTING] server is starting --")
        time.sleep(0.2)
        system('cls')
        print("[STARTING] server is starting \\")
        time.sleep(0.2)
        system('cls')
        print("[STARTING] server is starting |")
        time.sleep(0.2)
        system('cls')
        print("[STARTING] server is starting /")
        time.sleep(0.2)
        system('cls')
        print("[STARTING] server is starting --")
        time.sleep(0.2)
        system('cls')
    print("[RUNNING] server is running...") 
    
if __name__ == '__main__':
    TFTP_Introduction.start()
    input("Press enter to start TFTP server...")
    system('cls')
    loading()
    parent_dir=path.dirname(path.realpath(__file__))
    if(not path.exists(parent_dir+'/tftpboot')):
        mkdir(parent_dir+'/tftpboot')

    while(True):
        request_header=start_listening()
        if(int(request_header[0])==1):
            send_data(request_header[1],request_header[0],request_header[3])
        elif(int(request_header[0])==2):
            recieve_data(request_header[1])
        elif(int(request_header[0])==8):
            addr=request_header[3]
            send_server_info(addr)