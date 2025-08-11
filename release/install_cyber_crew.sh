#!/bin/bash
set -eu

TERMINAL_WIDTH=$(tput cols 2>/dev/null || echo 80)
SEPARATOR=$(printf '=%.0s' $(seq 1 $TERMINAL_WIDTH))

PACKAGE_NAME="cyber_crew"
WD=$(pwd)
VENV_NAME=".venv"
EXE_NAME="cyber-crew"
UNINSTALL_FILE="uninstall_cyber_crew.sh"
README_FILE="README.txt"

FULL_VENV_PATH="${WD}/${VENV_NAME}"
BIN_DIR="${FULL_VENV_PATH}/bin"

CONFIG_PATH="${WD}/${PACKAGE_NAME}/config"
UNINSTALL_PATH="${WD}/${UNINSTALL_FILE}"
README_PATH="${WD}/${README_FILE}"

echo ${SEPARATOR}
echo "Creating virtual environment..."
uv venv ${VENV_NAME}

echo "Installing from wheel..."
WHEEL_FILE=$(find "${WD}" -name "${PACKAGE_NAME}-*-py3-none-any.whl")
uv pip install "${WHEEL_FILE}"
rm "${WHEEL_FILE}"

echo "Creating API executables..."
cat > "${WD}/${EXE_NAME}" << EOF
#!/bin/bash
export cyber_crew_ROOT_DIR=${WD}
${BIN_DIR}/${EXE_NAME} "\$@"
EOF
chmod +x "${WD}/${EXE_NAME}"

echo "Creating uninstall script..."
cat > "${UNINSTALL_PATH}" << EOF
#!/bin/bash
set -eu
cd "${WD}"
rm -rf *
EOF
chmod +x "${UNINSTALL_PATH}"

cat > "${README_PATH}" << EOF
Cyber Crew has been installed successfully.
Run the application using './${EXE_NAME}'
To configure the application, edit the configuration files at: '${CONFIG_PATH}'
Add your environment variables to the '.env' file.
To uninstall, run: './${UNINSTALL_FILE}'
EOF

echo "${SEPARATOR}"
cat "${README_PATH}"
echo "${SEPARATOR}"

rm -- "$0"
