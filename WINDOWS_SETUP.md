# Panduan Setup di Windows

## Prerequisites

1. **Python 3.12** - Download dari [python.org](https://www.python.org/downloads/)
   - Saat install, **CENTANG** "Add Python to PATH"
2. **Git** (optional) - Download dari [git-scm.com](https://git-scm.com/download/win)

## Langkah 1: Copy/Download Project

```powershell
# Jika punya Git:
git clone <repository-url>
cd pinyin

# Atau extract ZIP ke folder, lalu:
cd path\to\pinyin
```

## Langkah 2: Jalankan Setup Otomatis (RECOMMENDED)

Script `run.bat` akan **otomatis setup** virtual environment dan install dependencies!

Buka **Command Prompt** (tidak perlu Administrator):

```cmd
cd path\to\pinyin
run.bat --text "你好世界"
```

**Script akan otomatis:**

1. ✅ Cek Python sudah terinstall
2. ✅ Buat virtual environment (jika belum ada)
3. ✅ Install semua dependencies (jika belum ada)
4. ✅ Jalankan program dengan argument yang diberikan

**Pertama kali:** Akan download ~500MB library (5-10 menit)
**Setelah setup:** Langsung jalan!

## Langkah 2B: Setup Manual (Alternative)

Jika ingin setup manual tanpa `run.bat`:

<details>
<summary>Klik untuk expand instruksi manual</summary>

Buka **Command Prompt** atau **PowerShell**:

```powershell
# Buat virtual environment
python -m venv .venv

# Aktifkan virtual environment
# Di Command Prompt:
.venv\Scripts\activate.bat

# Di PowerShell:
.venv\Scripts\Activate.ps1
```

**Catatan PowerShell:** Jika error "cannot be loaded because running scripts is disabled", jalankan:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Jalankan:

```powershell
python app.py --text "你好世界"
```

</details>

Jika berhasil, akan muncul:

```
📝 Teks Mandarin: 你好世界
🎵 Pinyin: ni hao shi jie
```

## Cara Penggunaan

### Method 1: Menggunakan run.bat (RECOMMENDED) ⭐

Script ini **otomatis handle semua setup**! Tidak perlu aktivasi venv manual.

```cmd
# 1. Text Processing
run.bat --text "你好世界"

# 2. Image Processing
run.bat --input image.jpg

# 3. Video Processing (default interval=5)
run.bat --input video.mp4

# 4. Video dengan interval custom (3=lengkap tapi lambat, 10=cepat tapi skip beberapa)
run.bat --input video.mp4 --interval 3

# 5. Specify output location
run.bat --input video.mp4 --output output\subtitles.srt
```

**Keuntungan run.bat:**

- ✅ Tidak perlu aktifkan venv manual
- ✅ Auto-install dependencies jika belum ada
- ✅ Langsung jalankan command tanpa setup
- ✅ Error handling built-in

### Method 2: Manual dengan Python (Alternative)

Jika sudah setup manual dan prefer kontrol penuh:

```powershell
# Aktifkan venv dulu
.venv\Scripts\activate.bat

# Lalu jalankan command
python app.py --text "一个好的菜板都不能有木心吖"
python app.py --input gambar.jpg
python app.py --input video.mp4 --interval 5
```

---

## Contoh Command

### 1. Proses Teks Mandarin

```cmd
run.bat --text "一个好的菜板都不能有木心吖"
```

### 2. Proses Gambar

```cmd
run.bat --input gambar.jpg
```

### 3. Proses Video (Generate Subtitle)

```cmd
# Default interval 5 (cepat, 99% subtitle terdeteksi)
run.bat --input video.mp4

# Interval 3 (lebih lengkap, tapi 2x lebih lama)
run.bat --input video.mp4 --interval 3

# Dengan verbose log
run.bat --input video.mp4 --verbose
```

### 4. Simpan ke File

```cmd
run.bat --input gambar.jpg --output hasil.txt
```

## Troubleshooting Windows

### Error: "Python not found"

- Install Python dari python.org
- Restart Command Prompt/PowerShell
- Cek dengan: `python --version`

### Error: "pip not found"

```powershell
python -m ensurepip --upgrade
```

### Error: "Microsoft Visual C++ required"

Download dan install **Visual C++ Redistributable**:
https://aka.ms/vs/17/release/vc_redist.x64.exe

### OCR Lambat di Windows

- Normal, karena EasyOCR berjalan di CPU
- Proses video 1 menit bisa memakan waktu 10-15 menit
- Gunakan `--interval 5` atau `--interval 10` untuk mempercepat

### Error: "torch" atau "CUDA"

Tidak masalah, program akan otomatis menggunakan CPU:

```
Using CPU. Note: This module is much faster with a GPU.
```

## File Output

### Video → Subtitle SRT

```
Input:  video.mp4
Output: video_subtitle.srt (otomatis dibuat)
```

File SRT bisa langsung digunakan di:

- VLC Media Player
- Windows Media Player (dengan subtitle support)
- Video Editor (Premiere, DaVinci Resolve, dll)

### Format SRT

```
1
00:00:00,000 --> 00:00:02,000
一个好的菜板都不能有木心吖
yí gè hǎo de cài bǎn dōu bù néng yǒu mù xīn yā
```

## Tips untuk Windows

1. **Gunakan PowerShell 7** (lebih modern):
   - Download: `winget install Microsoft.PowerShell`

2. **Background Processing:**

   ```powershell
   # Jalankan di background
   Start-Process python -ArgumentList "app.py --input video.mp4" -NoNewWindow

   # Atau buat batch file: run_video.bat
   @echo off
   .venv\Scripts\python.exe app.py --input %1
   pause
   ```

3. **Drag & Drop:**
   Buat file `process_video.bat`:

   ```batch
   @echo off
   echo Processing video...
   .venv\Scripts\python.exe app.py --input %1
   echo.
   echo Done! Check the subtitle file.
   pause
   ```

   Lalu drag video ke file .bat untuk otomatis proses.

## Performance di Windows

| Interval | Speed        | Coverage | Rekomendasi                  |
| -------- | ------------ | -------- | ---------------------------- |
| 10       | Sangat cepat | 95%      | Video panjang (>5 menit)     |
| 5        | Cepat        | 99%      | **Default, balance terbaik** |
| 3        | Lambat       | 99.9%    | Subtitle berubah <0.3 detik  |

**Estimasi waktu:**

- Video 1 menit + interval 5 = ~10-15 menit proses
- Video 1 menit + interval 3 = ~20-30 menit proses

## Update Dependencies

```powershell
pip install --upgrade -r requirements.txt
```

## Uninstall

```powershell
# Hapus virtual environment
rmdir /s .venv

# Atau hapus seluruh folder project
```

## Support

Jika ada error, check log file atau jalankan dengan `--verbose` untuk detail lebih lengkap.
