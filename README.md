# Animated Space Fireball Breaker - Dokumentasi & Changelog

Selamat datang di dokumentasi resmi **Animated Space Fireball Breaker**, sebuah game arkade klasik (*brick breaker*) berbasis Python Tkinter yang telah dirombak total menjadi game luar angkasa berteknologi tinggi yang modern, dinamis, dan mulus.

## 🚀 Fitur Utama & Peningkatan

### 1. **Tema Visual Luar Angkasa (Deep Space & Cyber Theme)**
* **Latar Belakang Kosmik Kaya Objek:** Mengganti latar belakang polos dengan pemandangan luar angkasa mendalam yang dilengkapi sabuk bintang (*starfield*), asteroid, nebula debu kosmik, komet/bintang jatuh yang melintas, serta planet-planet realistis (Planet Saturnus bercincin, Planet Merah/Mars, dan Gas Raksasa Biru).
* **Aset Luar Angkasa Beranimasi:**
  * **UFO (Pesawat Alien):** Melayang secara sinusoidal di latar belakang dengan lampu navigasi LED RGB yang berkedip secara periodik.
  * **Satelit Luar Angkasa:** Mengambang dengan efek gravitasi nol dan lampu suar peringatan merah yang berkedip.

### 2. **Fisika, Animasi Bola, & Kontrol Mulus (60 FPS)**
* **Bola Api Beranimasi (Fireballs):** Bola dirender sebagai bola plasma dengan efek api berlapis yang memiliki animasi berkobar (*flickering flames*) secara *real-time* di setiap *frame*.
* **Paddle Perisai Energi:** Papan pemukul didesain ulang dengan bodi lapis baja luar dan inti energi neon menyala di bagian tengah.
* **Kontrol Mulus (Continuous Movement):** Mekanisme input diubah dari lompatan diskrit menjadi sistem tahan tombol (*hold-to-move*) yang dikunci dengan batas dinding (*border-clamping*) agar pergerakan sangat halus tanpa getaran (*jitter*).

### 3. **Antarmuka Hologram Sci-Fi (HUD Panels)**
* **Panel Hologram Pop-up:** Teks pemberitahuan biasa digantikan dengan kotak dialog HUD bergaya Sci-Fi lengkap dengan ornamen sudut (*brackets*), garis pemindai (*scanlines*), dan teks neon bertumpuk.
* **Skema Warna Kontekstual:**
  * **Cyan (`#00FFFF`)**: Tampilan Layar *Start* / Siap Diretas.
  * **Hijau Neon (`#00FF55`)**: Tampilan *Sector Cleared* (Berhasil Menyelesaikan Level).
  * **Merah Kritis (`#FF0033`)**: Tampilan *Game Over* (Gagal / Koneksi Hilang).

### 4. **Mekanik Gameplay & Sistem Multiball**
* **Balok Kapsul Energi (Bricks):** Balok dirancang seperti sel energi teknologi tinggi yang memiliki bingkai logam, panel kaca gelap di tengah, garis laser energi, serta lampu indikator LED yang berubah warna saat menerima pukulan.
* **Multiball & Power-Up Dinamis:** Penghancuran balok memiliki peluang 15% menjatuhkan kotak energi emas. Menangkapnya akan membelah bola aktif menjadi banyak (dengan batas optimal 100 bola untuk menjaga kestabilan performa 60 FPS).
* **Sistem Nyawa Presisi:** Game over dipicu secara mutlak ketika nyawa menyentuh angka `0`, mencegah angka negatif dan memastikan sesi reset berjalan bersih.

## 🛠️ Arsitektur Kode & Kelas Utama
* **`GameObject`**: Kelas dasar untuk pengelolaan canvas, koordinat, pergerakan, dan penghapusan objek.
* **`Ball`**: Mengelola pantulan vektor, animasi jilatan api, dan deteksi tabrakan.
* **`Paddle`**: Mengontrol pergerakan luncur pemain dan penguncian batas layar.
* **`Brick`**: Mengatur status ketahanan, komponen visual multi-bagian, dan degradasi visual.
* **`PowerUp`**: Menangani fisika benda jatuh dan pemicu efek multiball.
* **`Game`**: Mesin penggerak utama (*60 FPS main loop*) yang mengelola animasi latar, status permainan (`idle`, `playing`, `transition`, `game_over`), serta rendering HUD.

## 🎮 Kontrol Permainan
* **Tombol Panah Kiri (`<Left>` / Tahan)**: Menggeser paddle ke kiri dengan mulus.
* **Tombol Panah Kanan (`<Right>` / Tahan)**: Menggeser paddle ke kanan dengan mulus.
* **Tombol Spasi (`<Space>`)**: Memulai permainan atau mempercepat transisi level.

# sceenshoot dokumentasi game!
![Menu Utama](<Screenshoot/Screenshot 2026-11-10 112211.png>)
![Pas Permainan](<Screenshoot/Screenshot 2026-11-10 112254.png>)
![sector sudah ke clear](<Screenshoot/Screenshot 2026-11-10 112342.png>)