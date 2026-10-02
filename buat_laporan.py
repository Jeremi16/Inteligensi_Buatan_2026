"""Generate PDF laporan Tugas Kelompok Kasus 01 (8 bab, tanpa emdash)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Preformatted, HRFlowable)
from reportlab.lib.enums import TA_JUSTIFY

OUT = "TugasKelompok_Rx_nim1_nim2_nim3_v2.pdf"

styles = getSampleStyleSheet()
judul = ParagraphStyle("judul", parent=styles["Heading1"], fontSize=16, leading=19,
                       textColor=colors.HexColor("#0f2a44"), spaceAfter=4)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=12, leading=15,
                    textColor=colors.HexColor("#0f2a44"), spaceBefore=10, spaceAfter=4)
h3 = ParagraphStyle("h3", parent=styles["Heading3"], fontSize=10.5, leading=13,
                    textColor=colors.HexColor("#0f2a44"), spaceBefore=6, spaceAfter=3)
body = ParagraphStyle("body", parent=styles["Normal"], fontSize=9.5, leading=13.5,
                      alignment=TA_JUSTIFY, spaceAfter=4)
small = ParagraphStyle("small", parent=styles["Normal"], fontSize=8.5, leading=11.5,
                       alignment=TA_JUSTIFY, spaceAfter=3)
mono = ParagraphStyle("mono", parent=styles["Code"], fontSize=6.5, leading=8)

story = []
add = story.append


def styled_table(data, widths, fs=8.5):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2f5aa0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), fs),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eaf0fa")]),
    ]))
    story.append(t)
    story.append(Spacer(1, 3 * mm))


add(Paragraph("Tugas Kelompok Berbasis Kasus 01", judul))
add(Paragraph("Robot Kurir Kampus: Rute GU (Gerbang Utama) ke LK (Lab Komputasi). Metode: UCS, IDS, GBFS, dan A Star. Inteligensi Buatan, 2026.", body))
add(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#b78d1e")))
add(Paragraph("Kelompok: Rx. Nama/NIM: [isi nim1, nim2, nim3]. Draf otomatis dari <b>search_kampus.py</b>.", small))
add(Spacer(1, 2 * mm))

add(Paragraph("Deskripsi Kasus", h2))
add(Paragraph("Kasus 01 bercerita tentang robot kurir kampus yang diberi misi mengantar barang dari Gerbang Utama yang disingkat GU menuju Lab Komputasi yang disingkat LK dengan melewati peta kampus yang dimodelkan sebagai graf tak berarah dan berbobot. Peta tersebut terdiri dari dua belas lokasi yaitu Gerbang Utama, Parkir Barat, Rektorat, Gedung Kuliah Umum, Perpustakaan, Kantin, Masjid, Aula, Asrama, Teknik Informatika, Sport Center, dan Lab Komputasi yang saling terhubung melalui sembilan belas jalur dengan bobot yang berbeda beda yang menyatakan jarak tempuh antar lokasi. Setiap lokasi juga dilengkapi dengan nilai heuristik h dalam kurung n yang berfungsi sebagai perkiraan jarak dari lokasi tersebut ke LK sehingga robot tidak berjalan secara membabi buta. Untuk menyelesaikan misi ini robot diuji dengan empat algoritma pencarian yang memiliki karakter berbeda beda yaitu UCS yang selalu memperluas simpul dengan biaya perjalanan terkecil dari titik awal, IDS yang melakukan pencarian mendalam berulang dengan batas kedalaman yang dinaikkan secara bertahap dan memakai bobot graf untuk menghitung total biaya di akhir, GBFS yang bersifat rakus karena hanya mengikuti nilai heuristik terkecil, serta A Star yang menggabungkan biaya perjalanan dan heuristik dalam fungsi f yang dihitung dari g ditambah h. Seluruh proses tersebut diwujudkan dalam sebuah program sederhana agar urutan simpul yang diperluas, rute yang ditemukan, dan total biayanya tercatat secara objektif. Hasil luaran program inilah yang kemudian dibandingkan dan dianalisis untuk melihat algoritma mana yang paling optimal, mana yang paling hemat langkah, dan mengapa perbedaan itu bisa terjadi pada peta yang sama.", body))
styled_table(
    [["Simpul", "Tetangga (bobot)"],
     ["GU", "PB(3), R(4)"], ["PB", "GU(3), GKU(4), K(6)"], ["R", "GU(4), PR(3), M(5)"],
     ["GKU", "PB(4), PR(2), K(3), IF(7)"], ["K", "PB(6), GKU(3), AS(5)"],
     ["PR", "R(3), GKU(2), A(6), IF(4)"], ["A", "PR(6), M(3), LK(5)"],
     ["M", "R(5), A(3), SC(6)"], ["IF", "GKU(7), PR(4), AS(4), LK(3)"],
     ["AS", "K(5), IF(4), SC(6)"], ["SC", "M(6), AS(6), LK(4)"], ["LK", "A(5), IF(3), SC(4)"]],
    [22 * mm, 140 * mm])
styled_table(
    [["Simpul", "h(n)", "Simpul", "h(n)", "Simpul", "h(n)"],
     ["GU", "12", "PB", "10", "R", "9"],
     ["GKU", "7", "PR", "6", "K", "9"],
     ["M", "7", "A", "4", "AS", "5"],
     ["IF", "2", "SC", "3", "LK", "0"]],
    [25 * mm, 15 * mm, 25 * mm, 15 * mm, 25 * mm, 15 * mm], fs=8)
add(Paragraph("Heuristik ini admissible dan konsisten. Contoh: R(9) &lt;= 3 + 6 = 9 dan PR(6) &lt;= 4 + 2 = 6, sehingga A Star dijamin optimal di graf ini.", small))

add(Paragraph("Tujuan", h2))
add(Paragraph("Tujuan dari pengerjaan kasus ini adalah memberikan pemahaman yang utuh tentang bagaimana empat algoritma pencarian bekerja pada satu peta yang sama sekaligus melatih kemampuan dalam menerjemahkan teori ke dalam program yang dapat diuji. Melalui implementasi UCS, IDS, GBFS, dan A Star dalam sebuah program sederhana, mahasiswa diharapkan mampu mencatat secara tertib urutan simpul yang diperluas, rute yang ditemukan dari GU ke LK, serta total biaya perjalanan yang dihasilkan oleh masing masing metode. Perbandingan tersebut kemudian dianalisis untuk menjawab pertanyaan yang lebih dalam yaitu mengapa suatu algoritma bisa menemukan jalur yang lebih murah, mengapa ada algoritma yang langkahnya sedikit tetapi hasilnya belum tentu optimal, serta bagaimana peran bobot jalur dan nilai heuristik dalam membentuk keputusan robot. Pada akhirnya laporan yang dikumpulkan dalam bentuk PDF tidak hanya menampilkan tangkapan luaran program sebagai bukti, tetapi juga memuat argumentasi yang menjelaskan kelebihan dan kekurangan setiap metode sehingga kelompok mampu memberikan rekomendasi algoritma yang paling tepat untuk kebutuhan robot kurir kampus.", body))

add(Paragraph("Metode yang Digunakan", h2))
add(Paragraph("Keempat algoritma dijalankan pada graf dan heuristik yang sama agar adil. Aturan bersama adalah tie break alfabetis: bila dua simpul memiliki prioritas sama maka nama yang lebih kecil menurut abjad dipilih dulu.", body))
add(Paragraph("3.1 UCS (Uniform Cost Search)", h3))
add(Paragraph("UCS selalu memperluas simpul dengan biaya perjalanan g(n) terkecil dari titik awal GU. Ia dijadikan acuan kebenaran karena selama bobot positif maka rute yang pertama mencapai LK dijamin termurah, walau ekspansinya banyak.", body))
add(Paragraph("3.2 IDS (Iterative Deepening Search)", h3))
add(Paragraph("IDS menaikkan batas kedalaman bertahap mulai dari nol lalu satu lalu dua dan seterusnya. Tiap batas dijalankan DFS alfabetis dengan path checking agar tidak berputar. IDS memakai jumlah edge sebagai kedalaman dan bukan bobot, sedangkan bobot baru dipakai di akhir untuk total biaya, sehingga ia dapat menemukan rute yang dangkal tetapi mahal.", body))
add(Paragraph("3.3 GBFS (Greedy Best First Search)", h3))
add(Paragraph("GBFS selalu memperluas simpul dengan heuristik h(n) terkecil tanpa peduli biaya yang sudah dikeluarkan. Ia cepat dan sedikit ekspansi, tetapi rapuh dan tidak menjamin optimal.", body))
add(Paragraph("3.4 A Star", h3))
add(Paragraph("A Star memakai f(n) = g(n) + h(n), gabungan biaya pasti dan perkiraan sisa. Karena h admissible dan konsisten di kasus ini, A Star optimal seperti UCS tetapi lebih sedikit ekspansi karena memangkas cabang mahal sejak dini.", body))

add(Paragraph("Hasil Luaran Program", h2))
add(Paragraph("Perintah: <b>python search_kampus.py</b>. Salinan persis luarannya:", small))
verbatim = """[UCS] ekspansi: GU -> PB -> R -> GKU -> PR -> K -> M -> IF -> A -> AS -> LK
  g: GU=0 PB=3 R=4 GKU=7 PR=7 K=9 M=9 IF=11 A=12 AS=14 LK=14
  Rute: GU -> R -> PR -> IF -> LK | Cost 14 (11 ekspansi)
