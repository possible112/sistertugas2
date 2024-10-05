import asyncio
import random
import tkinter as tk
from tkinter import ttk
import threading
import time

# Variabel global untuk menyimpan metrik
metrics = {
    "Request-Response": {"count": 0, "total_time": 0},
    "Publish-Subscribe": {"count": 0, "total_time": 0},
    "Message Passing": {"count": 0, "total_time": 0},
    "RPC": {"count": 0, "total_time": 0},
}

# Fungsi untuk mencatat metrik
def log_metrics(model, time_taken):
    metrics[model]["count"] += 1  # Menambahkan jumlah eksekusi model tertentu
    metrics[model]["total_time"] += time_taken  # Menambahkan waktu yang diperlukan ke total
    display_metrics(output_box)  # Memperbarui metrik secara real-time setelah setiap peristiwa

# Fungsi untuk menampilkan metrik
def display_metrics(output_box):
    output_box.insert(tk.END, "\n--- Metrik Real-Time ---\n", "info")  # Menyisipkan header di kotak output
    for model, data in metrics.items():
        avg_time = data["total_time"] / data["count"] if data["count"] > 0 else 0  # Menghitung rata-rata waktu
        output_box.insert(tk.END, f"{model}: Jumlah = {data['count']}, Rata-Rata Waktu = {avg_time:.2f} detik\n", "info")  # Menampilkan metrik untuk setiap model
    output_box.insert(tk.END, "\n", "info")  # Menambahkan baris baru untuk meningkatkan keterbacaan

# Model Request-Response (Asynchronous)
async def request_response_server(request_queue, response_queue, output_box, max_requests=3):
    while True:  # Berjalan terus-menerus untuk terus menangani permintaan
        if not request_queue.empty():  # Memeriksa apakah ada permintaan dalam antrean
            request = await request_queue.get()  # Mengambil permintaan berikutnya
            output_box.insert(tk.END, f"[Server] Menerima permintaan: {request}\n", "server")  # Mencatat permintaan yang diterima
            await asyncio.sleep(random.uniform(0.5, 2))  # Mensimulasikan penundaan pemrosesan
            response = f"Respons untuk {request}"  # Menyiapkan respons
            await response_queue.put(response)  # Mengirim respons kembali ke klien
        await asyncio.sleep(0.1)  # Menunggu sejenak sebelum memeriksa antrean lagi

async def request_response_client(request_queue, response_queue, output_box, max_requests=3):
    for i in range(max_requests):
        request = f"Permintaan Klien {i + 1}"  # Membuat pesan permintaan baru
        output_box.insert(tk.END, f"[Klien] Mengirim: {request}\n", "client")  # Mencatat permintaan yang dikirim

        start_time = time.time()  # Mencatat waktu mulai permintaan
        await request_queue.put(request)  # Mengirim permintaan ke server

        # Mensimulasikan kemungkinan timeout
        try:
            response = await asyncio.wait_for(response_queue.get(), timeout=3)  # Menunggu respons dengan timeout
            end_time = time.time()  # Mencatat waktu akhir
            elapsed_time = end_time - start_time  # Menghitung waktu yang berlalu
            log_metrics("Request-Response", elapsed_time)  # Mencatat metrik untuk model ini
            output_box.insert(tk.END, f"[Klien] Menerima: {response}\n", "client")  # Mencatat respons yang diterima
            output_box.insert(tk.END, f"Waktu yang berlalu untuk permintaan-respons ini: {elapsed_time:.2f} detik\n", "info")  # Menampilkan waktu yang berlalu
        except asyncio.TimeoutError:
            output_box.insert(tk.END, f"[Klien] Permintaan {request} telah timeout!\n", "client")  # Menangani kasus timeout

# Model Publish-Subscribe (Asynchronous)
async def dynamic_publisher(broker, topics, output_box):
    for topic in topics:
        for i in range(3):
            message = f"Pesan {i + 1} ke topik: {topic}"  # Membuat pesan baru untuk diterbitkan
            output_box.insert(tk.END, f"[Penerbit] Menerbitkan: '{message}' ke {topic}\n", "publisher")  # Mencatat pesan yang diterbitkan
            start_time = time.time()  # Mencatat waktu mulai penerbitan
            broker[topic] = message  # Menyimpan pesan di broker
            await asyncio.sleep(random.uniform(0.5, 1))  # Mensimulasikan waktu antara penerbitan
            end_time = time.time()  # Mencatat waktu akhir
            log_metrics("Publish-Subscribe", end_time - start_time)  # Mencatat metrik untuk model ini

