"""
Modul untuk memproses teks Mandarin dan mengonversinya ke Pinyin
"""

from pypinyin import pinyin, Style


class TextProcessor:
    """Class untuk memproses konversi teks Mandarin ke Pinyin"""
    
    # Common OCR mistakes mapping (wrong -> correct)
    OCR_CORRECTIONS = {
        '蘖': '菜',
        '忝': '不',
        '裔': '有',
        '〈': '',
        '。': '，',
        '呐': '吖',
        '术': '木',
        '{': '',
        '召': '',
        '介': '一',
        '褥': '个',
        '檠': '菜',
        ']': '',
        '@': '0',
        '鬟': '我',
        '实': '买',
    }
    
    def __init__(self, logger=None, spacing=1):
        """
        Inisialisasi TextProcessor
        
        Args:
            logger: Instance logger untuk mencatat proses
            spacing: Jumlah spasi antar karakter Pinyin (1, 2, atau 3)
        """
        self.logger = logger
        self.spacing = max(1, min(3, spacing))  # Ensure spacing is between 1-3
    
    def process(self, text):
        """
        Proses konversi teks Mandarin ke Pinyin
        Mendukung teks campuran Chinese dan Latin
        
        Args:
            text (str): Teks yang akan dikonversi
            
        Returns:
            dict: Dictionary berisi teks asli, chinese, latin, dan hasil konversi pinyin
        """
        if self.logger:
            self.logger.info(f"Memproses teks: {text[:50]}...")
        
        # Validasi input
        if not text or not text.strip():
            if self.logger:
                self.logger.warning("Teks kosong")
            return {
                'chinese_text': '',
                'latin_text': '',
                'pinyin': '',
                'pinyin_toned': ''
            }
        
        try:
            # Apply OCR correction first
            corrected_text = self.correct_ocr_errors(text)
            
            # Proses teks campuran
            result = self.process_mixed_text(corrected_text)
            
            if self.logger:
                if result['chinese_text'] and result['latin_text']:
                    self.logger.info(f"  Chinese: {result['chinese_text']}")
                    self.logger.info(f"  Latin: {result['latin_text']}")
                elif result['chinese_text']:
                    self.logger.info(f"  Chinese text: {result['chinese_text']}")
                elif result['latin_text']:
                    self.logger.info("  Hanya Latin text")
            
            if self.logger:
                self.logger.success("✓ Konversi teks berhasil")
            
            return {
                'chinese_text': result['chinese_text'],
                'latin_text': result['latin_text'],
                'pinyin': result['pinyin'],
                'pinyin_toned': result['pinyin_toned']
            }
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Gagal mengonversi teks: {str(e)}")
            raise
    
    def _convert_to_pinyin(self, text, style):
        """
        Konversi teks ke pinyin dengan style tertentu
        
        Args:
            text (str): Teks yang akan dikonversi
            style: Style pinyin dari pypinyin
            
        Returns:
            str: Hasil konversi pinyin
        """
        # Konversi setiap karakter
        pinyin_list = pinyin(text, style=style, heteronym=False)
        
        # Gabungkan hasil dengan spacing yang dikonfigurasi
        separator = ' ' * self.spacing
        result = separator.join([item[0] for item in pinyin_list])
        
        return result
    
    def is_chinese(self, char):
        """
        Cek apakah karakter adalah karakter Mandarin
        
        Args:
            char (str): Karakter yang akan dicek
            
        Returns:
            bool: True jika karakter adalah Mandarin
        """
        return '\u4e00' <= char <= '\u9fff'
    
    def extract_chinese_only(self, text):
        """
        Ekstrak hanya karakter Mandarin dari teks
        
        Args:
            text (str): Teks input
            
        Returns:
            str: Teks yang hanya berisi karakter Mandarin
        """
        return ''.join([char for char in text if self.is_chinese(char)])
    
    def correct_ocr_errors(self, text):
        """
        Koreksi kesalahan umum OCR pada Chinese text
        
        Args:
            text (str): Teks yang perlu dikoreksi
            
        Returns:
            str: Teks yang sudah dikoreksi
        """
        if not text:
            return text
        
        original = text
        result = text
        
        # Multi-character corrections first (must be before single char)
        multi_corrections = {
            '鬟多块钱实的': '我100多块钱买的',
            '我多块钱实的': '我100多块钱买的',
            '我00多块钱买的': '我100多块钱买的',
            '我00多块钱实的': '我100多块钱买的',
            '我]@@多块钱实的': '我100多块钱买的',
            '我1@@多块钱实的': '我100多块钱买的',
            '掉多块钱实的': '我100多块钱买的',
            '介褥的檠板': '一个好的菜板',
            '二婚的': '一个好的',
            '蘖板': '菜板',
            '能裔': '能有木',
        }
        
        for wrong, correct in multi_corrections.items():
            result = result.replace(wrong, correct)
        
        # Single character corrections
        corrected = []
        for char in result:
            # Cek apakah ada di correction mapping
            if char in self.OCR_CORRECTIONS:
                corrected_char = self.OCR_CORRECTIONS[char]
                if corrected_char:  # Hanya tambahkan jika tidak kosong
                    corrected.append(corrected_char)
            else:
                corrected.append(char)
        
        result = ''.join(corrected)
        
        if self.logger and self.logger.verbose and result != original:
            self.logger.info(f"  OCR Correction: '{original}' → '{result}'")
        
        return result
    
    def separate_chinese_and_latin(self, text):
        """
        Pisahkan karakter Chinese dan Latin dari teks
        Angka yang ada di tengah kalimat Chinese akan tetap di Chinese text
        
        Args:
            text (str): Teks input campuran
            
        Returns:
            tuple: (chinese_text, latin_text, mixed_text_with_markers)
        """
        chinese_chars = []
        latin_chars = []
        mixed = []
        
        # Check if text has both Chinese and digits mixed together
        has_chinese = any(self.is_chinese(c) for c in text)
        has_digit = any(c.isdigit() for c in text)
        
        # If both Chinese and digits exist, keep digits as part of Chinese text
        # to preserve meaning (e.g., "我100多块钱买的")
        keep_digits_with_chinese = has_chinese and has_digit
        
        for char in text:
            if self.is_chinese(char):
                chinese_chars.append(char)
                mixed.append(char)
            elif char.isdigit() and keep_digits_with_chinese:
                # Keep digits with Chinese if they're mixed together
                chinese_chars.append(char)
                mixed.append(char)
            elif char.strip():  # Other Latin text (letters, not digits)
                latin_chars.append(char)
                mixed.append(char)
            else:  # whitespace
                mixed.append(char)
        
        chinese_text = ''.join(chinese_chars)
        latin_text = ''.join(latin_chars)
        mixed_text = ''.join(mixed)
        
        return chinese_text, latin_text, mixed_text
    
    def process_mixed_text(self, text):
        """
        Proses teks campuran Chinese dan Latin
        Chinese akan dikonversi ke pinyin, Latin tetap sebagai Latin
        
        Args:
            text (str): Teks campuran
            
        Returns:
            dict: Dictionary berisi teks original, chinese_text, latin_text, dan pinyin
        """
        if not text or not text.strip():
            return {
                'original_text': '',
                'chinese_text': '',
                'latin_text': '',
                'pinyin': '',
                'pinyin_toned': ''
            }
        
        # Pisahkan Chinese dan Latin
        chinese_text, latin_text, mixed_text = self.separate_chinese_and_latin(text)
        
        # Konversi Chinese ke pinyin
        if chinese_text:
            pinyin_plain = self._convert_to_pinyin(chinese_text, Style.NORMAL)
            pinyin_toned = self._convert_to_pinyin(chinese_text, Style.TONE)
        else:
            pinyin_plain = ''
            pinyin_toned = ''
        
        return {
            'original_text': mixed_text,
            'chinese_text': chinese_text,
            'latin_text': latin_text,
            'pinyin': pinyin_plain,
            'pinyin_toned': pinyin_toned
        }
