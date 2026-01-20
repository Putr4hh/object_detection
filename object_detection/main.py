import cv2
from ultralytics import YOLO
import os
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class YOLODetector:
    """YOLO Real-time Object Detection"""
    
    def __init__(self, model_path='yolo26n.pt', camera_id=0, conf_threshold=0.5):
        """
        Initialize YOLO detector
        
        Args:
            model_path: Path to YOLO model file
            camera_id: Camera device ID (0 for default)
            conf_threshold: Confidence threshold for detections
        """
        self.model_path = model_path
        self.camera_id = camera_id
        self.conf_threshold = conf_threshold
        self.model = None
        self.camera = None
        self.fps = 0
        self.frame_count = 0
        self.start_time = None
        
        # Initialize
        self._validate_model()
        self._initialize_camera()
        self._load_model()
    
    def _validate_model(self):
        """Validasi model file ada"""
        if not os.path.exists(self.model_path):
            logger.error(f"Model file tidak ditemukan: {self.model_path}")
            exit(1)
        logger.info(f"Model file ditemukan: {self.model_path}")
    
    def _load_model(self):
        """Load YOLO model"""
        try:
            logger.info("Loading YOLO model...")
            self.model = YOLO(self.model_path)
            logger.info(f"Model loaded successfully. Confidence threshold: {self.conf_threshold}")
        except Exception as e:
            logger.error(f"Gagal memuat model: {e}")
            exit(1)
    
    def _initialize_camera(self):
        """Initialize camera"""
        try:
            logger.info(f"Membuka kamera (device ID: {self.camera_id})...")
            self.camera = cv2.VideoCapture(self.camera_id)
            
            if not self.camera.isOpened():
                logger.error("Tidak bisa membuka kamera!")
                exit(1)
            
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1980)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            self.camera.set(cv2.CAP_PROP_FPS, 60)
            
            logger.info("Kamera berhasil dibuka")
        except Exception as e:
            logger.error(f"Error initializing camera: {e}")
            exit(1)
    
    def _update_fps(self):
        """Update FPS counter"""
        if self.start_time is None:
            self.start_time = time.time()
        
        self.frame_count += 1
        elapsed = time.time() - self.start_time
        
        if elapsed >= 1.0:
            self.fps = self.frame_count / elapsed
            logger.info(f"FPS: {self.fps:.2f}")
            self.frame_count = 0
            self.start_time = None
    
    def detect(self, frame):
        """Deteksi objek dalam frame"""
        try:
            results = self.model(frame, verbose=False, conf=self.conf_threshold)
            return results[0]
        except Exception as e:
            logger.error(f"Error during detection: {e}")
            return None
    
    def draw_info(self, frame, result):
        """Draw detection info pada frame"""
        plot_frame = result.plot()
        
        # Draw FPS
        cv2.putText(plot_frame, f"FPS: {self.fps:.2f}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw detection count
        if result.boxes is not None:
            det_count = len(result.boxes)
            cv2.putText(plot_frame, f"Detections: {det_count}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return plot_frame
    
    def run(self):
        """Run detection loop"""
        logger.info("Mulai deteksi. Tekan 'q' untuk keluar, 's' untuk screenshot.")
        
        try:
            while True:
                ret, frame = self.camera.read()
                
                if not ret:
                    logger.error("Gagal membaca frame dari kamera")
                    break
                
                # Deteksi objek
                result = self.detect(frame)
                if result is None:
                    continue
                
                # Update FPS
                self._update_fps()
                
                # Draw info
                display_frame = self.draw_info(frame, result)
                
                # Tampilkan
                cv2.imshow('YOLO Object Detection', display_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    logger.info("User exit requested")
                    break
                elif key == ord('s'):
                    filename = f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
                    cv2.imwrite(filename, display_frame)
                    logger.info(f"Screenshot saved: {filename}")
        
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt detected")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up resources...")
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
        logger.info("Program selesai.")


if __name__ == "__main__":
    # Buat detector
    detector = YOLODetector(
        model_path='yolo26n.pt',
        camera_id=0,
        conf_threshold=0.5
    )
    
    # Jalankan
    detector.run()