1. Model Request-Response
Model ini menggunakan pola komunikasi di mana klien mengirim permintaan ke server, dan server memberikan respons setelah memproses permintaan tersebut.
Server: Menunggu permintaan dari antrean, memprosesnya dengan penundaan acak untuk mensimulasikan pemrosesan, dan mengirimkan respons kembali ke antrean respons.
Klien: Mengirimkan sejumlah permintaan ke server dan menunggu respons. Jika respons tidak diterima dalam batas waktu yang ditentukan, klien akan mencatat bahwa permintaan tersebut mengalami timeout.

2. Model Publish-Subscribe
Model ini melibatkan penerbit yang mengirimkan pesan ke topik tertentu dan pelanggan yang berlangganan ke topik tersebut untuk menerima pesan.
Penerbit: Mengirimkan pesan ke beberapa topik dengan penundaan acak, mencatat setiap pesan yang diterbitkan.
Pelanggan: Berlangganan ke beberapa topik secara acak dan menerima pesan yang diterbitkan. Setelah menerima pesan, pelanggan memprosesnya dan menghapus pesan dari broker.

3. Model Message Passing
Model ini mengirimkan pesan antara pengirim dan penerima menggunakan antrean.
Pengirim: Mengirimkan pesan ke antrean dengan kemungkinan kehilangan pesan (20% kemungkinan pesan hilang). Jika pesan berhasil dikirim, pengirim mencatat waktu pengiriman.
Penerima: Mengambil pesan dari antrean dan memprosesnya. Proses ini juga disertai penundaan acak untuk mensimulasikan pemrosesan yang bervariasi.

4. Model Remote Procedure Call (RPC)
Model ini memungkinkan klien untuk memanggil prosedur atau metode yang dieksekusi di server seolah-olah itu adalah bagian dari klien sendiri.
Server: Menjalankan metode yang diminta dengan argumen yang diberikan. Server mencatat waktu yang diperlukan untuk menjalankan metode dan mengembalikan hasilnya.
Klien: Memanggil metode pada server dan menunggu hasilnya dengan batas waktu tertentu. Jika hasil tidak diterima dalam batas waktu, klien akan mencoba lagi hingga jumlah percobaan maksimum tercapai.

Keempat model komunikasi ini menunjukkan cara yang berbeda untuk menangani interaksi antara berbagai komponen dalam sistem yang menggunakan asynchronous programming.
