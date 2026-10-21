"""Material presentasi kelas, terpisah dari naskah dan protokol penelitian."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
slides = []


def add(title, blocks, notes, source, kind="body", **extra):
    slides.append(dict(number=len(slides) + 1, title=title, blocks=blocks,
                       notes=notes.strip(), source=source, kind=kind, **extra))


add("Evaluasi musik hasil AI\nDeepBach dan Coconet", [], """
Saya mempresentasikan penelitian skripsi yang sedang saya kerjakan, dengan judul lengkap Evaluasi Musik Hasil AI DeepBach dan Coconet Berdasarkan Kaidah Gerak Suara Strube dalam Harmonisasi Chorale. Pertemuan ini membahas naskah final-thesis v5 yang aktif, terutama revisi arah pada 13 Oktober 2026. Tanggal presentasi ini adalah 21 Oktober 2026. Istilah final-thesis menunjukkan fase proyek skripsi; pekerjaan yang tersedia masih BAB I sampai III dan bahan persiapannya.

Penelitian saya berangkat dari tugas yang cukup akrab di kelas harmoni: sopran sudah tersedia, lalu tiga suara bawah harus disusun. DeepBach dan Coconet dapat mengerjakan tugas semacam itu. Saya ingin membaca pilihan gerak suara yang dihasilkan keduanya dengan pedoman Strube, termasuk kondisi yang membuat suatu kejadian diterima atau perlu dikoreksi. Hari ini saya akan menjelaskan masalah penelitian, perubahan desain, dasar teori, rencana pemeriksaan, serta pekerjaan yang masih perlu diselesaikan sebelum data utama dikumpulkan.
""", "metadata.tex; BAB I–III; PROGRESS.md", kind="cover",
    subtitle="Berdasarkan kaidah gerak suara Strube\ndalam harmonisasi chorale",
    author="Vincent Nuridzati Adittama · 23104810131",
    occasion="Seminar Musikologi 2\n21 Oktober 2026 · Program Studi S-1 Musik, ISI Yogyakarta")

add("Persoalan yang saya teliti", [
    ["Tugas musikal", "Satu melodi sopran diberikan kepada model. Model menyusun alto, tenor, dan bas dalam tekstur empat suara."],
    ["Pertanyaan evaluasi", "Bagaimana gerak suara keluaran sesuai dengan Strube, setelah syarat dan pengecualian kaidah diperiksa?"],
    ["Bentuk pembahasan", "Partitur, lokasi kejadian, alasan keputusan musikal, dan profil per kriteria pada kasus yang sama."],
    ["Posisi pekerjaan", "Naskah dan rancangan analisis tersedia. Pilot serta data utama model belum dijalankan."]], """
Objek yang saya periksa adalah musik hasil model, khususnya gerak suara pada harmonisasi simbolik. Kesamaan melodi sopran memungkinkan kita membandingkan cara sistem mengisi ruang pilihan yang sama. Meskipun tugasnya sama, konfigurasi kedua sistem mempunyai perbedaan yang perlu dicatat, sehingga perbandingannya saya batasi pada sistem yang benar-benar diuji.

Kata evaluasi di sini mempunyai ukuran tertentu. Saya menilai kesesuaian gerak suara terhadap pedoman Strube dalam konteks chorale. Sebuah harmonisasi dapat memenuhi satu kriteria tetapi bermasalah pada kriteria lain. Karena itu, hasil akhirnya direncanakan berupa profil yang dapat ditelusuri ke partitur. Saya belum mempunyai hasil generasi utama untuk menyatakan sistem mana yang lebih sering menghasilkan kejadian tertentu. Contoh sumber dan perhitungan ilustratif yang muncul dalam presentasi harus dibaca sesuai fungsinya masing-masing.
""", "BAB I: pertanyaan, tujuan; BAB III: objek dan analisis")

add("Peta pembahasan", [
    ["01  Masalah dan perubahan", "Tugas harmonisasi AI, posisi penelitian terdahulu, dan alasan desain penelitian dipersempit."],
    ["02  Pedoman Strube", "Fungsi akor, hubungan antarsuara, gerak melodis, serta syarat dan pengecualian."],
    ["03  Rencana penelitian", "Pemilihan kasus, generasi berulang, pemeriksaan partitur, dan ringkasan deskriptif."],
    ["04  Perkembangan dan diskusi", "Bukti yang sudah tersedia, batas pelaksanaan, keputusan terbuka, dan masukan kelas."]], """
Urutan presentasi mengikuti persoalan yang perlu dipahami teman-teman sebelum menilai rancangan penelitian. Saya menjelaskan dahulu tugas model dan masalah evaluasinya, lalu perubahan rancangan agar istilah dari versi lama tidak terbawa ke penjelasan metode sekarang. Setelah itu saya masuk ke Strube dan menunjukkan contoh mengapa suatu pola nada membutuhkan pembacaan konteks.

Bagian metode menjelaskan hubungan antara partitur dan angka yang nantinya dilaporkan. Bagian terakhir menyampaikan perkembangan yang sudah tercatat serta butir yang membutuhkan masukan. Lampiran menyediakan rincian teknis dan metodologis untuk diskusi. Durasi kelas belum ditetapkan dalam bahan ini. Jika waktu terbatas, saya dapat memakai alur ringkas yang tercantum dalam catatan presenter tanpa mengubah status penelitian atau menghilangkan pertanyaan utamanya.
""", "Susunan presentasi dari naskah aktif dan catatan perkembangan")

add("Harmonisasi simbolik empat suara", [
    ["Sopran tetap", "Tinggi nada dan waktu bunyi sopran menjadi masukan bersama. Tanda diam dan durasinya ikut dipertahankan."],
    ["Alto, tenor, dan bas", "Ketiga suara ini dihasilkan model. Analisis mengikuti identitas suara asal, termasuk ketika suara bersilangan."],
    ["Data simbolik", "MusicXML dan MIDI menyimpan informasi nada serta waktu. Informasi ini memungkinkan pembacaan interval dan lokasi partitur."],
    ["Lingkup pengamatan", "Penelitian memeriksa gerak horizontal tiap suara dan hubungan antarsuara. Persepsi pendengar berada di luar pengukuran."]], """
Musik simbolik menyediakan catatan tentang nada dan waktu, sehingga gerak suara dapat diperiksa secara terperinci. MusicXML juga dapat menyimpan ejaan nada serta struktur notasi. Informasi yang dibawa setiap format dan model perlu dibedakan. Nomor nada MIDI, misalnya, tidak langsung menentukan apakah sebuah nada harus dieja sebagai kres atau mol. Perbedaan ini berpengaruh ketika keputusan membutuhkan interval diatonis atau fungsi akor.

Empat suara berarti empat jalur yang identitasnya dipertahankan. Jika tenor bergerak lebih tinggi daripada alto, saya tetap membaca jalur tersebut sebagai tenor. Mengurutkan ulang nada dari tinggi ke rendah akan menghapus kejadian persilangan yang justru perlu diamati. Pada tugas model, yang dikunci adalah sopran. Harmonisasi cetak empat suara disimpan untuk pembacaan acuan, sedangkan alto, tenor, dan bas cetak tidak diberikan kepada model untuk disalin.
""", "BAB I: latar belakang; BAB III: transkripsi dan kontrol kualitas")

add("Masalah evaluasi pada harmonisasi AI", [
    ["Penggunaan", "Model dapat memberikan harmonisasi kepada pengguna yang belum tentu dapat memeriksa gerak suaranya sendiri."],
    ["Penilaian keluaran", "Uji dengar dan kedekatan statistik memberi informasi sesuai tujuannya. Pemeriksaan kaidah menjelaskan keputusan pada nada dan pasangan suara tertentu."],
    ["Kebutuhan penelitian ini", "Setiap dugaan penyimpangan perlu mempunyai lokasi, dasar kaidah, konteks, dan alasan keputusan."],
    ["Manfaat yang dituju", "Contoh pembacaan keluaran AI dapat menjadi bahan pertimbangan pengajar dan mahasiswa harmoni. Peningkatan hasil belajar belum diukur."]], """
Latar belakang naskah menyebut penggunaan model oleh musisi dan pengguna pemula. Relevansinya pada penelitian saya adalah adanya keluaran harmonisasi yang dapat langsung digunakan sebagai bahan musikal, padahal pemakainya mungkin belum mampu memeriksa seluruh gerak suara. Dari situ, saya memusatkan penelitian pada apa yang dapat diperiksa melalui partitur.

Tiap cara evaluasi menjawab pertanyaan tertentu. Uji pendengar dapat menjelaskan penilaian terhadap potongan musik, sedangkan ukuran statistik dapat menggambarkan kedekatan ciri terhadap suatu korpus. Saya memerlukan penjelasan yang menunjuk suara mana yang bergerak, interval apa yang terjadi, serta syarat Strube yang mendasari keputusan. Manfaat pendidikan saya nyatakan sebagai kemungkinan penggunaan bahan analisis. Penelitian ini belum menguji apakah bahan tersebut meningkatkan kemampuan mahasiswa atau apakah pendengar menyukai harmonisasinya.
""", "BAB I; BAB II: evaluasi dan penggunaan model; Louie et al. (2020); Zacharakis et al. (2021)")

add("Pijakan dari penelitian terdahulu", [
    ["DeepBach dan Coconet", "Hadjeres et al. (2017) dan Huang et al. (2017) menjelaskan model, tugas, serta evaluasi keluaran melalui pendengar dan ukuran model."],
    ["Bach Doodle", "Huang et al. (2019) menghitung kuint dan oktaf sejajar pada harmonisasi Coconet dengan music21."],
    ["Rubrik buku ajar", "Yan et al. (2018) menilai harmonisasi melalui sebelas kategori kesalahan dengan penilai manusia."],
    ["Posisi skripsi", "Satu kasus Strube dibaca melalui bantuan program dan keputusan partitur yang menyertakan syarat sumber."]], """
Saya mempertemukan dua pijakan yang paling dekat dengan kebutuhan penelitian. Bach Doodle menunjukkan bahwa gerak sejajar dapat dicatat secara komputasional dalam keluaran model. Yan dan rekan-rekan menunjukkan cara membaca harmonisasi melalui kategori buku ajar serta penilaian partitur. Dalam skripsi ini, program membantu mencari kejadian, sedangkan dasar normatif keputusan ditelusuri ke Strube.

Tugas Yan memakai bas tetap, sementara penelitian saya memakai sopran tetap. Rubriknya karena itu membantu membandingkan cakupan, tetapi bobot pengurangannya tidak langsung saya pindahkan. Klaim posisi penelitian juga saya batasi pada sumber yang sudah ditinjau. Naskah belum menemukan uraian kedua model pada satu kasus Strube yang mengaitkan keputusan dengan tahap dan pengecualian buku itu. Pernyataan ini tidak berarti seluruh penelitian musik AI di dunia sudah diperiksa atau bahwa topik ini pasti pertama.
""", "BAB II: tinjauan pustaka dan posisi penelitian; hadjeres2017; huang2017; huang2019; yan2018")

add("Temuan Bach Doodle sebagai latar", [], """
Angka pada slide ini seluruhnya berasal dari Huang dan rekan-rekan, tahun 2019, halaman 798. Angka tersebut bukan hasil skripsi saya. Mereka menganalisis 21,8 juta harmonisasi Coconet serta 382 chorale Bach dalam gabungan data latih dan validasi yang dibahas. Ukurannya adalah rata-rata kejadian per birama. Pada data penggunaan tersebut, gerak sejajar lebih sering muncul ketika melodi pengguna berada di luar batas wilayah sopran dan lompatan data yang dijadikan pembanding.

