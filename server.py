import socket
from prometheus_client import start_http_server, Gauge
import threading
import json

HOST = '127.0.0.1'
PORT = 8080

cpu = Gauge('cpu_usage', 'Usage of CPU', ['client_number'])
ram = Gauge('memory_usage', 'Usage of RAM', ['client_number'])
disk = Gauge('disk_usage', 'Usage of DISK', ['client_number'])

def handle_client(conn, addr, client_no):
    print(f'Client {client_no} connected to {addr}')

    try:
        while True:
            msg = conn.recv(1024).decode('UTF-8')
            metrices = json.loads(msg)
            print(f'Client{client_no} : {metrices}')
            cpu.labels(f'client_{client_no}').set(metrices['CPU'])
            ram.labels(f'client_{client_no}').set(metrices['RAM'])
            disk.labels(f'client_{client_no}').set(metrices['DISK'])

    except Exception as e:
        print(f'Client{client_no} dissconnected!')



start_http_server(8000)
client_number = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Socket is listening on {HOST}:{PORT}')

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr,client_number))
        thread.start()
        client_number += 1

