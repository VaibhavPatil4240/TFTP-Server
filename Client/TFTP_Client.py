import socket
import os
from reactivex import create
import browse

TERMINATING_DATA_LENGTH = 516
TFTP_TRANSFER_MODE = b'netascii'
BYTE_RANGE=65535
TFTP_OPCODES = {
    'unknown': 0,
    'read': 1,  # RRQ
    'write': 2,  # WRQ
    'data': 3,  # DATA
    'ack': 4,  # ACKNOWLEDGMENT
    'error': 5,
    'server':6}  # ERROR

TFTP_MODES = {
    'unknown': 0,
    'netascii': 1,
    'octet': 2,
    'mail': 3}
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = None
ADDR_BROD= ("255.255.255.255",69)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
def send_rq(filename, mode,opcode):
    request = bytearray()
    # First two bytes opcode - for read request
    request.append(0)
    request.append(opcode)
    
    # append the filename you are interested in
    filename = bytearray(filename.encode('utf-8'))
    request += filename
    # append the null terminator
    request.append(0)
    # append the mode of transfer
    form = bytearray(bytes(mode, 'utf-8'))
    request += form
    # append the last byte
    request.append(0)
    sent = sock.sendto(request, server_address)

def send_ack(ack_data, server):
    ack = bytearray(ack_data)
    ack[0] = 0
    ack[1] = TFTP_OPCODES['ack']
    sock.sendto(ack, server)

def server_error(data):
    opcode = data[:2]
    return int.from_bytes(opcode, byteorder='big') == TFTP_OPCODES['error']

server_error_msg = {
    0: "Not defined, see error message (if any).",
    1: "File not found.",
    2: "Access violation.",
    3: "Disk full or allocation exceeded.",
    4: "Illegal TFTP operation.",
    5: "Unknown transfer ID.",
    6: "File already exists.",
    7: "No such user."
}

def read_request(fileName):
    mode='octet'
    send_rq(fileName, mode,1)
    errorDetected=False
    file = open(fileName, "wb")
    while True:
        # Wait for the data from the server
        data, server = sock.recvfrom(600)
        if server_error(data):
            error_code = int.from_bytes(data[2:4], byteorder='big')
            print("***********************ERROR***********************")
            print("      2 bytes  2 bytes        string    1 byte\n      ------------------------------------------")
            print(f"      | 05    |  {error_code} |   {server_error_msg[error_code]}   |   0  |\n      ------------------------------------------")
            print(server_error_msg[error_code])
            errorDetected=True
            break

        send_ack(data[0:4], server)
        content = data[4:]
        file.write(content)

        opcode=int.from_bytes(data[:2], byteorder='big')
        block=int.from_bytes(data[2:3], byteorder='big')
        block1=int.from_bytes(data[3:4], byteorder='big')
        print("*********************DATA**************************")
        print(" 2 bytes    2 bytes       n bytes\n---------------------------------")
        print(f"| {opcode}  |  {block1}{block}  |    Data    |\n---------------------------------")

        if len(data) < TERMINATING_DATA_LENGTH:
            break
    if(not errorDetected):
        file.close()
    else:
        file.close()
        os.remove(fileName)


def write_request(filePath,opcode,addr):
    file=open(filePath,"rb")
    counter=0
    data=file.read(512)
    dataHeader=bytearray()
    dataHeader.append(0)
    dataHeader.append(2)
    while data:
        sock.sendto(dataHeader+counter.to_bytes(2, 'little')+data,addr)
        ack,add=sock.recvfrom(4)
        if server_error(ack):
            error_code = int.from_bytes(data[2:4], byteorder='big')
            print("***********************ERROR***********************")
            print("      2 bytes  2 bytes        string    1 byte")
            print(f"      | 05    |  {error_code} |   {server_error_msg[error_code]}   |   0  |")
            print(server_error_msg[error_code])
            break
        data=file.read(512)
        counter+=1
        counter%=BYTE_RANGE

def find_server(n=0):
    if(n==5):
        print("No response from any TFTP Server...")
        return
    elif(n>0):
        print("Retry Count ",n)
    request = bytearray()
    request.append(0)
    request.append(8)
    sock.sendto(request,ADDR_BROD)
    sock.settimeout(5)
    try:
        server_config,server=sock.recvfrom(1024)
        if(server_config[1]==6):
            return server_config[2:].decode('utf-8'),server
        else:
            server_error(server_config)
    except TimeoutError:
        find_server(n+1)
    return (None,None)

if __name__ == '__main__':
    while(True):
        print("Trying to find TFTP Server....")
        data=find_server()
        if(not data[0]==None):
            print("TFTP Server found...")
            print("Name: ",data[0])
            ip=input("Want to use  it [Y/N]: ")
            if(ip=='Y' or ip=='y'):
                server_address=data[1]
                break
            elif(ip=='N' or ip=='n'):
                exit(0)
            else:
                print("Invalid Input...")
                exit(0)
        ip=input("Want to retry [Y/N]: ")
        if(ip=='N' or ip=='n'):
            exit(0)
        elif(not(ip=='Y' or ip=='y')):
            print('Invalid input')
            exit(0)

    print("---------------WELCOME TO TRIVIAL FILE TRANSFER CLIENT---------------")
    while(True):
        print("\n1.Download file from TFTP server\n2.Upload file to TFTP server\n3.Exit\n")
        op=int(input("Choose option: "))
        if(op==1):
            filename=input("Enter the name of the file: ")
            read_request(filename)
        elif(op==2):
            path=[]
            op=int(input("\n1.Browse\n2.Enter path\nChoose option: "))
            if(op==1):
                source=create(browse.browse)
                source.subscribe(on_next= lambda s: path.append(s),on_error= lambda e:print("Error: ",e))
                try:
                    path=path[0]
                except IndexError:
                    break
            elif(op==2):
                path=input("Enter the path of the file you want to upload")
            elif(op==3):
                exit(0)
            else:
                print("Invalid Input")
                break
            fileName=path.split("\\")
            if(not os.path.isfile(path)):
                print("Not file")
                break
            if(not fileName or len(fileName)==1):
                fileName=path.split('/')
            print('Uploading: ',fileName[-1])
            send_rq(fileName[-1],"octet",2)
            write_request(path,"02",server_address)
        else:
            print("Invalid Input")
            break