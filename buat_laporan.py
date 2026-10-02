"""Generate PDF laporan Tugas Kelompok Kasus 01 (reportlab)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Preformatted, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

OUT = "TugasKelompok_Rx_nim1_nim2_nim3.pdf"

styles = getSampleStyleSheet()
judul = ParagraphStyle("judul", parent=styles["Heading1"], fontSize=16, leading=19,
                       textColor=colors.HexColor("#0f2a44"), spaceAfter=4)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=12, leading=15,
                    textColor=colors.HexColor("#0f2a44"), spaceBefore=10, spaceAfter=4)
body = ParagraphStyle("body", parent=styles["Normal"], fontSize=9.5, leading=13.5,
                      alignment=TA_JUSTIFY, spaceAfter=4)
small = ParagraphStyle("small", parent=styles["Normal"], fontSize=8.5, leading=11.5,
                       alignment=TA_JUSTIFY, spaceAfter=3)
center = ParagraphStyle("center", parent=styles["Normal"], fontSize=9.5, leading=13,
                        alignment=TA_CENTER, spaceAfter=2)
mono = ParagraphStyle("mono", parent=styles["Code"], fontSize=7.5, leading=9.5)

story = []

def add(p): story.append(p)

add(Paragraph("Tugas Kelompok &ndash; Berbasis Kasus 01", judul))
add(Paragraph("Robot Kurir Kampus: Rute GU (Gerbang Utama) &rarr; LK (Lab Komputasi)<br/>Metode: UCS, IDS, GBFS, A* &mdash; Inteligensi Buatan 2026", body))
add(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#b78d1e")))
add(Paragraph("Kelompok: Rx &mdash; Nama/NIM: [isi nim1, nim2, nim3] &mdash; File ini draf otomatis dari output program <b>search_kampus.py</b>. Ganti nama file menjadi <b>TugasKelompok_Rx_nim1_nim2_nim3.pdf</b> sesuai kelompok.", small))
add(Spacer(1, 2*mm))

add(Paragraph("1. Graf dan h(n)", h2))
add(Paragraph("Graf undirected 12 simpul, 19 edge (terverifikasi dari gambar hires). Tie-break alfabetis agar deterministik.", body))
graf_data = [
    ["Simpul", "Tetangga (bobot)"],
    ["GU", "PB(3), R(4)"],
    ["PB", "GU(3), GKU(4), K(6)"],
    ["R", "GU(4), PR(3), M(5)"],
    ["GKU", "PB(4), PR(2), K(3), IF(7)"],
    ["K", "PB(6), GKU(3), AS(5)"],
    ["PR", "R(3), GKU(2), A(6), IF(4)"],
    ["A", "PR(6), M(3), LK(5)"],
    ["M", "R(5), A(3), SC(6)"],
    ["IF", "GKU(7), PR(4), AS(4), LK(3)"],
    ["AS", "K(5), IF(4), SC(6)"],
    ["SC", "M(6), AS(6), LK(4)"],
    ["LK", "A(5), IF(3), SC(4)"],
]
t = Table(graf_data, colWidths=[22*mm, 140*mm])
t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2f5aa0")),
    ("TEXTCOLOR",(0,0),(-1,0),colors.white), ("FONTSIZE",(0,0),(-1,-1),8.5),
    ("GRID",(0,0),(-1,-1),0.4,colors.grey), ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#eaf0fa")])]))
story.append(t); story.append(Spacer(1,3*mm))

h_data = [["Simpul","h(n)"],["GU",12],["PB",10],["R",9],["GKU",7],["PR",6],["K",9],
          ["M",7],["A",4],["AS",5],["IF",2],["SC",3],["LK",0]]
t2 = Table(h_data, colWidths=[30*mm, 25*mm])
t2.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2f5aa0")),
    ("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTSIZE",(0,0),(-1,-1),8.5),
    ("GRID",(0,0),(-1,-1),0.4,colors.grey),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#eaf0fa")])]))
story.append(t2)
add(Paragraph("Heuristik diuji admissible dan konsisten (h(n) &le; biaya aktual ke LK, dan h(n) &le; c(n,m)+h(m) untuk semua edge). Contoh: R(9)&le;3+6=9, PR(6)&le;4+2=6, GU(12)&le;4+9=13. Karena itu A* dengan h ini dijamin optimal pada graf ini.", small))

add(Paragraph("2. Hasil luaran program (verbatim)", h2))
add(Paragraph("Perintah: <b>python search_kampus.py</b>. Di bawah ini salinan persis output yang dipakai sebagai bukti.", small))
verbatim = """======================================================================
KASUS 01: Robot kurir kampus GU -> LK
======================================================================

