#!/usr/bin/env python3
"""
Aplikasi CLI untuk konversi file SRT Mandarin ke SRT Pinyin
Scan folder dan convert semua file .srt Mandarin ke Pinyin
"""

import argparse
import sys
from pathlib import Path
from src.text_processor import TextProcessor
from src.utils import Logger


def parse_srt_file(srt_path):
    """Parse file SRT dan ekstrak subtitle entries"""
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = []
    blocks = content.strip().split('\n\n')
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            entry = {
                'index': lines[0],
                'timestamp': lines[1],
                'text': '\n'.join(lines[2:])
            }
            entries.append(entry)
    
    return entries


def convert_srt_to_pinyin(input_path, output_path, text_processor, logger):
    """Convert file SRT Mandarin ke Pinyin"""
    logger.info(f"📄 Memproses: {input_path.name}")
    
    # Parse file SRT
    entries = parse_srt_file(input_path)
    
    if not entries:
        logger.warning(f"⚠️  File kosong atau format tidak valid: {input_path.name}")
        return False
    
    # Convert setiap subtitle ke Pinyin
    converted_entries = []
    for entry in entries:
        chinese_text = entry['text']
        result = text_processor.process(chinese_text)
        pinyin_text = result.get('pinyin', chinese_text)
        
        converted_entries.append({
            'index': entry['index'],
            'timestamp': entry['timestamp'],
            'text': pinyin_text
        })
    
    # Tulis file SRT Pinyin
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, entry in enumerate(converted_entries):
            f.write(f"{entry['index']}\n")
            f.write(f"{entry['timestamp']}\n")
            f.write(f"{entry['text']}\n")
            if i < len(converted_entries) - 1:
                f.write("\n")
    
    logger.success(f"✓ Tersimpan: {output_path.name}")
    return True


def main():
    """Fungsi utama untuk convert SRT Mandarin ke Pinyin"""
    parser = argparse.ArgumentParser(
        description='Convert file SRT Mandarin ke SRT Pinyin',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python srt_to_pinyin.py --folder ./subtitles
  python srt_to_pinyin.py --file 1.srt
  python srt_to_pinyin.py --folder ./subtitles --output ./output
  python srt_to_pinyin.py --folder ./subtitles --spacing 2
  python srt_to_pinyin.py --folder ./subtitles --spacing 3 --verbose
        """
    )
    
    parser.add_argument('--folder', type=str, help='Folder berisi file .srt Mandarin')
    parser.add_argument('--file', type=str, help='Convert satu file .srt saja')
    parser.add_argument('--output', type=str, help='Folder output (default: sama dengan input)')
    parser.add_argument('--spacing', type=int, default=1, choices=[1, 2, 3],
                       help='Jumlah spasi antar karakter Pinyin (1, 2, atau 3, default: 1)')
    parser.add_argument('--verbose', action='store_true', help='Tampilkan log detail')
    
    args = parser.parse_args()
    
    # Validasi input
    if not args.folder and not args.file:
        parser.print_help()
        sys.exit(1)
    
    # Inisialisasi
    logger = Logger(verbose=args.verbose)
    text_processor = TextProcessor(logger, spacing=args.spacing)
    
    try:
        # Mode: Convert satu file
        if args.file:
            input_path = Path(args.file)
            if not input_path.exists():
                logger.error(f"File tidak ditemukan: {args.file}")
                sys.exit(1)
            
            if not input_path.suffix.lower() == '.srt':
                logger.error(f"File bukan format .srt: {args.file}")
                sys.exit(1)
            
            # Tentukan output path
            if args.output:
                output_dir = Path(args.output)
                output_dir.mkdir(parents=True, exist_ok=True)
                output_path = output_dir / f"{input_path.stem}(P).srt"
            else:
                output_path = input_path.parent / f"{input_path.stem}(P).srt"
            
            logger.info("=== Convert File SRT ke Pinyin ===\n")
            success = convert_srt_to_pinyin(input_path, output_path, text_processor, logger)
            
            if success:
                logger.success(f"\n✓ Konversi selesai!")
                logger.info(f"📁 Output: {output_path}")
        
        # Mode: Convert semua file dalam folder
        elif args.folder:
            folder_path = Path(args.folder)
            if not folder_path.exists():
                logger.error(f"Folder tidak ditemukan: {args.folder}")
                sys.exit(1)
            
            # Cari semua file .srt (kecuali yang sudah (P).srt)
            srt_files = [f for f in folder_path.glob('*.srt') if not f.stem.endswith('(P)')]
            
            if not srt_files:
                logger.warning(f"Tidak ada file .srt ditemukan di: {args.folder}")
                sys.exit(0)
            
            logger.info(f"=== Convert Batch SRT ke Pinyin ===")
            logger.info(f"📂 Folder: {folder_path}")
            logger.info(f"📊 Ditemukan {len(srt_files)} file SRT\n")
            
            # Tentukan output directory
            if args.output:
                output_dir = Path(args.output)
                output_dir.mkdir(parents=True, exist_ok=True)
            else:
                output_dir = folder_path
            
            # Convert setiap file
            success_count = 0
            for idx, srt_file in enumerate(srt_files, 1):
                logger.info(f"[{idx}/{len(srt_files)}]")
                output_path = output_dir / f"{srt_file.stem}(P).srt"
                if convert_srt_to_pinyin(srt_file, output_path, text_processor, logger):
                    success_count += 1
                print()  # Spasi antar file
            
            logger.success(f"✓ Selesai! {success_count}/{len(srt_files)} file berhasil dikonversi")
            logger.info(f"📁 Lokasi output: {output_dir}")
        
    except KeyboardInterrupt:
        logger.warning("\n\nProses dibatalkan oleh user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n✗ Terjadi kesalahan: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
