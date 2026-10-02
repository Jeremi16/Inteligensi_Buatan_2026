"""Generate DOCX laporan Tugas Kelompok Kasus 01 (8 bab, editable, tanpa emdash)."""
from docx import Document
from docx.shared import Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = "TugasKelompok_Rx_nim1_nim2_nim3_v2.docx"
NAVY = RGBColor(0x0F, 0x2A, 0x44)

doc = Document()

style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)
style.paragraph_format.space_after = Pt(4)

sec = doc.sections[0]
sec.top_margin = Mm(15); sec.bottom_margin = Mm(15)
sec.left_margin = Mm(15); sec.right_margin = Mm(15)

def heading(text, size=16):
    p = doc.add_heading(level=1)
    r = p.add_run(text)
    r.font.size = Pt(size); r.font.color.rgb = NAVY; r.bold = True
    return p

def h2(text):
    p = doc.add_heading(level=2)
    r = p.add_run(text)
    r.font.size = Pt(12); r.font.color.rgb = NAVY; r.bold = True
    return p

def h3(text):
    p = doc.add_heading(level=3)
    r = p.add_run(text)
    r.font.size = Pt(11); r.font.color.rgb = NAVY; r.bold = True
    return p

def para(text, italic=False, size=11, justify=True):
    p = doc.add_paragraph()
    if justify:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(text)
    r.italic = italic; r.font.size = Pt(size)
    return p

def shade_cells(row, color="2F5AA0"):
    for c in row.cells:
        tcPr = c._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), color)
        tcPr.append(shd)
        for par in c.paragraphs:
            for run in par.runs:
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                run.bold = True

def make_table(headers, rows):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        t.rows[0].cells[i].text = h
    shade_cells(t.rows[0])
    for ri, row in enumerate(rows, start=1):
        for ci, val in enumerate(row):
            t.rows[ri].cells[ci].text = str(val)
    for row in t.rows:
        for cell in row.cells:
            for par in cell.paragraphs:
                par.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for run in par.runs:
                    run.font.size = Pt(9)
    return t

def code_block(text):
    p = doc.add_paragraph()
    p.style = doc.styles["Normal"]
    r = p.add_run(text)
    r.font.name = "Consolas"; r.font.size = Pt(8)
    return p

# ---------- cover ----------
heading("Tugas Kelompok Berbasis Kasus 01", 16)
para("Robot Kurir Kampus: Rute GU (Gerbang Utama) ke LK (Lab Komputasi). Metode: UCS, IDS, GBFS, dan A Star. Mata kuliah Inteligensi Buatan, 2026.")
para("Kelompok: Rx. Nama/NIM: [isi nim1, nim2, nim3]. Dokumen ini adalah draf yang dibuat otomatis dari luaran program search_kampus.py. Ganti nama file menjadi TugasKelompok_Rx_nim1_nim2_nim3.docx dan pdf sesuai data kelompok sebelum dikumpulkan.",
     italic=True, size=9)

# ---------- 1. Deskripsi Kasus ----------
h2("Deskripsi Kasus")
para("Kasus 01 bercerita tentang robot kurir kampus yang diberi misi mengantar barang dari Gerbang Utama yang disingkat GU menuju Lab Komputasi yang disingkat LK dengan melewati peta kampus yang dimodelkan sebagai graf tak berarah dan berbobot. Peta tersebut terdiri dari dua belas lokasi yaitu Gerbang Utama, Parkir Barat, Rektorat, Gedung Kuliah Umum, Perpustakaan, Kantin, Masjid, Aula, Asrama, Teknik Informatika, Sport Center, dan Lab Komputasi yang saling terhubung melalui sembilan belas jalur dengan bobot yang berbeda beda yang menyatakan jarak tempuh antar lokasi. Setiap lokasi juga dilengkapi dengan nilai heuristik h dalam kurung n yang berfungsi sebagai perkiraan jarak dari lokasi tersebut ke LK sehingga robot tidak berjalan secara membabi buta. Untuk menyelesaikan misi ini robot diuji dengan empat algoritma pencarian yang memiliki karakter berbeda beda yaitu UCS yang selalu memperluas simpul dengan biaya perjalanan terkecil dari titik awal, IDS yang melakukan pencarian mendalam berulang dengan batas kedalaman yang dinaikkan secara bertahap dan memakai bobot graf untuk menghitung total biaya di akhir, GBFS yang bersifat rakus karena hanya mengikuti nilai heuristik terkecil, serta A Star yang menggabungkan biaya perjalanan dan heuristik dalam fungsi f yang dihitung dari g ditambah h. Seluruh proses tersebut diwujudkan dalam sebuah program sederhana agar urutan simpul yang diperluas, rute yang ditemukan, dan total biayanya tercatat secara objektif. Hasil luaran program inilah yang kemudian dibandingkan dan dianalisis untuk melihat algoritma mana yang paling optimal, mana yang paling hemat langkah, dan mengapa perbedaan itu bisa terjadi pada peta yang sama.")
para("Struktur graf yang dipakai (terverifikasi dari gambar resolusi tinggi, 19 edge, tak berarah):")
make_table(["Simpul", "Tetangga (bobot)"],
    [["GU", "PB(3), R(4)"], ["PB", "GU(3), GKU(4), K(6)"], ["R", "GU(4), PR(3), M(5)"],
     ["GKU", "PB(4), PR(2), K(3), IF(7)"], ["K", "PB(6), GKU(3), AS(5)"],
     ["PR", "R(3), GKU(2), A(6), IF(4)"], ["A", "PR(6), M(3), LK(5)"],
     ["M", "R(5), A(3), SC(6)"], ["IF", "GKU(7), PR(4), AS(4), LK(3)"],
     ["AS", "K(5), IF(4), SC(6)"], ["SC", "M(6), AS(6), LK(4)"], ["LK", "A(5), IF(3), SC(4)"]])
