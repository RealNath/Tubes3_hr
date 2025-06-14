# Tubes3 : ATS CV Reader

Aplikasi berbasis Python untuk membaca isi file PDF CV dalam format ATS dan mencari CV yang cocok dengan keyword yang dimasukkan dan membuat summary-nya dengan teknik pencocokan Regex dan pencarian pola string dengan metode KMP (Knuth-Morris-Pratt) dan BM (Boyer-Moore)

## Penjelasan

[Diisi entar]

## Dibuat oleh

* Dzubyan Ilman Ramadhan (10122010)
* Buege Mahara Putra (13523037)
* Jonathan Levi (13523037)

## Instalasi & Membuka Aplikasi

1. Clone kode aplikasi

   ```bash
   git clone https://github.com/RealNath/Tubes3_hr.git
   ```

2. Cd ke folder data, buat *database*

   ```bash
   cd data
   mysql -u root -p < cv_database.sql
   ```

3. Cd ke root, lakukan *seeding* *database*

   ```bash
   cd ..
   python data/seeder.py
   ```

4. Buat virtual environment lokal

   ```bash
   python -m venv venv
   ```

5. Aktivasi virtual environment
   * Cmd (Windows): `venv\Scripts\activate.bat`
   * PowerShell (Windows): `venv\Scripts\Activate.ps1`
6. Install library-library Python yang dibutuhkan

   ```bash
   pip install -r requirements.txt
   ```

7. Jalankan program utamanya

   ```bash
   python main.py
   ```

## Cara Menggunakan Aplikasi

1. Masukkan semua file pdf CV yang ingin dicarikan ke folder `data\pdf`
2. Jalankan `python main.py`
3. Masukkan keyword, mode pencarian, dan banyak hasil yang ingin ditampilkan
4. Tekan tombol "Search"
5. Setelah beberapa saat, akan muncul hasil pencarian yang sesuai dengan parameter yang dimasukkan. Tiap hasil akan dilengkapi dengan tombol untuk melihat summary CV dan tombol untuk membuka file PDF aslinya.
