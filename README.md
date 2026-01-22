# 🎯 Pinyin Converter - Mandarin to Pinyin

[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)]()
[![Python](https://img.shields.io/badge/python-3.7%2B-brightgreen)]()

Aplikasi CLI untuk konversi tulisan Mandarin ke Pinyin dengan dukungan OCR gambar dan video.

---

## 📦 Dual Program dalam 1 Script

### **Program 1: Video/Image → SRT Mandarin**

Extract teks Mandarin dari video/gambar, auto-generate subtitle `.srt`

### **Program 2: SRT Mandarin → Pinyin**

Convert file subtitle Mandarin ke Pinyin (setelah edit manual)

---

## 🚀 Quick Start

### Windows

```cmd
# Program 1: Extract dari video
run.bat --input video.mp4

# Program 2: Convert SRT ke Pinyin
run.bat --convert subtitle.srt
run.bat --convert-folder .\subtitles
```

### macOS / Linux

```bash
chmod +x run.sh

# Program 1: Extract dari video
./run.sh --input video.mp4

# Program 2: Convert SRT ke Pinyin
./run.sh --convert subtitle.srt
./run.sh --convert-folder ./subtitles
```

---

## 💡 Contoh Penggunaan

### 1️⃣ Extract Subtitle dari Video

```bash
./run.sh --input video.mp4
```

**Output:** `video_subtitle.srt` (Mandarin)

### 2️⃣ Edit Manual (dengan text editor)

- Buka `video_subtitle.srt`
- Perbaiki teks Mandarin yang salah
- Sesuaikan timing subtitle
- Simpan file

### 3️⃣ Convert ke Pinyin

```bash
./run.sh --convert video_subtitle.srt
```

**Output:** `video_subtitle(P).srt` (Pinyin)

### 4️⃣ Batch Convert (Multiple Files)

```bash
./run.sh --convert-folder ./subtitles
```

**Hasil:**

```
subtitles/
├── 1.srt → 1(P).srt
├── 2.srt → 2(P).srt
├── 3.srt → 3(P).srt
└── ...
```

---

## 🎯 Workflow Lengkap

```
Video → Extract → SRT Mandarin → Edit Manual → Convert → SRT Pinyin
         (P1)                                      (P2)
```

---

## 🛠️ Commands Reference

### Program 1 (Video/Image OCR):

```bash
./run.sh --text "你好世界"                    # Text input
./run.sh --input image.jpg                    # Image OCR
./run.sh --input video.mp4                    # Video OCR
./run.sh --input video.mp4 --interval 60      # Custom interval
./run.sh --help                               # Show help
```

### Program 2 (SRT Converter):

```bash
./run.sh --convert file.srt                   # Single file
./run.sh --convert-folder ./subtitles         # Batch folder
./run.sh --convert-help                       # Show help
```

---

## 📝 File Naming Convention

Program 2 akan menambah suffix `(P)` untuk file Pinyin:

| Input (Mandarin) | Output (Pinyin)   |
| ---------------- | ----------------- |
| `video.srt`      | `video(P).srt`    |
| `1.srt`          | `1(P).srt`        |
| `episode1.srt`   | `episode1(P).srt` |

---

## 📄 Example Output

### Input: `1.srt` (Mandarin)

```srt
1
00:00:01,500 --> 00:00:03,500
早上好
```

### Output: `1(P).srt` (Pinyin)

```srt
1
00:00:01,500 --> 00:00:03,500
zao shang hao
```

---

**Made with ❤️ for Chinese language learners**
