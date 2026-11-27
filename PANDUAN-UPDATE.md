# Panduan update harian Loker MT

Dokumen ini dipakai oleh tugas terjadwal Claude yang memperbarui `data.json` setiap hari. Halaman `index.html` membaca `data.json`, jadi halaman publik ikut berubah begitu perubahan masuk ke branch `main`.

## Alur harian

1. Ambil `main` terbaru, lalu buat branch `update/YYYY-MM-DD` (tanggal WIB).
2. Cek ulang setiap program di `data.json`:
   - Buka sumber dan link pendaftarannya. Perbarui deadline, status, dan syarat kalau berubah (diperpanjang, ditutup lebih awal, kuota penuh).
   - Program yang deadline-nya sudah lewat lebih dari 7 hari: hapus dari `data.json`. Yang baru lewat tidak perlu dihapus; halaman otomatis memindahkannya ke "Sudah tutup".
3. Cari program MT baru yang sedang buka (lihat "Yang boleh masuk").
4. Tambahkan hanya program yang status bukanya bisa dipastikan dari minimal satu sumber yang bisa dibuka (deadline yang masih berlaku, atau lowongan resmi yang masih aktif di situs karier perusahaan), dan link pendaftarannya mengarah ke portal resmi perusahaan atau portal rekrutmen resminya.
5. Ubah `updated` ke tanggal hari ini (WIB, format `YYYY-MM-DD`).
6. Jalankan `python3 scripts/validate.py`. Jangan lanjut kalau gagal.
7. Commit, push branch, lalu buka pull request ke `main` dengan ringkasan: program baru, program yang dihapus, dan perubahan deadline atau syarat. Tulis juga program yang ditandai "Perlu dicek" dan alasannya.
8. Kalau tidak ada perubahan selain tanggal, tetap buka pull request dengan ringkasan "Tidak ada perubahan lowongan".

## Situs yang wajib dicek setiap hari

Berita lowongan sering terlambat atau tidak memuat program perusahaan multinasional. Selain pencarian web, buka langsung halaman karier berikut dan cari kata "management trainee", "graduate", "development program", atau "ODP" dengan lokasi Indonesia:

- FMCG dan multinasional: jobs.colgate.com, careers.unilever.com, nestle.co.id/jobs, careers.danone.com, pgcareers.com, career.indofood.com
- Grup usaha: career.astra.co.id
- Perbankan: karir.bca.co.id, bankmandiri.co.id/karir, e-recruitment.bri.co.id, recruitment.bni.co.id, jobs.talentics.id
- BUMN: rekrutmenbersama.fhcibumn.id

Kalau sebuah situs tidak bisa dibuka, catat di ringkasan pull request supaya pemilik repo bisa mengeceknya manual. Lowongan resmi tanpa deadline boleh masuk dengan `iso: null`, `cek: true`, dan status yang menyebut deadline tidak dicantumkan.

## Yang boleh masuk

- Program Management Trainee, ODP, graduate program, future leader program, atau sejenisnya untuk fresh graduate dan early career.
- Perusahaan kredibel: BUMN, bank, perusahaan pembiayaan dan asuransi yang diawasi OJK, FMCG, ritel, manufaktur, energi, teknologi, dan grup usaha besar.
- Masih buka per tanggal update.

## Yang tidak boleh masuk

- MLM, network marketing, atau skema rekrutmen downline.
- Pialang atau broker forex, komoditas, dan kripto; pekerjaan "trader" atau "marketing investasi".
- Rekrutmen agen asuransi atau agen penjualan berbasis komisi yang diberi label "management trainee".
- Lowongan yang meminta biaya pendaftaran, pelatihan, atau seragam.
- Lowongan yang hanya muncul di satu situs tanpa jejak resmi apa pun dari perusahaannya.

## Format setiap program di `data.json`

| Field | Isi |
| --- | --- |
| `program` | Nama program resmi |
| `perusahaan` | Nama badan hukum dan nama populer, misalnya `PT Bank Central Asia Tbk (BCA)` |
| `tentang` | 1 kalimat tentang perusahaan |
| `syarat` | Syarat lengkap dalam satu paragraf, dipisah titik koma |
| `info` | Detail program: durasi, rotasi, penempatan, benefit |
| `deadline` | Teks deadline seperti di sumber, misalnya `30 November 2026` |
| `iso` | Deadline format `YYYY-MM-DD`, atau `null` kalau tidak tercantum |
| `status` | `Masih buka`, atau keterangan singkat seperti `Perlu dicek: deadline tidak tercantum resmi` |
| `link` | URL pendaftaran resmi, harus diawali `https://` |
| `sumber` | URL sumber yang dipakai untuk memverifikasi, harus diawali `https://` |
| `sektor` | Salah satu: `Perbankan`, `Pembiayaan & Asuransi`, `FMCG & Distribusi`, `Ritel`, `Manufaktur` |
| `tags` | 2–3 label singkat, misalnya `S1/S2`, `IPK ≥ 3,00`, `Usia ≤ 24 (S1)` |
| `cek` | `true` kalau ada informasi yang belum pasti, selain itu `false` |

Program yang tidak cocok dengan sektor yang ada: pilih sektor terdekat. Kalau sering terjadi, tambahkan sektor baru di `SECTORS` pada `index.html` dan di daftar sektor `scripts/validate.py`.