doc.add_paragraph()
make_table(["Simpul", "h(n)", "Simpul", "h(n)", "Simpul", "h(n)"],
    [["GU", 12, "PB", 10, "R", 9],
     ["GKU", 7, "PR", 6, "K", 9],
     ["M", 7, "A", 4, "AS", 5],
     ["IF", 2, "SC", 3, "LK", 0]])
para("Nilai heuristik di atas telah diuji admissible dan konsisten, artinya tidak pernah melebihi biaya sebenarnya ke LK dan memenuhi h(n) <= c(n,m) + h(m) untuk setiap edge. Contohnya R(9) <= 3 + 6 = 9 dan PR(6) <= 4 + 2 = 6. Sifat ini penting karena menjamin A Star menemukan rute optimal pada graf ini.",
     italic=True, size=9)

# ---------- 2. Tujuan ----------
h2("Tujuan")
para("Tujuan dari pengerjaan kasus ini adalah memberikan pemahaman yang utuh tentang bagaimana empat algoritma pencarian bekerja pada satu peta yang sama sekaligus melatih kemampuan dalam menerjemahkan teori ke dalam program yang dapat diuji. Melalui implementasi UCS, IDS, GBFS, dan A Star dalam sebuah program sederhana, mahasiswa diharapkan mampu mencatat secara tertib urutan simpul yang diperluas, rute yang ditemukan dari GU ke LK, serta total biaya perjalanan yang dihasilkan oleh masing masing metode. Perbandingan tersebut kemudian dianalisis untuk menjawab pertanyaan yang lebih dalam yaitu mengapa suatu algoritma bisa menemukan jalur yang lebih murah, mengapa ada algoritma yang langkahnya sedikit tetapi hasilnya belum tentu optimal, serta bagaimana peran bobot jalur dan nilai heuristik dalam membentuk keputusan robot. Pada akhirnya laporan yang dikumpulkan dalam bentuk PDF tidak hanya menampilkan tangkapan luaran program sebagai bukti, tetapi juga memuat argumentasi yang menjelaskan kelebihan dan kekurangan setiap metode sehingga kelompok mampu memberikan rekomendasi algoritma yang paling tepat untuk kebutuhan robot kurir kampus.")