[UCS] Urutan ekspansi (pop terkecil g):
  GU -> PB -> R -> GKU -> PR -> K -> M -> IF -> A -> AS -> LK
  g saat pop: {'GU': 0, 'PB': 3, 'R': 4, 'GKU': 7, 'PR': 7, 'K': 9, 'M': 9, 'IF': 11, 'A': 12, 'AS': 14, 'LK': 14}
  Rute : GU -> R -> PR -> IF -> LK
  Cost : 14 | node diekspansi: 11

[IDS] Iterative Deepening (DFS alfabetis, limit 0..n):
  limit=0 (1 kunjungan): GU => belum ketemu
  limit=1 (3 kunjungan): GU -> PB -> R => belum ketemu
  limit=2 (7 kunjungan): GU -> PB -> GKU -> K -> R -> M -> PR => belum ketemu
  limit=3 (17 kunjungan): GU -> PB -> GKU -> IF -> K -> PR -> K -> AS -> GKU -> R -> M -> A -> SC -> PR -> A -> GKU -> IF => belum ketemu
  limit=4 (6 kunjungan): GU -> PB -> GKU -> IF -> AS -> LK => KETEMU GU -> PB -> GKU -> IF -> LK
  Rute : GU -> PB -> GKU -> IF -> LK
  Cost (jumlah bobot) : 17 | depth solusi: 4 | total kunjungan kumulatif: 34

[GBFS] Urutan ekspansi (pop terkecil h):
  GU -> R -> PR -> IF -> LK
  Rute : GU -> R -> PR -> IF -> LK
  Cost : 14 | node diekspansi: 5

[A*] Urutan ekspansi (pop terkecil f=g+h):
  GU -> PB -> R -> PR -> IF -> GKU -> LK
  detail pop (g,h,f): {'GU': (0,12,12), 'PB': (3,10,13), 'R': (4,9,13), 'PR': (7,6,13), 'IF': (11,2,13), 'GKU': (7,7,14), 'LK': (14,0,14)}
  Rute : GU -> R -> PR -> IF -> LK
  Cost : 14 | node diekspansi: 7

