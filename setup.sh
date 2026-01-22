#!/bin/bash
# Script setup otomatis untuk Pinyin Converter
# Untuk macOS/Linux

set -e  # Exit on error

echo "🚀 Setup Pinyin Converter..."
echo "================================"

# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Cek Python installation
echo -e "\n${YELLOW}[1/5]${NC} Memeriksa Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION ditemukan"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION ditemukan"
    PYTHON_CMD="python"
else
    echo -e "${RED}✗${NC} Python tidak ditemukan!"
    echo ""
    echo "Silakan install Python terlebih dahulu:"
    echo "  macOS: brew install python3"
    echo "  Linux: sudo apt-get install python3"
    echo ""
    exit 1
fi

# Cek versi Python minimal 3.7
PYTHON_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')

if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]; }; then
    echo -e "${RED}✗${NC} Python versi minimal 3.7 diperlukan"
    echo "Versi Anda: $PYTHON_VERSION"
    exit 1
fi

# Cek/buat virtual environment
echo -e "\n${YELLOW}[2/5]${NC} Memeriksa virtual environment..."
if [ ! -d ".venv" ]; then
    echo "Membuat virtual environment..."
    $PYTHON_CMD -m venv .venv
    echo -e "${GREEN}✓${NC} Virtual environment dibuat"
else
    echo -e "${GREEN}✓${NC} Virtual environment sudah ada"
fi

# Aktivasi virtual environment
echo -e "\n${YELLOW}[3/5]${NC} Mengaktifkan virtual environment..."
source .venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment aktif"

# Upgrade pip
echo -e "\n${YELLOW}[4/5]${NC} Meng-upgrade pip..."
pip install --upgrade pip -q
echo -e "${GREEN}✓${NC} Pip berhasil di-upgrade"

# Install dependencies
echo -e "\n${YELLOW}[5/5]${NC} Menginstall dependencies..."
echo "Ini mungkin memakan waktu 5-10 menit..."
echo "(Model EasyOCR ~500MB akan didownload saat pertama kali dijalankan)"
echo ""

pip install -r requirements.txt

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✓ Setup selesai!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Cara menggunakan:"
echo "  ./run.sh --text \"你好世界\""
echo "  ./run.sh --input gambar.jpg"
echo "  ./run.sh --input video.mp4"
echo ""
echo "Atau jalankan langsung:"
echo "  source .venv/bin/activate"
echo "  python app.py --text \"你好\""
echo ""
