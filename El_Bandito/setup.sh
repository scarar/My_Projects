#!/bin/bash

BASE_ENV_PATH=~/venvs
DEFAULT_ENV_NAME="elbandito_env"

# Create venvs directory if it doesn't exist
mkdir -p "$BASE_ENV_PATH"

print_separator() {
    echo "============================================================"
}

print_banner() {
    print_separator
    echo " 🚀 Python Virtual Environment Setup Tool"
    echo "    Author: Your Friendly Setup Script"
    echo "    Purpose: Easily manage Python virtual environments"
    print_separator
}

list_envs() {
    echo "🔍 Existing virtual environments:"
    ls "$BASE_ENV_PATH"
    echo ""
}

# Print welcome banner
print_banner

# Loop to let user manage environments
while true; do
    list_envs
    read -p "Enter the name for your virtual environment (default: $DEFAULT_ENV_NAME, 'new' to create new, or 'exit' to quit): " ENV_NAME

    if [[ "$ENV_NAME" == "exit" ]]; then
        echo "👋 Exiting the setup. Have a great day!"
        exit 0
    elif [[ "$ENV_NAME" == "new" || -z "$ENV_NAME" ]]; then
        read -p "Enter a name for your new environment (default: $DEFAULT_ENV_NAME): " NEW_NAME
        ENV_NAME=${NEW_NAME:-$DEFAULT_ENV_NAME}
        break
    fi

    ENV_PATH="$BASE_ENV_PATH/$ENV_NAME"

    if [ -d "$ENV_PATH" ]; then
        echo "⚠️  Virtual environment '$ENV_NAME' already exists."
        read -p "Do you want to remove it? (y/n): " remove_choice
        if [[ "$remove_choice" =~ ^[Yy]$ ]]; then
            deactivate 2>/dev/null
            rm -rf "$ENV_PATH"
            echo "✅ Removed environment '$ENV_NAME'."
        fi

        read -p "Do you want to recreate it now? (y/n): " recreate_choice
        if [[ "$recreate_choice" =~ ^[Yy]$ ]]; then
            break
        else
            echo "❌ Skipping recreation. Please choose another name."
        fi
    else
        break
    fi

done

ENV_PATH="$BASE_ENV_PATH/$ENV_NAME"
echo "🔧 Creating Python virtual environment at: $ENV_PATH"
python3 -m venv "$ENV_PATH"

if [ $? -ne 0 ]; then
    echo "❌ Failed to create the virtual environment."
    exit 1
fi

# Activate the virtual environment in the current shell
source "$ENV_PATH/bin/activate"
echo "✅ Virtual environment '$ENV_NAME' is now active!"

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install required build tools
echo "🔧 Installing required system build tools (may prompt for sudo)..."
sudo apt update && sudo apt install -y build-essential cmake python3-dev libcapstone-dev

# Install common libraries except pwntools (for now)
echo "📦 Installing common Python libraries (excluding pwntools)..."
COMMON_PACKAGES="requests websocket-client urllib3 beautifulsoup4 lxml html5lib flask numpy pandas paramiko cryptography"
pip install $COMMON_PACKAGES

# Try installing pwntools separately with fallback message
#echo "📦 Attempting to install pwntools (might fail on ARM systems)..."
#pip install pwntools || echo "⚠️  pwntools failed to install. You may need to install 'capstone' manually or skip pwntools."

# Check for requirements.txt
if [ -f "requirements.txt" ]; then
    read -p "📄 requirements.txt detected. Install from it? (y/n): " req_choice
    if [[ "$req_choice" =~ ^[Yy]$ ]]; then
        pip install -r requirements.txt
        echo "✅ Installed packages from requirements.txt."
    else
        echo "ℹ️ Skipped requirements.txt installation."
    fi
fi

# Final message
print_separator
echo "🎉 Setup complete! You're ready to build, hack, or automate."
echo "🔹 To activate this environment later, run:"
echo "   source $ENV_PATH/bin/activate"
print_separator