async def dynamic_subscriber(broker, topics, output_box):
    subscribed_topics = random.sample(topics, random.randint(1, len(topics)))  # Secara acak berlangganan ke beberapa topik
    output_box.insert(tk.END, f"[Pelanggan] Berlangganan ke: {', '.join(subscribed_topics)}\n", "subscriber")  # Mencatat topik yang disubscribekan
    while True:
        for topic in subscribed_topics:
            if topic in broker:  # Memeriksa apakah ada pesan untuk topik yang disubscribekan
                message = broker[topic]  # Mengambil pesan dari broker
                output_box.insert(tk.END, f"[Pelanggan] Menerima: '{message}' dari topik: '{topic}'\n", "subscriber")  # Mencatat pesan yang diterima
                await asyncio.sleep(random.uniform(1, 2))  # Mensimulasikan waktu pemrosesan yang bervariasi
                output_box.insert(tk.END, f"[Pelanggan] Selesai memproses pesan: '{message}'\n", "subscriber")  # Mencatat penyelesaian pemrosesan
                del broker[topic]  # Menghapus pesan setelah diproses
        await asyncio.sleep(0.1)  # Menunggu sejenak sebelum memeriksa topik lagi

# Model Message Passing
async def message_passing_sender(queue, message, output_box):
    if random.random() > 0.2:  # 80% kemungkinan pesan berhasil dikirim
        output_box.insert(tk.END, f"[Pengirim] Mengirim pesan: '{message}'\n", "sender")  # Mencatat pesan yang dikirim
        start_time = time.time()  # Mencatat waktu mulai pengiriman
        await asyncio.sleep(random.uniform(0.5, 1.5))  # Mensimulasikan penundaan jaringan
        await queue.put(message)  # Mengirim pesan ke antrean
        end_time = time.time()  # Mencatat waktu akhir
        log_metrics("Message Passing", end_time - start_time)  # Mencatat metrik untuk model ini
    else:
        output_box.insert(tk.END, f"[Pengirim] Pesan '{message}' hilang dalam perjalanan!\n", "sender")  # Menangani kasus kehilangan pesan

async def message_passing_receiver(queue, output_box):
    while True:
        if not queue.empty():  # Memeriksa apakah antrean tidak kosong
            message = await queue.get()  # Mengambil pesan dari antrean
            output_box.insert(tk.END, f"[Penerima] Menerima pesan: '{message}'\n", "receiver")  # Mencatat pesan yang diterima
            await asyncio.sleep(random.uniform(0.5, 2))  # Mensimulasikan penundaan pemrosesan
        await asyncio.sleep(0.1)  # Menghindari busy-waiting

# Model Remote Procedure Call (RPC)
async def rpc_server(method_name, *args):
    start_time = time.time()  # Memulai penghitungan waktu
    output_box.insert(tk.END, f"[Server] Menjalankan: {method_name} dengan argumen: {args}\n", "rpc_server")  # Mencatat RPC yang dieksekusi
    await asyncio.sleep(random.uniform(1, 2))  # Mensimulasikan waktu eksekusi RPC
    end_time = time.time()  # Menghentikan penghitungan waktu
    log_metrics("RPC", end_time - start_time)  # Mencatat metrik untuk RPC
    return f"Hasil dari {method_name}"  # Mengembalikan hasil eksekusi

async def rpc_client(method_name, output_box, *args):
    retries = 3  # Jumlah maksimal percobaan
    for attempt in range(retries):
        try:
            output_box.insert(tk.END, f"[Klien] Mencoba panggilan RPC {method_name}, percobaan {attempt + 1}/{retries}\n", "client")  # Mencatat upaya panggilan RPC
            result = await asyncio.wait_for(rpc_server(method_name, *args), timeout=5)  # Memanggil RPC dengan batas waktu
            output_box.insert(tk.END, f"[Klien] Mendapatkan hasil: {result}\n", "client")  # Mencatat hasil yang diterima
            break  # Keluar dari loop jika berhasil
        except asyncio.TimeoutError:
            output_box.insert(tk.END, f"[Klien] Timeout saat memanggil {method_name}, percobaan berikutnya...\n", "client")  # Menangani timeout


