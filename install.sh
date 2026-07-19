#!/data/data/com.termux/files/usr/bin/bash
# ==============================================
# G4F AI Studio - Termux + Rooted Android Installer
# ==============================================

set -e

echo "🚀 G4F AI Studio Installer for Termux (Rooted)"
echo "=============================================="

# === CONFIG ===
REPO_RAW="https://raw.githubusercontent.com/QWERTY-enter/g4f-ai-studio/main"
TERMUX_HOME="$HOME"
PHP_WWW="/data/adb/php7/files/www"

# === FUNCTIONS ===
force_mkdir() {
    if [ ! -d "$1" ]; then
        echo "[+] Creating directory: $1"
        mkdir -p "$1"
    else
        echo "[=] Directory exists: $1"
    fi
}

force_download() {
    local url="$1"
    local dest="$2"
    echo "[+] Downloading: $dest"
    curl -fsSL "$url" -o "$dest" || {
        echo "[-] Failed to download $url"
        exit 1
    }
}

# === 1. UPDATE & INSTALL DEPENDENCIES ===
echo "[1/6] Updating Termux packages..."
pkg update -y && pkg upgrade -y

echo "[2/6] Installing required packages..."
pkg install -y python python-pip git curl wget termux-api tsu 2>/dev/null || true

# Install Python packages
echo "[3/6] Installing Python dependencies..."
pip install --upgrade pip
pip install flask g4f python-dotenv requests

# === 4. CREATE DIRECTORIES ===
echo "[4/6] Preparing directories..."

force_mkdir "$TERMUX_HOME"
force_mkdir "$PHP_WWW"

# === 5. DOWNLOAD FILES ===
echo "[5/6] Downloading project files..."

# Download app.py → Termux home
force_download "$REPO_RAW/app.py" "$TERMUX_HOME/app.py"

# Download index.html → PHP web directory
force_download "$REPO_RAW/index.html" "$PHP_WWW/index.html"

# Create .env example
cat > "$TERMUX_HOME/.env.example" <<EOF
G4F_API_KEY=your_g4f_api_key_here
EOF

echo "[+] Files installed:"
echo "    - $TERMUX_HOME/app.py"
echo "    - $PHP_WWW/index.html"

# === 6. CLEANUP ===
echo "[6/6] Cleaning up installer..."
rm -f "$0" 2>/dev/null || true

echo ""
echo "✅ Installation Complete!"
echo ""
echo "📌 Next Steps:"
echo "1. Edit API Key:"
echo "   cp $TERMUX_HOME/.env.example $TERMUX_HOME/.env"
echo "   nano $TERMUX_HOME/.env"
echo ""
echo "2. Run Backend (in Termux):"
echo "   cd ~"
echo "   python app.py"
echo ""
echo "3. Open Frontend:"
echo "   http://localhost:8080   (or your PHP web server port)"
echo ""
echo "Note: Run backend with 'tsu' or 'sudo' if needed for root access."
echo "=============================================="