# ---------- 3. Metode yang Digunakan ----------
h2("Metode yang Digunakan")
para("Keempat algoritma dijalankan pada graf dan nilai heuristik yang sama agar hasilnya dapat dibandingkan secara adil. Aturan tambahan yang dipakai bersama adalah tie break alfabetis, yaitu ketika dua simpul memiliki nilai prioritas yang sama maka simpul yang namanya lebih kecil menurut abjad dipilih lebih dulu, sehingga setiap eksekusi program selalu menghasilkan urutan yang sama.")
h3("3.1 UCS (Uniform Cost Search)")
para("UCS selalu memperluas simpul dengan biaya perjalanan g(n) terkecil yang dihitung dari titik awal GU. Pencariannya melebar mengikuti murahnya biaya dan bukan mengikuti dekatnya dugaan ke tujuan. Karena sifatnya yang sistematis ini UCS dijadikan sebagai acuan kebenaran, sebab selama semua bobot jalur bernilai positif maka rute yang pertama kali mencapai LK dijamin memiliki biaya termurah, meskipun jumlah simpul yang diperluas biasanya cukup banyak.")
h3("3.2 IDS (Iterative Deepening Search)")
para("IDS menggabungkan keunggulan pencarian mendalam yang hemat memori dengan kelengkapan pencarian melebar melalui cara menaikkan batas kedalaman secara bertahap mulai dari nol lalu satu lalu dua dan seterusnya. Pada setiap batas, pencarian mendalam dilakukan dengan urutan tetangga yang diurutkan secara alfabetis agar hasilnya deterministik, dan simpul yang sudah ada dalam satu jalur tidak dikunjungi ulang untuk menghindari putaran. Perlu dipahami bahwa IDS pada tugas ini tidak memakai bobot untuk menentukan urutan perluasan melainkan hanya memakai jumlah edge sebagai kedalaman, sedangkan bobot baru dipakai di akhir untuk menghitung total biaya rute yang ditemukan, sehingga IDS bisa saja menemukan rute yang dangkal tetapi mahal.")
h3("3.3 GBFS (Greedy Best First Search)")
para("GBFS bersifat rakus karena selalu memperluas simpul dengan nilai heuristik h(n) terkecil tanpa memperhitungkan biaya yang sudah dikeluarkan dari titik awal. Cara ini membuat GBFS biasanya sangat cepat dan hanya memperluas sedikit simpul karena ia langsung mengejar dugaan yang paling menjanjikan, tetapi ia juga rapuh karena sekali heuristiknya mengarahkan ke cabang yang keliru maka hasilnya bisa jauh dari optimal dan tidak ada jaminan kebenaran biaya.")
h3("3.4 A Star")
para("A Star menggabungkan kelebihan UCS dan GBFS melalui fungsi f(n) yang dihitung dari penjumlahan biaya perjalanan g(n) dan nilai heuristik h(n), sehingga setiap simpul dinilai dari biaya yang sudah pasti dikeluarkan ditambah perkiraan sisa biaya menuju tujuan. Karena nilai heuristik pada kasus ini telah terbukti admissible dan konsisten, A Star dijamin menemukan rute optimal seperti UCS tetapi dengan jumlah perluasan yang lebih sedikit karena heuristiknya berhasil memangkas cabang cabang yang mahal sejak dini.")

# ---------- 4. Hasil Luaran Program ----------
h2("Hasil Luaran Program")
para("Program dijalankan dengan perintah python search_kampus.py. Berikut adalah salinan persis luarannya sebagai bukti:", italic=True, size=9)
verbatim = """======================================================================
KASUS 01: Robot kurir kampus GU -> LK
======================================================================

[UCS] Urutan ekspansi (pop terkecil g):
  GU -> PB -> R -> GKU -> PR -> K -> M -> IF -> A -> AS -> LK
  g saat pop: GU=0, PB=3, R=4, GKU=7, PR=7, K=9, M=9, IF=11, A=12, AS=14, LK=14
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
  detail pop (g,h,f): GU(0,12,12), PB(3,10,13), R(4,9,13), PR(7,6,13), IF(11,2,13), GKU(7,7,14), LK(14,0,14)
  Rute : GU -> R -> PR -> IF -> LK
  Cost : 14 | node diekspansi: 7

--- RINGKASAN ---
UCS   | ekspansi: 11 | rute: GU -> R -> PR -> IF -> LK | cost: 14
IDS   | ekspansi: 34 (kumulatif, solusi depth 4) | rute: GU -> PB -> GKU -> IF -> LK | cost: 17
GBFS  | ekspansi: 5 | rute: GU -> R -> PR -> IF -> LK | cost: 14
A*    | ekspansi: 7 | rute: GU -> R -> PR -> IF -> LK | cost: 14"""
code_block(verbatim)
para("Pemeriksaan menyeluruh atas semua jalur sederhana membuktikan jalur termurah adalah GU R PR IF LK dengan biaya 4 + 3 + 4 + 3 = 14, sedangkan posisi kedua ditempati jalur GU PB GKU PR IF LK dengan biaya 3 + 4 + 2 + 4 + 3 = 16. Jadi biaya 14 adalah optimal dan biaya 17 dari IDS adalah suboptimal.",
     italic=True, size=9)