Temuan itu memberi alasan untuk memeriksa gerak suara keluaran AI. Lingkupnya tetap perlu dibaca: hanya satu model, melodi dari pengguna, dan dua jenis gerak sejajar. Saya tidak menggunakan nilai ini sebagai ambang lulus atau target angka yang harus direplikasi oleh kasus Strube. Kasus, versi sistem, masukan, serta definisi penghitungan penelitian saya dapat berbeda. Penjelasan pada slide berikutnya berpindah ke rancangan skripsi dan riwayat perubahannya.
""", "Huang et al. (2019), The Bach Doodle, hlm. 798; BAB I–II", kind="table",
    columns=["Rata-rata kejadian per birama", "Coconet", "Chorale Bach"],
    rows=[["Kuint sejajar", "0,365", "0,023"], ["Oktaf sejajar", "0,391", "0,009"]],
    caption="Data penelitian Huang et al. (2019): 21,8 juta harmonisasi Coconet dan 382 chorale Bach dalam data latih/validasi yang dianalisis.")

add("Riwayat rancangan penelitian", [], """
Penelitian ini berjalan sebagai satu proyek yang berlanjut. Proposal v1 dan v2 menjadi tonggak fase proposal. Catatan kelas Seminar Musikologi 2 atas v2 tersimpan sebagai F01 sampai F12. Skripsi v3 melanjutkan fase itu, kemudian v4 memuat perbaikan dari review teman dan audit. Catatan teman P01 sampai P17 mempunyai asal yang berbeda dari masukan dosen.

Sesudah pertemuan Pembimbing I mengenai v4, saya menyusun v5. V5 pertama pada 8–9 Oktober masih memakai banyak melodi dalam satu konteks chorale dan perbandingan zona fermata. Pada 13 Oktober, rancangan berubah menjadi satu kasus dari Strube dengan pembacaan syarat gerak suara. Nomor v5 tetap dipakai untuk naskah aktif. Tanggal-tanggal ini adalah tanggal dokumen atau revisi, bukan tanggal persetujuan akademik. Tanggal pertemuan pertama dengan Pembimbing I belum dinyatakan pasti dalam catatan sumber.

Peralihan v2 ke v3 juga mempunyai alasan teknis dan metodologis. Model pada desain awal tidak menerima kendali masukan yang setara: antarmuka NotaGen yang diperiksa tidak mempertahankan sopran tertentu seperti tugas dua sistem lainnya, dan kondisi A–D tidak membentuk perlakuan yang sebanding. Indeks Strube Score awal juga memerlukan dasar kategori, rumus, dan pembatasan klaim yang lebih jelas. Karena itu, desain beralih ke dua model dengan tugas bersama serta definisi kaidah yang ditelusuri ke sumber. Peralihan v3 ke v4 kemudian memperbaiki sumber sitasi, istilah, struktur penjelasan, pengaturan model, kontrol kualitas, dan pencatatan percobaan. Kesiapan perangkat lunak historis pada tahap tersebut tetap perlu dibedakan dari pelaksanaan data model.
""", "perubahan-v2-ke-v3.md; perubahan-v3-ke-v4.md; perubahan-v4-ke-v5.md; PROGRESS.md", kind="table",
    columns=["Tahap", "Rancangan dan perkembangan"],
    rows=[["Proposal v1–v2", "Tiga model dan kondisi masukan A–D pada desain awal."], ["Skripsi v3–v4", "Dua model, asal melodi Strube/Bach, lima pemeriksaan otomatis."], ["V5, 8–9 Oktober", "40 melodi chorale, lima generasi/model, zona fermata."], ["V5, 13 Oktober", "Satu calon kasus Strube, keputusan kontekstual, profil deskriptif."]],
    caption="Urutan revisi mencatat perubahan desain. Persetujuan dosen dan bukti pelaksanaan dicatat tersendiri.")

add("Masukan yang membentuk revisi", [
    ["Kelas Seminar Musikologi 2", "F01–F12 mencatat judul, pendekatan, rumusan pertanyaan, grand theory, posisionalitas, serta asal rumus."],
    ["Review teman", "P01–P17 berkaitan dengan keterbacaan, istilah, sumber, struktur, dan kejelasan penjelasan."],
    ["Pembimbing I", "G01–G15 menekankan tahap Strube, konteks latihan, lingkup kecil, lokasi kejadian, dan pertimbangan musikal."],
    ["Keputusan peneliti", "Revisi kasus tunggal, dua pertanyaan, dan rencana dua model perlu dibawa kembali untuk kesepakatan akademik."]], """
Saya membedakan asal setiap perubahan agar penjelasan revisi dapat diperiksa. F01–F12 berasal dari catatan saya tentang kelas bersama Bu Suryati dan Pak Galih. Catatan itu berupa parafrasa dan ingatan peneliti, sehingga saya tidak menyajikannya sebagai kutipan persis dosen. P01–P17 adalah review teman. G01–G15 merangkum pertemuan dengan Pak Gathut berdasarkan transkrip yang diserahkan pada 6 Oktober, dengan beberapa bagian percakapan yang masih perlu dikonfirmasi.

Arahan untuk memperhatikan konteks dan memperkecil kasus mendasari perubahan besar. Mempertahankan dua model merupakan pilihan saya yang belum tercatat sebagai persetujuan beliau. Sebagian jawaban metode pada catatan lama masih mencerminkan rancangan kuantitatif lintas melodi. Karena desain sekarang berubah, kesesuaian pendekatan dan kebutuhan hipotesis harus dibahas kembali. Presentasi ini menyampaikan posisi terbaru, sambil menjaga catatan lama sebagai riwayat.
""", "supervision/feedback.md F01–F12, G01–G15; review-teman-2026-10-04.md; perubahan-v4-ke-v5.md")

add("Perubahan pada fokus dan penilaian", [], """
Perubahan ini menyangkut apa yang ditanyakan dan bagaimana keputusan dibuat. Pada desain lama, hitungan pemeriksa dipakai langsung sebagai ukuran utama beberapa larangan. Setelah membaca contoh dan syarat Strube, saya perlu memberi ruang bagi keadaan yang diterima, penyimpangan yang terkonfirmasi, dan kejadian yang belum cukup jelas untuk diputuskan. Perbedaan status tersebut harus tetap terlihat ketika hasil diringkas.

Gerak horizontal tiap suara juga masuk pembacaan. Melihat interval vertikal saja dapat mengabaikan bagaimana alto, tenor, atau bas mencapai dan meninggalkan nada tertentu. Harmonisasi cetak dipakai untuk membahas pilihan yang tersedia pada sumber. Keluaran model dapat berbeda dari contoh cetak dan tetap memenuhi pedoman. Karena itu, selisih nada dengan acuan tidak otomatis menjadi kesalahan. Fermata tetap membantu pembacaan kadens dan metadata yang diperlukan model, dengan peran yang sesuai lingkup kasus.
""", "perubahan-v4-ke-v5.md; BAB I–III", kind="table",
    columns=["Aspek", "Desain sebelumnya", "Rancangan sekarang"],
    rows=[["Fokus", "Hitungan dan zona fermata", "Gerak suara dan konteks keputusan"], ["Tanda program", "Langsung masuk hitungan utama", "Kandidat untuk pembacaan partitur"], ["Harmonisasi acuan", "Perbandingan dengan Bach", "Pilihan cetak Strube, identitas diperiksa"], ["Cakupan suara", "Lima kategori otomatis", "Ditambah gerak melodis dan pola pendamping"]])

add("Perubahan pada skala dan analisis", [], """
Perubahan jumlah melodi mengubah target kesimpulan. Desain 40 melodi dengan lima generasi per model menghasilkan rencana 400 keluaran. Rancangan sekarang merencanakan satu kasus dengan 20 percobaan per model, sehingga jumlah rencana percobaannya 40. Keduanya tidak sebanding sebagai jumlah sampel melodi. Angka 20 pada rancangan sekarang dipilih dari beban pemeriksaan partitur yang rinci, tanpa perhitungan daya statistik untuk repertoar.

Uji berpasangan lintas melodi dan hipotesis zona dari desain lama tidak dibawa ke rancangan kasus. Ringkasan sekarang memakai profil per kriteria, penyebut yang sesuai, serta lokasi dan alasan kejadian. Saya juga tidak menggabungkan kategori menjadi satu indeks penalti berbobot. Perubahan seperti ini perlu diikuti versi instrumen serta protokol yang jelas. Naskah sudah menjelaskan rencana baru, sedangkan perangkat lunaknya belum mengimplementasikan seluruh rencana tersebut.
""", "perubahan-v4-ke-v5.md; research/protocol.md versi 4.0", kind="table",
    columns=["Aspek", "V5, 8–9 Oktober", "V5 aktif"],
    rows=[["Bahan", "40 melodi", "Satu kasus, MODEL 285 sebagai calon"], ["Pengulangan", "5 generasi/model/melodi", "20 percobaan/model, direncanakan"], ["Ringkasan", "Per birama dan indeks bobot", "Per kriteria, kesempatan, episode/durasi"], ["Analisis", "Uji lintas melodi dan zona", "Deskriptif pada satu kasus"]])

add("Pertanyaan dan tujuan penelitian", [
    ["Pertanyaan pertama", "Bagaimana kesesuaian gerak suara harmonisasi DeepBach dan Coconet pada melodi chorale yang dipilih dengan kaidah Strube, setelah memperhatikan kondisi penerapan dan pengecualiannya?"],
    ["Pertanyaan kedua", "Bagaimana perbedaan profil gerak suara kedua model pada kasus tersebut, ditinjau dari kejadian yang berulang, lokasi partitur, dan harmonisasi acuan yang tersedia?"]], """
Dua pertanyaan ini saya pertahankan sesuai naskah aktif. Pertanyaan pertama memerlukan keputusan yang dapat ditelusuri ke kaidah dan konteks. Jawabannya perlu menunjukkan contoh partitur serta alasan mengapa suatu kejadian menyimpang, diterima menurut syarat, atau masih belum dapat diputuskan. Jumlah kejadian membantu merangkum, tetapi tidak menggantikan alasan keputusan.

Pertanyaan kedua memerlukan perbandingan profil kedua sistem pada masukan yang sama. Yang dibandingkan antara lain kriteria yang muncul, lokasi berulang, variasi antarkeluaran, serta pilihan gerak terhadap acuan cetak. Tujuannya mengikuti pertanyaan tersebut: menganalisis kesesuaian kontekstual dan membandingkan profil. Saya tidak menguji penyebab arsitektural atau keunggulan umum model pada seluruh musik. Jika pembimbing menetapkan satu model sebagai lingkup yang lebih sesuai, pertanyaan kedua dan judul harus diselaraskan sebelum pengumpulan data.
""", "BAB I: Pertanyaan Penelitian dan Tujuan Penelitian", kind="questions")

add("Strube sebagai pedoman penelitian", [
    ["Kerangka harmoni", "Fungsi akor dalam hubungan tonal dan penulisan empat suara memberi konteks bagi gerak serta resolusi nada."],
    ["Kaidah dalam tahap pengajaran", "Materi dasar, contoh, syarat, dan pengecualian dibaca menurut posisi pembahasannya dalam buku."],
    ["Operasionalisasi peneliti", "Peneliti menetapkan kejadian, pasangan suara, kesempatan pemeriksaan, dan cara pencatatan berdasarkan sumber."],
    ["Batas penerapan", "Kesesuaian pada kriteria terpilih menjelaskan aspek gerak suara. Mutu estetis seluruh musik memerlukan penilaian lain."]], """
Strube merupakan landasan langsung keputusan musikal dalam penelitian ini. Dalam Preface, ia menjelaskan asal bukunya sebagai bahan pengajaran dan menyebut pertimbangan kebiasaan, cita rasa, serta guru. Pada halaman 6, fungsi trinada I, IV, dan V serta penulisan empat suara menjadi bagian dasar. Kaidah antarsuara lalu berkembang bersama materi akor dan konteks yang lebih lanjut.

Susunan kerangka umum, kaidah, dan definisi operasional adalah cara saya menjelaskan hubungan teori dengan instrumen. Susunan tersebut tidak saya atribusikan sebagai taksonomi tiga tingkat yang dibuat Strube. Pedoman buku juga tidak langsung berubah menjadi kode. Saya harus menentukan peristiwa mana yang dicatat, bagaimana bunyi yang ditahan dibaca, dan informasi apa yang diperlukan untuk menilai pengecualian. Keputusan operasional itu menjadi tanggung jawab peneliti dan perlu dijelaskan sebagai adaptasi.
""", "Strube (1928), Preface dan hlm. 6; BAB II: teori Strube; BAB III: instrumen")

add("Peran teori pendukung", [], """
Saya memakai tiap sumber untuk pekerjaan yang berbeda. Strube mendasari keputusan tentang gerak suara. Briot, Hadjeres, dan Pachet menyediakan kerangka untuk menjelaskan model melalui tujuan, representasi, arsitektur, tantangan, dan strategi. Kerangka ini membantu menghindari penjelasan yang menyederhanakan seluruh perbedaan keluaran menjadi perbedaan LSTM dan CNN.

