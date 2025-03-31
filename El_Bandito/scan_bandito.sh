#!/bin/bash

# Color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TARGET="10.10.30.163"

echo -e "${BLUE}========== El Bandito Flag Hunt ==========${NC}\n"

# Check port 80 main page
echo -e "${YELLOW}Checking port 80 main page:${NC}"
curl -s http://$TARGET
echo -e "\n"

# Check the JavaScript file mentioned in nmap scan
echo -e "${YELLOW}Checking messages.js on port 80:${NC}"
curl -s http://$TARGET/static/messages.js
echo -e "\n"

# Check main page on port 8080
echo -e "${YELLOW}Checking port 8080 main page:${NC}"
curl -s http://$TARGET:8080
echo -e "\n"

# Check various HTML pages on port 8080
echo -e "${YELLOW}Checking common HTML pages on port 8080:${NC}"
for page in index burn wallet about admin login settings user profile token tokens coin coins dashboard; do
    echo -e "${GREEN}Checking /$page.html:${NC}"
    curl -s http://$TARGET:8080/$page.html | grep -i "flag\|thm\|hidden" --color=auto
    echo -e "\n"
done

# Check various API endpoints on port 8080
echo -e "${YELLOW}Checking common API endpoints on port 8080:${NC}"
for endpoint in api api/v1 api/status api/info api/tokens api/coins api/users api/admin api/flag; do
    echo -e "${GREEN}Checking /$endpoint:${NC}"
    curl -s http://$TARGET:8080/$endpoint
    echo -e "\n"
done

# Check for source files
echo -e "${YELLOW}Checking for source code files:${NC}"
for file in app.js jquery-1.10.2.min.js; do
    echo -e "${GREEN}Checking /$file:${NC}"
    curl -s http://$TARGET:8080/$file | head -n 20
    echo -e "\n"
done

# Check for assets
echo -e "${YELLOW}Checking assets:${NC}"
curl -s http://$TARGET:8080/assets
echo -e "\n"

# Check for Bandit-Coin specific endpoints
echo -e "${YELLOW}Checking Bandit-Coin specific endpoints:${NC}"
for endpoint in wallet burn transfer transaction transactions block blocks; do
    echo -e "${GREEN}Checking /$endpoint:${NC}"
    curl -s http://$TARGET:8080/$endpoint
    echo -e "\n"
done

# Check for hidden directories
echo -e "${YELLOW}Checking common hidden directories:${NC}"
for dir in .git .svn .env .secret .hidden admin; do
    echo -e "${GREEN}Checking /$dir:${NC}"
    curl -s http://$TARGET:8080/$dir
    echo -e "\n"
done

# Check for source code
echo -e "${YELLOW}Searching JavaScript files for flag patterns:${NC}"
curl -s http://$TARGET:8080/assets/index-6i4x9C9e.js | grep -i "flag\|thm\|hidden" --color=auto
echo -e "\n"

echo -e "${BLUE}========== Scan Complete ==========${NC}"
