
#!/usr/bin/env python3

#123 pen

import socket
import paramiko
# paramiko is a python library for SSHv2, for client and server
# functionality and can be used to run remote shell commands
# or transferring files
import threading

from secret import secret

class SSHServer(paramiko.ServerInterface):
    def check_auth_password(self,username: str, password: str) -> int:
        print(f"{username}:{password}")
        return paramiko.AUTH_FAILED
    # above line asks user to input a password and the honeypot will
    # detect this string and print it to the terminal

def handle_connection(client_sock):
    transport = paramiko.Transport(client_sock)
    server_key = paramiko.RSAKey.from_private_key_file(secret())
    transport.add_server_key(server_key)
    #ssh = paramiko.ServerInterface()
    ssh = SSHServer()
    transport.start_server(server=ssh)

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF_INET = IPv4, SOCK_STREAM = TCP

    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # When this program is closed and reopened the address will be
    # reused, it will not be in a closed state listening for packets

    server_sock.bind(('', 2222))
    # '' = listens to all interfaces on port 2222 = port

    server_sock.listen(223)
    # 223 is an arbitrary number for how much you want to qeue before
    # accepting

    #input() # tester for input

    while True:

        client_sock, client_addr = server_sock.accept()
    # accept() says go check the qeue and establish an incoming connection
    # return a different socket so the listener can keep on listening
    # and the address of the client can connect



        print(f"Connection from {client_addr[0]}:{client_addr[1]}")

        t = threading.Thread(target=handle_connection, args=(client_sock,))
        # threading allows for the listener to keep on listening
        # and the client to connect

        t.start()

    # client_sock.send(b"Hello from the other side\n")
    # print(client_sock.recv(256).decode())
    # above line sends message once tcp connection is established

#--------------------------------------------------------------
# above lines are all that's needed to test a TCP/IP
# 3 way handshake


        #transport = paramiko.Transport(client_sock)
    # above line asks paramiko to take the newly handshaked
    # socket and use it to run SSH

    # server_key = paramiko.RSAKey.generate(2048)
    # SSH servers have to have a key to be able to connect
    # this line generates the key through paramiko but
    # generating a new key every time can cause errors
    # another way is shown below with below line and
    # ssh-keygen "key" in folder

        #server_key = paramiko.RSAKey.from_private_key_file("key")

        #transport.add_server_key(server_key)

        #ssh = paramiko.ServerInterface()

        #transport.start_server(server=ssh)



if __name__ == "__main__":
    main()
# above line makes the script run as a standalone program



# netstat -tnlp | grep 2222 = check if the port is open
# f5 gives file path
# nc 127.0.0.1 2222 = connects to the ipaddress and port 2222
# ssh localhost -p 2222 = connects to port 2222 via ssh
# ssh-keygen - generates an ssh key
# ssh-keygen -t rsa
# ssh-keygen -f (folder path) - generates an ssh key pair (public and
# private key) and saves it to a folder of your choice