Pearce, Meredith, dan Wiggins menjelaskan hubungan tujuan sistem dengan cara evaluasi. Huron memberi penjelasan perseptual mengenai kemandirian suara dalam konvensi musikal tertentu. Saya menggunakan penjelasan Huron dalam pembahasan teori, tanpa menyatakan sudah mengukur persepsi pendengar. Flyvbjerg membantu alasan pengetahuan kontekstual dari studi kasus. Lazic membantu menjelaskan pengamatan bertingkat dan risiko pseudoreplikasi. Penerapan kedua sumber metodologi tersebut pada generasi musik merupakan penalaran penelitian ini, bukan hasil eksperimen mereka tentang DeepBach atau Coconet.
""", "BAB II; BAB III; researcher-guide.md", kind="table",
    columns=["Sumber", "Peran dalam penelitian"],
    rows=[["Strube", "Dasar kaidah, konteks, dan keputusan gerak suara"], ["Briot, Hadjeres, Pachet", "Penjelasan sistem generatif dan batas perbandingan"], ["Pearce, Meredith, Wiggins", "Kesesuaian tujuan dan cara evaluasi"], ["Huron", "Penjelasan perseptual keterpisahan suara"], ["Flyvbjerg; Lazic", "Kasus kontekstual dan unit pengamatan bertingkat"]])

add("DeepBach dan Coconet pada tugas yang sama", [], """
DeepBach memakai representasi deretan nada dan simbol penahan, dengan informasi posisi ketukan serta fermata. Model mengisi ulang nada dengan pseudo-Gibbs sampling berdasarkan konteks. Coconet memakai piano roll dan jaringan konvolusional untuk melengkapi partitur yang sebagian dikosongkan. Pelatihannya menggunakan orderless NADE, sedangkan generasinya dapat memakai blocked Gibbs sampling. Penjelasan ini cukup untuk memahami jenis masukan dan proses pengisian suara.

Keduanya dipilih karena dapat diberi sopran tetap pada tekstur chorale. Umur publikasi model tidak menjadi ukuran kecocokan tugas. Sebelum memasukkan model yang lebih baru, saya perlu memastikan apakah antarmukanya benar-benar dapat mempertahankan melodi dan menghasilkan identitas suara yang sepadan. Data pelatihan, representasi, bobot, serta sampling kedua model berbeda. Saya akan mencatat konfigurasi yang dijalankan, sehingga hasil kelak merujuk sistem yang teridentifikasi.
""", "Hadjeres et al. (2017), §2; Huang et al. (2017), §3; BAB II", kind="table",
    columns=["Aspek", "DeepBach", "Coconet"],
    rows=[["Representasi", "Nada, penahan, metadata", "Piano roll empat suara"], ["Jaringan", "Rekuren LSTM", "Konvolusional"], ["Generasi", "Pseudo-Gibbs sampling", "Blocked Gibbs sampling"], ["Tugas penelitian", "Sopran tetap, isi A/T/B", "Sopran tetap, isi A/T/B"]],
    caption="Perbedaan keluaran dibaca pada gabungan konfigurasi sistem yang diuji.")

add("Kesesuaian tugas dan batas perbandingan", [
    ["Alasan memakai Strube", "Kedua model mempelajari chorale Bach dan dapat mengerjakan harmonisasi empat suara. Strube menjadi pedoman eksternal untuk membaca keluarannya."],
    ["Data latih dan kasus", "Kesamaan lingkungan musikal belum membuktikan MODEL 285 berada di luar data latih. Isi pelatihan checkpoint perlu diperiksa tersendiri."],
    ["Representasi", "Piano roll Coconet tidak mempertahankan ejaan enharmonis asli atau membedakan seluruh pengulangan nada dari nada ditahan."],
    ["Cakupan kesimpulan", "Hasil berlaku pada kasus, bobot, representasi, serta pengaturan yang benar-benar diuji."]], """
Model tidak harus dilatih dari buku Strube agar keluarannya dapat diperiksa dengan pedoman tersebut. Yang diperlukan adalah alasan kesesuaian tugas dan keterbukaan terhadap batas evaluasi. Pada penelitian ini, tugasnya adalah menulis tiga suara bawah untuk sopran tetap dalam lingkungan chorale. Saya menilai hasil menurut pedoman yang dinyatakan, tanpa menganggap model memahami tahap pengajaran Strube.

Ada dua ketidakpastian yang perlu dijaga. Pertama, jumlah data pada makalah asli tidak menetapkan riwayat bobot yang akhirnya saya jalankan. Kedua, identitas karya di balik MODEL dan keanggotaannya dalam pelatihan belum terverifikasi. Karena itu, saya belum dapat mengklaim generalisasi pada melodi yang pasti baru bagi model. Ejaan yang hilang dalam representasi juga dapat membatasi keputusan diatonis atau fungsi. Ketika inferensi tidak cukup, status belum dapat diputuskan harus tetap tersedia.
""", "BAB I–II; research/protocol.md 4.0: source eligibility dan models")

add("MODEL 285 sebagai calon kasus", [
    ["Sumber", "Bab Harmonization of Chorales, Strube (1928), hlm. 174–176. MODEL 285 memuat lima sistem harmonisasi empat suara."],
    ["Tugas yang disiapkan", "Sopran menjadi masukan tetap. Harmonisasi cetak menjadi acuan untuk membahas pilihan alto, tenor, dan bas."],
    ["Syarat kelayakan", "Seluruh nada, waktu, tanda diam, birama, dan identitas suara harus terbaca serta terverifikasi sebelum pengumpulan utama."],
    ["Kendala sumber", "Bas awal tertutup cap dan durasi akhir sopran belum pasti. Salinan lebih jelas masih diperlukan."]], """
Pemilihan MODEL didasarkan pada konteks bab dan tersedianya harmonisasi empat suara dalam sumber yang sama. EXERCISES 286 yang menyusul MODEL memuat soal melodi. Saya tidak memperlakukan MODEL sebagai kunci jawaban untuk seluruh latihan itu. Identitas karya serta penyusun harmonisasi cetak juga perlu dibuktikan sebelum menyebut acuan ini sebagai harmonisasi asli Bach.

Ketersediaan gambar halaman belum sama dengan transkripsi yang lengkap. Audit sumber menemukan bagian bas awal yang tertutup cap dan durasi akhir sopran yang masih memerlukan salinan lebih jelas. Saya tidak mengisi bagian tersebut dengan tebakan. Jika sumber tidak dapat dipulihkan secara sahih, rancangan menyediakan kemungkinan memilih kasus lain dari konteks chorale sebelum hasil model diketahui. Alasan pemilihan atau penggantian kasus harus dicatat, sehingga tidak dipengaruhi oleh keluaran yang paling sesuai dengan dugaan peneliti.
""", "BAB III: pemilihan kasus; studi-kasus-model-285-strube.md; research/protocol.md 4.0")

add("Satu kasus dan generasi berulang", [], """
Slide ini membedakan tiga tingkat pengamatan. Kasus musikalnya satu melodi. Setiap percobaan sistem dapat menghasilkan satu keluaran atau catatan kegagalan. Di dalam satu keluaran terdapat banyak transisi atau episode gerak suara. Semua kejadian itu berbagi konteks musikal dari harmonisasi yang sama.

Rencana 20 percobaan per model berarti 40 percobaan pada satu kasus. Angka ini terkait beban pemeriksaan partitur dan masih memerlukan kesepakatan akademik. Generasi berulang dapat menunjukkan variasi jawaban model terhadap masukan tetap apabila tiap percobaan dimulai dari inisialisasi baru dengan pengaturan yang dicatat. Jumlah tersebut tidak membuat penelitian menjadi 40 kasus melodi. Keluaran identik dan percobaan gagal tetap disimpan, karena keduanya juga memberi informasi tentang proses dan variasi sistem. Frekuensi musikal harus menyebut jumlah keluaran layak yang menjadi penyebutnya, bersama jumlah seluruh percobaan.
""", "BAB III: Unit Analisis dan Pengulangan; Lazic (2010); research/protocol.md 4.0", kind="table",
    columns=["Tingkat", "Arti dan rencana jumlah"],
    rows=[["Kasus musikal", "1 melodi chorale"], ["Percobaan model", "20 per model, 40 total, direncanakan"], ["Keluaran layak", "Diketahui sesudah kontrol kualitas"], ["Kejadian gerak suara", "Transisi, keadaan, atau episode di dalam keluaran"]],
    caption="Pengulangan menjelaskan variasi pada masukan tetap. Jumlah kasus melodi tetap satu.")

add("Cakupan pembacaan gerak suara", [
    ["Hubungan antarsuara", "Kuint sejajar, oktaf/unisono sejajar, tumpang tindih, jarak antarsuara, serta persilangan."],
    ["Gerak horizontal", "Langkah, lompatan, arah, dan kelanjutan alto, tenor, serta bas, termasuk gerak sesudah lompatan bas."],
    ["Pola pendamping", "Gerak searah menuju kuint atau oktaf tersembunyi dibaca dengan syarat yang relevan."],
    ["Konteks keputusan", "Akor, penggandaan, nada penuntun, septim, nada nonakor, modulasi, serta kadens membantu penafsiran bila diperlukan."]], """
Peta sumber memuat 14 keluarga yang relevan untuk fokus penelitian. Tujuh keluarga menyusun pembacaan utama dan pendamping; tujuh keluarga lainnya membantu konteks harmoni. Jumlah ini merupakan inventaris yang dipilih dan dijelaskan untuk tugas sekarang. Saya tidak menyatakan sudah membuat pemeriksa seluruh isi buku Strube.

Lima kategori pemeriksa awal memberi titik masuk komputasional, tetapi pembacaan gerak tidak berhenti pada tanda program. Saya juga membaca alur tiap suara dan pola yang memerlukan konteks beberapa nada. Syarat penggunaan kategori berbeda-beda. Ada kejadian yang berbentuk transisi, ada keadaan yang berlangsung lama, dan ada rentang struktural yang melintasi nada hias. Penghitungan perlu mempertahankan perbedaan itu. Peta kaidah mencatat halaman, tahap pembahasan, contoh dan pengecualian, serta bagian yang masih memerlukan pemeriksaan manusia.
""", "BAB II: teori Strube; BAB III: kriteria; study/peta-kaidah-gerak-suara-strube.md")

add("Syarat pada kuint dan oktaf sejajar", [
    ["Pemeriksaan awal", "Catat interval sebelum dan sesudah, arah gerak, pasangan suara, serta apakah kedua nada benar-benar bergerak."],
    ["Kemurnian dan fungsi", "Gerak kuint perlu memperhatikan kemurnian interval, perubahan fungsi, dan kedudukan nada lewat."],
    ["Nada ditahan dan suspensi", "Interval yang ditahan berbeda dari gerak sejajar. Suspensi dan nada hias dapat memerlukan pembacaan rentang struktural."],
    ["Dasar keputusan", "Strube hlm. 9, 12, 23, 34–35, 45, 83, dan 96 memberi konteks yang harus dipilih sesuai kejadian."]], """
Kuint dan oktaf sejajar menjadi perhatian karena berhubungan dengan keterpisahan suara. Namun, membaca dua nomor interval secara berurutan belum cukup. Pada kuint, saya perlu membedakan kemurnian interval serta konteks fungsi dan nada nonakor. Strube membahas keadaan kuint tidak murni menuju kuint murni dan kondisi gerak lewat pada halaman 34–35. Pembahasan IV dan II pada halaman 45 juga menunjukkan bahwa tahap pengajaran memengaruhi anjuran yang diberikan.

