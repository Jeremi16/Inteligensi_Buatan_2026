# Inteligensi Buatan 2026 — Kasus 01: Robot Kurir Kampus GU → LK

Implementasi UCS, IDS, GBFS, dan A* untuk rute GU (Gerbang Utama) → LK (Lab Komputasi).

## Isi repo
- `search_kampus.py` — program utama (graf 12 simpul / 19 edge, h(n) sesuai soal, tie-break alfabetis)
- `TugasKelompok_Rx_nim1_nim2_nim3.docx` — draf laporan yang bisa diedit (sudah termasuk revisi Bab 2b: jalur 16 vs 17)
- `TugasKelompok_Rx_nim1_nim2_nim3.pdf` — versi PDF
- `buat_docx.py`, `buat_laporan.py` — generator laporan

## Cara jalan
```bash
python search_kampus.py
python buat_docx.py     # regenerasi DOCX
python buat_laporan.py  # regenerasi PDF (butuh reportlab)
```

## Hasil (terverifikasi brute force, optimal = 14)
| Metode | Rute | Cost | Ekspansi |
|---|---|---|---|
| UCS | GU → R → PR → IF → LK | 14 optimal | 11 |
| IDS | GU → PB → GKU → IF → LK | 17 suboptimal | 34 kumulatif (solusi depth 4) |
| GBFS | GU → R → PR → IF → LK | 14 (kebetulan optimal) | 5 |
| A* | GU → R → PR → IF → LK | 14 optimal | 7 |

Catatan IDS: jalur `GU-PB-GKU-PR-IF-LK = 16` memang lebih murah dari `17`, tapi depth-nya 5 vs 4 — IDS berhenti di depth 4 pertama cabang PB (lihat Bab 2b di DOCX).

## TODO sebelum dikumpulkan
- Ganti `Rx` / `nim1_nim2_nim3` dengan data kelompok asli
- Tambah nama anggota, screenshot terminal, gambar graf
