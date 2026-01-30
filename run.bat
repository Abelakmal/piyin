@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo Pinyin Converter - Dual Mode
echo ========================================
echo.

if "%CI%"=="true" (set IS_CI=1) else (set IS_CI=0)

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
REM Argument routing
REM --------------------------------------------
set SCRIPT_EXIT=0
:ARG_LOOP
if "%~1"=="" goto MENU
if /i "%~1"=="--convert" goto CONVERT
if /i "%~1"=="-convert" goto CONVERT
if /i "%~1"=="--convert-folder" goto CONVERT_FOLDER
if /i "%~1"=="-convert-folder" goto CONVERT_FOLDER
if /i "%~1"=="--convert-help" goto CONVERT_HELP
if /i "%~1"=="-convert-help" goto CONVERT_HELP
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
echo   run.bat --convert-folder .\subtitles 2    # 2 spasi antar karakter
echo   run.bat --convert-folder .\subtitles 3    # 3 spasi antar karakter
echo.
echo Help:
echo   run.bat --help
echo   run.bat --convert-help
goto END

:CONVERT
python srt_to_pinyin.py --file "%~2"
set SCRIPT_EXIT=%ERRORLEVEL%
goto END

:CONVERT_FOLDER
set FOLDER_ARG=%~2
set SPACING_ARG=%~3
if "%SPACING_ARG%"=="" set SPACING_ARG=1
python srt_to_pinyin.py --folder "%FOLDER_ARG%" --spacing %SPACING_ARG%
set SCRIPT_EXIT=%ERRORLEVEL%
goto END

:CONVERT_HELP
python srt_to_pinyin.py --help
set SCRIPT_EXIT=%ERRORLEVEL%
goto END

:DEFAULT
python app.py %*
set SCRIPT_EXIT=%ERRORLEVEL%
goto END

:END
echo.
if "%IS_CI%"=="0" pause
exit /b %SCRIPT_EXIT%