Untuk oktaf dan unisono, saya perlu memastikan kedua suara bergerak, bukan sekadar mempertahankan interval. Suspensi serta hiasan memerlukan pemeriksaan yang dapat melintasi satu atau lebih peristiwa. Saya tidak menyatakan setiap konteks lanjut selalu membolehkan paralel. Keputusan harus menyebut syarat tertentu yang benar-benar dapat diterapkan pada kejadian itu. Pemeriksa historis yang hanya mengenali pasangan kuint murni belum mencakup seluruh persoalan tersebut.
""", "Strube (1928), hlm. 9, 12, 23, 34–35, 45, 83, 96; BAB II–III")

add("Tumpang tindih pada Fig. 33 Strube", [
    ["Panel good pertama", "Bas D3 ke G3 melewati F♯3 tenor sebelumnya. Tenor melangkah ke G3."],
    ["Panel avoid", "Tenor B3 ke F♯3 melewati G3 bas sebelumnya. Tenor dan bas sama-sama melompat."]], """
Gambar ini merupakan potongan Fig. 33 dari Strube, halaman cetak 13. Semua label good dan avoid pada gambar dipertahankan. Saya membahas panel good pertama dan panel avoid. Panel good di tengah terlihat dalam sumber, tetapi tidak termasuk dua transkripsi yang dipakai pada pemeriksaan awal proyek.

Pada panel pertama, bas bergerak dari D3 ke G3, sehingga tujuan bas lebih tinggi daripada F-kres3 tenor pada keadaan sebelumnya. Tenor bergerak melangkah menuju G3. Pada panel avoid, tenor turun dari B3 ke F-kres3, melampaui G3 bas sebelumnya, dan bas turun ke D3. Kedua suara melompat. Huruf dan angka di sini menunjukkan tinggi nada bunyi dan nomor oktaf. Perbedaan gerak kedua suara memberi alasan mengapa bentuk tumpang tindih perlu dibaca bersama syarat sumber. Dua MusicXML yang sudah dimasukkan hanya memberi bukti pemeriksaan terhadap kondisi ini; pemeriksaan sumber oleh peneliti dan cakupan kaidah lain masih diperlukan.
""", "Strube (1928), hlm. 13, Fig. 33; assets/strube-fig33-provenance.json; BAB II", kind="image",
    image="assets/strube-fig33.png")

add("Jarak, persilangan, dan gerak melodis", [
    ["Jarak antarsuara", "Ambang lebih dari 12 semiton mencari kandidat. Lama keadaan serta kelonggaran S–A dan A–T ikut diperiksa."],
    ["Persilangan", "Semua pasangan dicatat. Pedoman chorale membedakan melampaui sopran dari persilangan sesekali di suara bawah."],
    ["Gerak tiap suara", "Interval, arah, langkah, lompatan, dan kelanjutan bas menjelaskan bagaimana tiap suara mencapai nada berikutnya."],
    ["Kebutuhan konteks", "Status kejadian memerlukan alasan musikal. Bentuk yang terdeteksi belum menetapkan keputusan menurut Strube."]], """
Jarak antarsuara menunjukkan mengapa keadaan berdurasi perlu dibedakan dari satu transisi. Strube halaman 20 memberi kelonggaran berbeda bagi sopran-alto, alto-tenor, dan bas. Pada alto-tenor, keadaan selebar tepat satu oktaf juga perlu diperiksa karena syarat sementara menyangkut jarak itu. Menghitung hanya berapa kali kisi waktu melampaui ambang dapat menggandakan satu keadaan panjang menjadi banyak kejadian.

Pada halaman 174, Strube membolehkan persilangan sesekali di antara suara bawah bila memperbaiki gerak, dengan batas bahwa suara lain tidak melampaui sopran. Karena itu, saya mencatat seluruh persilangan dan alasan keputusan, termasuk lama serta alurnya. Untuk gerak melodis, pembacaan mengikuti arah suara, banyaknya lompatan, dan kelanjutannya. Pada bas, halaman 23 membahas pengisian kembali celah sesudah lompatan sekst atau oktaf. Pencatatan semiton membantu profil, sementara kategori langkah diatonis tetap membutuhkan ejaan yang cukup.
""", "Strube (1928), hlm. 7, 13, 20, 23, 174; BAB II–III")

add("Program dan keputusan musikal", [
    ["Pencatatan", "Program membaca nada, waktu, interval, pasangan suara, serta lokasi kandidat kejadian."],
    ["Pemeriksaan partitur", "Peneliti membaca konteks akor, jenis gerak, tahap, dan pengecualian sumber yang relevan."],
    ["Status keputusan", "Menyimpang terkonfirmasi, diterima menurut syarat atau pengecualian, atau belum dapat diputuskan."],
    ["Jejak keputusan", "Setiap status disertai sumber halaman, alasan, ketidakpastian, identitas keluaran, serta versi instrumen."]], """
Pemisahan tugas ini menentukan arti angka hasil penelitian. Tanda program adalah kandidat untuk diperiksa. Sebuah kandidat bisa menjadi penyimpangan terkonfirmasi setelah syarat sumber dibaca, bisa diterima dengan alasan tertentu, atau tetap belum pasti. Status ketiga perlu dipertahankan agar kekurangan informasi tidak berubah menjadi keputusan bahwa suatu kejadian bebas masalah.

Saya juga perlu memeriksa bagian tanpa tanda. Program dapat melewatkan pola karena definisi awalnya sempit, misalnya gerak kuint tidak murni menuju kuint murni atau pola struktural melalui nada hias. Naskah merencanakan pemeriksaan semua kandidat dan profil horizontal, ditambah pemilihan kesempatan tanpa tanda dengan seed tercatat untuk lima keluarga awal. Pemeriksaan ulang oleh saya sendiri membantu keterlacakan perubahan keputusan, tetapi tidak memberikan angka kesepakatan antarpenilai. Jika penilai lain dilibatkan kelak, prosedurnya harus ditambahkan secara terbuka.
""", "BAB III: instrumen dan pemeriksaan instrumen; research/protocol.md 4.0")

add("Alur penelitian yang direncanakan", [
    ["1  Sumber dan kriteria", "Pilih kasus yang terbaca lengkap, verifikasi transkripsi, lalu tetapkan kaidah beserta syarat pencatatannya."],
    ["2  Instrumen dan uji coba", "Periksa contoh sumber, waktu, identitas suara, dan kelayakan model. Simpan uji coba terpisah, lalu bekukan prosedur."],
    ["3  Pengumpulan utama", "Mulai setiap percobaan dari inisialisasi baru. Simpan masukan, bobot, pengaturan, keluaran mentah, dan kegagalan."],
    ["4  Analisis kasus", "Periksa kualitas, baca partitur, tentukan status kejadian, lalu bandingkan profil serta lokasi berulang."]], """
Urutan ini menunjukkan hubungan ketergantungan pekerjaan. Sumber yang belum lengkap menghalangi pembekuan masukan. Kriteria yang belum diterjemahkan dengan benar juga menghalangi pemakaian angka sebagai hasil utama. Saya perlu memastikan prosedur teknis dan keputusan musikal dapat berjalan pada kasus yang dipilih sebelum memulai pengumpulan utama.

Uji coba teknis dapat memeriksa kemampuan sistem menerima kasus, mempertahankan sopran, menjaga durasi, serta memisahkan suara. Jika kasus yang sama dipakai saat pilot, keputusan sesudah pilot dibatasi pada kelayakan teknis dan pembekuan prosedur. Pengumpulan utama dimulai lagi dengan inisialisasi baru. Perubahan kriteria atau pengaturan setelah melihat hasil perlu dicatat beserta konsekuensinya. Alur ini merupakan rencana dalam naskah; presentasi kelas tidak menjadi perintah untuk memasang model, menjalankan pilot, atau mengumpulkan data.
""", "BAB III: Rancangan Alur Penelitian; research/protocol.md 4.0")

add("Transkripsi dan kontrol kualitas", [
    ["Sumber tetap tersimpan", "MusicXML sumber dipertahankan sebelum konversi. Nada, durasi, tanda diam, ikatan, birama, dan identitas suara dibaca ulang."],
    ["Kelayakan teknis", "Empat suara terpisah dan monofonik, panjang sesuai masukan, kisi not seperenam belas, serta sopran tetap."],
    ["Keluaran gagal", "Catat seluruh percobaan dan alasan ketidaklayakan. Kegagalan tidak diganti diam-diam dengan hasil tambahan."],
    ["Kelayakan musikal", "Keluaran yang secara teknis layak tetap dianalisis walaupun memuat penyimpangan gerak suara."]], """
Kontrol kualitas memeriksa apakah berkas dapat mewakili tugas yang direncanakan. Saya membutuhkan empat suara yang identitasnya jelas, masing-masing monofonik, panjang waktu yang sesuai, dan sopran yang sama dalam tinggi nada serta waktu bunyi. Identitas suara berasal dari bagian atau saluran sumber. Persilangan tidak diperbaiki dengan menukar label suara.

Kisi waktu direncanakan pada not seperenam belas. Jika sumber tidak dapat direpresentasikan secara sah pada kisi tersebut, saya harus menilai kelayakan kasus atau mengubah protokol dengan alasan yang tercatat. Saya tidak membulatkan ritme diam-diam. Keluaran yang gagal secara teknis tetap berada dalam daftar percobaan. Sebaliknya, keluaran yang mengandung penyimpangan musikal tetap menjadi data jika memenuhi syarat teknis. Memilih hanya hasil yang terdengar atau terlihat paling baik akan mengubah gambaran perilaku model pada kasus yang sama.
""", "BAB III: transkripsi, generasi, kontrol kualitas; research/protocol.md 4.0")

add("Transisi, episode, dan durasi", [
    ["Transisi", "Perubahan tinggi nada ketika kedua suara berbunyi pada kedua ujung pemeriksaan. Tanda diam memutus kesinambungan."],
    ["Episode", "Rentang berkesinambungan ketika kondisi jarak atau persilangan berlaku pada pasangan yang sama, walaupun nada berganti."],
    ["Representasi bersama", "Nada sama yang berurutan disatukan untuk pembacaan bunyi bersama. Berkas mentah dan notasi sumber tetap tersimpan."],
    ["Rentang struktural", "Pola melalui suspensi atau nada hias dicatat tersendiri agar penyebut dan hitungannya sesuai."]], """
Definisi peristiwa menentukan apa yang sebenarnya dihitung. Untuk gerak sejajar, saya memerlukan dua keadaan bunyi yang terhubung oleh perubahan nada. Kedua suara harus berbunyi pada dua ujung itu. Untuk jarak atau persilangan, saya memerlukan lama kondisi dan jumlah episode. Sebuah kondisi yang berlangsung empat langkah kisi tidak otomatis menjadi empat kejadian baru.

Perbandingan representasi juga memerlukan aturan bersama. Coconet tidak membedakan seluruh nada sama yang diulang dari nada ditahan. Rencana penelitian menyatukan nada sama yang berurutan pada representasi perbandingan bunyi, sambil menyimpan sumber mentah. Pengubahan ini harus dijelaskan karena memengaruhi jumlah kesempatan. Durasi episode dilaporkan dalam satuan not seperempat. Saya tidak mengukur waktu audio dalam detik. Pola struktural yang melintasi nada hias disimpan sebagai rentang analisis tersendiri agar tidak dibagi dengan jumlah transisi langsung yang tidak sepadan.
""", "BAB III: instrumen; research/protocol.md 4.0: operational event/time plan")

add("Penyebut dan ketidakpastian keputusan", [
    ["Kriteria transisi", "R = D/O dan Q = U/O. D adalah penyimpangan terkonfirmasi, U kandidat belum diputuskan, O kesempatan yang memenuhi syarat."],
    ["Pelaporan", "Setiap rasio menyertakan pembilang dan penyebut. Jika O = 0, nilai dinyatakan tidak tersedia."],
    ["Kriteria keadaan", "Jarak dan persilangan memakai episode serta durasi terhadap waktu kedua suara berbunyi bersama."],
    ["Pembacaan hasil", "R yang rendah perlu dibaca bersama Q. Banyak keputusan belum pasti membatasi klaim kesesuaian."]], """
Rasio ini merupakan rumusan operasional peneliti untuk merangkum keputusan pada kesempatan yang sama. Huruf g dan r dalam naskah masing-masing menunjuk keluaran dan kriteria. Pembilang tidak boleh mencakup rentang struktural yang tidak berada dalam daftar kesempatan langsung pada penyebut. Dengan demikian, angka tetap terkait kejadian yang benar-benar diperiksa.

