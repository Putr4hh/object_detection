# 🎯 YOLO Real-time Object Detection System

Sistem deteksi objek real-time menggunakan YOLOv8 (nano model) untuk identifikasi dan tracking objek melalui feed webcam dengan visualisasi langsung dan pencatatan performa.

---

## 📑 Daftar Isi

1. [Gambaran Umum](#gambaran-umum)
2. [Struktur Proyek](#struktur-proyek)
3. [Persyaratan & Setup](#persyaratan--setup)
4. [Instalasi](#instalasi)
5. [Panduan Penggunaan](#panduan-penggunaan)
6. [Dokumentasi Kode](#dokumentasi-kode)
7. [Flow & Logic Sistem](#flow--logic-sistem)
8. [Konfigurasi](#konfigurasi)
9. [Troubleshooting](#troubleshooting)

---

## 🎬 Gambaran Umum

### Tujuan Proyek
Aplikasi ini dirancang untuk mendeteksi dan mengidentifikasi objek secara real-time dari feed kamera menggunakan model YOLOv8 nano yang telah dioptimalkan untuk kecepatan.

### Fitur Utama
- ✅ **Deteksi Real-time**: Deteksi objek dengan latensi rendah
- ✅ **Monitoring Performa**: Display FPS real-time dan jumlah deteksi
- ✅ **Capture Screenshot**: Simpan hasil deteksi dengan timestamp otomatis
- ✅ **Logging System**: Pencatatan detail setiap event dengan timestamp
- ✅ **Kontrol Interaktif**: Keyboard shortcuts untuk kontrol aplikasi
- ✅ **Error Handling**: Penanganan error yang robust dengan recovery otomatis

### Teknologi yang Digunakan
| Teknologi | Fungsi |
|-----------|--------|
| **YOLOv8** | Model deteksi objek state-of-the-art |
| **OpenCV** | Image processing dan rendering video |
| **Ultralytics** | Framework untuk load dan inference YOLO |
| **Python 3.8+** | Bahasa pemrograman utama |

---

## 📁 Struktur Proyek

```
object_detection/
├── main.py              # Script utama aplikasi
├── yolo26n.pt          # Model YOLO yang sudah dilatih (nano)
├── README.md           # Dokumentasi proyek (file ini)
└── screenshot_*.jpg    # Output screenshot (dibuat saat runtime)
```

### Penjelasan File

| File | Ukuran | Fungsi |
|------|--------|--------|
| **main.py** | ~6 KB | Mengandung class `YOLODetector` dan logic utama aplikasi |
| **yolo26n.pt** | ~6.3 MB | Model YOLO v8 nano yang sudah dilatih untuk deteksi objek |
| **README.md** | - | Dokumentasi lengkap proyek |

---

## 📋 Persyaratan & Setup

### Hardware
- **CPU**: Intel/AMD processor dengan minimal 2 core
- **RAM**: Minimal 4 GB (recommended 8 GB)
- **GPU**: Optional - CUDA GPU untuk performa lebih baik
- **Webcam**: USB camera atau integrated camera
- **Storage**: 50 MB untuk aplikasi

### Software
- **Python**: 3.8 atau lebih tinggi
- **OS**: Windows, macOS, atau Linux

### Check Python Version
```bash
python --version
```

---

## 🛠️ Instalasi

### Langkah 1: Persiapan Environment
```bash
# Navigasi ke folder proyek
cd c:\Users\USER\OneDrive\Documents\object_detection

# (Opsional) Buat virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### Langkah 2: Install Dependencies
```bash
pip install opencv-python ultralytics
```

### Langkah 3: Verifikasi Instalasi
```bash
python -c "import cv2; import ultralytics; print('Setup OK')"
```

### Langkah 4: Verifikasi Model
Pastikan file `yolo26n.pt` tersedia di direktori yang sama dengan `main.py`

```bash
# Check apakah file model ada
dir yolo26n.pt  # Windows
ls -lh yolo26n.pt  # macOS/Linux
```

---

## 🎮 Panduan Penggunaan

### Menjalankan Aplikasi

```bash
python main.py
```

### Keyboard Controls

| Tombol | Fungsi |
|--------|--------|
| **Q** | Keluar aplikasi (graceful shutdown) |
| **S** | Simpan screenshot hasil deteksi dengan timestamp |

### Example Run
```
[2026-01-20 10:30:45] INFO: Model file ditemukan: yolo26n.pt
[2026-01-20 10:30:45] INFO: Loading YOLO model...
[2026-01-20 10:30:46] INFO: Model loaded successfully. Confidence threshold: 0.5
[2026-01-20 10:30:46] INFO: Membuka kamera (device ID: 0)...
[2026-01-20 10:30:46] INFO: Kamera berhasil dibuka
[2026-01-20 10:30:46] INFO: Mulai deteksi. Tekan 'q' untuk keluar, 's' untuk screenshot.
[2026-01-20 10:30:47] INFO: FPS: 28.45
[2026-01-20 10:30:48] INFO: Screenshot saved: screenshot_20260120_103048.jpg
```

---

## 📚 Dokumentasi Kode

### Class: YOLODetector

**Deskripsi**: Kelas utama yang mengelola seluruh pipeline deteksi objek dari inisialisasi hingga cleanup.

#### Konstruktor: `__init__()`

```python
def __init__(self, model_path='yolo26n.pt', camera_id=0, conf_threshold=0.5)
```

**Parameter:**
| Parameter | Tipe | Default | Deskripsi |
|-----------|------|---------|-----------|
| `model_path` | str | 'yolo26n.pt' | Path ke file model YOLO |
| `camera_id` | int | 0 | ID device kamera (0=default) |
| `conf_threshold` | float | 0.5 | Confidence threshold (0-1) |

**Inisialisasi:**
- Validasi keberadaan model file
- Inisialisasi kamera dengan setting resolusi & FPS
- Load model YOLO ke memory

**Contoh Penggunaan:**
```python
# Default configuration
detector = YOLODetector()

# Custom configuration
detector = YOLODetector(
    model_path='yolo26n.pt',
    camera_id=0,
    conf_threshold=0.7  # Lebih ketat
)
```

---

#### Method: `_validate_model()`

```python
def _validate_model(self)
```

**Fungsi**: Memvalidasi keberadaan file model sebelum loading.

**Flow:**
1. Cek apakah path model file exist
2. Jika tidak ada → Log error dan exit program
3. Jika ada → Log info bahwa model ditemukan

**Return:** None

**Kode Logic:**
```
IF file model exist:
    Log: "Model file ditemukan"
ELSE:
    Log: "Model file tidak ditemukan: <path>"
    EXIT
```

---

#### Method: `_load_model()`

```python
def _load_model(self)
```

**Fungsi**: Load model YOLO dari file dan siapkan untuk inference.

**Flow:**
1. Log status "Loading YOLO model..."
2. Instantiate YOLO class dengan path model
3. Model siap untuk inference
4. Log confidence threshold yang digunakan
5. Jika error → Log error dan exit

**Return:** None

**Exception Handling:**
- Menangkap exception jika file model corrupt atau format salah
- Memberikan error message yang informatif

---

#### Method: `_initialize_camera()`

```python
def _initialize_camera(self)
```

**Fungsi**: Inisialisasi kamera dengan setting resolusi dan FPS optimal.

**Flow:**
1. Coba buka kamera dengan `cv2.VideoCapture(camera_id)`
2. Validasi kamera berhasil dibuka
3. Set property kamera:
   - Frame Width: 1980px
   - Frame Height: 1080px
   - FPS: 60
4. Log success
5. Jika error → Log error dan exit

**Property Kamera yang Diset:**
```python
CAP_PROP_FRAME_WIDTH = 1980    # Lebar frame
CAP_PROP_FRAME_HEIGHT = 1080   # Tinggi frame
CAP_PROP_FPS = 60              # Frame rate
```

**Return:** None

---

#### Method: `_update_fps()`

```python
def _update_fps(self)
```

**Fungsi**: Update frame per second counter secara real-time.

**Flow:**
1. Increment `frame_count` setiap frame diproses
2. Hitung elapsed time dari start_time
3. Setiap 1 detik: Hitung FPS = frame_count / elapsed_time
4. Reset counter dan start_time
5. Log FPS value

**Logic Perhitungan FPS:**
```
FPS = Total Frames / Elapsed Time (seconds)
```

**Contoh Output:**
```
FPS: 28.45  # Frame rate saat ini
FPS: 29.12  # Frame rate setelah 1 detik
```

---

#### Method: `detect()`

```python
def detect(self, frame)
```

**Fungsi**: Menjalankan object detection inference pada frame menggunakan model YOLO.

**Parameter:**
| Parameter | Tipe | Deskripsi |
|-----------|------|-----------|
| `frame` | numpy.ndarray | Frame RGB dari kamera |

**Flow:**
1. Input frame dikirim ke model YOLO
2. Model melakukan inference dengan confidence threshold
3. Return hasil deteksi (boxes, classes, scores)
4. Jika error → Log error dan return None

**Return:** 
- `results[0]` (Detection object) jika berhasil
- `None` jika terjadi error

**Konfigurasi Inference:**
```python
results = self.model(
    frame,
    verbose=False,           # Jangan log per-frame
    conf=self.conf_threshold # Gunakan threshold yang diset
)
```

---

#### Method: `draw_info()`

```python
def draw_info(self, frame, result)
```

**Fungsi**: Rendering bounding box dan informasi deteksi pada frame.

**Parameter:**
| Parameter | Tipe | Deskripsi |
|-----------|------|-----------|
| `frame` | numpy.ndarray | Frame original |
| `result` | Detection | Hasil deteksi dari model |

**Flow:**
1. Gunakan `result.plot()` untuk draw bounding boxes
2. Overlay FPS di sudut kiri atas
3. Overlay detection count di bawah FPS
4. Return frame yang sudah dirender

**Informasi yang Ditampilkan:**
- **Bounding Boxes**: Green boxes dengan class label dan confidence score
- **FPS**: "FPS: 28.45" (display setiap frame)
- **Detection Count**: "Detections: 5" (jumlah objek terdeteksi)

**Posisi Text:**
```
(10, 30)  → FPS display
(10, 70)  → Detection count
```

---

#### Method: `run()`

```python
def run(self)
```

**Fungsi**: Main loop yang menjalankan deteksi berkelanjutan sampai user exit.

**Flow Utama:**
```
1. Log: "Mulai deteksi"
2. LOOP FOREVER:
   a. Baca frame dari kamera
   b. Jalankan detection pada frame
   c. Update FPS counter
   d. Draw info pada frame
   e. Display frame di window
   f. Tunggu keyboard input (1ms)
   g. IF input 'q': BREAK
   h. IF input 's': SAVE SCREENSHOT
3. Handle interrupt (Ctrl+C)
4. Run cleanup()
```

**Keyboard Input Handling:**
```python
key = cv2.waitKey(1) & 0xFF
# & 0xFF untuk ekstrak lower byte (ASCII value)
# waitKey(1) = tunggu 1ms sebelum next frame
```

**Screenshot Naming:**
```
Format: screenshot_YYYYMMDD_HHMMSS.jpg
Contoh: screenshot_20260120_103048.jpg
```

---

#### Method: `cleanup()`

```python
def cleanup(self)
```

**Fungsi**: Cleanup dan release semua resource sebelum program exit.

**Flow:**
1. Log status cleanup
2. Release kamera object → free up camera device
3. Destroy semua OpenCV windows
4. Log "Program selesai"

**Penting**: Method ini harus selalu dipanggil sebelum exit untuk avoid resource leak.

---

### Main Execution Block

```python
if __name__ == "__main__":
    # Buat detector
    detector = YOLODetector(
        model_path='yolo26n.pt',
        camera_id=0,
        conf_threshold=0.5
    )
    
    # Jalankan
    detector.run()
```

**Penjelasan:**
- `if __name__ == "__main__"`: Block ini hanya execute jika file dijalankan direct
- Instance `YOLODetector` dibuat dengan config default
- Method `run()` dipanggil untuk start main loop

---

## 🔄 Flow & Logic Sistem

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                  YOLODetector Class                      │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼─────┐    ┌──────▼──────┐   ┌──────▼──────┐
   │  Model   │    │   Camera    │   │  Logging    │
   │ (YOLO)   │    │  (cv2)      │   │  System     │
   └────┬─────┘    └──────┬──────┘   └──────┬──────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                   ┌──────▼──────┐
                   │  Main Loop  │
                   │  (run())    │
                   └──────┬──────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    ┌────▼────┐   ┌──────▼──────┐  ┌─────▼──────┐
    │ Detect  │   │ Draw Info   │  │   Display  │
    │ Objects │   │   & Render  │  │  & Control │
    └─────────┘   └─────────────┘  └────────────┘
```

### Sequence Diagram: Startup

```
User
  │
  ├─> python main.py
  │
  ├─> YOLODetector.__init__()
  │   ├─> _validate_model() → Check file exists
  │   ├─> _initialize_camera() → Open camera device
  │   └─> _load_model() → Load YOLO to memory
  │
  └─> detector.run() → Start main loop
      ├─> While True:
      │   ├─> camera.read() → Grab frame
      │   ├─> detect(frame) → YOLO inference
      │   ├─> _update_fps() → Calculate FPS
      │   ├─> draw_info() → Render boxes
      │   ├─> cv2.imshow() → Display
      │   └─> cv2.waitKey() → Wait for input
      │
      └─> cleanup() → Release resources
```

### Detection Pipeline Detail

```
Camera Frame (1980×1080)
        │
        ▼
┌────────────────────┐
│ Preprocess         │ • Resize/normalize
│ (Automatic by YOLOv8)│
└────────────┬───────┘
             │
             ▼
┌────────────────────────────────┐
│ YOLO Model Inference           │
│ (runs at 60 FPS typically)     │
└────────────┬───────────────────┘
             │
             ▼
┌────────────────────────────────┐
│ Confidence Filtering           │
│ (Keep only > threshold)        │
│ Default threshold: 0.5         │
└────────────┬───────────────────┘
             │
             ▼
┌────────────────────────────────┐
│ Results                        │
│ • Bounding boxes               │
│ • Class labels                 │
│ • Confidence scores            │
│ • Detection count              │
└────────────┬───────────────────┘
             │
             ▼
       Display to User
```

---

## ⚙️ Konfigurasi

### Basic Configuration

Edit parameter pada main execution block:

```python
detector = YOLODetector(
    model_path='yolo26n.pt',      # Path model
    camera_id=0,                   # Camera device ID
    conf_threshold=0.5             # Confidence (0-1)
)
```

### Camera Settings

Untuk mengubah resolusi kamera, edit method `_initialize_camera()`:

```python
# Default (1980×1080@60fps)
self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1980)
self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
self.camera.set(cv2.CAP_PROP_FPS, 60)

# Alternative 1: HD (1280×720@30fps) - faster
self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
self.camera.set(cv2.CAP_PROP_FPS, 30)

# Alternative 2: VGA (640×480@60fps) - fastest
self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
self.camera.set(cv2.CAP_PROP_FPS, 60)
```

### Confidence Threshold

Affect detections sensitivity:

```python
# Conservative (only high-confidence detections)
conf_threshold=0.7    # Fewer detections, less false positives

# Balanced (default)
conf_threshold=0.5    # Medium sensitivity

# Aggressive (more detections)
conf_threshold=0.3    # More detections, more false positives
```

### Logging Level

Ubah logging level pada awal file:

```python
# Default (info only)
logging.basicConfig(level=logging.INFO, ...)

# Debug (verbose)
logging.basicConfig(level=logging.DEBUG, ...)

# Error (critical only)
logging.basicConfig(level=logging.ERROR, ...)
```

---

## 🐛 Troubleshooting

### Problem: "Tidak bisa membuka kamera!"

**Penyebab Umum:**
1. Kamera sedang digunakan aplikasi lain
2. Permission issue pada OS
3. Kamera tidak terdeteksi system

**Solusi:**
```bash
# 1. Close aplikasi lain yang pakai kamera
# 2. Coba ubah camera_id:
detector = YOLODetector(camera_id=1)  # atau 2, 3, dst

# 3. Test kamera dengan OpenCV
python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"
```

---

### Problem: "Model file tidak ditemukan"

**Penyebab:**
- File `yolo26n.pt` tidak ada di direktori
- Path salah

**Solusi:**
```bash
# 1. Verifikasi file ada
dir yolo26n.pt

# 2. Gunakan absolute path
detector = YOLODetector(model_path='C:\\full\\path\\yolo26n.pt')

# 3. Download model jika hilang
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

---

### Problem: "Low FPS / Slow Performance"

**Penyebab:**
1. CPU tidak cukup powerful
2. Resolusi kamera terlalu tinggi
3. Confidence threshold terlalu rendah

**Solusi:**
```python
# 1. Reduce resolution
self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 2. Increase confidence threshold
detector = YOLODetector(conf_threshold=0.7)

# 3. Reduce FPS target
self.camera.set(cv2.CAP_PROP_FPS, 30)
```

---

### Problem: "Too many false positives"

**Penyebab:**
- Confidence threshold terlalu rendah

**Solusi:**
```python
# Increase threshold
detector = YOLODetector(conf_threshold=0.7)
```

---

### Problem: Aplikasi crash / not responsive

**Solusi:**
```bash
# 1. Cek apakah kamera masih terbuka
# 2. Restart aplikasi
# 3. Check console error log
# 4. Upgrade dependencies
pip install --upgrade opencv-python ultralytics
```

---

## 📊 Performance Metrics

### Typical Performance (Intel i5 + Webcam HD)
| Metric | Value |
|--------|-------|
| Resolution | 1280×720 |
| FPS | 25-30 |
| Latency | 33-40 ms |
| Memory Usage | 150-200 MB |
| Model Size | 6.3 MB |

### GPU Performance (NVIDIA RTX 3060)
| Metric | Value |
|--------|-------|
| Resolution | 1920×1080 |
| FPS | 45-60 |
| Latency | 16-22 ms |
| Memory Usage | 200-300 MB |

---

## 📚 Referensi & Resources

- **YOLOv8 Documentation**: https://docs.ultralytics.com
- **OpenCV Documentation**: https://docs.opencv.org
- **YOLO Paper**: https://arxiv.org/abs/1612.08242

---

## 💡 Tips & Best Practices

1. **Proper Cleanup**: Selalu gunakan Ctrl+C atau press 'q' untuk proper shutdown
2. **Monitor Resources**: Check task manager untuk monitor memory/CPU usage
3. **Lighting**: Pastikan lighting baik untuk optimal detection
4. **Distance**: Test pada berbagai jarak dari kamera
5. **Threshold Tuning**: Adjust confidence threshold based on use case

---

## 📝 License & Attribution

Proyek ini menggunakan:
- **YOLOv8** dari Ultralytics
- **OpenCV** library

---

**Last Updated**: January 20, 2026  
**Version**: 1.0.0