para("Catatan revisi mengenai jalur biaya 16. Sering muncul pertanyaan mengapa IDS tidak memilih jalur GU PB GKU PR IF LK yang biayanya 16 dan jelas lebih murah dari 17. Jawabannya terletak pada definisi IDS yang memakai batas depth atau jumlah edge dan bukan batas biaya. Jalur biaya 16 memiliki depth 5 sedangkan rute IDS memiliki depth 4, sehingga pada saat limit mencapai 4 dan solusi pertama ditemukan di cabang PB, pencarian langsung berhenti dan tidak pernah mencoba jalur depth 5 tersebut. Dengan kata lain 16 lebih kecil dari 17 dari sisi biaya tetapi 5 lebih besar dari 4 dari sisi depth, sehingga IDS mengabaikannya. Jika diinginkan IDS yang sadar biaya maka yang dipakai adalah varian IDA Star dengan batas f = g + h.")
make_table(["Jalur", "Perhitungan", "Cost", "Depth", "Keterangan"],
    [["GU R PR IF LK", "4+3+4+3", "14", "4", "Optimal (UCS, GBFS, A Star)"],
     ["GU PB GKU PR IF LK", "3+4+2+4+3", "16", "5", "Lebih murah dari IDS tetapi depth 5"],
     ["GU PB GKU IF LK", "3+4+7+3", "17", "4", "Rute IDS: depth 4 pertama di cabang PB"],
     ["GU R M A LK", "4+5+3+5", "17", "4", "Contoh jalur depth 4 lain dengan biaya sama"]])

# ---------- 5. Analisis Perbandingan Metode ----------
h2("Analisis Perbandingan Metode")
make_table(["Aspek", "UCS", "IDS", "GBFS", "A Star"],
    [["Prioritas", "g(n)", "depth dengan DFS", "h(n)", "f = g + h"],
     ["Ekspansi", "11", "34 kumulatif (6 pada limit 4)", "5", "7"],
     ["Rute", "GU R PR IF LK", "GU PB GKU IF LK", "GU R PR IF LK", "GU R PR IF LK"],
     ["Cost", "14 optimal", "17 suboptimal", "14, kebetulan optimal", "14 optimal"],
     ["Edge", "4", "4", "4", "4"]])
para("Ditinjau dari urutan ekspansi, UCS melebar berdasarkan biaya yaitu GU(0), PB(3), R(4), GKU(7), PR(7), K(9), M(9), IF(11), A(12), AS(14), dan LK(14) sehingga total ada 11 simpul karena ia harus membuktikan bahwa tidak ada jalur dengan biaya di bawah 14. A Star jauh lebih fokus dengan urutan GU(12), PB(13), R(13), PR(13), IF(13), GKU(14), dan LK(14) sehingga hanya 7 simpul, karena nilai heuristiknya berhasil memangkas cabang mahal seperti K, M, A, AS, dan SC yang bahkan tidak pernah diperluas. GBFS adalah yang paling rakus dengan hanya 5 simpul yaitu GU lalu R lalu PR lalu IF lalu LK karena ia langsung mengikuti nilai heuristik yang menurun yaitu 12 lalu 9 lalu 6 lalu 2 lalu 0 tanpa menoleh ke cabang PB sama sekali.")
para("Ditinjau dari rute dan biaya, UCS dan A Star sama sama menemukan rute optimal 14 yaitu GU R PR IF LK. GBFS pada kasus ini juga menemukan biaya 14, tetapi itu merupakan kebetulan yang terjadi karena heuristiknya mengarah ke koridor yang memang optimal, sedangkan secara teori GBFS tidak menjamin optimal karena ia mengabaikan biaya perjalanan yang sudah dikeluarkan. IDS menemukan GU PB GKU IF LK dengan biaya 3 + 4 + 7 + 3 = 17 pada depth 4. Menariknya solusi optimal juga memiliki depth 4, tetapi IDS berhenti pada solusi depth 4 pertama yang ditemui DFS alfabetis yaitu cabang PB yang diperiksa sebelum cabang R, sehingga ia mendapatkan yang mahal bukan yang murah. Hal ini sekaligus menjawab instruksi pada soal yang meminta memakai bobot untuk IDS, karena bobot tersebut ternyata tidak mengubah urutan pencarian DFS dan hanya dipakai untuk menghitung biaya akhir.")
para("Ditinjau dari efisiensi, IDS adalah yang paling boros karena setiap kenaikan limit mengulang seluruh pohon dari awal yaitu limit 0, 1, 2, dan 3 yang semuanya gagal dengan 1 + 3 + 7 + 17 kunjungan sebelum limit 4 berhasil dengan 6 kunjungan, sehingga totalnya 34 kunjungan untuk graf yang hanya berisi 12 simpul. Kelebihannya adalah hemat memori dengan kompleksitas memori sebanding depth dan tetap lengkap, tetapi kekurangannya adalah waktu berlipat dan buta terhadap biaya, sehingga IDS cocok bila semua edge memiliki bobot seragam dan kurang cocok di sini karena bobot bervariasi dari 2 sampai 7.")
para("Ditinjau dari peran heuristik, karena h bersifat admissible dan konsisten pada seluruh edge maka A Star menjadi optimal sekaligus efisien dengan 7 ekspansi dibanding 11 milik UCS. GBFS dengan 5 ekspansi adalah yang tercepat pada kasus ini tetapi juga yang paling rapuh, sebab jika ada satu saja simpul yang heuristiknya overestimate maka ia dapat tersesat ke cabang mahal seperti K AS SC LK. UCS tetap aman tanpa heuristik tetapi harus membayar dengan ekspansi tambahan.")

