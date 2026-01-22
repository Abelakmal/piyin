"""
Modul untuk memproses gambar dengan OCR dan konversi ke Pinyin
"""

import cv2
import numpy as np

# Disable PaddleOCR for Python 3.12 compatibility
PADDLEOCR_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

from .text_processor import TextProcessor


class ImageProcessor:
    """Class untuk memproses gambar dengan OCR dan konversi ke Pinyin"""
    
    def __init__(self, logger=None, ocr_engine='easy'):
        """
        Inisialisasi ImageProcessor
        
        Args:
            logger: Instance logger untuk mencatat proses
            ocr_engine (str): OCR engine to use ('paddle' or 'easy', default: 'paddle')
        """
        self.logger = logger
        self.text_processor = TextProcessor(logger)
        self.ocr_engine = ocr_engine
        self.reader = None
    
    def _initialize_ocr(self):
        """Inisialisasi OCR reader (lazy loading)"""
        if self.reader is None:
            if self.logger:
                self.logger.info(f"Menginisialisasi OCR engine ({self.ocr_engine})...")
            
            if self.ocr_engine == 'paddle' and PADDLEOCR_AVAILABLE:
                # PaddleOCR - lebih akurat untuk Chinese
                self.reader = PaddleOCR(
                    use_angle_cls=True,
                    lang='ch'
                )
                if self.logger:
                    self.logger.success("✓ PaddleOCR engine siap")
            elif self.ocr_engine == 'easy' and EASYOCR_AVAILABLE:
                # EasyOCR - backup option
                self.reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
                if self.logger:
                    self.logger.success("✓ EasyOCR engine siap")
            else:
                # Fallback
                if PADDLEOCR_AVAILABLE:
                    if self.logger:
                        self.logger.warning(f"Engine '{self.ocr_engine}' tidak tersedia, menggunakan PaddleOCR")
                    self.ocr_engine = 'paddle'
                    self.reader = PaddleOCR(use_angle_cls=True, lang='ch')
                elif EASYOCR_AVAILABLE:
                    if self.logger:
                        self.logger.warning(f"Engine '{self.ocr_engine}' tidak tersedia, menggunakan EasyOCR")
                    self.ocr_engine = 'easy'
                    self.reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
                else:
                    raise ImportError("Tidak ada OCR engine yang tersedia. Install paddleocr atau easyocr.")
    
    def process(self, image_path, confidence_threshold=0.1):
        """
        Proses gambar: OCR -> Ekstrak teks -> Konversi ke Pinyin
        Menggunakan PaddleOCR dengan language correction
        
        Args:
            image_path (str): Path ke file gambar
            confidence_threshold (float): Minimum confidence untuk menerima hasil OCR (default: 0.1, rendah untuk PaddleOCR)
            
        Returns:
            dict: Dictionary berisi teks hasil OCR dan pinyin
        """
        if self.logger:
            self.logger.info(f"Membaca gambar: {image_path}")
        
        try:
            # Baca gambar
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Tidak dapat membaca gambar: {image_path}")
            
            if self.logger:
                self.logger.info(f"Dimensi gambar: {image.shape[1]}x{image.shape[0]}")
            
            # Inisialisasi OCR
            self._initialize_ocr()
            
            # Preprocessing untuk meningkatkan akurasi
            if self.logger:
                self.logger.info("Preprocessing gambar untuk meningkatkan akurasi OCR...")
            
            preprocessed_image = self.preprocess_image(image)
            
            # Lakukan OCR dengan multiple attempts
            if self.logger:
                self.logger.info("Melakukan OCR pada gambar...")
            
            # OCR pada gambar original
            if self.logger and self.logger.verbose:
                self.logger.info("  Attempting OCR on original image...")
            
            if self.ocr_engine == 'paddle':
                results_original = self._paddle_readtext(image)
            else:
                results_original = self.reader.readtext(image, detail=1)
            
            # OCR pada gambar preprocessed
            if self.logger and self.logger.verbose:
                self.logger.info("  Attempting OCR on preprocessed image...")
            
            if self.ocr_engine == 'paddle':
                results_preprocessed = self._paddle_readtext(preprocessed_image)
            else:
                results_preprocessed = self.reader.readtext(preprocessed_image, detail=1)
            
            # Gabungkan hasil dan ambil yang terbaik berdasarkan confidence
            all_results = {}
            
            for (bbox, text, prob) in results_original:
                if self.logger and self.logger.verbose:
                    self.logger.info(f"  [Original] '{text}' (confidence: {prob:.2f})")
                if prob >= confidence_threshold:
                    # Use text as key to avoid duplicates of same text
                    text_key = text.strip()
                    if text_key not in all_results or prob > all_results[text_key][1]:
                        all_results[text_key] = (bbox, prob)
            
            for (bbox, text, prob) in results_preprocessed:
                if self.logger and self.logger.verbose:
                    self.logger.info(f"  [Preprocessed] '{text}' (confidence: {prob:.2f})")
                if prob >= confidence_threshold:
                    text_key = text.strip()
                    # Only add if this text doesn't exist or has higher confidence
                    if text_key not in all_results or prob > all_results[text_key][1]:
                        all_results[text_key] = (bbox, prob)
            
            # Jika tidak ada hasil dengan confidence threshold, coba ambil semua dari original
            if not all_results and results_original:
                if self.logger:
                    self.logger.info("  No high-confidence results, using all results from original image...")
                for (bbox, text, prob) in results_original:
                    text_key = text.strip()
                    if text_key not in all_results:
                        all_results[text_key] = (bbox, prob)
            
            # Ekstrak teks yang sudah deduplicated
            detected_texts = []
            for text_key, (bbox, prob) in all_results.items():
                if self.logger and self.logger.verbose:
                    self.logger.info(f"  Selected: '{text_key}' (confidence: {prob:.2f})")
                detected_texts.append(text_key)
            
            # Gabungkan semua teks yang terdeteksi
            full_text = ''.join(detected_texts)  # Tanpa spasi untuk Chinese
            
            if not full_text.strip():
                if self.logger:
                    self.logger.warning("Tidak ada teks yang terdeteksi dalam gambar")
                return {
                    'chinese_text': '',
                    'latin_text': '',
                    'pinyin': '',
                    'pinyin_toned': '',
                    'ocr_results': []
                }
            
            if self.logger:
                self.logger.success(f"✓ OCR selesai, terdeteksi {len(detected_texts)} teks")
            
            # Konversi ke pinyin
            if self.logger:
                self.logger.info("Mengonversi hasil OCR ke pinyin...")
            
            pinyin_result = self.text_processor.process(full_text)
            pinyin_result['ocr_results'] = list(all_results.values()) if all_results else []
            
            return pinyin_result
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Gagal memproses gambar: {str(e)}")
            raise
    
    def preprocess_image(self, image):
        """
        Preprocessing gambar untuk meningkatkan akurasi OCR
        Menggunakan gentle preprocessing yang tidak terlalu agresif
        
        Args:
            image: OpenCV image object
            
        Returns:
            Preprocessed image
        """
        # Resize jika terlalu kecil (OCR lebih baik pada gambar besar)
        height, width = image.shape[:2]
        if width < 1200 or height < 200:
            # Scale up untuk teks kecil
            scale = max(1200 / width, 200 / height, 2.0)  # Min scale 2x
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
            if self.logger and self.logger.verbose:
                self.logger.info(f"  Resized image to {new_width}x{new_height} (scale: {scale:.1f}x)")
        
        # Convert ke grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Increase contrast using CLAHE (lebih gentle)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Light denoising only
        denoised = cv2.fastNlMeansDenoising(enhanced, h=7)
        
        return denoised  # Return grayscale dengan enhancement, tanpa threshold
    
    def _paddle_readtext(self, image):
        """
        Wrapper untuk PaddleOCR yang mengembalikan format yang sama dengan EasyOCR
        
        Args:
            image: OpenCV image (BGR atau Grayscale)
            
        Returns:
            list: [(bbox, text, confidence), ...]
        """
        try:
            # PaddleOCR expects RGB
            if len(image.shape) == 2:  # Grayscale
                image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            else:  # BGR
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Call ocr
            result = self.reader.ocr(image_rgb)
            
            # Convert PaddleOCR format to EasyOCR-like format
            formatted_results = []
            if result and len(result) > 0 and result[0]:
                for line in result[0]:
                    if line and len(line) >= 2:
                        bbox = line[0]  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                        if len(line[1]) >= 2:
                            text = line[1][0]  # text
                            confidence = line[1][1]  # confidence score
                            formatted_results.append((bbox, text, confidence))
            
            # Debug logging
            if self.logger and self.logger.verbose:
                self.logger.info(f"  PaddleOCR raw results: {len(formatted_results)} items")
                for bbox, text, conf in formatted_results:
                    self.logger.info(f"    '{text}' (conf: {conf:.2f})")
            
            return formatted_results
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error in _paddle_readtext: {str(e)}")
            return []
