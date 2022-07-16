import socket
import time
import psutil
import json

HOST = '127.0.0.1'
PORT = 8080

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f'Connected to Server {HOST}:{PORT}')
            counter = 0
            while True:
                metrics = {
                    'CPU': psutil.cpu_percent(interval=1),
                    'RAM': psutil.virtual_memory()[2],
                    'DISK': psutil.disk_usage('/')[3]
                    }
            
                message = json.dumps(metrics)      
                s.send(message.encode('UTF-8'))

                print(f'Message{counter} sent to server')
                counter += 1
                time.sleep(2)


        except Exception as e:
            print('connection lost!')
            inp = input('Would you like to try again? (y/n)')
            if inp == 'y':
                continue
            else:
                break