--- RINGKASAN ---
UCS   | ekspansi: 11 | rute: GU -> R -> PR -> IF -> LK | cost: 14
IDS   | ekspansi: 34 (kumulatif, solusi depth 4) | rute: GU -> PB -> GKU -> IF -> LK | cost: 17
GBFS  | ekspansi: 5 | rute: GU -> R -> PR -> IF -> LK | cost: 14
A*    | ekspansi: 7 | rute: GU -> R -> PR -> IF -> LK | cost: 14"""
story.append(Preformatted(verbatim, mono, maxLineLength=100))
add(Spacer(1,2*mm))
add(Paragraph("Verifikasi optimalitas (brute force semua simple path): jalur termurah adalah GU-R-PR-IF-LK = 4+3+4+3 = <b>14</b>. Runner-up GU-PB-GKU-PR-IF-LK = 3+4+2+4+3 = 16. Jadi cost 14 = optimal, cost 17 (IDS) = suboptimal.", small))

add(Paragraph("3. Tabel perbandingan", h2))
cmp_data = [
    ["Aspek", "UCS", "IDS", "GBFS", "A*"],
    ["Prioritas", "g(n)", "depth (DFS)", "h(n)", "f=g+h"],
    ["Ekspansi*", "11", "34 kum. (6 di limit 4)", "5", "7"],
    ["Rute", "GU-R-PR-IF-LK", "GU-PB-GKU-IF-LK", "GU-R-PR-IF-LK", "GU-R-PR-IF-LK"],
    ["Cost", "14 optimal", "17 suboptimal", "14 (kebetulan optimal)", "14 optimal"],
    ["Edge", "4", "4", "4", "4"],
]
ct = Table(cmp_data, colWidths=[22*mm, 32*mm, 38*mm, 35*mm, 35*mm])
ct.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2f5aa0")),
    ("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTSIZE",(0,0),(-1,-1),8),
    ("GRID",(0,0),(-1,-1),0.4,colors.grey),("VALIGN",(0,0),(-1,-1),"TOP"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#eef3fb")])]))
story.append(ct)
add(Paragraph("*Ekspansi = jumlah node di-pop. IDS menghitung ulang tiap limit (total 1+3+7+17+6=34). Rute IDS dangkal (depth 4) tapi mahal karena meminimalkan jumlah edge, bukan bobot.", small))

add(Paragraph("4. Analisis perbandingan", h2))
add(Paragraph("<b>Urutan ekspansi.</b> UCS melebar berdasar biaya: GU(0), PB(3), R(4), GKU(7), PR(7), K(9), M(9), IF(11), A(12), AS(14), LK(14) &mdash; 11 node karena harus membuktikan tidak ada jalur &lt;14. A* jauh lebih fokus: GU(12), PB(13), R(13), PR(13), IF(13), GKU(14), LK(14) &mdash; hanya 7 node, h memangkas cabang mahal (K, M, A, AS, SC tidak pernah di-pop). GBFS paling rakus: GU&rarr;R&rarr;PR&rarr;IF&rarr;LK (5 node), langsung mengikuti h menurun 12&rarr;9&rarr;6&rarr;2&rarr;0 tanpa menoleh ke cabang PB.", body))
add(Paragraph("<b>Rute dan cost.</b> UCS dan A* menemukan optimal 14 (GU-R-PR-IF-LK). GBFS di kasus ini juga 14, tapi itu kebetulan karena h mengarah ke koridor optimal; secara teori GBFS tidak menjamin optimal (ia mengabaikan g). IDS menemukan GU-PB-GKU-IF-LK = 3+4+7+3 = 17 pada depth 4. Depth sama-sama 4 dengan solusi optimal, tetapi IDS berhenti pada solusi depth-4 pertama yang ditemui DFS alfabetis (cabang PB lebih dulu dari R), bukan yang termurah. Ini menjawab instruksi 'gunakan bobot untuk IDS': bobot tidak mengubah urutan DFS, hanya dipakai menghitung cost akhir.", body))
add(Paragraph("<b>Mengapa IDS boros?</b> Setiap kenaikan limit mengulang seluruh pohon: limit 0,1,2,3 gagal (1+3+7+17 kunjungan) sebelum limit 4 berhasil. Total 34 kunjungan untuk graf 12 simpul. Kelebihannya hemat memori O(d) dan tetap lengkap; kekurangannya waktu berlipat dan buta biaya. Cocok bila edge seragam, tidak cocok di sini karena bobot bervariasi 2&ndash;7.", body))
add(Paragraph("<b>Peran heuristik.</b> Karena h admissible + konsisten (dicek per edge), A* optimal sekaligus efisien (7 vs 11 ekspansi). GBFS (5 ekspansi) paling cepat di sini tetapi rapuh: jika h overestimate di satu simpul, ia bisa tersesat (misal bila h(K) kecil, GBFS akan membelok ke K-AS-SC-LK yang mahal). UCS aman tanpa h tetapi membayar dengan ekspansi ekstra.", body))
add(Paragraph("<b>Kesimpulan praktis untuk robot kurir.</b> Untuk peta kampus ini: pakai A* (optimal + sedikit ekspansi). UCS sebagai baseline kebenaran. GBFS hanya bila butuh jawaban sangat cepat dan h terpercaya. IDS tidak disarankan untuk optimasi biaya; gunakan hanya bila memori sangat terbatas atau yang penting sedikitrch transit (edge), bukan jarak meter.", body))

add(Paragraph("5. Cara reproduce & lampiran kode", h2))
add(Paragraph("1) Simpan <b>search_kampus.py</b> dan PDF ini dalam satu folder. 2) Jalankan <b>python search_kampus.py</b> &mdash; output harus sama persis dengan Bab 2. 3) Tie-break alfabetis, DLS memakai path-checking (hindari cycle satu jalur), UCS/GBFS/A* memakai graph-search. 4) Ganti placeholder Rx/NIM di cover, lalu export/rename final menjadi <b>TugasKelompok_Rx_nim1_nim2_nim3.pdf</b>. Kode lengkap ada di file pendamping; ringkasan struktur: dict GRAPH + H, fungsi ucs(), dls()/ids(), gbfs(), astar(), path_cost().", body))
add(Paragraph("Draf ini belum final: tambahkan nama anggota, NIM, kelas, screenshot terminal, dan gambar graf kampus sebelum dikumpulkan.", small))

doc = SimpleDocTemplate(OUT, pagesize=A4, topMargin=15*mm, bottomMargin=15*mm,
                        leftMargin=15*mm, rightMargin=15*mm, title="Tugas Kelompok Kasus 01 GU-LK")
doc.build(story)
print("OK ->", OUT)
