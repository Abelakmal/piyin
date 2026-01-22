"""
Utility functions dan classes untuk aplikasi
"""

import sys
from datetime import datetime


class Logger:
    """Simple logger untuk menampilkan pesan dengan warna"""
    
    # ANSI color codes
    COLORS = {
        'RED': '\033[91m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'BLUE': '\033[94m',
        'MAGENTA': '\033[95m',
        'CYAN': '\033[96m',
        'WHITE': '\033[97m',
        'RESET': '\033[0m',
        'BOLD': '\033[1m'
    }
    
    def __init__(self, verbose=False):
        """
        Inisialisasi logger
        
        Args:
            verbose (bool): Jika True, tampilkan semua log detail
        """
        self.verbose = verbose
    
    def _print(self, message, color=None, prefix=None):
        """Helper untuk print dengan warna"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if prefix:
            msg = f"[{timestamp}] {prefix} {message}"
        else:
            msg = f"[{timestamp}] {message}"
        
        if color and sys.stdout.isatty():  # Cek jika terminal support warna
            print(f"{color}{msg}{self.COLORS['RESET']}")
        else:
            print(msg)
    
    def info(self, message):
        """Log informasi"""
        if self.verbose:
            self._print(message, self.COLORS['CYAN'], "ℹ")
        else:
            self._print(message)
    
    def success(self, message):
        """Log sukses"""
        self._print(message, self.COLORS['GREEN'], "✓")
    
    def warning(self, message):
        """Log peringatan"""
        self._print(message, self.COLORS['YELLOW'], "⚠")
    
    def error(self, message):
        """Log error"""
        self._print(message, self.COLORS['RED'], "✗")
    
    def debug(self, message):
        """Log debug (hanya tampil jika verbose=True)"""
        if self.verbose:
            self._print(message, self.COLORS['MAGENTA'], "DEBUG")


def save_to_file(results, output_path):
    """
    Simpan hasil konversi ke file
    
    Args:
        results (list): List hasil konversi
        output_path (str): Path file output
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("HASIL KONVERSI MANDARIN KE PINYIN\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for idx, result in enumerate(results, 1):
            f.write(f"\n{'='*60}\n")
            f.write(f"HASIL #{idx}\n")
            f.write(f"{'='*60}\n\n")
            
            # Jika hasil dari video
            if 'frames' in result:
                f.write(f"Tipe: VIDEO\n")
                f.write(f"Total frame diproses: {len(result['frames'])}\n")
                f.write(f"Durasi: {result.get('duration', 'N/A')} detik\n\n")
                
                for frame_idx, frame_data in enumerate(result['frames'], 1):
                    f.write(f"\n--- Frame #{frame_idx} (Timestamp: {frame_data['timestamp']}s) ---\n")
                    f.write(f"Teks Mandarin: {frame_data.get('chinese_text', '')}\n")
                    f.write(f"Pinyin: {frame_data.get('pinyin', '')}\n")
                    if frame_data.get('pinyin_toned'):
                        f.write(f"Pinyin (dengan nada): {frame_data.get('pinyin_toned', '')}\n")
            
            # Jika hasil dari teks/gambar
            else:
                f.write(f"Teks Mandarin: {result.get('chinese_text', '')}\n")
                f.write(f"Pinyin: {result.get('pinyin', '')}\n")
                if result.get('pinyin_toned'):
                    f.write(f"Pinyin (dengan nada): {result.get('pinyin_toned', '')}\n")
        
        f.write(f"\n{'='*60}\n")
        f.write("END OF FILE\n")
        f.write(f"{'='*60}\n")


def format_timestamp(seconds):
    """
    Format detik ke format MM:SS
    
    Args:
        seconds (float): Waktu dalam detik
        
    Returns:
        str: Format MM:SS
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def format_srt_timestamp(seconds):
    """
    Format detik ke format SRT timestamp (HH:MM:SS,mmm)
    
    Args:
        seconds (float): Waktu dalam detik
        
    Returns:
        str: Format HH:MM:SS,mmm
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def save_to_srt(video_result, output_path):
    """
    Simpan hasil OCR video ke format SRT (SubRip Subtitle)
    Setiap subtitle ditampilkan dari kemunculan pertama hingga subtitle berikutnya muncul
    
    Args:
        video_result (dict): Hasil OCR video
        output_path (str): Path file output .srt
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        if not video_result.get('frames'):
            f.write("# Tidak ada teks yang terdeteksi\n")
            return
        
        frames = video_result['frames']
        
        for idx, frame_data in enumerate(frames, 1):
            # Nomor subtitle
            f.write(f"{idx}\n")
            
            # Timestamp start: dari kemunculan pertama
            start_time = float(frame_data['timestamp'])
            
            # Timestamp end: sampai subtitle berikutnya muncul, atau +2 detik jika ini subtitle terakhir
            if idx < len(frames):
                # Ada subtitle berikutnya, gunakan timestamp subtitle berikutnya
                end_time = float(frames[idx]['timestamp'])
            else:
                # Subtitle terakhir, tampilkan selama 2 detik
                end_time = start_time + 2.0
            
            f.write(f"{format_srt_timestamp(start_time)} --> {format_srt_timestamp(end_time)}\n")
            
            # Tulis hanya Chinese text (tanpa pinyin)
            # Pinyin akan ditambahkan nanti saat convert dengan program 2
            chinese_text = frame_data.get('chinese_text', '').strip()
            latin_text = frame_data.get('latin_text', '').strip()
            
            # Gabungkan Chinese dan Latin jika ada keduanya
            if chinese_text and latin_text:
                f.write(f"{chinese_text} {latin_text}\n")
            elif chinese_text:
                f.write(f"{chinese_text}\n")
            elif latin_text:
                f.write(f"{latin_text}\n")
            
            # Baris kosong pemisah
            f.write("\n")
