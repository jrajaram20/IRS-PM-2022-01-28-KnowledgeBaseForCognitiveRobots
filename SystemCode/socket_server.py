from ast import While
from operator import truth
import socket
from time import time

#host = socket.gethostname()
#host='192.168.1.3'
#print(host)
#port = 5000
#s = socket.socket()		# TCP socket object
#s.bind((host,port))
#s.listen(5)

#print("Waiting for client...")
#conn,addr = s.accept()	        # Accept connection when client connects
##print("Connected by ", addr)
#print(conn)

class robot:
    def __init__(self, h, p):
        self.s = socket.socket()		# TCP socket object
        self.s.bind((h,p))
        self.s.listen(5)
        print("Waiting for client...")
        self.conn,self.addr = self.s.accept()	        # Accept connection when client connects
        print("Connected by ", self.addr)

    def rcvdata(self):
        while self.conn:
            try:
                data = self.conn.recv(1024).decode("utf-8")
                #print(data)
                #d = data.decode("utf-8")
                #print(d)
                return data
            except:
                pass
                print("unable to receive data")        # exit from loop if no data
        

    def senddata(self,msg):
        while self.conn:
            try:
                self.conn.sendall(msg.encode())	 
                return "done"
            except:
                pass        # exit from loop if no data
                print("unable to send data")   # Send the received data back to client

    def closeconn(self):
        self.conn.close()

if __name__ == "__main__":
    host = '192.168.1.3'
    port = 5000
    r = Robot(host, port)
    while r.s:
        d = r.rcvdata()
        print(d)
        if(d=="start"):
            r.senddata("ack")
            break
        else:
            continue

