#!/bin/bash
set -eu

TERMINAL_WIDTH=$(tput cols 2>/dev/null || echo 80)
SEPARATOR=$(printf '=%.0s' $(seq 1 $TERMINAL_WIDTH))

# Check for required arguments
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <USERNAME> <PASSWORD>"
  exit 1
fi

USERNAME="$1"
PASSWORD="$2"

# Create the CTF directory structure
CTF_DIR="example_ctf"
ALPHA_DIR="${CTF_DIR}/alpha"
BRAVO_DIR="${CTF_DIR}/bravo"
CHARLIE_DIR="${CTF_DIR}/charlie"

# Cleanup function
cleanup() {
  echo ${SEPARATOR}
  echo "Cleaning up..."
  if [ -d "${CTF_DIR}" ]; then
    rm -rf "${CTF_DIR}"
    echo "CTF directory removed."
  fi
  echo "Mission complete!"
  echo ${SEPARATOR}
}

trap cleanup EXIT

echo ${SEPARATOR}
echo "Creating CTF directory structure..."

mkdir -p "${CTF_DIR}"
mkdir -p "${ALPHA_DIR}"
mkdir -p "${BRAVO_DIR}"
mkdir -p "${CHARLIE_DIR}"

# Place the flag in one of the directories
echo "FLAG{congratulations_you_found_it}" > "${CTF_DIR}/bravo/flag.txt"

# Add random text files to each directory
echo "Just a decoy file." > "${ALPHA_DIR}/notes.txt"
echo "Nothing to see here." > "${ALPHA_DIR}/readme.txt"

echo "This is not the flag." > "${BRAVO_DIR}/decoy.txt"

echo "Random thoughts." > "${CHARLIE_DIR}/log.txt"
echo "Another distraction." > "${CHARLIE_DIR}/info.txt"

tree "${CTF_DIR}"

# Kick off the Cyber Crew mission
echo ${SEPARATOR}
echo "Running the Cyber Crew mission..."
uv run cyber-crew -u "${USERNAME}" -p "${PASSWORD}" -m "Find the flag located in the '${CTF_DIR}' directory. It has the format 'FLAG{...}'."
