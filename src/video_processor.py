"""
Modul untuk memproses video dengan OCR dan konversi ke Pinyin
"""

import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from difflib import SequenceMatcher
from .image_processor import ImageProcessor
from .text_processor import TextProcessor


class VideoProcessor:
    """Class untuk memproses video dengan OCR dan konversi ke Pinyin"""
    
    def __init__(self, logger=None, max_workers=2, bottom_only=True, bottom_ratio=0.3, similarity_threshold=0.65, frame_interval=5):
        """
        Inisialisasi VideoProcessor
        
        Args:
            logger: Instance logger untuk mencatat proses
            max_workers (int): Jumlah thread untuk parallel processing (default: 2)
            bottom_only (bool): Hanya proses bagian bawah frame untuk subtitle (default: True)
            bottom_ratio (float): Rasio bagian bawah yang diproses (default: 0.3 = 30%)
            similarity_threshold (float): Threshold untuk mendeteksi teks duplikat (default: 0.65 = 65% sama)
            frame_interval (int): Interval frame untuk diproses (default: 5 = ~6x per detik, tangkap subtitle cepat)
        """
        self.logger = logger
        self.image_processor = ImageProcessor(logger)
        self.text_processor = TextProcessor(logger)
        self.max_workers = max_workers
        self.resize_width = 1280  # Resize frame untuk mempercepat OCR
        self.bottom_only = bottom_only  # Fokus hanya bagian bawah
        self.bottom_ratio = bottom_ratio  # Berapa persen dari bawah (0.3 = 30%)
        self.similarity_threshold = similarity_threshold  # Threshold untuk deduplikasi
        self.frame_interval = frame_interval  # Interval frame
        self.last_text = ""  # Menyimpan teks terakhir untuk perbandingan
        self.last_timestamp = 0  # Timestamp teks terakhir
    
    def process(self, video_path, enable_parallel=True):
        """
        Proses video: Ekstrak frame -> OCR -> Konversi ke Pinyin
        
        Args:
            video_path (str): Path ke file video
            enable_parallel (bool): Gunakan parallel processing (default: True)
            
        Returns:
            dict: Dictionary berisi hasil OCR dan pinyin dari setiap frame
        """
        if self.logger:
            self.logger.info(f"Membuka video: {video_path}")
        
        try:
            # Buka video
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise ValueError(f"Tidak dapat membuka video: {video_path}")
            
            # Info video
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            
            if self.logger:
                self.logger.info(f"FPS: {fps:.2f}, Total frame: {frame_count}, Durasi: {duration:.2f}s")
                self.logger.info(f"Memproses setiap frame ke-{self.frame_interval}")
            
            results = []
            frame_number = 0
            processed_count = 0
            
            # Inisialisasi OCR sekali saja
            self.image_processor._initialize_ocr()
            
            # Batch processing untuk parallel execution
            if enable_parallel:
                frames_to_process = []
                
                while True:
                    ret, frame = cap.read()
                    
                    if not ret:
                        break
                    
                    # Kumpulkan frame pada interval tertentu
                    if frame_number % self.frame_interval == 0:
                        timestamp = frame_number / fps if fps > 0 else 0
                        frames_to_process.append((frame.copy(), frame_number, timestamp))
                    
                    frame_number += 1
                
                cap.release()
                
                # Proses frame secara parallel
                if self.logger:
                    self.logger.info(f"Memproses {len(frames_to_process)} frame secara parallel...")
                
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = [executor.submit(self._process_frame, frame, fn, ts) 
                              for frame, fn, ts in frames_to_process]
                    
                    for i, future in enumerate(futures):
                        frame_result = future.result()
                        
                        if frame_result and (frame_result.get('chinese_text') or frame_result.get('latin_text')):
                            # Gabungkan chinese dan latin untuk comparison
                            current_text = frame_result.get('chinese_text', '') + frame_result.get('latin_text', '')
                            
                            # Cek similarity dengan teks sebelumnya
                            if self._is_duplicate_text(current_text):
                                if self.logger and self.logger.verbose:
                                    self.logger.info(f"  - Frame #{frame_result['frame_number']}: Teks duplikat, dilewati")
                                continue
                            
                            # Teks baru yang berbeda, simpan
                            results.append(frame_result)
                            processed_count += 1
                            self.last_text = current_text
                            self.last_timestamp = frames_to_process[i][2]
                            
                            if self.logger:
                                self.logger.success(f"  ✓ Frame #{frame_result['frame_number']}: {frame_result['chinese_text'][:50]}...")
                        else:
                            if self.logger and self.logger.verbose:
                                self.logger.info(f"  - Frame #{frames_to_process[i][1]}: Tidak ada teks terdeteksi")
            else:
                # Sequential processing (mode lama)
                while True:
                    ret, frame = cap.read()
                    
                    if not ret:
                        break
                    
                    # Proses frame pada interval tertentu
                    if frame_number % self.frame_interval == 0:
                        timestamp = frame_number / fps if fps > 0 else 0
                        
                        if self.logger:
                            self.logger.info(f"\nMemproses frame #{frame_number} (t={timestamp:.2f}s)")
                        
                        # Lakukan OCR pada frame
                        frame_result = self._process_frame(frame, frame_number, timestamp)
                        
                        if frame_result and (frame_result.get('chinese_text') or frame_result.get('latin_text')):
                            # Gabungkan chinese dan latin untuk comparison
                            current_text = frame_result.get('chinese_text', '') + frame_result.get('latin_text', '')
                            
                            # Cek similarity dengan teks sebelumnya
                            if self._is_duplicate_text(current_text):
                                if self.logger and self.logger.verbose:
                                    self.logger.info("  - Teks duplikat, dilewati")
                                continue
                            
                            # Teks baru yang berbeda, simpan
                            results.append(frame_result)
                            processed_count += 1
                            self.last_text = current_text
                            self.last_timestamp = timestamp
                            
                            if self.logger:
                                self.logger.success(f"  ✓ Teks terdeteksi: {frame_result['chinese_text'][:50]}...")
                        else:
                            if self.logger and self.logger.verbose:
                                self.logger.info("  - Tidak ada teks Mandarin terdeteksi")
                    
                    frame_number += 1
                
                cap.release()
            
            if self.logger:
                self.logger.success(f"\n✓ Selesai memproses video")
                self.logger.info(f"Total frame diproses: {processed_count}/{frame_count//self.frame_interval}")
            
            return {
                'frames': results,
                'video_info': {
                    'fps': fps,
                    'frame_count': frame_count,
                    'duration': duration,
                    'processed_frames': processed_count
                },
                'duration': duration
            }
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Gagal memproses video: {str(e)}")
            raise
    
    def _process_frame(self, frame, frame_number, timestamp):
        """
        Proses satu frame video dengan dual OCR (original + preprocessed) dan error correction
        
        Args:
            frame: OpenCV frame object
            frame_number (int): Nomor frame
            timestamp (float): Timestamp dalam detik
            
        Returns:
            dict: Hasil OCR dan konversi pinyin
        """
        try:
            # Preprocessing frame untuk mempercepat OCR
            processed_frame = self._preprocess_frame(frame)
            
            # Skip frame jika terlalu gelap atau kosong
            if self._is_blank_frame(frame):
                return None
            
            # Lakukan OCR pada frame original dan preprocessed untuk akurasi maksimal
            confidence_threshold = 0.1
            
            # OCR pada frame original (setelah bottom crop dan resize)
            # Apply bottom crop dan resize ke original frame
            original_frame = self._crop_and_resize_frame(frame)
            
            if self.logger and self.logger.verbose:
                self.logger.info(f"    Attempting OCR on original frame...")
            
            results_original = self.image_processor.reader.readtext(original_frame, detail=1)
            
            # OCR pada frame preprocessed
            if self.logger and self.logger.verbose:
                self.logger.info(f"    Attempting OCR on preprocessed frame...")
            
            results_preprocessed = self.image_processor.reader.readtext(processed_frame, detail=1)
            
            # Gabungkan hasil dengan text-based deduplication
            all_results = {}
            
            for (bbox, text, prob) in results_original:
                if self.logger and self.logger.verbose:
                    self.logger.info(f"    [Original] '{text}' (confidence: {prob:.2f})")
                if prob >= confidence_threshold:
                    text_key = text.strip()
                    if text_key not in all_results or prob > all_results[text_key][1]:
                        all_results[text_key] = (bbox, prob)
            
            for (bbox, text, prob) in results_preprocessed:
                if self.logger and self.logger.verbose:
                    self.logger.info(f"    [Preprocessed] '{text}' (confidence: {prob:.2f})")
                if prob >= confidence_threshold:
                    text_key = text.strip()
                    if text_key not in all_results or prob > all_results[text_key][1]:
                        all_results[text_key] = (bbox, prob)
            
            # Jika tidak ada hasil, gunakan semua dari original dengan confidence rendah
            if not all_results and results_original:
                if self.logger and self.logger.verbose:
                    self.logger.info("    No high-confidence results, using all results from original frame...")
                for (bbox, text, prob) in results_original:
                    text_key = text.strip()
                    if text_key not in all_results:
                        all_results[text_key] = (bbox, prob)
            
            # Ekstrak teks yang sudah deduplicated
            detected_texts = []
            for text_key, (bbox, prob) in all_results.items():
                if self.logger and self.logger.verbose:
                    self.logger.info(f"    Selected: '{text_key}' (confidence: {prob:.2f})")
                detected_texts.append(text_key)
            
            # Gabungkan teks tanpa spasi untuk Chinese
            full_text = ''.join(detected_texts)
            
            if not full_text.strip():
                return None
            
            # Apply OCR error correction
            corrected_text = self.text_processor.correct_ocr_errors(full_text)
            
            if self.logger and self.logger.verbose and corrected_text != full_text:
                self.logger.info(f"    OCR correction: '{full_text}' -> '{corrected_text}'")
            
            # Bersihkan karakter aneh/simbol yang bukan Chinese atau Latin valid
            cleaned_text = self._clean_text(corrected_text)
            
            if not cleaned_text.strip():
                return None
            
            # Konversi ke pinyin dengan Chinese/Latin separation
            pinyin_result = self.text_processor.process(cleaned_text)
            
            # Tambahkan metadata
            pinyin_result['frame_number'] = frame_number
            pinyin_result['timestamp'] = f"{timestamp:.2f}"
            
            return pinyin_result
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error memproses frame {frame_number}: {str(e)}")
            return None
    
    def _preprocess_frame(self, frame):
        """
        Preprocessing frame untuk meningkatkan akurasi OCR
        
        Args:
            frame: OpenCV frame object
            
        Returns:
            frame: Preprocessed frame
        """
        # Jika bottom_only aktif, crop hanya bagian bawah
        if self.bottom_only:
            height, width = frame.shape[:2]
            # Hitung posisi mulai crop dari atas (misalnya 70% dari atas jika bottom_ratio=0.3)
            start_y = int(height * (1 - self.bottom_ratio))
            # Crop hanya bagian bawah
            frame = frame[start_y:height, 0:width]
            
            if self.logger and self.logger.verbose:
                self.logger.info(f"    Cropping frame: bagian bawah {self.bottom_ratio*100:.0f}% (dari y={start_y})")
        
        # Resize frame jika terlalu kecil (OCR lebih baik pada gambar cukup besar)
        height, width = frame.shape[:2]
        if width < 800:
            scale = 800 / width
            new_width = 800
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        elif width > self.resize_width:
            # Resize jika terlalu besar
            scale = self.resize_width / width
            new_height = int(height * scale)
            frame = cv2.resize(frame, (self.resize_width, new_height), interpolation=cv2.INTER_AREA)
        
        # Convert ke grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Increase contrast using CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(enhanced, h=10)
        
        # Sharpen untuk meningkatkan edge detection
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        sharpened = cv2.filter2D(denoised, -1, kernel)
        
        # Adaptive threshold
        processed = cv2.adaptiveThreshold(
            sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        return processed
    
    def _crop_and_resize_frame(self, frame):
        """
        Crop dan resize frame tanpa preprocessing agresif (untuk OCR pada original)
        
        Args:
            frame: OpenCV frame object
            
        Returns:
            frame: Cropped and resized frame
        """
        # Jika bottom_only aktif, crop hanya bagian bawah
        if self.bottom_only:
            height, width = frame.shape[:2]
            start_y = int(height * (1 - self.bottom_ratio))
            frame = frame[start_y:height, 0:width]
        
        # Resize frame jika terlalu kecil atau terlalu besar
        height, width = frame.shape[:2]
        if width < 800:
            scale = 800 / width
            new_width = 800
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        elif width > self.resize_width:
            scale = self.resize_width / width
            new_height = int(height * scale)
            frame = cv2.resize(frame, (self.resize_width, new_height), interpolation=cv2.INTER_AREA)
        
        return frame
    
    def _is_blank_frame(self, frame, threshold=10):
        """
        Deteksi apakah frame kosong/gelap
        
        Args:
            frame: OpenCV frame object
            threshold: Threshold untuk mendeteksi frame blank
            
        Returns:
            bool: True jika frame kosong
        """
        # Konversi ke grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Hitung mean brightness
        mean_brightness = np.mean(gray)
        
        # Frame terlalu gelap
        if mean_brightness < threshold:
            return True
        
        # Hitung variance untuk deteksi uniformity
        variance = np.var(gray)
        
        # Frame terlalu uniform (kemungkinan blank)
        if variance < 100:
            return True
        
        return False
    
    def _clean_text(self, text):
        """
        Bersihkan teks dari karakter aneh/simbol yang bukan Chinese atau Latin valid
        
        Args:
            text (str): Teks input
            
        Returns:
            str: Teks yang sudah dibersihkan
        """
        cleaned = []
        for char in text:
            # Terima: Chinese, Latin (a-zA-Z), angka (0-9), spasi
            if self.text_processor.is_chinese(char) or char.isalnum() or char.isspace():
                cleaned.append(char)
            # Abaikan karakter lain seperti {, }, [, ], (, ), dll
        
        return ''.join(cleaned)
    
    def _is_duplicate_text(self, current_text):
        """
        Cek apakah teks saat ini adalah duplikat dari teks sebelumnya
        Hanya membandingkan Chinese text untuk menghindari noise dari OCR error
        
        Args:
            current_text (str): Teks yang baru terdeteksi
            
        Returns:
            bool: True jika teks adalah duplikat (similarity tinggi)
        """
        if not self.last_text:
            return False
        
        # Ekstrak hanya Chinese text untuk perbandingan (lebih akurat)
        current_chinese = self.text_processor.extract_chinese_only(current_text)
        last_chinese = self.text_processor.extract_chinese_only(self.last_text)
        
        if not current_chinese or not last_chinese:
            # Jika salah satu tidak ada Chinese, bandingkan full text
            similarity = SequenceMatcher(None, current_text, self.last_text).ratio()
        else:
            # Bandingkan hanya Chinese text
            similarity = SequenceMatcher(None, current_chinese, last_chinese).ratio()
        
        if self.logger and self.logger.verbose:
            self.logger.info(f"    Similarity: {similarity:.2f} (threshold: {self.similarity_threshold})")
        
        # Jika similarity >= threshold, anggap duplikat
        return similarity >= self.similarity_threshold
    
    def extract_frame_at_time(self, video_path, timestamp):
        """
        Ekstrak frame pada timestamp tertentu
        
        Args:
            video_path (str): Path ke file video
            timestamp (float): Timestamp dalam detik
            
        Returns:
            frame: OpenCV frame object
        """
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Set posisi frame
        frame_number = int(timestamp * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        ret, frame = cap.read()
        cap.release()
        
        return frame if ret else None
