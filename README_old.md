# 🎯 Pinyin Converter - Mandarin to Pinyin CLI App

[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)]()
[![Python](https://img.shields.io/badge/python-3.7%2B-brightgreen)]()
[![License](https://img.shields.io/badge/license-Educational-orange)]()

Aplikasi Command Line Interface (CLI) untuk mengonversi tulisan Mandarin (Chinese characters) ke Pinyin dengan dukungan OCR untuk gambar dan video.

---

## ✨ Fitur Utama

- 🔤 **Konversi Teks**: Input teks Mandarin langsung → Pinyin dengan nada
- 📷 **OCR Gambar**: Ekstrak teks Mandarin dari gambar (JPG, PNG, dll)
- 🎬 **OCR Video**: Proses video frame-by-frame dengan timestamp
- 📺 **Subtitle SRT**: Auto-generate file subtitle (.srt) untuk video
- 🚀 **Auto Setup**: Script otomatis untuk semua platform
- 💾 **Export**: Simpan hasil ke file .txt atau .srt
- 🎨 **Terminal Colorful**: Output berwarna dan informatif

---

## 🚀 Quick Start

### 🪟 Windows

```cmd
# Double-click atau jalankan:
run.bat --text "你好世界"
```

### 🍎 macOS

```bash
chmod +x run.sh && ./run.sh --text "你好世界"
```

### 🐧 Linux

```bash
chmod +x run.sh && ./run.sh --text "你好世界"
```

**First time?** Script akan otomatis:

- ✅ Cek Python
- ✅ Buat virtual environment
- ✅ Install dependencies
- ✅ Jalankan aplikasi

---

## 📖 Dokumentasi Lengkap

| Dokumen                     | Deskripsi                          | Link                                   |
| --------------------------- | ---------------------------------- | -------------------------------------- |
| 🚀 **Quick Installation**   | Setup cepat untuk semua platform   | [INSTALL_GUIDE.md](INSTALL_GUIDE.md)   |
| 🌐 **Cross-Platform Guide** | Panduan detail Windows/macOS/Linux | [CROSS_PLATFORM.md](CROSS_PLATFORM.md) |
| ✅ **Compatibility Matrix** | Tabel kompatibilitas lengkap       | [COMPATIBILITY.md](COMPATIBILITY.md)   |
| 📺 **SRT Subtitle Format**  | Cara pakai & format subtitle       | [SRT_FORMAT.md](SRT_FORMAT.md)         |
| � **SRT Converter Guide**  | Convert SRT Mandarin ke Pinyin     | [SRT_CONVERTER_GUIDE.md](SRT_CONVERTER_GUIDE.md) |
| 📝 **Workflow Guide**       | Workflow lengkap video → Pinyin    | [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) |
| �📋 **Usage Examples**       | Contoh penggunaan lanjutan         | [USAGE.md](USAGE.md)                   |
| 🧪 **Testing Guide**        | Test cases & checklist             | [TEST.md](TEST.md)                     |
| 📄 **Academic Report**      | Template laporan tugas kuliah      | [LAPORAN.md](LAPORAN.md)               |

---

## 💡 Contoh Penggunaan

### 1️⃣ Konversi Teks

```bash
./run.sh --text "新年快乐"
```

**Output:**

```
📝 Teks Asli: 新年快乐
🔤 Pinyin: xin nian kuai le
🎵 Dengan Nada: xīn nián kuài lè
```

### 2️⃣ OCR dari Gambar

```bash
./run.sh --input chinese_text.png --verbose
```

**Hasil:**

- Deteksi teks Mandarin otomatis
- Konversi ke Pinyin
- Confidence score per teks

### 3️⃣ OCR Video + Subtitle

```bash
./run.sh --input video.mp4 --interval 30
```

**Output:**

- Console: Hasil per frame dengan timestamp
- File: `video_subtitle.srt` (auto-generated!)

**Format SRT:**

```srt
1
00:00:05,000 --> 00:00:06,000
这胶水没粘好啊啊
zhè jiāo shuǐ méi zhān hǎo a a
```

### 4️⃣ Save ke File

```bash
./run.sh --text "中国" --output hasil.txt
```

---

## � Program Kedua: SRT Mandarin → Pinyin Converter

Setelah mendapatkan subtitle `.srt` dari video (program pertama), Anda dapat:

1. **Edit manual** file `.srt` Mandarin untuk memperbaiki teks & timing
2. **Convert ke Pinyin** menggunakan program kedua

### Workflow:
```
Video → SRT Mandarin → Edit Manual → SRT Pinyin
```

### Convert Single File:
```bash
python srt_to_pinyin.py --file video_subtitle.srt
```

**Output:** `video_subtitle(P).srt` (Pinyin version)

### Convert Batch (Multiple Files):
```bash
python srt_to_pinyin.py --folder ./subtitles
```

**Contoh:**
```
Input folder:          Output:
├── 1.srt              ├── 1(P).srt    ← Pinyin
├── 2.srt              ├── 2(P).srt    ← Pinyin
├── 3.srt              ├── 3(P).srt    ← Pinyin
├── 4.srt              ├── 4(P).srt    ← Pinyin
└── 5.srt              └── 5(P).srt    ← Pinyin
```

**📖 Dokumentasi Lengkap:**
- [SRT_CONVERTER_GUIDE.md](SRT_CONVERTER_GUIDE.md) - Cara penggunaan detail
- [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) - Workflow lengkap video → Pinyin

---

## �📊 Platform Support

| Platform         | Status          | Auto Setup | Notes                 |
| ---------------- | --------------- | ---------- | --------------------- |
| 🪟 Windows 10/11 | ✅ Full Support | `run.bat`  | Python manual install |
| 🍎 macOS 10.15+  | ✅ Full Support | `run.sh`   | Python pre-installed  |
| 🐧 Ubuntu 20.04+ | ✅ Full Support | `run.sh`   | Apt packages needed   |
| 🐧 Debian 10+    | ✅ Full Support | `run.sh`   | Apt packages needed   |
| 🐧 Fedora/CentOS | ✅ Full Support | `run.sh`   | DNF/YUM packages      |

Lihat [COMPATIBILITY.md](COMPATIBILITY.md) untuk detail lengkap.

---

## 🛠️ Requirements

### Minimum:

- **Python**: 3.7+
- **RAM**: 4GB
- **Storage**: 2GB
- **OS**: Windows 10 / macOS 10.15 / Linux (recent)

### Recommended:

- **Python**: 3.10+
- **RAM**: 8GB
- **Storage**: 5GB
- **GPU**: Optional (NVIDIA CUDA untuk speed boost)

---

## 📦 Dependencies

Semua dependencies otomatis terinstall:

| Package       | Version  | Purpose                    |
| ------------- | -------- | -------------------------- |
| pypinyin      | 0.50.0   | Konversi Mandarin → Pinyin |
| easyocr       | 1.7.0    | OCR engine (deep learning) |
| opencv-python | 4.8.1.78 | Image & video processing   |
| Pillow        | 9.5.0    | Image manipulation         |
| torch         | Latest   | Backend untuk EasyOCR      |

Total download: ~1GB (first time only)

---

## 🎓 Untuk Tugas Kuliah

Aplikasi ini cocok untuk:

- ✅ Demonstrasi OCR dan NLP
- ✅ Tugas Computer Vision
- ✅ Project Machine Learning
- ✅ Penelitian bahasa Mandarin
- ✅ Portfolio programming

**Template laporan**: Lihat [LAPORAN.md](LAPORAN.md)

---

## 📝 CLI Parameters

```
--text TEXT          Input teks Mandarin langsung
--input FILE         Path ke file gambar atau video
--output FILE        Simpan hasil ke file txt
--interval N         Interval frame untuk video (default: 30)
--verbose            Tampilkan log detail proses
--help               Tampilkan help message
```

**Examples:**

```bash
# Basic
./run.sh --text "你好"

# Image with verbose
./run.sh --input gambar.jpg --verbose

# Video with custom interval
./run.sh --input video.mp4 --interval 60

# Save to file
./run.sh --text "学习中文" --output result.txt
```

---

## 🎯 Format Support

### Input:

- **Text**: Direct CLI input
- **Images**: JPG, PNG, BMP, TIFF, WebP
- **Videos**: MP4, AVI, MOV, MKV, FLV, WMV

### Output:

- **Console**: Formatted terminal output
- **Text**: .txt files
- **Subtitle**: .srt files (auto for video)

---

## 🚀 Installation

### Option 1: Auto (Recommended)

**Windows:**

```cmd
run.bat
```

**macOS/Linux:**

```bash
chmod +x setup.sh run.sh
./setup.sh
```

### Option 2: Manual

**All Platforms:**

```bash
# 1. Create venv
python3 -m venv .venv

# 2. Activate
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# 3. Install
pip install -r requirements.txt

# 4. Run
python app.py --text "你好"
```

**Detail lengkap:** [CROSS_PLATFORM.md](CROSS_PLATFORM.md)

---

## 💻 System Requirements

### Windows:

- Windows 10/11 (64-bit)
- Python 3.7+ (download dari python.org)
- 4GB RAM minimum

### macOS:

- macOS 10.15+
- Python 3.7+ (pre-installed)
- Xcode Command Line Tools

### Linux:

- Ubuntu 20.04+ / Debian 10+ / Fedora 35+
- Python 3.7+
- System libraries: `libgl1-mesa-glx libglib2.0-0`

---

## 🔧 Troubleshooting

### ❓ Common Issues:

**Python not found**

```bash
# Install Python from official website
# Make sure "Add to PATH" is checked
```

**Permission denied (macOS/Linux)**

```bash
chmod +x setup.sh run.sh
```

**Dependencies fail to install**

```bash
# Ensure stable internet (downloads ~1GB)
# Check Python version: python --version
```

**OCR slow performance**

```bash
# Normal on CPU, faster with GPU
# For video: increase --interval value
```

**Subtitle timing off**

```bash
# Adjust --interval parameter
# Or edit .srt file manually
```

**Lihat troubleshooting lengkap:** [CROSS_PLATFORM.md](CROSS_PLATFORM.md)

---

## 📈 Performance

| Task                 | CPU Mode | GPU Mode | Memory  |
| -------------------- | -------- | -------- | ------- |
| Text conversion      | < 1s     | < 1s     | ~50 MB  |
| Image OCR (1080p)    | 3-5s     | 1-2s     | ~500 MB |
| Video (1 min, 30fps) | 3-5 min  | 1-2 min  | ~1 GB   |

**Tips untuk speed:**

- Gunakan `--interval 60-120` untuk video besar
- GPU (CUDA) akan otomatis terdeteksi jika tersedia
- Close aplikasi lain untuk free up RAM

---

## 🌟 Key Features

### 🎨 Smart OCR

- Deteksi otomatis karakter Mandarin
- Confidence score per deteksi
- Support gambar low-light dengan preprocessing

### ⏱️ Video Processing

- Frame sampling intelligent
- Timestamp akurat per deteksi
- Auto-generate subtitle SRT

### 📺 Subtitle SRT

- Format standar (compatible all players)
- Dual subtitle: Mandarin + Pinyin
- Ready untuk VLC, YouTube, video editors

### 🚀 Easy Setup

- Auto-detect Python
- One-command setup
- Cross-platform scripts

---

## 📚 Documentation Tree

```
pinyin/
├── 📄 README.md                 # This file
├── 🚀 INSTALL_GUIDE.md          # Quick installation
├── 🌐 CROSS_PLATFORM.md         # Platform-specific guide
├── ✅ COMPATIBILITY.md          # Compatibility matrix
├── 📺 SRT_FORMAT.md             # Subtitle format info
├── 📋 USAGE.md                  # Usage examples
├── 🧪 TEST.md                   # Testing guide
├── 📄 LAPORAN.md                # Academic report template
│
├── 🎬 app.py                    # Main application
├── 🪟 run.bat                   # Windows runner
├── 🐧 run.sh                    # macOS/Linux runner
├── ⚙️ setup.sh                  # Setup script
├── 📦 requirements.txt          # Python dependencies
│
├── src/                         # Source code
│   ├── text_processor.py        # Text conversion
│   ├── image_processor.py       # Image OCR
│   ├── video_processor.py       # Video OCR
│   └── utils.py                 # Utilities
│
└── examples/                    # Sample files
    ├── sample_text.txt
    ├── sample_subtitle.srt
    └── (add your samples here)
```

---

## 🎓 Academic Use

### Citation Format (if needed):

```
Pinyin Converter - CLI Application for Mandarin OCR and Transliteration
Version 1.0, January 2026
Educational Project
```

### Features for Academic Projects:

- ✅ Open source libraries
- ✅ No API keys required
- ✅ Runs offline (after first setup)
- ✅ Complete documentation
- ✅ Report template included

---

## 🆘 Getting Help

### Check Version & Help:

```bash
./run.sh --help
```

### Enable Verbose Logging:

```bash
./run.sh --input file.mp4 --verbose
```

### Check Dependencies:

```bash
source .venv/bin/activate
pip list
```

### Report Issues:

Include:

- Platform (Windows/macOS/Linux)
- Python version
- Error message
- Command used

---

## 🔄 Updates

To update dependencies:

```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install --upgrade -r requirements.txt
```

---

## 📊 Project Stats

- **Lines of Code**: ~1000+
- **Files**: 20+
- **Documentation**: 8 files
- **Platforms**: 3 (Windows, macOS, Linux)
- **Languages**: Python, Bash, Batch
- **Dependencies**: 5 major packages

---

## 🎯 Use Cases

1. **Learning Mandarin**: Convert text untuk practice pronunciation
2. **Subtitle Creation**: Auto-generate subtitle dari video
3. **OCR Projects**: Extract Chinese text dari images
4. **Research**: Analyze Chinese text corpus
5. **Academic**: Demonstrate NLP & CV techniques

---

## ⚠️ Limitations

- OCR accuracy: 80-95% (depends on image quality)
- Video processing: Slow for large files (use high interval)
- GPU: Optional (works fine on CPU)
- First run: Downloads ~1GB of models

---

## 🔐 Privacy

- **No cloud processing**: Everything runs locally
- **No data collection**: Your files stay on your machine
- **No API calls**: Except initial model download
- **Offline capable**: After first setup

---

## 📄 License

Educational & Research Use Only
Free to use, modify, and distribute for non-commercial purposes.

---

## 🙏 Acknowledgments

Built with:

- [pypinyin](https://github.com/mozillazg/python-pinyin) - Pinyin conversion
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) - OCR engine
- [OpenCV](https://opencv.org/) - Image/video processing
- [PyTorch](https://pytorch.org/) - Deep learning backend

---

## 📞 Support

- 📖 Documentation: Check files in project root
- 🐛 Issues: Describe problem with details
- 💡 Feature requests: Open for suggestions
- 🤝 Contributions: Welcome!

---

## 🎉 Quick Links

- [▶️ Quick Start](#-quick-start)
- [📖 Full Documentation](#-dokumentasi-lengkap)
- [🌐 Platform Guide](CROSS_PLATFORM.md)
- [✅ Compatibility](COMPATIBILITY.md)
- [📺 Subtitle Format](SRT_FORMAT.md)

---

**Happy learning! 学习愉快！新年快乐！** 🎊

**Version**: 1.0.0
**Last Updated**: 7 January 2026
**Status**: ✅ Production Ready
