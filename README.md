# AI Head Tracking Mouse with Cursor Overlay

## 📌 Deskripsi (Indonesia)

Project ini adalah aplikasi Computer Vision yang memungkinkan pengguna mengontrol mouse menggunakan pergerakan kepala secara real-time.

Sistem ini menggunakan MediaPipe Face Mesh untuk mendeteksi wajah dan menghitung arah (yaw & pitch), kemudian mengubahnya menjadi pergerakan kursor mouse.

Selain itu, terdapat fitur visual berupa lingkaran overlay pada kursor untuk mempermudah tracking posisi mouse.

---

## 📌 Description (English)

This project is a Computer Vision application that allows users to control the mouse using real-time head movement.

It uses MediaPipe Face Mesh to detect facial landmarks and calculate head orientation (yaw & pitch), which is then mapped to cursor movement.

It also includes a visual cursor overlay for better tracking.

---

## ⚙️ Features

* Real-time head tracking
* Mouse control using face movement
* Smooth cursor movement (smoothing + acceleration)
* Calibration system
* Toggle mouse control (ON/OFF)
* Cursor overlay visualization (green circle)
* FPS-independent movement system

---

## 🧠 How It Works

Sistem bekerja dengan cara:

1. Mengambil input dari webcam
2. Mendeteksi wajah menggunakan MediaPipe Face Mesh 
3. Menghitung:

   * Posisi wajah (nose center)
   * Rotasi kepala (yaw & pitch)
4. Mengubah data tersebut menjadi pergerakan mouse
5. Menggunakan smoothing dan acceleration agar pergerakan halus

File utama:

* `MonitorTracking.py` → sistem AI head tracking & mouse control 
* `CursorCircle.py` → overlay lingkaran pada kursor 

---

## 📦 Requirements

Gunakan Python 3.9 – 3.11 (disarankan)

Install dependencies:

```bash id="k2a9vx"
pip install opencv-python mediapipe numpy pyautogui keyboard PyQt5
```

---

## 🚀 Installation

1. Clone repository:

```bash id="r9y2xo"
git clone https://github.com/username/head-tracking-mouse.git
```

2. Masuk ke folder:

```bash id="k0jv83"
cd head-tracking-mouse
```

3. Install dependencies:

```bash id="f8z0kc"
pip install -r requirements.txt
```

---

## ▶️ Cara Menjalankan

### 1. Jalankan Head Tracking

```bash id="8k0qv1"
python MonitorTracking.py
```

### 2. (Opsional) Jalankan Cursor Overlay

```bash id="6k92mf"
python CursorCircle.py
```

---

## 🖥️ Cara Penggunaan

* Hadapkan wajah ke kamera
* Tekan:

  * `C` → untuk kalibrasi posisi netral
  * `F7` → untuk ON/OFF kontrol mouse
  * `Q` → keluar program
* Gerakkan kepala untuk menggerakkan cursor

---

## ⚡ Teknologi yang Digunakan

* OpenCV → pengolahan video
* MediaPipe → face tracking & landmark detection
* PyAutoGUI → kontrol mouse
* NumPy → perhitungan numerik
* PyQt5 → tampilan overlay

---

## 📁 Struktur Project

```
project/
│── MonitorTracking.py     # AI head tracking & mouse control
│── CursorCircle.py        # Cursor overlay (visual)
│── README.md
```

---

## 📸 Output

Program akan menampilkan:

* Webcam dengan landmark wajah
* Status tracking (yaw, pitch, movement)
* Pergerakan cursor secara real-time
* Overlay lingkaran pada cursor

---

## ⚠️ Catatan

* Pastikan pencahayaan cukup agar wajah terdeteksi dengan baik
* Webcam harus aktif dan tidak digunakan aplikasi lain
* Jika cursor terlalu sensitif, bisa disesuaikan di parameter kode

---

## 👨‍💻 Author

Kiandra

---

## 📄 License

Free to use for learning and development purposes.
