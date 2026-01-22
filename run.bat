@echo off
REM ============================================
REM Pinyin Converter - Dual Mode (Windows)
REM CI-safe batch script
REM ============================================

setlocal enabledelayedexpansion

echo ========================================
echo Pinyin Converter - Dual Mode
echo ========================================
echo.

REM Detect CI environment (GitHub Actions sets CI=true)
if "%CI%"=="true" (
    set IS_CI=1
) else (
    set IS_CI=0
)

REM UTF-8 output
chcp 65001 >nul

REM --------------------------------------------
REM Python setup
REM --------------------------------------------
set REQUIRED_PYTHON_VERSION=3.10
set PYTHON_EXEC=python

python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan.
    if "%IS_CI%"=="1" (
        echo Python harus disediakan oleh runner CI.
        exit /b 1
    ) else (
        echo Silakan install Python 3.10 terlebih dahulu.
        goto END
    )
)

echo [INFO] Python ditemukan:
python --version
echo.

REM --------------------------------------------
REM Virtual environment
REM --------------------------------------------
if not exist ".venv" (
    echo [SETUP] Membuat virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Gagal membuat virtual environment
        exit /b 1
    )
)

call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Gagal mengaktifkan virtual environment
    exit /b 1
)

REM --------------------------------------------
REM Dependencies
REM --------------------------------------------
python -c "import pypinyin" >nul 2>nul
if %errorlevel% neq 0 (
    echo [SETUP] Installing dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Gagal install dependencies
        exit /b 1
    )
)

REM --------------------------------------------
REM Argument routing (NO else-if!)
REM --------------------------------------------
if "%~1"=="" goto MENU
if "%~1"=="--convert" goto CONVERT
if "%~1"=="--convert-folder" goto CONVERT_FOLDER
if "%~1"=="--convert-help" goto CONVERT_HELP
goto DEFAULT

:MENU
echo ====================================================
echo Program 1: Video/Image to SRT Mandarin
echo ====================================================
echo   run.bat --input video.mp4
echo   run.bat --input image.jpg
echo   run.bat --text "<sample text>"
echo.
echo ====================================================
echo Program 2: SRT Mandarin to Pinyin
echo ====================================================
echo   run.bat --convert file.srt
echo   run.bat --convert-folder .\subtitles
echo.
echo Help:
echo   run.bat --help
echo   run.bat --convert-help
goto END

:CONVERT
shift
python srt_to_pinyin.py --file %*
goto END

:CONVERT_FOLDER
shift
python srt_to_pinyin.py --folder %*
goto END

:CONVERT_HELP
python srt_to_pinyin.py --help
goto END

:DEFAULT
python app.py %*
goto END

:END
echo.
if "%IS_CI%"=="0" (
    echo Tekan tombol apa saja untuk keluar...
    pause >nul
)
exit /b 0
