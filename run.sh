#!/bin/bash
# Script untuk menjalankan Pinyin Converter
# Support 2 program:
#   1. app.py - Extract video/image ke SRT Mandarin
#   2. srt_to_pinyin.py - Convert SRT Mandarin ke Pinyin
# Untuk macOS/Linux

# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Versi Python yang dibutuhkan untuk PaddleOCR
REQUIRED_PYTHON_VERSION="3.10"
PYTHON_CANDIDATE="python${REQUIRED_PYTHON_VERSION}"

# Fungsi bantu: cek command
has_cmd() { command -v "$1" >/dev/null 2>&1; }

PYTHON_EXEC=""
if has_cmd "$PYTHON_CANDIDATE"; then
    PYTHON_EXEC="$PYTHON_CANDIDATE"
elif has_cmd "python3.10"; then
    PYTHON_EXEC="python3.10"
elif has_cmd "python3" && [ "$(python3 -c 'import sys; print(sys.version_info[:2])' 2>/dev/null)" = "(3, 10)" ]; then
    PYTHON_EXEC="python3"
else
    echo -e "${YELLOW}[INFO] Python ${REQUIRED_PYTHON_VERSION} tidak ditemukan. Mencoba instal otomatis...${NC}"

    # 1) Coba Homebrew (macOS)
    if has_cmd brew; then
        echo -e "${BLUE}[INFO] Menemukan Homebrew — menginstall python@${REQUIRED_PYTHON_VERSION}${NC}"
        brew install python@${REQUIRED_PYTHON_VERSION} || true
        BREW_PFX=$(brew --prefix python@${REQUIRED_PYTHON_VERSION} 2>/dev/null || true)
        if [ -x "${BREW_PFX}/bin/python3.10" ]; then
            PYTHON_EXEC="${BREW_PFX}/bin/python3.10"
        fi
    fi

    # 2) Coba apt-get (Debian/Ubuntu)
    if [ -z "$PYTHON_EXEC" ] && has_cmd apt-get; then
        echo -e "${BLUE}[INFO] Menggunakan apt-get untuk menginstall python3.10${NC}"
        sudo apt-get update && sudo apt-get install -y python3.10 python3.10-venv || true
        if has_cmd python3.10; then
            PYTHON_EXEC="python3.10"
        fi
    fi

    # 3) Coba pyenv
    if [ -z "$PYTHON_EXEC" ]; then
        if has_cmd pyenv; then
            echo -e "${BLUE}[INFO] Menemukan pyenv — menginstall Python ${REQUIRED_PYTHON_VERSION}${NC}"
            pyenv install -s 3.10.13 || true
            pyenv local 3.10.13 || true
            export PATH="${PYENV_ROOT:-$HOME/.pyenv}/shims:$PATH"
            if has_cmd python; then
                PYTHON_EXEC="$(pyenv which python 2>/dev/null || command -v python)"
            fi
        else
            # coba install pyenv otomatis (non-interaktif installer)
            if has_cmd curl; then
                echo -e "${BLUE}[INFO] Menginstall pyenv (auto) untuk menginstall Python ${REQUIRED_PYTHON_VERSION}${NC}"
                curl https://pyenv.run | bash || true
                export PATH="$HOME/.pyenv/bin:$HOME/.pyenv/shims:$PATH"
                export PYENV_ROOT="$HOME/.pyenv"
                if has_cmd pyenv; then
                    pyenv install -s 3.10.13 || true
                    pyenv local 3.10.13 || true
                    PYTHON_EXEC="$(pyenv which python 2>/dev/null || command -v python)"
                fi
            fi
        fi
    fi

    if [ -z "$PYTHON_EXEC" ]; then
        echo -e "${RED}[ERROR] Gagal menginstall Python otomatis. Silakan install Python 3.10 secara manual:${NC}"
        echo "  macOS: brew install python@3.10"
        echo "  Ubuntu: sudo apt-get install python3.10 python3.10-venv"
        echo "  or use pyenv: https://github.com/pyenv/pyenv"
        exit 1
    fi
fi

echo -e "${GREEN}[OK] Menggunakan Python: $PYTHON_EXEC${NC}"
$PYTHON_EXEC --version
echo ""

# Cek apakah sudah di-setup
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠ Virtual environment belum ada${NC}"
    echo "Membuat virtual environment dengan Python ${REQUIRED_PYTHON_VERSION}..."
    $PYTHON_EXEC -m venv .venv
    echo -e "${GREEN}✓ Virtual environment dibuat${NC}"
    echo ""
fi

# Cek apakah dependencies sudah terinstall
if [ -d ".venv" ]; then
    # Aktivasi venv
    source .venv/bin/activate
    
    # Verifikasi Python version di venv
    VENV_PYTHON_VERSION=$(python --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
    echo -e "${BLUE}[INFO] Using Python ${VENV_PYTHON_VERSION} in virtual environment${NC}"
    
    if [[ "$VENV_PYTHON_VERSION" != "$REQUIRED_PYTHON_VERSION" ]]; then
        echo -e "${YELLOW}⚠ Virtual environment menggunakan Python versi yang salah${NC}"
        echo "Menghapus dan membuat ulang dengan Python ${REQUIRED_PYTHON_VERSION}..."
        deactivate 2>/dev/null || true
        rm -rf .venv
        $PYTHON_EXEC -m venv .venv
        source .venv/bin/activate
        echo -e "${GREEN}✓ Virtual environment dibuat ulang${NC}"
        echo ""
    fi
    
    # Cek apakah pypinyin sudah terinstall
    if ! pip show pypinyin &> /dev/null; then
        echo -e "${YELLOW}⚠ Dependencies belum lengkap${NC}"
        echo "Menginstall dependencies..."
        pip install --upgrade pip -q
        pip install -r requirements.txt -q
        echo -e "${GREEN}✓ Dependencies terinstall${NC}"
        echo ""
    fi
else
    echo -e "${RED}✗ Setup gagal!${NC}"
    exit 1
fi

# Jalankan aplikasi dengan arguments yang diberikan
if [ $# -eq 0 ]; then
    # Jika tidak ada arguments, tampilkan menu
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║        PINYIN CONVERTER - Dual Mode Script            ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}Program 1: Video/Image → SRT Mandarin${NC}"
    echo "  ./run.sh --input video.mp4"
    echo "  ./run.sh --input image.jpg"
    echo "  ./run.sh --text \"你好世界\""
    echo ""
    echo -e "${GREEN}Program 2: SRT Mandarin → Pinyin${NC}"
    echo "  ./run.sh --convert file.srt"
    echo "  ./run.sh --convert-folder ./subtitles"
    echo ""
    echo "Help:"
    echo "  ./run.sh --help          (Program 1 help)"
    echo "  ./run.sh --convert-help  (Program 2 help)"
    echo ""
else
    # Deteksi mode berdasarkan argument
    if [[ "$1" == "--convert" ]]; then
        # Mode: Convert SRT Mandarin ke Pinyin (single file)
        shift
        python srt_to_pinyin.py --file "$@"
    elif [[ "$1" == "--convert-folder" ]]; then
        # Mode: Convert batch folder
        shift
        python srt_to_pinyin.py --folder "$@"
    elif [[ "$1" == "--convert-help" ]]; then
        # Help untuk program 2
        python srt_to_pinyin.py --help
    else
        # Mode default: Program 1 (app.py)
        python app.py "$@"
    fi
fi