# ---------- 6. Kesimpulan ----------
h2("Kesimpulan")
para("Berdasarkan seluruh hasil dan analisis di atas dapat disimpulkan bahwa A Star adalah algoritma yang paling tepat untuk kebutuhan robot kurir pada peta kampus ini karena ia menemukan rute optimal dengan biaya 14 sekaligus hanya memperluas 7 simpul berkat bantuan heuristik yang admissible dan konsisten. UCS menempati posisi sebagai pembanding kebenaran karena ia juga menemukan biaya 14 meskipun harus memperluas 11 simpul. GBFS memang hanya membutuhkan 5 ekspansi dan ikut menemukan biaya 14, tetapi sifatnya yang mengabaikan biaya perjalanan membuat keberhasilannya pada kasus ini tidak dapat dijadikan jaminan untuk peta lain. IDS tidak disarankan untuk optimasi biaya karena ia menemukan rute 17 yang suboptimal dengan total 34 kunjungan berulang, dan ia hanya relevan bila memori sangat terbatas atau bila yang dipentingkan adalah sedikitnya jumlah transit dan bukan murahnya jarak. Rekomendasi praktisnya adalah memakai A Star sebagai algoritma utama robot dan memakai UCS sebagai acuan pengujian kebenaran setiap kali peta atau heuristik diubah.")

# ---------- 7. Daftar Pustaka ----------
h2("Daftar Pustaka")
para("Russell, S. dan Norvig, P. (2021). Artificial Intelligence: A Modern Approach, edisi keempat. Hoboken: Pearson. Bab 3 tentang uninformed search dan Bab 4 tentang informed search menjadi landasan teori UCS, IDS, GBFS, dan A Star.")
para("Materi kuliah Inteligensi Buatan, Pertemuan 3, Tugas Kelompok Berbasis Kasus 01 (2026). Spesifikasi graf kampus GU ke LK, nilai h(n), dan ketentuan luaran program serta analisis perbandingan.")
para("Dokumentasi Python 3. Modul heapq: implementasi priority queue yang dipakai untuk antrean UCS, GBFS, dan A Star dalam program pendamping.")
para("Hart, P., Nilsson, N., dan Raphael, B. (1968). A Formal Basis for the Heuristic Determination of Minimum Cost Paths. IEEE Transactions on Systems Science and Cybernetics, 4(2), 100 sampai 107. Dasar formal sifat admissible dan konsistensi heuristik pada A Star.")

# ---------- 8. Lampiran ----------
h2("Lampiran (Source Code)")
para("Seluruh eksperimen direproduksi dari satu file program yaitu search_kampus.py. Cara menjalankannya adalah menyimpan file tersebut bersama dokumen ini dalam satu folder lalu menjalankan perintah python search_kampus.py sehingga luarannya sama persis dengan Bab 4. Perintah python buat_docx.py dipakai untuk membuat ulang dokumen ini sedangkan perintah python buat_laporan.py dipakai untuk membuat ulang versi PDF yang membutuhkan pustaka reportlab. Struktur program terdiri dari kamus GRAPH dan H, fungsi bantu neighbors_sorted, reconstruct, dan path_cost, serta empat fungsi utama yaitu ucs, dls dan ids, gbfs, dan astar.")
with open("search_kampus.py", "r", encoding="utf-8") as f:
    code_block(f.read())
para("Catatan: ganti placeholder Rx dan nim1 nim2 nim3 pada sampul dengan data kelompok yang sebenarnya, lalu tambahkan nama anggota, screenshot terminal, dan gambar graf kampus sebelum dokumen ini dikumpulkan.", italic=True, size=9)

doc.save(OUT)
print("OK ->", OUT)