Q membantu memperlihatkan keterbatasan keputusan. Misalnya, suatu keluaran dapat mempunyai sedikit penyimpangan terkonfirmasi karena banyak kandidat belum dapat diputuskan. Saya tidak boleh langsung menyebut keluaran itu sangat sesuai dengan Strube. Untuk jarak dan persilangan, penghitungan terpisah memakai episode dan durasi, dengan waktu bunyi bersama sebagai konteks penyebut. Semua nilai harus dilaporkan bersama bilangan asalnya. Slide lampiran memberi contoh hitung dengan angka rekaan yang secara eksplisit merupakan ilustrasi, sehingga tidak tertukar dengan hasil model.
""", "BAB III: Metode Analisis Data, R dan Q; research/protocol.md 4.0")

add("Bentuk analisis dan hasil yang dituju", [
    ["Per keluaran", "Profil gerak A/T/B, keputusan per kriteria, lokasi kejadian, serta alasan penerimaan atau koreksi."],
    ["Per sistem", "Percobaan, keluaran layak/gagal, keluaran unik, median, rentang antarkuartil, dan rentang nilai per kriteria."],
    ["Per lokasi partitur", "Frekuensi keluaran yang memuat pola pada lokasi tertentu, dengan kode suara, kriteria, dan status."],
    ["Pembahasan musikal", "Contoh berulang, contoh diterima melalui syarat, serta kasus belum pasti dipilih dengan alasan yang tercatat."]], """
Hasil yang direncanakan harus menjawab pertanyaan pada dua tingkat. Pada tingkat keluaran, pembaca dapat mengikuti keputusan ke partitur dan sumber. Pada tingkat sistem, pembaca dapat melihat variasi antarkeluaran pada masukan tetap. Jika suatu pola muncul pada sebagian keluaran layak, saya melaporkan pembilang serta jumlah keluaran layaknya, sekaligus jumlah seluruh percobaan.

Contoh diskusi tidak dipilih hanya karena menunjukkan keluaran yang paling buruk atau paling sesuai. Saya ingin memperlihatkan pola berulang, penerimaan bersyarat, dan ketidakpastian yang memengaruhi keputusan. Harmonisasi cetak juga dibaca dengan kriteria yang sama. Median dan rentang antarkuartil adalah rencana ringkasan deskriptif, dengan data individual tetap tersedia. Belum ada nilai dari model yang dapat saya isi pada slide ini. BAB hasil dan kesimpulan akan ditulis sesudah pengumpulan utama, tanpa mengganti data yang belum ada dengan dugaan.
""", "BAB III: Metode Analisis Data; PROGRESS.md: main data dan results")

add("Pemeriksaan instrumen", [
    ["Pemetaan isi", "Kriteria dihubungkan dengan halaman, tahap, contoh diterima/ditolak, serta pengecualian Strube."],
    ["Pemeriksaan teknis", "Uji interval, waktu, tanda diam, nada ditahan, pemetaan suara, episode, dan pembacaan ulang berkas."],
    ["Pemeriksaan musikal", "Baca seluruh kandidat dan bagian tanpa tanda. Catat kejadian yang terlewat dan perubahan keputusan."],
    ["Batas bukti", "Dua panel Fig. 33 memeriksa kondisi tumpang tindih tertentu. Keduanya belum memvalidasi seluruh instrumen."]], """
Pemeriksaan instrumen mempunyai beberapa pekerjaan yang saling mendukung. Pemetaan isi menilai apakah kategori dan prosedur cocok dengan sumber. Uji perangkat lunak menilai apakah kode menerapkan definisi yang dinyatakan. Pembacaan partitur menilai apakah keputusan dapat dibenarkan secara musikal. Masing-masing mempunyai bukti yang berbeda.

Proyek sudah mempunyai dua transkripsi Fig. 33 dengan catatan asal. Pembacaan ulang perangkat lunak menjaga nada dan durasi yang dimasukkan; pemeriksa lama menghasilkan hitungan overlap 0 pada panel good pertama dan 1 pada panel avoid. Bukti itu terbatas pada kondisi dua panel. Ketepatan nada masukan masih perlu diperiksa peneliti terhadap sumber. Keberhasilan uji kode, pengulangan berkas yang sama, dan variasi hasil generator tidak dapat dijadikan pengganti validitas seluruh instrumen. Pemeriksaan ulang oleh penilai yang sama juga tidak sama dengan kesepakatan antarpenilai.
""", "BAB III: Pemeriksaan Instrumen; PROGRESS.md: source and verification evidence")

add("Perkembangan yang sudah tercatat", [
    ["Naskah v5", "BAB I–III, judul, dan abstrak mengikuti arah kasus. Versi aktif memuat 32 kunci sitasi yang telah diperiksa keterhubungannya saat review sebelumnya."],
    ["Bahan Strube", "Peta 14 keluarga kaidah, OCR teks kedua scan, dan skrip OCR yang masuk repositori pada 21 Oktober tersedia."],
    ["Contoh notasi", "Dua panel Fig. 33 mempunyai MusicXML, 16 peristiwa nada, dan catatan asal transkripsi."],
    ["Bahan kerja peneliti", "Panduan belajar, latihan bimbingan, lembar arah, catatan perubahan, serta ledger pembacaan sumber tersimpan."]], """
Bagian ini melaporkan bahan yang tercatat dalam repositori. Angka 32 kunci sitasi merupakan catatan review naskah sebelumnya, bukan klaim bahwa setiap buku sudah dibaca penuh oleh peneliti. Ledger membedakan pemeriksaan sumber oleh asisten dari pembacaan mandiri saya. Demikian pula, OCR teks seluruh halaman berarti seluruh halaman PDF mempunyai keluaran teks, tanpa menjamin proofreading seluruh buku atau ketepatan notasi musik.

Kedua scan yang diproses mencakup 147 halaman PDF bahasa Inggris dan 91 halaman PDF bahasa Indonesia. Angka tersebut adalah jumlah halaman PDF scan, bukan nomor halaman cetak buku. Pada 21 Oktober, commit 7c64d76 menambahkan dua skrip OCR ke repositori, yaitu ocr_strube.py dan ocr_strube_tesseract.py. Ini menambahkan jejak prosedur pemrosesan teks yang sudah ada, tanpa mengubahnya menjadi transkripsi musik. Verifikasi OCR bertanggal 11 Oktober membatasi pemeriksaan manual pada halaman terpilih.

Peta kaidah dan contoh Fig. 33 membantu penyiapan instrumen. Bahan yang tersedia belum menyediakan hasil harmonisasi utama. Presentasi ini memakai pemeriksaan status dokumen dan sumber yang ada; saya tidak menjalankan ulang generasi atau mengklaim adanya data baru dari model.
""", "PROGRESS.md (13 Oktober); aset Fig. 33; skrip OCR, commit 7c64d76 (21 Oktober)")

add("Rancangan tertulis dan perangkat lunak", [], """
Perbedaan ini perlu disampaikan karena repositori sudah memuat banyak perintah eksperimen. Perintah bawaan yang tersedia masih berasal dari protokol historis 3.0 dengan instrumen 2.0. Desain itu memakai 40 melodi serta zona fermata. Menjalankannya sekarang tidak otomatis melaksanakan BAB III yang sudah direvisi.

Protokol 4.0 dan instrumen kontekstual 3.0 sudah dijelaskan sebagai rencana tertulis. Implementasi perlu menambahkan atau menyesuaikan rekaman konteks, episode, seluruh persilangan, gerak horizontal, penyebut, dan pemeriksaan pola yang terlewat. Rencana ini juga perlu diperiksa melalui sumber dan pilot sebelum dibekukan. Saya mempertahankan kode serta hasil historis untuk keterlacakan. Keberadaan pipeline lama atau dry-run dengan model palsu tidak memberi bukti hasil DeepBach dan Coconet untuk kasus sekarang. Penyiapan presentasi tidak mengubah evaluator atau protokol.
""", "research/protocol.md: pembuka, versi 4.0; PROGRESS.md", kind="table",
    columns=["Lapisan", "Status yang tercatat"],
    rows=[["BAB I–III aktif", "Sudah memakai rancangan kasus Strube"], ["Protokol 4.0", "Rencana tertulis, belum dibekukan"], ["Instrumen kontekstual 3.0", "Direncanakan, belum diimplementasikan penuh"], ["Perintah eksperimen bawaan", "Masih protokol historis 3.0 / instrumen 2.0"], ["Pilot dan data utama", "Belum dijalankan untuk rancangan kasus"]])

add("Pekerjaan sebelum pengumpulan utama", [
    ["Sumber dan kasus", "Dapatkan notasi yang jelas, periksa transkripsi lengkap, dan tetapkan kelayakan kasus sebelum melihat hasil model."],
    ["Kesepakatan akademik", "Konfirmasikan satu/dua model, kriteria, jumlah percobaan, metode deskriptif, kebutuhan hipotesis, dan format prodi."],
    ["Instrumen dan protokol", "Implementasikan rencana kontekstual, periksa contoh dan kejadian terlewat, lalu jalankan pilot terpisah saat diminta."],
    ["Pengumpulan dan penulisan", "Bekukan prosedur, kumpulkan semua percobaan, analisis partitur, kemudian tulis hasil serta kesimpulan."]], """
Saya masih memerlukan keputusan dan bukti pada beberapa bagian yang saling berkaitan. Salinan yang lebih jelas dapat memastikan apakah MODEL 285 memang layak. Kesepakatan lingkup dengan pembimbing menentukan apakah dua sistem tetap dibandingkan dan berapa percobaan yang dapat dipertanggungjawabkan untuk pemeriksaan rinci. Jumlah model serta percobaan tidak saya anggap sudah disetujui hanya karena tertulis dalam naskah.

Setelah itu, perangkat lunak perlu mengikuti definisi penelitian. Pilot membantu memastikan kelayakan teknis dan beban kerja, dengan keluaran yang dipisahkan dari data utama. Pengumpulan utama baru dimulai setelah pembekuan prosedur. Bila ada perubahan sesudahnya, versi dan analisis yang terdampak harus dicatat. Bagian hasil, kesimpulan, dan abstrak berbasis temuan akan mengikuti data sebenarnya. Format tugas akhir dan persyaratan front matter juga perlu dikonfirmasi karena naskah masih memakai kelas format proposal yang sama.
""", "PROGRESS.md: completion gates; researcher-guide.md; rancangan-kesepakatan-v5.md")

add("Batas kesimpulan penelitian", [
    ["Satu kasus", "Profil menjelaskan respons sistem pada melodi yang dipilih. Kesimpulan lintas repertoar memerlukan kasus tambahan."],
    ["Konfigurasi sistem", "Data latih, representasi, bobot, dan prosedur berbeda. Perbandingan ini tidak mengisolasi sebab arsitektural."],
    ["Penafsiran musikal", "Ejaan serta fungsi yang belum pasti dapat membatasi keputusan. Alasan dan alternatif perlu tetap terlihat."],
    ["Lingkup manfaat", "Penelitian menyediakan analisis gerak suara. Keindahan, persepsi pendengar, dan peningkatan hasil belajar belum diukur."]], """
Batas ini menentukan cara saya nanti menulis kesimpulan. Jika suatu profil ditemukan pada kasus yang dipilih, saya dapat menjelaskannya dengan kondisi sistem dan kriteria yang dipakai. Saya belum dapat menyatakan bahwa salah satu model lebih baik untuk seluruh musik atau bahwa jaringan tertentu menyebabkan setiap perbedaan. Sumber kasus yang mungkin berada dalam data latih juga membatasi klaim tentang respons pada melodi yang belum pernah dipelajari.

