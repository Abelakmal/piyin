@echo off
setlocal

echo ========================================
echo Pinyin Converter - Dual Mode
echo ========================================
echo.

chcp 65001 >nul

REM --------------------------------------------
REM Python check
REM --------------------------------------------
python --version >nul 2>nul || (
    echo [ERROR] Python tidak ditemukan
    exit /b 1
)

echo [INFO] Python ditemukan:
python --version
echo.

REM --------------------------------------------
REM Virtual environment
REM --------------------------------------------
if not exist ".venv" (
    echo [SETUP] Membuat virtual environment...
    python -m venv .venv || (
        echo [ERROR] Gagal membuat virtual environment
        exit /b 1
    )
)

call .venv\Scripts\activate.bat || (
    echo [ERROR] Gagal mengaktifkan virtual environment
    exit /b 1
)

REM --------------------------------------------
REM Dependencies
REM --------------------------------------------
python -c "import pypinyin" >nul 2>nul || (
    echo [SETUP] Installing dependencies...
    python -m pip install --upgrade pip || exit /b 1
    python -m pip install -r requirements.txt || exit /b 1
)

REM --------------------------------------------
REM Argument dispatch
REM --------------------------------------------
if "%~1"=="" goto MENU

if /i "%~1"=="--convert" (
    if "%~2"=="" goto CONVERT_HELP
    python srt_to_pinyin.py --file "%~2"
    goto END
)

if /i "%~1"=="--convert-folder" (
    if "%~2"=="" goto CONVERT_HELP
    python srt_to_pinyin.py --folder "%~2"
    goto END
)

if /i "%~1"=="--convert-help" (
    python srt_to_pinyin.py --help
    goto END
)

if /i "%~1"=="--help" goto MENU

REM --------------------------------------------
REM Default: app.py only gets its own args
REM --------------------------------------------
python app.py %*
goto END

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

:CONVERT_HELP
echo Usage:
echo   run.bat --convert file.srt
echo   run.bat --convert-folder folder_path
goto END

:END
echo.
pause
exit /b 0
