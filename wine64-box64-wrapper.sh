#!/bin/bash
# Define paths
WINE_ROOT="/home/scarar/Hacking/TryHackMe/scripts/c++/wine-x86_64"
WINE64_PATH="$WINE_ROOT/bin/wine64"
BOX64_PATH="$WINE_ROOT/bin"
WINEPREFIX="$HOME/.wine64"
# Function to display usage information
show_usage() {
    echo "Usage: $0 <windows_executable> [arguments...]"
    echo
    echo "This script runs Windows executables on ARM64 using box64 and wine64."
    echo
    echo "Options:"
    echo "  --debug    Enable Wine debugging output"
    echo "  --help     Display this help message"
    echo "  --version  Display Wine version information"
    exit 1
}
# Process special commands
if [ "$1" == "--help" ]; then
    show_usage
elif [ "$1" == "--version" ]; then
    BOX64_PATH="$BOX64_PATH" box64 "$WINE64_PATH" --version
    exit 0
fi
# Check if an argument was provided
if [ $# -eq 0 ]; then
    show_usage
fi
# Set debug mode if requested
DEBUG_MODE=0
if [ "$1" == "--debug" ]; then
    DEBUG_MODE=1
    shift
fi
# Get the executable path
EXECUTABLE="$1"
if [[ "$EXECUTABLE" != /* ]]; then
    # If not an absolute path, make it relative to current directory
    EXECUTABLE="$(pwd)/$EXECUTABLE"
fi
# Check if the file exists
if [ ! -f "$EXECUTABLE" ]; then
    echo "Error: File '$EXECUTABLE' not found."
    exit 1
fi
# Get the directory of the executable
EXEC_DIR=$(dirname "$EXECUTABLE")
EXEC_NAME=$(basename "$EXECUTABLE")
# Change to the executable's directory (important for Windows apps)
cd "$EXEC_DIR"
# Set environment variables
export BOX64_PATH="$BOX64_PATH"
export WINEPREFIX="$WINEPREFIX"
# Run with debug output if requested
if [ $DEBUG_MODE -eq 1 ]; then
    export WINEDEBUG=+all
    BOX64_LOG=1 box64 "$WINE64_PATH" "$EXEC_NAME" "${@:2}" 2>&1 | tee wine-debug.log
else
    # Run the executable with any additional arguments
    box64 "$WINE64_PATH" "$EXEC_NAME" "${@:2}"
fi