Keputusan partitur membawa penafsiran. Peneliti perlu menyimpan dasar halaman serta ketidakpastian ketika ejaan atau fungsi memiliki lebih dari satu kemungkinan. Program yang konsisten menghitung definisinya belum tentu mencakup seluruh alasan musikal. Manfaat praktis yang saya tuju adalah bahan pemeriksaan keluaran AI dalam pelajaran harmoni. Klaim bahwa mahasiswa belajar lebih baik atau pendengar menyukai hasilnya memerlukan penelitian dengan data yang memang mengukur hal tersebut.
""", "BAB I: manfaat; BAB II: evaluasi dan Huron; BAB III: batas analisis")

add("Butir untuk diskusi kelas", [
    ["Lingkup kasus", "Apakah satu kasus dengan pembacaan rinci sudah sesuai dengan pertanyaan dan beban skripsi ini?"],
    ["Jumlah model", "Apakah perbandingan DeepBach–Coconet tetap membantu, atau perlu dibatasi menjadi satu model?"],
    ["Dasar keputusan", "Apakah pemetaan syarat Strube dan tiga status keputusan sudah cukup jelas untuk ditelusuri pembaca?"],
    ["Metode dan sumber", "Apa yang perlu diperjelas tentang pendekatan, kebutuhan hipotesis, notasi acuan, serta format penelitian prodi?"]], """
Saya mengharapkan masukan yang dapat diterjemahkan menjadi langkah kerja. Untuk lingkup, saya perlu mengetahui apakah kedalaman kasus sesuai dengan tujuan skripsi. Untuk jumlah sistem, saya perlu menimbang manfaat pertanyaan perbandingan terhadap beban pemeriksaan serta arahan Pembimbing I. Untuk instrumen, saya ingin menguji apakah pembaca dapat mengikuti hubungan antara kaidah, syarat, data partitur, dan keputusan.

Masukan dari teman dan dosen akan dicatat dengan nama pembicara bila diketahui, nomor slide, isi masukan, serta tindak lanjut. Saya akan membedakan kutipan yang benar-benar tercatat dari parafrasa. Usulan kelas juga perlu dibedakan dari keputusan yang kemudian disepakati bersama pembimbing. Berkas masukan sesi ini sudah disiapkan dalam folder presentasi, masih kosong sebelum diskusi berlangsung. Perubahan naskah sesudah kelas akan merujuk masukan tertentu dan bukti perubahan yang benar-benar dikerjakan.
""", "Pertanyaan diskusi dari butir terbuka PROGRESS.md dan rancangan-kesepakatan-v5.md", kind="questions")

# Lampiran merupakan bahan diskusi, bukan bagian pengumpulan data.
add("Lampiran · Rincian kriteria", [], """
Lampiran ini membantu ketika dosen atau teman meminta hubungan langsung antara kriteria dan halaman sumber. Kaidah dibaca bersama pembahasan dan pengecualiannya, sehingga halaman yang sama dapat mendukung pekerjaan yang berbeda. Tabel memberi peta awal untuk kembali ke buku.

Lima kategori komputasional awal tidak mencakup seluruh pembacaan. Gerak melodis menjadi bagian wajib profil, sedangkan interval tersembunyi merupakan pola pendamping. Kategori yang memerlukan fungsi akor, ejaan, atau rangkaian struktural harus menyimpan informasi yang cukup sebelum diberi status. Daftar ini tidak memberi lisensi menerapkan satu ambang numerik secara sama pada semua bab. Peneliti tetap memeriksa konteks chorale dan bunyi aturan yang relevan dengan tiap kejadian.
""", "BAB II–III; peta-kaidah-gerak-suara-strube.md", kind="table", appendix=True,
    columns=["Kriteria", "Pemeriksaan", "Strube, hlm."],
    rows=[["Kuint sejajar", "Interval, arah, kemurnian, fungsi", "9, 12, 34–35, 45"], ["Oktaf/unisono", "Gerak, nada ditahan, suspensi", "9, 23, 83, 96"], ["Tumpang tindih", "S–A, A–T, T–B dan jenis gerak", "12–13"], ["Jarak dan persilangan", "Pasangan, episode, durasi, konteks", "20, 174"], ["Melodis dan tersembunyi", "Alur A/T/B dan jenis pendekatan", "7, 12–13, 20, 23, 109"]])

add("Lampiran · Identitas dan pengaturan model", [], """
Tabel ini menyajikan pengaturan awal yang tertulis dalam BAB III dan protokol 4.0. Pengaturan efektif harus diperiksa terhadap implementasi saat pilot diminta. Sebuah nilai pada dokumen belum membuktikan wrapper benar-benar menerimanya atau bahwa generasi sudah dijalankan.

Untuk DeepBach, implementasi PyTorch yang direncanakan berada pada commit 6d75cb940f3aa53e02f9eade34d58e472e0c95d7. Coconet direncanakan memakai paket @magenta/music versi 1.23.1 dengan checkpoint coconet/bach. Hash bobot dan paket aktual, konfigurasi, identitas masukan, serta hasil setiap percobaan perlu disimpan. Seed DeepBach dicatat dari bilangan awal protokol. Antarmuka Coconet perlu diaudit untuk dukungan seed. Nomor percobaan sama pada dua sistem hanya membantu administrasi dan tidak membentuk pasangan acak yang sepadan. Parameter kedua sistem tidak langsung bermakna setara meskipun sama-sama dinamai temperature atau iterasi.
""", "BAB III: objek dan generasi; research/protocol.md 4.0", kind="table", appendix=True,
    columns=["Item rencana", "DeepBach", "Coconet"],
    rows=[["Implementasi", "PyTorch, commit tercatat", "@magenta/music 1.23.1"], ["Bobot", "Bobot implementasi, hash dicatat", "coconet/bach, hash dicatat"], ["Iterasi awal", "500", "96"], ["Temperature awal", "1,0", "0,99"], ["Seed", "Turunan seed protokol dicatat", "Dukungan antarmuka perlu diaudit"]],
    caption="Pengaturan awal dalam rencana. Nilai efektif dan kelayakannya belum diverifikasi melalui pilot kasus ini.")

add("Lampiran · Bentuk lembar keputusan", [
    ["Identitas dan lokasi", "Kode keluaran, versi instrumen, kriteria, pasangan/suara, birama, ketukan, serta waktu awal/akhir."],
    ["Bukti musikal", "Nada sebelum/sesudah, interval, arah, langkah/lompatan, lama keadaan, dan konteks harmoni."],
    ["Keputusan", "Status, kaidah dan halaman Strube, syarat yang berlaku, alasan, serta ketidakpastian."],
    ["Pemeriksaan ulang", "Asal kandidat atau temuan tanpa tanda, perubahan keputusan, alasan perubahan, serta hubungan dengan contoh partitur."]], """
Lembar keputusan direncanakan menjadi penghubung data simbolik dengan pembahasan. Kode keluaran memungkinkan pembaca menemukan berkas asal. Lokasi serta waktu memungkinkan pencocokan dengan partitur. Nada dan interval memberikan bukti yang diperiksa. Kolom sumber dan alasan menjelaskan mengapa bukti tersebut mendapat status tertentu.

Saya juga perlu mengetahui apakah suatu kejadian berasal dari tanda program atau ditemukan ketika memeriksa bagian tanpa tanda. Jika satu jenis pola terlewat, pemeriksaan pola sejenis pada keluaran lain perlu dicatat sebelum ringkasan kriteria dibuat. Kolom keputusan tetap menyediakan pilihan belum dapat diputuskan. Contoh yang belum pasti tidak perlu dipaksa masuk kategori diterima atau menyimpang untuk memudahkan statistik. Format pada slide ini menjelaskan rencana isian; belum ada baris hasil utama dari model yang ditampilkan.
""", "BAB III: instrumen dan keterlacakan; research/protocol.md 4.0", appendix=True)

add("Lampiran · Contoh rasio transisi", [
    ["Angka ilustratif", "Dalam satu keluaran rekaan, satu kriteria mempunyai O = 20 kesempatan, D = 2 penyimpangan, dan U = 3 kandidat belum diputuskan."],
    ["Penghitungan", "R = 2/20 = 0,10. Q = 3/20 = 0,15. Pembilang dan penyebut menyertai kedua rasio."],
    ["Pembacaan", "Sepuluh persen kesempatan memuat penyimpangan terkonfirmasi dan lima belas persen masih belum diputuskan."],
    ["Batas contoh", "Angka ini hanya menjelaskan rumus. Angka ini tidak berasal dari DeepBach, Coconet, atau harmonisasi cetak."]], """
Saya menggunakan angka rekaan agar cara menghitung dapat dijelaskan tanpa mengisi hasil yang belum tersedia. Dua puluh kesempatan dalam contoh ini adalah jumlah kesempatan pemeriksaan satu kriteria pada satu keluaran. Angka itu tidak berkaitan dengan rencana dua puluh percobaan per model. D dan U harus berasal dari daftar kesempatan yang sama dengan O.

Hasil 0,10 dan 0,15 menunjukkan dua informasi yang berbeda. Yang pertama merangkum penyimpangan yang telah terkonfirmasi. Yang kedua menunjukkan keputusan yang masih terbuka. Saya tidak menyebut sisa 75 persen otomatis sebagai kejadian diterima menurut pengecualian, sebab sebagian kesempatan dapat tidak menghasilkan kandidat sama sekali. Kandidat yang diterima dilaporkan tersendiri beserta alasan. Bila tidak ada kesempatan yang memenuhi syarat, rasio dinyatakan tidak tersedia. Contoh ini merupakan penjelasan matematis dan bukan simulasi keluaran model.
""", "Rumus BAB III; angka dibuat hanya untuk ilustrasi penghitungan", appendix=True)

add("Lampiran · Contoh episode jarak", [
    ["Keadaan rekaan", "Jarak di atas ambang bertahan selama tiga langkah kisi not seperenam belas pada pasangan yang sama."],
    ["Unit pencatatan", "Keadaan itu membentuk satu episode berdurasi 3/4 satuan not seperempat, selama kondisi tetap berkesinambungan."],
    ["Dasar keputusan", "Ambang menemukan kandidat. Lama keadaan, pasangan suara, dan syarat Strube menentukan pembacaan musikal."],
    ["Batas contoh", "Ilustrasi ini menjelaskan pengelompokan waktu. Angka dan keadaan ini bukan hasil penelitian."]], """
Pada kisi not seperenam belas, satu langkah sama dengan seperempat satuan not seperempat. Tiga langkah karena itu berdurasi 0,75 satuan not seperempat. Bila kondisi jarak dan pasangan suara tetap sama tanpa putus, pencatatan membentuk satu episode. Nada boleh berganti selama kondisi yang didefinisikan tetap berlangsung.

Jika salah satu suara berhenti atau kondisi hilang, episode berakhir. Durasi episode perlu dibandingkan dengan waktu kedua suara benar-benar berbunyi bersama. Keadaan yang sama pada bagian dengan tanda diam tidak boleh memakai seluruh panjang partitur sebagai penyebut secara otomatis. Pengelompokan waktu ini merupakan pilihan operasional peneliti yang perlu diimplementasikan dan diuji. Status menurut Strube tetap membutuhkan pembacaan syarat sesekali atau sementara, sehingga panjang keadaan dan ambang teknis belum memberi keputusan normatif sendiri.
""", "BAB III: episode dan durasi; contoh rekaan untuk menjelaskan satuan waktu", appendix=True)

add("Lampiran · Metode dan hipotesis", [
    ["Pendekatan tertulis", "Studi kasus evaluatif dengan analisis partitur, pencatatan komputasional, dan statistik deskriptif."],
    ["Peran angka", "Hitungan merangkum keputusan yang mempunyai dasar partitur. Alasan musikal tetap menjadi bagian jawaban penelitian."],
    ["Hipotesis", "Naskah aktif tidak memakai hipotesis statistik tentang populasi chorale atau uji berpasangan lintas melodi."],
    ["Butir kesepakatan", "Penamaan pendekatan dan kebutuhan hipotesis menurut prodi perlu dibahas kembali setelah perubahan desain."]], """
Jika ditanya apakah penelitian ini kualitatif atau kuantitatif, saya mulai dari prosedur yang tertulis. Rancangannya studi kasus evaluatif. Saya membaca partitur dan menentukan status berdasarkan sumber, kemudian meringkas keputusan itu secara numerik. Naskah tidak mengajukan studi partisipan atau desain mixed methods tersendiri. Penggunaan angka saja belum menjelaskan target inferensi atau membuat kejadian di dalam satu partitur menjadi sampel independen.