[IDS] limit0: GU (belum) | limit1: GU->PB->R (belum)
  limit2: GU->PB->GKU->K->R->M->PR (belum, 7 kunjungan)
  limit3: 17 kunjungan (belum)
  limit4: GU->PB->GKU->IF->AS->LK => KETEMU GU->PB->GKU->IF->LK
  Cost 17, depth 4, total kumulatif 34
[GBFS] ekspansi: GU->R->PR->IF->LK | Cost 14 (5 ekspansi)
[A*] ekspansi: GU->PB->R->PR->IF->GKU->LK
  (g,h,f): GU(0,12,12) PB(3,10,13) R(4,9,13) PR(7,6,13) IF(11,2,13) GKU(7,7,14) LK(14,0,14)
  Rute: GU->R->PR->IF->LK | Cost 14 (7 ekspansi)"""
story.append(Preformatted(verbatim, mono, maxLineLength=100))
add(Spacer(1, 2 * mm))
add(Paragraph("Brute force semua jalur sederhana: termurah GU R PR IF LK = 4+3+4+3 = <b>14</b>, runner-up GU PB GKU PR IF LK = 3+4+2+4+3 = <b>16</b>. Jadi 14 optimal, 17 (IDS) suboptimal.", small))
add(Paragraph("Catatan revisi jalur 16. IDS memakai batas depth dan bukan batas biaya. Jalur biaya 16 berdepth 5 sedangkan rute IDS berdepth 4, sehingga saat limit 4 menemukan solusi pertama di cabang PB maka pencarian berhenti dan tidak pernah mencoba jalur depth 5. Jadi 16 &lt; 17 dari sisi biaya tetapi 5 &gt; 4 dari sisi depth. Varian sadar biaya dari IDS adalah IDA Star dengan batas f = g + h.", small))
styled_table(
    [["Jalur", "Hitung", "Cost", "Depth", "Keterangan"],
     ["GU R PR IF LK", "4+3+4+3", "14", "4", "Optimal (UCS, GBFS, A Star)"],
     ["GU PB GKU PR IF LK", "3+4+2+4+3", "16", "5", "Lebih murah dari IDS, depth 5"],
     ["GU PB GKU IF LK", "3+4+7+3", "17", "4", "Rute IDS, depth 4 cabang PB"],
     ["GU R M A LK", "4+5+3+5", "17", "4", "Contoh depth 4 lain"]],
    [32 * mm, 28 * mm, 14 * mm, 14 * mm, 74 * mm], fs=7.5)

add(Paragraph("Analisis Perbandingan Metode", h2))
styled_table(
    [["Aspek", "UCS", "IDS", "GBFS", "A Star"],
     ["Prioritas", "g(n)", "depth via DFS", "h(n)", "f = g + h"],
     ["Ekspansi", "11", "34 kumulatif", "5", "7"],
     ["Rute", "GU R PR IF LK", "GU PB GKU IF LK", "GU R PR IF LK", "GU R PR IF LK"],
     ["Cost", "14 optimal", "17 suboptimal", "14 kebetulan", "14 optimal"],
     ["Edge", "4", "4", "4", "4"]],
    [22 * mm, 32 * mm, 38 * mm, 35 * mm, 35 * mm], fs=8)
add(Paragraph("Urutan ekspansi. UCS: GU(0), PB(3), R(4), GKU(7), PR(7), K(9), M(9), IF(11), A(12), AS(14), LK(14), total 11 simpul. A Star: GU(12), PB(13), R(13), PR(13), IF(13), GKU(14), LK(14), hanya 7 simpul karena memangkas K, M, A, AS, SC. GBFS: GU, R, PR, IF, LK, hanya 5 simpul mengikuti h menurun 12, 9, 6, 2, 0.", body))
add(Paragraph("Rute dan biaya. UCS dan A Star optimal 14. GBFS ikut 14 tetapi itu kebetulan karena heuristik mengarah ke koridor optimal, dan teori tidak menjaminnya. IDS mendapat 17 pada depth 4 karena berhenti di solusi depth 4 pertama cabang PB yang diperiksa sebelum cabang R. Bobot tidak mengubah urutan DFS IDS dan hanya dipakai menghitung biaya akhir.", body))
add(Paragraph("Efisiensi. IDS paling boros: 1+3+7+17+6 = 34 kunjungan untuk 12 simpul. Hemat memori O(d) dan lengkap, tetapi buta biaya dan hanya cocok bila bobot seragam, sedangkan di sini bobot 2 sampai 7.", body))
add(Paragraph("Peran heuristik. Karena h admissible dan konsisten, A Star optimal sekaligus efisien (7 vs 11). GBFS tercepat (5) tetapi rapuh bila ada overestimate. UCS aman tanpa heuristik tetapi membayar ekspansi ekstra.", body))

add(Paragraph("Kesimpulan", h2))
add(Paragraph("A Star adalah algoritma yang paling tepat untuk robot kurir pada peta ini karena menemukan rute optimal biaya 14 dengan hanya 7 ekspansi. UCS menjadi pembanding kebenaran dengan biaya yang sama tetapi 11 ekspansi. GBFS cepat (5 ekspansi) namun tidak terjamin. IDS tidak disarankan untuk optimasi biaya karena menghasilkan 17 dengan 34 kunjungan, dan hanya relevan bila memori sangat terbatas atau yang dipentingkan adalah jumlah transit dan bukan jarak. Rekomendasi praktis: pakai A Star sebagai algoritma utama dan UCS sebagai acuan pengujian setiap kali peta atau heuristik diubah.", body))

add(Paragraph("Daftar Pustaka", h2))
add(Paragraph("Russell, S. dan Norvig, P. (2021). <i>Artificial Intelligence: A Modern Approach</i>, edisi keempat. Hoboken: Pearson. Bab 3 dan 4 untuk teori UCS, IDS, GBFS, dan A Star.", small))
add(Paragraph("Materi kuliah Inteligensi Buatan, Pertemuan 3, Tugas Kelompok Berbasis Kasus 01 (2026). Spesifikasi graf GU ke LK, nilai h(n), dan ketentuan luaran program serta analisis.", small))
add(Paragraph("Dokumentasi Python 3. Modul <i>heapq</i>: priority queue untuk antrean UCS, GBFS, dan A Star.", small))
add(Paragraph("Hart, P., Nilsson, N., dan Raphael, B. (1968). A Formal Basis for the Heuristic Determination of Minimum Cost Paths. <i>IEEE Transactions on Systems Science and Cybernetics</i>, 4(2), 100-107. Dasar sifat admissible dan konsisten pada A Star.", small))

add(Paragraph("Lampiran (Source Code)", h2))
add(Paragraph("File <b>search_kampus.py</b> lengkap di bawah. Reproduksi: simpan bersama dokumen ini lalu jalankan <b>python search_kampus.py</b>. Perintah <b>python buat_docx.py</b> membuat ulang DOCX ini dan <b>python buat_laporan.py</b> membuat ulang PDF (butuh reportlab).", body))
with open("search_kampus.py", "r", encoding="utf-8") as f:
    story.append(Preformatted(f.read(), mono, maxLineLength=95))
add(Spacer(1, 2 * mm))
add(Paragraph("Catatan: ganti placeholder Rx dan nim1 nim2 nim3 dengan data kelompok, lalu tambahkan screenshot terminal dan gambar graf sebelum dikumpulkan.", small))

doc = SimpleDocTemplate(OUT, pagesize=A4, topMargin=15 * mm, bottomMargin=15 * mm,
                        leftMargin=15 * mm, rightMargin=15 * mm,
                        title="Tugas Kelompok Kasus 01 GU-LK")
doc.build(story)
print("OK ->", OUT)
