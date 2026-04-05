# 🧠 Head Tracking Mouse Control

## 🇮🇩 Penjelasan Program

Program ini adalah aplikasi berbasis Python yang memungkinkan pengguna untuk mengontrol pergerakan mouse menggunakan gerakan kepala secara real-time melalui webcam.

Program memanfaatkan:

* **MediaPipe Face Mesh** untuk mendeteksi titik-titik wajah
* **OpenCV** untuk pengolahan gambar dari kamera
* Perhitungan vektor untuk menentukan arah kepala (yaw & pitch)

Pergerakan kepala kemudian diterjemahkan menjadi pergerakan kursor pada layar.

### 🎯 Tujuan

* Membuat sistem kontrol alternatif tanpa menggunakan mouse fisik
* Eksperimen teknologi computer vision dan AI
* Dasar untuk pengembangan aplikasi seperti:

  * Kontrol game
  * Aksesibilitas (untuk pengguna dengan keterbatasan fisik)
  * Human-computer interaction berbasis gesture

---

## 🇬🇧 Program Description

This program is a Python-based application that allows users to control the mouse cursor using head movements in real-time via a webcam.

It utilizes:

* **MediaPipe Face Mesh** for facial landmark detection
* **OpenCV** for video processing
* Vector calculations to estimate head orientation (yaw & pitch)

The head movement is then mapped into cursor movement on the screen.

### 🎯 Purpose

* Create an alternative input system without a physical mouse
* Explore computer vision and AI concepts
* Serve as a foundation for applications such as:

  * Game control
  * Accessibility tools
  * Gesture-based human-computer interaction

---

## ⚙️ REQUIREMENTS

* Python 3.x
* OpenCV
* MediaPipe
* NumPy
* PyAutoGUI
* Keyboard

Install dependencies:

```bash
pip install opencv-python mediapipe numpy pyautogui keyboard
```

---

## 🚀 Cara Menggunakan (How to Use)

### 🇮🇩

1. Pastikan semua library sudah terinstall
2. Jalankan program:

   ```bash
   python MonitorTracking.py
   ```
3. Pastikan webcam aktif
4. Hadapkan wajah ke kamera
5. Gunakan gerakan kepala untuk mengontrol mouse

### 🎮 Kontrol:

* Tekan **F7** → Aktif / Nonaktif kontrol mouse
* Tekan **C** → Kalibrasi posisi tengah
* Tekan **Q** → Keluar dari program

---

### 🇬🇧

1. Make sure all dependencies are installed
2. Run the program:

   ```bash
   python MonitorTracking.py
   ```
3. Ensure your webcam is active
4. Face the camera
5. Move your head to control the cursor

### 🎮 Controls:

* Press **F7** → Toggle mouse control
* Press **C** → Calibrate center position
* Press **Q** → Exit the program

---

## 📌 Notes

* Make sure lighting is sufficient for better tracking
* Keep your face clearly visible to the camera
* Run as administrator if keyboard input does not work properly

---

## 🔥 Future Improvements

* Eye blink detection for clicking
* Smoother tracking (Kalman filter)
* GUI interface
* Multi-monitor support

---