Pertanyaan ini perlu dibahas terbuka karena catatan kelas pada versi sebelumnya meminta kejelasan variabel dan hipotesis. Jawaban lama mengikuti desain yang berbeda. Setelah beralih ke satu kasus, naskah aktif memakai perbandingan deskriptif tanpa hipotesis statistik untuk populasi chorale. Saya tidak membawa power analysis atau Wilcoxon lintas melodi dari rancangan sebelumnya. Jika prodi atau pembimbing meminta bentuk lain, perubahan harus diselaraskan pada pertanyaan, unit, analisis, dan protokol sebelum data utama.
""", "BAB II: Hipotesis; BAB III: Metode Pendekatan; feedback.md F02/F07/F11, G07", appendix=True)

add("Lampiran · Risiko dan respons yang direncanakan", [], """
Risiko yang disebut di sini sudah berkaitan dengan kondisi sumber dan rancangan. Jika sumber tetap tidak terbaca, memilih kasus lain sebelum generasi merupakan langkah yang tersedia, dengan dokumentasi alasan. Jika kedua sistem tidak dapat menerima representasi yang sama, saya perlu menilai kelayakan tugas dan lingkup, tanpa memaksa konversi yang mengubah melodi diam-diam.

Jika jumlah keluaran layak kecil, jumlah itu harus terlihat dalam laporan. Percobaan tambahan memerlukan revisi rencana sebelum batch berikutnya, sambil menyimpan kegagalan sebelumnya. Jika banyak keputusan bergantung pada ejaan yang hilang, saya melaporkan alternatif dan batas keputusan. Jika cakupan dua sistem terlalu besar, saya perlu membahas satu model bersama pembimbing dan menyelaraskan judul serta pertanyaannya. Respons ini menjaga hubungan antara persoalan dan keputusan yang bisa diperiksa; belum ada risiko tersebut yang saya laporkan sebagai hasil pilot kasus.
""", "BAB III; research/protocol.md 4.0; PROGRESS.md", kind="table", appendix=True,
    columns=["Risiko", "Respons yang dicatat dalam rancangan"],
    rows=[["Notasi sumber tetap kabur", "Cari salinan jelas atau pilih kasus lain sebelum hasil diketahui"], ["Keluaran teknis tidak layak", "Simpan kegagalan dan laporkan penyebut aktual"], ["Ejaan/fungsi ambigu", "Catat inferensi, alternatif, atau status belum diputuskan"], ["Beban dua model berlebihan", "Bahas lingkup dan selaraskan pertanyaan sebelum pengumpulan"]])

add("Lampiran · Rujukan model dan evaluasi", [
    ["Hadjeres, Pachet, Nielsen (2017)", "DeepBach: A Steerable Model for Bach Chorales Generation. PMLR 70, 1362–1371."],
    ["Huang et al. (2017)", "Counterpoint by Convolution. ISMIR, 211–218."],
    ["Huang et al. (2019)", "The Bach Doodle: Approachable Music Composition with Machine Learning at Scale. ISMIR, 793–800."],
    ["Yan et al. (2018)", "Part-invariant Model for Music Generation and Harmonization. ISMIR, 204–210."]], """
Daftar ini memuat sumber langsung untuk model dan dua pijakan evaluasi. Detail bibliografi mengikuti berkas references.bib skripsi. Halaman yang mendukung angka Bach Doodle adalah 798. Bagian model dibaca bersama §2 DeepBach dan §3 Coconet. Rubrik Yan perlu dilihat dalam konteks tugas bas dan penilai manusia, bukan dipindahkan sebagai skor Strube.

Tautan sumber asli tersedia dalam catatan sumber paket presentasi. Presentasi ini menyintesis naskah serta pemeriksaan sumber yang sudah tercatat. Penyusunan slide tidak menambah klaim bahwa seluruh penelusuran pustaka sudah diperbarui sampai hari ini. Untuk membaca sumber pendukung lain, gunakan daftar pustaka naskah dan ledger pembacaan; perhatikan apakah pemeriksaan suatu klaim berasal dari teks lengkap, abstrak, atau masih memerlukan bacaan peneliti.
""", "thesis/references.bib: hadjeres2017, huang2017, huang2019, yan2018", appendix=True)

add("Lampiran · Rujukan teori dan metode", [
    ["Strube (1928)", "The Theory and Use of Chords: A Text-book of Harmony. Oliver Ditson Company."],
    ["Briot, Hadjeres, Pachet (2020)", "Deep Learning Techniques for Music Generation. Kerangka model pada hlm. 11–13."],
    ["Pearce, Meredith, Wiggins (2002); Huron (2001)", "Tujuan evaluasi komposisi otomatis dan penjelasan perseptual gerak suara."],
    ["Flyvbjerg (2006); Lazic (2010)", "Five Misunderstandings About Case-Study Research dan The Problem of Pseudoreplication in Neuroscientific Studies."]], """
Strube menjadi sumber utama kaidah dan pembacaan contoh. Briot dan rekan-rekan membantu penjelasan sistem. Pearce dan rekan-rekan membantu membatasi evaluasi pada tujuan yang dipilih. Huron membantu pembahasan teoritis mengenai kemandirian suara, dengan pengakuan pada konvensi musikalnya.