# Asynchronous Simulation Execution
def run_simulation(selected_model, output_box, message_input=None):
    asyncio.run(start_simulation(selected_model, output_box, message_input))


async def start_simulation(selected_model, output_box, message_input=None):
    if selected_model == "Request-Response":
        output_box.insert(tk.END, "Starting Request-Response Model...\n", "info")
        request_queue = asyncio.Queue()
        response_queue = asyncio.Queue()
        await asyncio.gather(
            request_response_server(request_queue, response_queue, output_box),
            request_response_client(request_queue, response_queue, output_box)
        )

    elif selected_model == "Publish-Subscribe":
        output_box.insert(tk.END, "Starting Publish-Subscribe Model...\n", "info")
        broker = {}
        topics = ["topic1", "topic2", "topic3"]
        await asyncio.gather(
            dynamic_publisher(broker, topics, output_box),
            dynamic_subscriber(broker, topics, output_box)
        )

    elif selected_model == "Message Passing":
        output_box.insert(tk.END, "Starting Message Passing Model...\n", "info")
        queue = asyncio.Queue()
        await asyncio.gather(
            message_passing_sender(queue, message_input, output_box),
            message_passing_receiver(queue, output_box)
        )

    elif selected_model == "RPC":
        output_box.insert(tk.END, "Starting RPC Model...\n", "info")
        await rpc_client("compute_sum", output_box, 5, 10)


# Function to start the simulation in a new thread
def start_simulation_thread():
    selected_model = model_choice.get()
    message_input = message_entry.get() if selected_model == "Message Passing" else None
    output_box.delete(1.0, tk.END)  # Clear output box
    simulation_thread = threading.Thread(target=run_simulation, args=(selected_model, output_box, message_input))
    simulation_thread.start()


def update_ui(event):
    if model_choice.get() == "Message Passing":
        message_label.pack(pady=5)
        message_entry.pack(pady=5)
    else:
        message_label.pack_forget()
        message_entry.pack_forget()


# Tkinter GUI setup
def run_tkinter():
    global root, model_choice, output_box, message_entry, message_label
    root = tk.Tk()
    root.title("Sistem Terdistribusi")
    root.geometry("800x600")

    root.configure(bg="#1A1A2E")  # Dark navy background

    label = tk.Label(root, text="Pilih model Komunikasi", font=("Arial", 14), bg="#1A1A2E", fg="#EAEAEA")
    label.pack(pady=10)

    model_choice = ttk.Combobox(root, values=["Request-Response", "Publish-Subscribe", "Message Passing", "RPC"])
    model_choice.pack(pady=10)
    model_choice.current(0)
    model_choice.bind("<<ComboboxSelected>>", update_ui)  # Bind the update function

    # Entry for message input (for Message Passing)
    message_label = tk.Label(root, text="Enter message for Message Passing:", font=("Arial", 12), bg="#1A1A2E", fg="#EAEAEA")
    message_entry = tk.Entry(root, width=50)

    # Button to start simulation
    start_button = tk.Button(root, text="Start Simulation", command=start_simulation_thread, bg="#FF6F61", fg="white")
    start_button.pack(pady=10)

    # Textbox for output
    output_box = tk.Text(root, height=20, width=80, bg="#2C2C54", fg="white", font=("Arial", 12))
    output_box.pack(pady=10)

    # Configure output box tag colors
    output_box.tag_configure("client", foreground="#FFB300")
    output_box.tag_configure("server", foreground="#5EB1FF")
    output_box.tag_configure("publisher", foreground="#FF6F61")
    output_box.tag_configure("subscriber", foreground="#FFDA79")
    output_box.tag_configure("sender", foreground="#FF8C00")
    output_box.tag_configure("receiver", foreground="#E91E63")
    output_box.tag_configure("rpc_server", foreground="#673AB7")
    output_box.tag_configure("info", foreground="#EAEAEA")

    root.mainloop()

if __name__ == "__main__":
    run_tkinter()
