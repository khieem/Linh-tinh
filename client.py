import socket 
import threading 

PORT = 4720
IP = '192.168.1.61'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT)) 


def receive(): 
   while True: 
      try: 
         message = client.recv(1024).decode('utf8') 
         
         # if the messages from the server is NAME send the client's name 
         if message == 'NAME': 
            client.send(b'hello there')
         else: 
            # insert messages to text box 
            print(message) 
      except: 
         # an error will be printed on the command line or console if there's an error 
         print("An error occured!") 
         client.close() 
         break
   
# function to send essages 
def sendMessage(): 
   while True: 
      message = input('nhap tin nhan: ') 
      client.send(message.encode('utf8'))	 

recv_thread = threading.Thread(target=receive) 
recv_thread.start()

send_thread = threading.Thread(target=sendMessage) 
send_thread.start() 