Flyvbjerg dan Lazic dipakai secara metodologis dengan batas penerapan yang dijelaskan pada naskah. Sumber pertama mendukung nilai pengetahuan kontekstual dari studi kasus. Sumber kedua menjelaskan masalah pengamatan bertingkat dan independensi. Kedua sumber tidak menetapkan bahwa dua puluh generasi per model merupakan jumlah yang tervalidasi untuk penelitian saya. Jumlah itu tetap pilihan beban pemeriksaan. Untuk syarat tiap kaidah dan lokasi sumber yang lebih rinci, peta kaidah dan catatan pembacaan proyek memberikan rute kembali ke halaman yang dipakai.
""", "thesis/references.bib; BAB II–III; study/researcher-guide.md", appendix=True)


def compact_deck():
    """Ten classroom slides, with concise speaking notes."""
    cover = dict(slides[0])
    slides.clear()
    cover["notes"] = "Saya membahas skripsi v5 tentang gerak suara pada harmonisasi DeepBach dan Coconet menurut Strube. Tugasnya mempertahankan sopran dan menghasilkan alto, tenor, serta bas. Presentasi ini menjelaskan objek, research gap, teori, metode, hipotesis kerja, dan perubahan rancangan."
    slides.append(cover)

    add("Objek material dan objek formal", [
        ["Objek material", "Harmonisasi simbolik empat suara hasil DeepBach dan Coconet."],
        ["Objek formal", "Kesesuaian gerak suara menurut kaidah Strube beserta syarat dan pengecualiannya."],
        ["Batas kajian", "Sopran tetap; model menghasilkan alto, tenor, dan bas."]],
        """Objek material menjawab apa yang diteliti: harmonisasi hasil kedua model dalam bentuk data nada dan waktu. Objek formal menjelaskan sudut pembacaannya: kesesuaian gerak suara menurut Strube. Jadi, model merupakan sistem penghasil dan kategori pembanding; bahan yang dianalisis adalah musik keluarannya. Penelitian memeriksa hubungan antarsuara sekaligus gerak horizontal alto, tenor, dan bas. Tidak ada partisipan atau uji dengar. Pembagian material–formal ini memperjelas objek yang sudah dijelaskan dalam BAB III.""",
        "BAB I–III; catatan kelas F02 tentang objek dan pendekatan", kind="brief")
    add("Masalah, pertanyaan, dan tujuan", [
        ["Masalah", "Keluaran harmonisasi perlu diperiksa pada kejadian musikal tertentu."],
        ["Pertanyaan", "Bagaimana kesesuaiannya dengan Strube, dan bagaimana profil kedua model berbeda?"],
        ["Tujuan", "Menjelaskan keputusan gerak suara dan membandingkan profil pada kasus yang sama."]],
        """Penilaian pendengar atau kedekatan statistik belum menjelaskan alasan penerimaan setiap pilihan gerak suara. Bach Doodle memberi pijakan penghitungan paralel, sedangkan Yan et al. memberi contoh penilaian melalui kategori buku ajar. Pertanyaan pertama saya memeriksa kesesuaian setelah syarat dan pengecualian Strube dibaca. Pertanyaan kedua membandingkan jenis kejadian, lokasi berulang, dan pilihan terhadap acuan cetak. Manfaat yang dituju ialah bahan pemeriksaan bagi pengajar dan mahasiswa harmoni. Peningkatan hasil belajar tidak diukur.""",
        "BAB I; Huang et al. (2019); Yan et al. (2018)", kind="brief")
    add("Landasan teori dan operasionalisasi", [
        ["Grand theory", "Teori harmoni Strube: fungsi akor dan penulisan empat suara."],
        ["Kaidah", "Gerak suara dibaca menurut tahap, contoh, syarat, dan pengecualian Strube."],
        ["Operasionalisasi", "Peneliti menetapkan kejadian, indikator, penyebut, dan dasar keputusan."]],
        """Strube menjadi dasar langsung penilaian musikal. Fungsi akor membantu membaca tujuan gerak dan resolusi; kaidah merinci hubungan suara. Pembagian kerangka umum, kaidah, dan operasionalisasi merupakan susunan penjelasan peneliti, bukan pembagian yang dinyatakan Strube. Briot et al. membantu menjelaskan sistem generatif, Pearce et al. membatasi tujuan evaluasi, dan Huron memberi penjelasan perseptual. Flyvbjerg mendukung pembacaan kasus kontekstual; Lazic membantu membedakan kasus dan pengamatan berulang. Hasil penelitian tetap mengenai gerak suara, dengan kriteria yang dapat ditelusuri ke sumber.""",
        "BAB II; Strube (1928), Preface, hlm. 6–23 dan 174", kind="brief")
    add("Pendekatan dan hipotesis", [
        ["Pendekatan", "Studi kasus evaluatif dengan analisis partitur."],
        ["Data dan analisis", "Pencatatan komputasional dan statistik deskriptif mendukung keputusan musikal."],
        ["Hipotesis", "Tidak memakai hipotesis statistik tentang populasi chorale."]],
        """Naskah aktif menyebut studi kasus evaluatif: partitur dibaca, kejadian dicatat secara numerik, lalu hasil diringkas secara deskriptif. Penjelasan ini memperjelas pekerjaan penelitian tanpa menambahkan desain mixed methods yang belum dirumuskan. Angka meliputi interval, jumlah, durasi, dan variasi keluaran. Alasan musikal mendasari status setiap kejadian. Satu kasus tidak menyediakan pasangan melodi untuk uji lintas melodi. Catatan kelas lama meminta kejelasan pendekatan dan hipotesis; kesesuaiannya dengan rancangan kasus sekarang masih perlu dikonfirmasikan kepada pembimbing/prodi.""",
        "BAB II: Hipotesis; BAB III: Metode Pendekatan; F02/F07/F11 dan G07", kind="brief")
    add("Kasus dan unit analisis", [
        ["Kasus musikal", "Satu chorale Strube. MODEL 285 masih calon; notasi perlu diperjelas."],
        ["Keluaran", "Rencana 20 percobaan per model. Jumlah dan dua model belum disepakati pembimbing."],
        ["Kejadian", "Transisi atau episode gerak suara di dalam tiap keluaran."]],
        """Kasus dipilih secara purposif karena konteks chorale dan adanya harmonisasi acuan cetak. Bas awal serta durasi akhir sopran MODEL 285 belum terbaca pasti, sehingga transkripsi lengkap belum terverifikasi. Satu melodi dengan 40 percobaan tetap satu kasus. Jumlah 20 per model mengikuti rencana beban pemeriksaan, bukan power statistik. Simpan keluaran identik dan kegagalan; jumlah keluaran layak diketahui sesudah kontrol kualitas. Acuan cetak belum terverifikasi sebagai harmonisasi asli Bach dan tidak menjadi satu-satunya jawaban yang diterima.""",
        "BAB III: pemilihan kasus, unit analisis, pengulangan; protokol 4.0", kind="brief")
    add("Pembanding, kondisi, dan indikator", [
        ["Pembanding", "DeepBach dan Coconet pada konfigurasi yang dicatat."],
        ["Kondisi bersama", "Sopran yang sama dalam tinggi nada dan waktu bunyi."],
        ["Indikator", "Jenis, jumlah, lokasi, dan durasi kejadian; gerak melodis serta status keputusan."]],
        """DeepBach memakai jaringan LSTM dan metadata, sedangkan Coconet memakai jaringan konvolusional serta piano roll. Keduanya dapat mengisi tiga suara bawah untuk sopran tetap. Kategori sistem adalah pembanding; sopran menjadi kondisi bersama, sedangkan gerak suara menjadi aspek yang diamati. Ini tidak diposisikan sebagai eksperimen yang mengisolasi sebab arsitektural. Kriteria mencakup paralel, tumpang tindih, jarak, persilangan, gerak melodis, serta interval tersembunyi sebagai pendamping. Transisi dilaporkan bersama kesempatan yang sesuai; jarak/persilangan memakai episode dan durasi. Keterbatasan ejaan nada dapat menyisakan ketidakpastian.""",
        "BAB II: model; BAB III: Variabel dan Aspek yang Diamati serta analisis", kind="brief")
    add("Instrumen dan posisi peneliti", [
        ["Instrumen", "Peta kaidah, pemeriksa kandidat berbasis music21, dan lembar keputusan partitur."],
        ["Keputusan", "Menyimpang terkonfirmasi, diterima bersyarat, atau belum dapat diputuskan."],
        ["Posisionalitas", "Peneliti mempelajari Strube; sumber, alasan, dan ketidakpastian perlu dicatat."]],
        """Program membantu menemukan kandidat. Peneliti memeriksa konteks dan memberi status berdasarkan sumber. Latar sebagai mahasiswa musik yang mempelajari Strube dapat memengaruhi pilihan kasus dan penafsiran. Pengendaliannya berupa kriteria sebelum pengumpulan, penyimpanan seluruh percobaan, alasan keputusan, serta pemeriksaan bagian tanpa tanda program. Pemeriksaan teknis kode dibedakan dari validasi musikal. Dua panel Fig. 33 baru memberi bukti terbatas untuk kondisi tumpang tindih; pemeriksaan ulang sendiri bukan kesepakatan antarpenilai. Protokol kontekstual 4.0/instrumen 3.0 masih rencana tertulis; perintah bawaan memakai desain historis 3.0/instrumen 2.0.""",
        "BAB III: instrumen, pemeriksaan, posisionalitas; F09/F10; research/protocol.md", kind="brief")
    add("Perubahan utama rancangan", [],
        """Catatan kelas F01–F12 meminta kejelasan judul, objek, pendekatan, pertanyaan, teori, posisionalitas, dan asal rumus. Review teman P01–P17 memperbaiki keterbacaan serta sumber. Masukan Pembimbing I G01–G15 menekankan konteks Strube dan kasus kecil. V5 pada 8–9 Oktober masih memakai 40 melodi dan zona fermata; revisi 13 Oktober beralih ke satu kasus dan keputusan kontekstual. Fermata kini menjadi konteks kadens/metadata. Mempertahankan dua model adalah pilihan peneliti yang masih memerlukan kesepakatan, bukan persetujuan pembimbing yang sudah tercatat.""",
        "Catatan perubahan v2–v5; feedback F01–F12/G01–G15; review teman P01–P17", kind="table",
        columns=["Aspek", "Desain sebelumnya", "V5 aktif"],
        rows=[["Bahan", "40 melodi", "Satu kasus Strube"],
              ["Penilaian", "Hitungan otomatis", "Keputusan kontekstual"],
              ["Analisis", "Uji lintas melodi/zona", "Profil deskriptif"]],
        caption="Revisi 13 Oktober 2026 mengikuti konteks kaidah dan penyempitan lingkup.")
    add("Perkembangan dan masukan kelas", [
        ["Tersedia", "BAB I–III, peta kaidah, OCR teks, dan dua contoh Fig. 33."],
        ["Belum selesai", "Notasi lengkap, kesepakatan lingkup, implementasi instrumen, pilot, dan data utama."],
        ["Masukan kelas", "Kejelasan objek, pendekatan/hipotesis, batas kasus, dan jumlah model."]],
        """Perkembangan saat ini berupa naskah dan persiapan sumber, belum hasil utama model. Dua skrip OCR ditambahkan ke repositori pada 21 Oktober; OCR teks tidak memverifikasi notasi musik. Urutan berikutnya ialah memperoleh sumber yang jelas, menyepakati lingkup, menyesuaikan instrumen, lalu menjalankan pilot terpisah sebelum membekukan pengumpulan utama. Kesimpulan kelak dibatasi pada kasus dan konfigurasi yang diuji; keindahan, persepsi pendengar, serta peningkatan belajar berada di luar pengukuran. Catat masukan kelas dengan penyampai, isi, keputusan aktual, dan tindak lanjut pada formulir yang tersedia.""",
        "PROGRESS.md; protokol 4.0; skrip OCR, commit 7c64d76", kind="brief")
    add("Research gap dan posisi penelitian", [
        ["Sudah dikaji", "Bach Doodle menghitung kuint dan oktaf sejajar pada keluaran Coconet."],
        ["Celah kajian", "Dalam sumber yang ditinjau, belum ada uraian kedua model pada satu kasus Strube dengan syarat dan pengecualiannya."],
        ["Posisi penelitian", "Menghubungkan kejadian, lokasi partitur, dan alasan keputusan menurut Strube."]],
        """Gap ini tertulis pada BAB I bagian Rumusan Masalah dan BAB II bagian Posisi Penelitian. Huang et al. (2019) menghitung kuint dan oktaf sejajar pada Coconet dengan melodi pengguna. Yan et al. (2018) menilai soal bas dengan rubrik buku ajar. Keduanya menjadi pijakan, tetapi sumber yang ditinjau belum menguraikan DeepBach dan Coconet pada satu contoh chorale Strube dengan tahap serta pengecualian sebagai dasar keputusan. Penelitian ini menggabungkan pencatatan komputasional dan pembacaan kontekstual partitur. Klaim gap dibatasi pada sumber yang ditinjau, tanpa mengklaim topik ini pertama di dunia.""",
        "BAB I: Rumusan Masalah; BAB II: Posisi Penelitian; Huang et al. (2019); Yan et al. (2018)", kind="brief")
    add("Hipotesis kerja pada kasus terpilih", [
        ["H1 · Kesesuaian", "Pada masing-masing model, terdapat keluaran yang memuat penyimpangan gerak suara terkonfirmasi menurut Strube."],
        ["H2 · Perbandingan", "DeepBach dan Coconet menghasilkan profil gerak suara yang berbeda pada kasus yang sama."]],
        """Ini usulan hipotesis kerja untuk presentasi, ditambahkan atas permintaan peneliti. Naskah v5 saat ini belum memuatnya sehingga penyelarasan naskah/protokol dan pembahasan pembimbing masih diperlukan. H1 bertolak dari laporan gerak sejajar pada keluaran kedua model; penyimpangan harus terkonfirmasi setelah syarat Strube diperiksa. Kejadian belum diputuskan tidak dihitung sebagai penyimpangan. H2 membandingkan profil per kriteria dan lokasi pada sopran yang sama, tanpa menentukan model unggul. Analisis direncanakan deskriptif; hipotesis ini tidak menyatakan signifikansi populasi atau sebab arsitektural. Kriteria keputusan dukungan perlu ditetapkan sebelum pengumpulan; tanpa keluaran layak, hipotesis terkait tidak dapat dinilai.""",
        "Usulan presentasi; dasar H1: Hadjeres et al. (2017), Huang et al. (2019); H2: pertanyaan penelitian kedua",
        kind="questions")
    # Exclude the progress slide from the classroom presentation.
    slides[5]["title"] = "Metode, kasus, dan unit analisis"
    slides[5]["blocks"] = [
        ["Pendekatan", "Studi kasus evaluatif pada satu chorale Strube. MODEL 285 masih calon."],
        ["Unit analisis", "Kasus melodi, keluaran harmonisasi, dan kejadian gerak suara dibedakan."],
        ["Pengulangan", "Rencana 20 percobaan per model; dua model dan jumlahnya masih perlu kesepakatan."]]
    slides[5]["notes"] = "Penelitian memadukan analisis partitur, pencatatan komputasional, dan statistik deskriptif. Kasus dipilih purposif dari bab chorale Strube; bas awal dan durasi akhir sopran MODEL 285 masih perlu salinan jelas. Satu melodi dengan 40 percobaan tetap satu kasus. Jumlah 20 per model mengikuti beban pemeriksaan, bukan power statistik. Sopran dipertahankan sama dalam nada dan waktu; model mengisi A/T/B. Simpan keluaran identik dan kegagalan. Ringkas jumlah, lokasi, kesempatan transisi, serta episode/durasi per kriteria. Acuan cetak bukan satu-satunya jawaban dan belum terverifikasi sebagai harmonisasi asli Bach."
    reordered = [slides[i] for i in [0, 1, 10, 2, 3, 5, 11, 7, 8]]
    slides[:] = reordered
    for number, slide in enumerate(slides, 1):
        slide["number"] = number
    assert len(slides) == 9


def main():
    compact_deck()
    # Sumber klaim adalah working tree aktif, bukan rekonstruksi sebuah tag.
    sources = [
        "docs/final-thesis/thesis/metadata.tex",
        "docs/final-thesis/thesis/chapters/01-pendahuluan.tex",
        "docs/final-thesis/thesis/chapters/02-tinjauan-pustaka.tex",
        "docs/final-thesis/thesis/chapters/03-metode-penelitian.tex",
        "docs/final-thesis/thesis/references.bib",
        "docs/final-thesis/PROGRESS.md", "research/protocol.md",
        "docs/final-thesis/supervision/feedback.md",
        "docs/final-thesis/supervision/perubahan-v2-ke-v3.md",
        "docs/final-thesis/supervision/perubahan-v3-ke-v4.md",
        "docs/final-thesis/supervision/perubahan-v4-ke-v5.md",
        "research/scripts/ocr_strube.py", "research/scripts/ocr_strube_tesseract.py",
    ]
    manifest = dict(date="2026-10-21", timezone="Asia/Jakarta", manuscript="final-thesis v5, active working tree",
                    sources=[dict(path=p, sha256=hashlib.sha256((ROOT / p).read_bytes()).hexdigest()) for p in sources])
    (HERE / "source-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    (HERE / "slides.json").write_text(json.dumps(slides, ensure_ascii=False, indent=2) + "\n")
    out = ["# Catatan presenter: Seminar Musikologi 2", "",
           "21 Oktober 2026. Vincent Nuridzati Adittama, 23104810131. Final-thesis v5.", "",
           "9 slide termasuk sampul. Gunakan paragraf berikut sebagai pegangan singkat, lalu jelaskan dengan bahasa sendiri. Durasi dapat disesuaikan sekitar 10–15 menit.", ""]
    for x in slides:
        out.extend([f"## Slide {x['number']:02d}. {x['title'].replace(chr(10), ' ')}", "",
                    x["notes"], "", f"Sumber: {x['source']}.", ""])
    out.extend(["## Masukan kelas", "",
                "Isi [masukan-kelas.md](masukan-kelas.md) setelah masukan benar-benar disampaikan. Pisahkan usulan dari keputusan pembimbing yang terkonfirmasi.", "",
                "## Rujukan", "",
                "Rincian bibliografi tersedia pada [bibliografi skripsi](../../thesis/references.bib); status pembacaan pada [reading-notes.csv](../../records/reading-notes.csv). [Manifest sumber](source-manifest.json) menyimpan identitas sumber lokal.", "",
                "## Perubahan penyajian", "",
                "Slide perkembangan dihapus sesuai permintaan peneliti sehingga tersisa 9 slide. Research gap berada pada slide 3 dan usulan hipotesis kerja pada slide 7; hipotesis ini belum berada dalam naskah v5 dan perlu diselaraskan sebelum pengumpulan. Catatan tetap satu paragraf per slide. Naskah dan protokol penelitian tidak diubah dalam pekerjaan presentasi ini.", ""])
    (HERE / "presenter-notes.md").write_text("\n".join(out))
    print(f"Prepared {len(slides)} slides; notes {len(' '.join(out).split())} words")



if __name__ == "__main__":
    main()
