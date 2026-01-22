#!/usr/bin/env python3
"""
Aplikasi CLI untuk konversi Mandarin ke Pinyin
Mendukung input: teks, gambar, dan video
"""

import argparse
import sys
import os
from pathlib import Path

# Import modul processor
from src.text_processor import TextProcessor
from src.image_processor import ImageProcessor
from src.video_processor import VideoProcessor
from src.utils import Logger, save_to_file, save_to_srt


def main():
    """Fungsi utama aplikasi CLI"""
    parser = argparse.ArgumentParser(
        description='Konversi tulisan Mandarin ke Pinyin dari teks, gambar, atau video',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python app.py --text "你好世界"
  python app.py --input gambar.jpg
  python app.py --input video.mp4
  python app.py --input gambar.jpg --output hasil.txt
        """
    )
    
    # Argumen untuk input
    parser.add_argument('--text', type=str, help='Input teks Mandarin langsung')
    parser.add_argument('--input', type=str, help='Path ke file gambar atau video')
    parser.add_argument('--output', type=str, help='Simpan hasil ke file (opsional)')
    parser.add_argument('--interval', type=int, default=30, 
                       help='Interval frame untuk ekstraksi video (default: 30)')
    parser.add_argument('--verbose', action='store_true', 
                       help='Tampilkan log detail proses')
    
    args = parser.parse_args()
    
    # Inisialisasi logger
    logger = Logger(verbose=args.verbose)
    
    # Validasi input
    if not args.text and not args.input:
        parser.print_help()
        sys.exit(1)
    
    results = []
    
    try:
        # Proses input teks
        if args.text:
            logger.info("=== Memproses Input Teks ===")
            text_processor = TextProcessor(logger)
            result = text_processor.process(args.text)
            results.append(result)
            print_result(result)
        
        # Proses input file
        if args.input:
            input_path = Path(args.input)
            
            # Validasi file exists
            if not input_path.exists():
                logger.error(f"File tidak ditemukan: {args.input}")
                sys.exit(1)
            
            # Deteksi tipe file
            file_extension = input_path.suffix.lower()
            
            # Proses gambar
            if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']:
                logger.info(f"=== Memproses Gambar: {input_path.name} ===")
                image_processor = ImageProcessor(logger)
                result = image_processor.process(str(input_path))
                results.append(result)
                print_result(result)
            
            # Proses video
            elif file_extension in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']:
                logger.info(f"=== Memproses Video: {input_path.name} ===")
                video_processor = VideoProcessor(logger, frame_interval=args.interval)
                result = video_processor.process(str(input_path))
                results.append(result)
                print_video_result(result)
                
                # Auto-generate SRT file untuk video
                if result.get('frames'):
                    srt_filename = input_path.stem + '_subtitle.srt'
                    srt_path = input_path.parent / srt_filename
                    logger.info(f"\n=== Membuat File Subtitle SRT ===")
                    save_to_srt(result, str(srt_path))
                    logger.success(f"✓ Subtitle SRT disimpan: {srt_filename}")
            
            else:
                logger.error(f"Format file tidak didukung: {file_extension}")
                logger.info("Format yang didukung: JPG, PNG, MP4, AVI, MOV, MKV")
                sys.exit(1)
        
        # Simpan hasil ke file jika diminta
        if args.output and results:
            logger.info(f"\n=== Menyimpan Hasil ke {args.output} ===")
            save_to_file(results, args.output)
            logger.success(f"Hasil berhasil disimpan ke: {args.output}")
        
        logger.success("\n✓ Proses selesai!")
        
    except KeyboardInterrupt:
        logger.warning("\n\nProses dibatalkan oleh user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n✗ Terjadi kesalahan: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def print_result(result):
    """Cetak hasil konversi teks/gambar"""
    print("\n" + "="*60)
    print("HASIL KONVERSI")
    print("="*60)
    
    chinese_text = result.get('chinese_text', '')
    latin_text = result.get('latin_text', '')
    
    if chinese_text or latin_text:
        if chinese_text:
            print(f"\n 📝 Teks Mandarin:")
            print(f"   {chinese_text}")
        
        if latin_text:
            print(f"\n 🔤 Teks Latin:")
            print(f"   {latin_text}")
        
        if chinese_text:
            print(f"\n 🎵 Pinyin:")
            print(f"   {result.get('pinyin', '')}")
    else:
        print("\n⚠️  Tidak ada teks yang terdeteksi")
    
    print("\n" + "="*60)


def print_video_result(result):
    """Cetak hasil konversi video"""
    print("\n" + "="*60)
    print("HASIL KONVERSI VIDEO")
    print("="*60)
    
    if result.get('frames'):
        print(f"\n📹 Total frame diproses: {len(result['frames'])}")
        print(f"⏱️  Durasi video: {result.get('duration', 'N/A')} detik")
        
        for idx, frame_data in enumerate(result['frames'], 1):
            chinese_text = frame_data.get('chinese_text', '')
            latin_text = frame_data.get('latin_text', '')
            
            if chinese_text or latin_text:
                print(f"\n--- Frame #{idx} (Timestamp: {frame_data['timestamp']}s) ---")
                
                if chinese_text:
                    print(f"📝 Chinese: {chinese_text}")
                if latin_text:
                    print(f"🔤 Latin: {latin_text}")
                if chinese_text:
                    print(f"🎵 Pinyin: {frame_data.get('pinyin', '')}")
    else:
        print("\n⚠️  Tidak ada teks yang terdeteksi dalam video")
    
    print("\n" + "="*60)


if __name__ == '__main__':
    main()
