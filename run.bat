@echo off
REM Script untuk menjalankan Pinyin Converter di Windows
REM Support 2 program:
REM   1. app.py - Extract video/image ke SRT Mandarin
REM   2. srt_to_pinyin.py - Convert SRT Mandarin ke Pinyin

setlocal enabledelayedexpansion

echo ========================================
echo Pinyin Converter - Dual Mode
echo ========================================
echo.

REM Set code page to UTF-8 to better handle non-ASCII output in CI
chcp 65001 >nul

REM Cek/siapkan Python versi spesifik (untuk PaddleOCR)
set REQUIRED_PYTHON_VERSION=3.10
set PYTHON_EXE_NAME=python%REQUIRED_PYTHON_VERSION%

REM Coba temukan python3.10 atau gunakan py launcher
where %PYTHON_EXE_NAME% >nul 2>nul
if %errorlevel% neq 0 (
    py -%REQUIRED_PYTHON_VERSION% --version >nul 2>nul
    if %errorlevel% neq 0 (
        echo [INFO] Python %REQUIRED_PYTHON_VERSION% tidak ditemukan di sistem.
        echo Akan mencoba download dan install otomatis (membutuhkan hak admin)...
        set PYTHON_INSTALLER=python-3.10.11-amd64.exe
        set PYTHON_URL=https://www.python.org/ftp/python/3.10.11/%PYTHON_INSTALLER%
        if not exist %PYTHON_INSTALLER% (
            echo [DOWNLOAD] Mengunduh installer Python 3.10...
            powershell -Command "Try { Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%' -UseBasicParsing } Catch { exit 1 }"
            if %errorlevel% neq 0 (
                echo [ERROR] Gagal mengunduh installer. Silakan download manual dari %PYTHON_URL%
                pause
                exit /b 1
            )
        )
        echo [INSTALL] Menjalankan installer Python 3.10 (silent)...
        start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1
        REM cek lagi setelah instalasi
        where %PYTHON_EXE_NAME% >nul 2>nul
        if %errorlevel% neq 0 (
            py -%REQUIRED_PYTHON_VERSION% --version >nul 2>nul
            if %errorlevel% neq 0 (
                echo [ERROR] Python %REQUIRED_PYTHON_VERSION% masih belum terdeteksi setelah instalasi.
                echo Silakan install manual dari %PYTHON_URL%
                pause
                exit /b 1
            ) else (
                set PYTHON_EXEC=py -%REQUIRED_PYTHON_VERSION%
            )
        ) else (
            set PYTHON_EXEC=%PYTHON_EXE_NAME%
        )
    ) else (
        set PYTHON_EXEC=py -%REQUIRED_PYTHON_VERSION%
    )
) else (
    set PYTHON_EXEC=%PYTHON_EXE_NAME%
)

%PYTHON_EXEC% --version
echo.

REM Cek virtual environment
if not exist ".venv" (
    echo [SETUP] Virtual environment belum ada
    echo Membuat virtual environment...
    %PYTHON_EXEC% -m venv .venv
    echo [OK] Virtual environment dibuat
    echo.
)

REM Aktivasi virtual environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo [ERROR] Gagal mengaktifkan virtual environment
    pause
    exit /b 1
)

REM Cek dependencies
python -c "import pypinyin" >nul 2>nul
if %errorlevel% neq 0 (
    echo [SETUP] Installing dependencies...
    echo Ini mungkin memakan waktu 5-10 menit...
    echo.
    pip install --upgrade pip
    pip install -r requirements.txt
    echo.
    echo [OK] Dependencies terinstall
    echo.
)

REM Jalankan aplikasi
if "%~1"=="" (
    REM Jika tidak ada arguments, tampilkan menu
    echo ====================================================
    echo Program 1: Video/Image to SRT Mandarin
    echo ====================================================
    echo   run.bat --input video.mp4
    echo   run.bat --input image.jpg
    REM contoh teks Mandarin (non-ASCII) dihilangkan untuk kestabilan CI
    echo   run.bat --text "<sample text>"
    echo.
    echo ====================================================
    echo Program 2: SRT Mandarin to Pinyin
    echo ====================================================
    echo   run.bat --convert file.srt
    echo   run.bat --convert-folder .\subtitles
    echo.
    echo Help:
    echo   run.bat --help          (Program 1 help)
    echo   run.bat --convert-help  (Program 2 help)
    echo.
) else if "%~1"=="--convert" (
    REM Mode: Convert SRT Mandarin ke Pinyin (single file)
    shift
    python srt_to_pinyin.py --file %*
) else if "%~1"=="--convert-folder" (
    REM Mode: Convert batch folder
    shift
    python srt_to_pinyin.py --folder %*
) else if "%~1"=="--convert-help" (
    REM Help untuk program 2
    python srt_to_pinyin.py --help
) else (
    REM Mode default: Program 1 (app.py)
    python app.py %*
)

echo.
pause
